#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Two channel multi-rtl RX to cfile
# Author: Piotr Krysik
# Description: Sample application for recording to binary files the samples from inputs of two channel multi-rtl receiver
# Generated: Thu Aug  4 07:29:39 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import multi_rtl


class mutlirtl_rx_to_cfile_2chan(gr.top_block):

    def __init__(self, ch0_id_string="0", ch1_id_string="1", fname_ch0="ch0.cfile", fname_ch1="ch1.cfile", freq_ch0=939e6, freq_ch1=939e6, freq_corr=0, gain_ch0=30, gain_ch1=30, nsamples=int(1e10), samp_rate=1e6, sync_freq=939e6, sync_gain_ch0=30, sync_gain_ch1=30):
        gr.top_block.__init__(self, "Two channel multi-rtl RX to cfile")

        ##################################################
        # Parameters
        ##################################################
        self.ch0_id_string = ch0_id_string
        self.ch1_id_string = ch1_id_string
        self.fname_ch0 = fname_ch0
        self.fname_ch1 = fname_ch1
        self.freq_ch0 = freq_ch0
        self.freq_ch1 = freq_ch1
        self.freq_corr = freq_corr
        self.gain_ch0 = gain_ch0
        self.gain_ch1 = gain_ch1
        self.nsamples = nsamples
        self.samp_rate = samp_rate
        self.sync_freq = sync_freq
        self.sync_gain_ch0 = sync_gain_ch0
        self.sync_gain_ch1 = sync_gain_ch1

        ##################################################
        # Blocks
        ##################################################
        self.multi_rtl_source = multi_rtl.multi_rtl_source(sample_rate=samp_rate, num_channels=2, ppm=freq_corr, sync_center_freq=sync_freq, rtlsdr_id_strings= [ 
          ch0_id_string, 
          ch1_id_string, 
          "2", 
          "3", 
          "4", 
          "5", 
          "6", 
          "7", 
          "8", 
          "9", 
          "10", 
          "11", 
          "12", 
          "13", 
          "14", 
          "15", 
          "16", 
          "17", 
          "18", 
          "19", 
          "20", 
          "21", 
          "22", 
          "23", 
          "24", 
          "25", 
          "26", 
          "27", 
          "28", 
          "29", 
          "30", 
          "31", 
          ])
        self.multi_rtl_source.set_sync_gain(sync_gain_ch0, 0)
        self.multi_rtl_source.set_gain(gain_ch0, 0)
        self.multi_rtl_source.set_center_freq(freq_ch0, 0)
        self.multi_rtl_source.set_gain_mode(False, 0)
        self.multi_rtl_source.set_sync_gain(sync_gain_ch1, 1)
        self.multi_rtl_source.set_gain(gain_ch1, 1)
        self.multi_rtl_source.set_center_freq(freq_ch1, 1)
        self.multi_rtl_source.set_gain_mode(False, 1)
          
        self.head_ch1 = blocks.head(gr.sizeof_gr_complex*1, nsamples)
        self.head_ch0 = blocks.head(gr.sizeof_gr_complex*1, nsamples)
        self.file_sink_ch1 = blocks.file_sink(gr.sizeof_gr_complex*1, fname_ch1, False)
        self.file_sink_ch1.set_unbuffered(False)
        self.file_sink_ch0 = blocks.file_sink(gr.sizeof_gr_complex*1, fname_ch0, False)
        self.file_sink_ch0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.head_ch0, 0), (self.file_sink_ch0, 0))    
        self.connect((self.head_ch1, 0), (self.file_sink_ch1, 0))    
        self.connect((self.multi_rtl_source, 0), (self.head_ch0, 0))    
        self.connect((self.multi_rtl_source, 1), (self.head_ch1, 0))    

    def get_ch0_id_string(self):
        return self.ch0_id_string

    def set_ch0_id_string(self, ch0_id_string):
        self.ch0_id_string = ch0_id_string

    def get_ch1_id_string(self):
        return self.ch1_id_string

    def set_ch1_id_string(self, ch1_id_string):
        self.ch1_id_string = ch1_id_string

    def get_fname_ch0(self):
        return self.fname_ch0

    def set_fname_ch0(self, fname_ch0):
        self.fname_ch0 = fname_ch0
        self.file_sink_ch0.open(self.fname_ch0)

    def get_fname_ch1(self):
        return self.fname_ch1

    def set_fname_ch1(self, fname_ch1):
        self.fname_ch1 = fname_ch1
        self.file_sink_ch1.open(self.fname_ch1)

    def get_freq_ch0(self):
        return self.freq_ch0

    def set_freq_ch0(self, freq_ch0):
        self.freq_ch0 = freq_ch0
        self.multi_rtl_source.set_center_freq(self.freq_ch0, 0)

    def get_freq_ch1(self):
        return self.freq_ch1

    def set_freq_ch1(self, freq_ch1):
        self.freq_ch1 = freq_ch1
        self.multi_rtl_source.set_center_freq(self.freq_ch1, 1)

    def get_freq_corr(self):
        return self.freq_corr

    def set_freq_corr(self, freq_corr):
        self.freq_corr = freq_corr
        self.multi_rtl_source.set_freq_corr(self.freq_corr)

    def get_gain_ch0(self):
        return self.gain_ch0

    def set_gain_ch0(self, gain_ch0):
        self.gain_ch0 = gain_ch0
        self.multi_rtl_source.set_gain(self.gain_ch0, 0)

    def get_gain_ch1(self):
        return self.gain_ch1

    def set_gain_ch1(self, gain_ch1):
        self.gain_ch1 = gain_ch1
        self.multi_rtl_source.set_gain(self.gain_ch1, 1)

    def get_nsamples(self):
        return self.nsamples

    def set_nsamples(self, nsamples):
        self.nsamples = nsamples
        self.head_ch0.set_length(self.nsamples)
        self.head_ch1.set_length(self.nsamples)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_sync_freq(self):
        return self.sync_freq

    def set_sync_freq(self, sync_freq):
        self.sync_freq = sync_freq
        self.multi_rtl_source.set_sync_center_freq(self.sync_freq)

    def get_sync_gain_ch0(self):
        return self.sync_gain_ch0

    def set_sync_gain_ch0(self, sync_gain_ch0):
        self.sync_gain_ch0 = sync_gain_ch0
        self.multi_rtl_source.set_sync_gain(self.sync_gain_ch0, 0)

    def get_sync_gain_ch1(self):
        return self.sync_gain_ch1

    def set_sync_gain_ch1(self, sync_gain_ch1):
        self.sync_gain_ch1 = sync_gain_ch1
        self.multi_rtl_source.set_sync_gain(self.sync_gain_ch1, 1)


def argument_parser():
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option(
        "", "--ch0-id-string", dest="ch0_id_string", type="string", default="0",
        help="Set ch0-id-string [default=%default]")
    parser.add_option(
        "", "--ch1-id-string", dest="ch1_id_string", type="string", default="1",
        help="Set ch1-id-string [default=%default]")
    parser.add_option(
        "", "--fname-ch0", dest="fname_ch0", type="string", default="ch0.cfile",
        help="Set fname-ch0 [default=%default]")
    parser.add_option(
        "", "--fname-ch1", dest="fname_ch1", type="string", default="ch1.cfile",
        help="Set fname-ch1 [default=%default]")
    parser.add_option(
        "", "--freq-ch0", dest="freq_ch0", type="eng_float", default=eng_notation.num_to_str(939e6),
        help="Set freq-ch0 [default=%default]")
    parser.add_option(
        "", "--freq-ch1", dest="freq_ch1", type="eng_float", default=eng_notation.num_to_str(939e6),
        help="Set freq_ch1 [default=%default]")
    parser.add_option(
        "-p", "--freq-corr", dest="freq_corr", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set freq-corr [default=%default]")
    parser.add_option(
        "", "--gain-ch0", dest="gain_ch0", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set gain-ch0 [default=%default]")
    parser.add_option(
        "", "--gain-ch1", dest="gain_ch1", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set gain-ch1 [default=%default]")
    parser.add_option(
        "-N", "--nsamples", dest="nsamples", type="intx", default=int(1e10),
        help="Set nsamples [default=%default]")
    parser.add_option(
        "-r", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set samp-rate [default=%default]")
    parser.add_option(
        "", "--sync-freq", dest="sync_freq", type="eng_float", default=eng_notation.num_to_str(939e6),
        help="Set sync-freq [default=%default]")
    parser.add_option(
        "", "--sync-gain-ch0", dest="sync_gain_ch0", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set sync-gain-ch0 [default=%default]")
    parser.add_option(
        "", "--sync-gain-ch1", dest="sync_gain_ch1", type="eng_float", default=eng_notation.num_to_str(30),
        help="Set sync-gain-ch1 [default=%default]")
    return parser


def main(top_block_cls=mutlirtl_rx_to_cfile_2chan, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(ch0_id_string=options.ch0_id_string, ch1_id_string=options.ch1_id_string, fname_ch0=options.fname_ch0, fname_ch1=options.fname_ch1, freq_ch0=options.freq_ch0, freq_ch1=options.freq_ch1, freq_corr=options.freq_corr, gain_ch0=options.gain_ch0, gain_ch1=options.gain_ch1, nsamples=options.nsamples, samp_rate=options.samp_rate, sync_freq=options.sync_freq, sync_gain_ch0=options.sync_gain_ch0, sync_gain_ch1=options.sync_gain_ch1)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
