#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
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
        postpad_X = M-len(X)-maxlag
    else:
        postpad_X = 0

    if len(Y) < M:
        postpad_Y = M-len(Y)
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
    def __init__(self, samp_rate=2e6, num_channels=2, rtlsdr_id_strings=['00000001','00000002'], sync_samples=3e5, sync_fc=100e6, sync_gain=25, fcs=[939400000, 939400000], gains=[25, 25], ppm=0):
        gr.hier_block2.__init__(self,
            "multi_rtl_source",
            gr.io_signature(0,0,0),  # Input signature
            gr.io_signature(num_channels, num_channels, gr.sizeof_gr_complex)# Output signature
        ) 

        self.num_channels = num_channels
        self.rtlsdr_id_strings = rtlsdr_id_strings
        self.sync_samples = int(sync_samples)
        self.sync_gain = sync_gain
        self.samp_rate = samp_rate
        self.sync_fc = sync_fc
        self.gains = gains
        self.fcs = fcs            
        self.delays = {}
        self.rtlsdr_sources = {}
        self.delay_blocks = {}
        self.vsinks = {}
        self.sync_fc = sync_fc
        self.ppm = ppm
        self.ns = {}
        self.vsink_notifier = vector_sink_fullness_notifier(self)
        self.full_vsinks_counter = 0

        for chan in xrange(0,self.num_channels):
            if chan <= len(rtlsdr_id_strings):
                rtl_args= "numchan=" + str(1) + " " + "rtl=" + rtlsdr_id_strings[chan]
                self.rtlsdr_sources[chan] = osmosdr.source( args=rtl_args) 
            else:
                self.rtlsdr_sources[chan] = osmosdr.source( args="numchan=" + str(1) )

            self.rtlsdr_sources[chan].set_sample_rate(self.samp_rate)
            self.rtlsdr_sources[chan].set_center_freq(self.sync_fc, 0)
            self.rtlsdr_sources[chan].set_freq_corr(self.ppm, 0)
            self.rtlsdr_sources[chan].set_dc_offset_mode(2, 0)
            self.rtlsdr_sources[chan].set_iq_balance_mode(2, 0)
            self.rtlsdr_sources[chan].set_gain_mode(False, 0)
            self.rtlsdr_sources[chan].set_gain(self.sync_gain, 0)
            self.rtlsdr_sources[chan].set_if_gain(20, 0)
            self.rtlsdr_sources[chan].set_bb_gain(20, 0)
            self.rtlsdr_sources[chan].set_antenna("", 0)
            self.rtlsdr_sources[chan].set_bandwidth(0, 0)
             
        for chan in xrange(0,self.num_channels):          
            self.delay_blocks[chan] = blocks.delay(gr.sizeof_gr_complex*1, 0)
            self.vsinks[chan] = multi_rtl.vector_sink_cn(1, True, int(sync_samples), self.vsink_notifier)
            
            #connect blocks
            self.connect((self.rtlsdr_sources[chan], 0), (self.vsinks[chan], 0))
            self.connect((self.rtlsdr_sources[chan], 0), (self.delay_blocks[chan], 0))
            self.connect((self.delay_blocks[chan], 0),(self, chan)) 
       
        
    def fullness_report(self):
        self.full_vsinks_counter = self.full_vsinks_counter + 1
        if(self.full_vsinks_counter>=self.num_channels):
            self.compute_and_set_delays()

    def compute_and_set_delays(self):
        N = self.sync_samples
        for chan in xrange(0,self.num_channels):
            self.rtlsdr_sources[chan].set_gain(self.gains[chan], 0)    
            self.rtlsdr_sources[chan].set_center_freq(self.fcs[chan], 0)
            
        self.delays[0] = 0;
        sync_data_0 = self.vsinks[0].data()
        for chan in xrange(1,self.num_channels):
            sync_data_n = self.vsinks[chan].data()
            result_corr = abs(xcorr(sync_data_0,sync_data_n,int(len(sync_data_0)/2)))
            self.delays[chan]=len(result_corr)/2-argmax(result_corr)
        #set delays
        for chan in xrange(0,self.num_channels):        
            print "delay",chan,": ",self.delays[chan]
            self.delay_blocks[chan].set_dly(-int(self.delays[chan]))
#    def set_sync_gain(chan, gain):
#        self.rtlsdr_sources[chan].set_gain(gain, 0)
#        
#    def set_gain_mode(channel, gain_mode):
#        self.rtlsdr_sources[chan].set_gain_mode(False, 0)        

#    def set_ppm(ppm):
#        self.rtlsdr_sources[chan].set_freq_corr(ppm, 0)
    
