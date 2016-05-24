#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Piotr Krysik <ptrkrysik@gmail.com>.
# 
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation: either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY: without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software: see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import blocks
from threading import Lock
from gnuradio import gr
from gnuradio.filter import firdes
from grc_gnuradio import blks2
import osmosdr
import time
import multi_rtl
from numpy import *
from pylab import *
from math import log,ceil
import threading

def xcorr(X,Y,maxlag):
    N = max(len(X),len(Y))
    N_nextpow2 = ceil(log(N + maxlag,2))
    M = 2**N_nextpow2
    if len(X) < M:
        postpad_X = int(M-len(X)-maxlag)
    else:
        postpad_X = 0

    if len(Y) < M:
        postpad_Y = int(M-len(Y))
    else:
        postpad_Y = 0
        
    pre  = fft( pad(X, (maxlag,postpad_X), 'constant', constant_values=(0, 0)) )
    post = fft( pad(Y, (0,postpad_Y), 'constant', constant_values=(0, 0)) )
    cor  = ifft( pre * conj(post) )
    R = cor[0:2*maxlag]
    return R

class vector_sink_fullness_notifier(gr.feval):
    """
    This class allows C++ code to callback into python.
    """
    def __init__(self, b):
        gr.feval.__init__(self)
        self.b = b
        self.d_mutex = threading.Lock()

    def eval(self):
        """
        This method is called by vector_sink_cn when it is full
        """
        self.d_mutex.acquire()
        try:
            self.b.fullness_report()
        except Exception, e:
            print "Vector sink fullness notification exception: ", e
        finally:
            self.d_mutex.release()

class multi_rtl_source(gr.hier_block2):
    """
    docstring for block multi_rtl_source
    """
    def __init__(self, 
                 sample_rate=2e6, 
                 num_channels=2, 
                 rtlsdr_id_strings=[], 
                 sync_period=0.15, sync_center_freq=100e6, sync_gains={}, 
                 center_freqs={}, gains={}, 
                 ppm=0
                ):
        gr.hier_block2.__init__(self,
            "multi_rtl_source",
            gr.io_signature(0,0,0),  # Input signature
            gr.io_signature(num_channels, num_channels, gr.sizeof_gr_complex)# Output signature
        ) 

        self.state = "sync" #states: sync, work

        #options that aren't changed when switching between "work" and "sync" states
        self.num_channels = num_channels
        self.rtlsdr_id_strings = rtlsdr_id_strings
        self.sample_rate = sample_rate
        self.delays = {}
        self.ppm = ppm

#        self.if_gains = {}
#        self.bb_gains = {}
#        self.bandwidths = {}
#        self.dc_offset_modes = {}
#        self.iq_balance_modes = {}
#        self.gain_modes = {}

        #options used in "work" state
        self.gains = gains
        self.center_freqs = center_freqs            

        #synchronization options (number of samples for measurement of the delay, frequency and gains)
        self.sync_samples = int(round(sync_period*sample_rate/2)*2)
        self.sync_gains = sync_gains
        self.sync_center_freq = sync_center_freq

        #blocks
        self.phase_amplitude_corrections = {}        
        self.phase_and_amplitude_correctors = {}
        self.rtlsdr_sources = {}
        self.delay_blocks = {}
        self.vsinks = {}
        
        self.vsink_notifier = vector_sink_fullness_notifier(self) #object providing callback function for notifying the multi_rtl that 
                                                                  #vsinks are full

        for chan in xrange(0,self.num_channels):
            if (chan <= len(rtlsdr_id_strings)) and (rtlsdr_id_strings is not ""):
                rtl_args= "numchan=" + str(1) + " " + "rtl=" + rtlsdr_id_strings[chan]
                self.rtlsdr_sources[chan] = osmosdr.source( args=rtl_args) 
            else:
                rtl_args= "numchan=" + str(1) + " " + "rtl=" + str(chan)            
                self.rtlsdr_sources[chan] = osmosdr.source( args="numchan=" + str(1) )

            self.rtlsdr_sources[chan].set_sample_rate(self.sample_rate)
            self.rtlsdr_sources[chan].set_freq_corr(self.ppm, 0)
#            self.rtlsdr_sources[chan].set_dc_offset_mode(2, 0)
#            self.rtlsdr_sources[chan].set_iq_balance_mode(2, 0)
            self.rtlsdr_sources[chan].set_gain_mode(False, 0)
            self.rtlsdr_sources[chan].set_if_gain(24, 0)
            self.rtlsdr_sources[chan].set_antenna("", 0)
#            self.rtlsdr_sources[chan].set_bandwidth(0, 0)

        self.set_freq_corr(self.ppm)
        self.apply_synchronization_settings()

        self.vsink = multi_rtl.vector_sink_cn(1, True, int(self.sync_samples), int(num_channels), self.vsink_notifier)
             
        for chan in xrange(0,self.num_channels):          
            self.delay_blocks[chan] = blocks.delay(gr.sizeof_gr_complex*1, 0)
            self.phase_amplitude_corrections[chan]=1.0
            self.phase_and_amplitude_correctors[chan] = blocks.multiply_const_vcc((self.phase_amplitude_corrections[chan], ))

            
            #connect blocks
            self.connect((self.rtlsdr_sources[chan], 0), (self.vsink, chan))
            self.connect((self.rtlsdr_sources[chan], 0), (self.delay_blocks[chan], 0))
            self.connect((self.delay_blocks[chan], 0),(self.phase_and_amplitude_correctors[chan], 0))
            self.connect((self.phase_and_amplitude_correctors[chan], 0),(self, chan)) 
       
        
    def fullness_report(self):
#        self.full_vsinks_counter = self.full_vsinks_counter + 1
#        if(self.full_vsinks_counter>=self.num_channels):
        self.compute_and_set_delays()

    def compute_and_set_delays(self):
        N = self.sync_samples
        #set target frequency and gain
        self.apply_operational_settings()
        
        self.delays[0] = 0
        sync_data = self.vsink.data()
        
        self.phase_amplitude_corrections[0]=1
        var0=var(sync_data[0])
        for chan in xrange(1,self.num_channels):
            result_corr       = xcorr(sync_data[0],sync_data[chan],int(len(sync_data[0])/2))
            max_position      = argmax(abs(result_corr))
            self.delays[chan] = len(result_corr)/2-max_position

            self.phase_amplitude_corrections[chan] = result_corr[max_position]/sqrt(mean(real(sync_data[chan])**2+imag(sync_data[chan])**2))
            self.phase_and_amplitude_correctors[chan].set_k((sqrt(var0/var(sync_data[chan]))*(exp(1j*angle(self.phase_amplitude_corrections[chan]))),))
#            print "sqrt(var0/var(sync_data[chan])): ",sqrt(var0/var(sync_data[chan]))
        #set delays
        for chan in xrange(0,self.num_channels):        
            print "Delay of channel ",chan,": ",self.delays[chan],' phase diff: ', (angle(self.phase_amplitude_corrections[chan])/pi*180), " [deg]"
            self.delay_blocks[chan].set_dly(-int(self.delays[chan]))
        
        self.state = "work"

    def synchronize(self):
        if self.state == "work":
          #set synchronization frequency and gain
            self.apply_synchronization_settings()
            self.state = "sync"
            self.full_vsinks_counter = 0

            time.sleep(0.1) #this is potential race condition, it would be good to avoid this in order to clear 
            self.vsink.reset()
    
    def apply_synchronization_settings(self):
        for chan in xrange(0,self.num_channels):
            self.rtlsdr_sources[chan].set_center_freq(self.sync_center_freq, 0)
            if(len(self.sync_gains) == self.num_channels):
                self.rtlsdr_sources[chan].set_gain(self.sync_gains[chan], 0)
            else:
                self.rtlsdr_sources[chan].set_gain(30, 0) #this is meant mainly for GRC so the block is created even if gains are not given
                                                          #TODO: decide if this is good
                
    def apply_operational_settings(self):
        for chan in xrange(0,self.num_channels):
            self.rtlsdr_sources[chan].set_gain(self.gains[chan], 0)    
            self.rtlsdr_sources[chan].set_center_freq(self.center_freqs[chan], 0)


#getters and setters for operational parameters
    def get_num_channels(self):
        return self.num_channels
    
#    def set_sample_rate(self, rate):
#        pass

    def get_sample_rate(self):
        return self.sample_rate

    def get_freq_range(self, chan=0):
        self.rtlsdr_sources[chan].get_freq_range()
    
    def set_center_freq(self, freq, chan=0): #b. istotna
        self.center_freqs[chan] = freq
        print "setting center freq",freq
        if self.state == "work":
            self.rtlsdr_sources[chan].set_center_freq(freq, 0)

    def get_center_freq(self, chan=0): #b. istotna
        return self.center_freqs[chan]
        
    def set_freq_corr(self, ppm):  #b. istotna
        self.ppm = ppm
        print "setting freq corr",ppm
        for chan in xrange(0,self.num_channels):
            self.rtlsdr_sources[chan].set_freq_corr(self.ppm, 0)
        
    def get_freq_corr(self):    #b. istotna
        return self.ppm
        
    def get_gain_names(self, chan=0): #dziwna
        self.rtlsdr_sources[chan].get_gain_names(0)
        
    def get_gain_range(self, chan=0): #malo istotna
        self.rtlsdr_sources[chan].get_gain_range(0)
        
    def get_gain_range(self, name, chan=0): #malo istotna i dziwna
        self.rtlsdr_sources[chan].get_gain_range(name,0)
    
    def set_gain_mode(self, mode, chan=0):
        self.rtlsdr_sources[chan].set_gain_mode(mode,0)
        
    def get_gain_mode(self, chan=0):
        return self.rtlsdr_sources[chan].get_gain_mode(chan)
        
    def set_gain(self, gain, chan=0):
        self.gains[chan] = gain
        if self.state == "work":
            self.rtlsdr_sources[chan].set_gain(gain,0)
        
#    def set_gain(self, gain, name, chan):
#        pass

    def get_gain(self, chan=0):
        return self.gains[chan]
        
    def get_current_gain(self, name, chan=0):
        return self.rtlsdr_sources[chan].get_gain(name,0)
        
    def set_if_gain(self, gain, chan=0):
        self.if_gains[chan] = gain

    def get_if_gain(self, chan=0):
        if chan in if_gains:
            return self.if_gains[chan]
        else:
            return None

#synchronization options
    def set_sync_center_freq(self, freq): #b. istotna
        self.sync_center_freq = freq
        if self.state == "sync":
            self.rtlsdr_sources[chan].set_center_freq(freq, 0)
        

    def get_sync_center_freq(self): #b. istotna
        return self.sync_center_freq
    
#    def set_sync_gain_mode(self, automatic, chan):
#        pass
        
#    def get_sync_gain_mode(self, chan):
#        pass
        
    def set_sync_gain(self, gain, chan=0):
        self.sync_gains[chan] = gain
        if self.state == "sync":
            self.rtlsdr_sources[chan].set_gain(gain,0)

#    def set_sync_gain_mode(self, automatic, chan=0):
#        self.sync_gain_modes[chan] = gain
#        if self.state == "sync":
#            self.rtlsdr_sources[chan].set_gain_mode(automatic,0)
        
#    def set_sync_gain(self, gain, name, chan):
#        pass

    def get_sync_gain(self, chan=0):
        return self.sync_gains[chan]
        
#    def get_sync_gain(self, name, chan):
#        pass
        
#    def set_sync_if_gain(self, gain, chan):
#        pass


