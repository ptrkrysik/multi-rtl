#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: mutlirtl_rx_to_cfile_2chan
# Author: Antoni Przybylik
# Description: Sample application for recording to binary files the samples from inputs of two channel multi-rtl receiver
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import multi_rtl

class mutlirtl_rx_to_cfile_2chan(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "mutlirtl_rx_to_cfile_2chan")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000

        ##################################################
        # Blocks
        ##################################################
        self.multi_rtl_source_0 = multi_rtl.multi_rtl_source(sample_rate=samp_rate, num_channels=2, ppm=0, sync_center_freq=939400000, rtlsdr_id_strings= [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31' ])
        self.multi_rtl_source_0.set_sync_gain(10, 0)
        self.multi_rtl_source_0.set_gain(10, 0)
        self.multi_rtl_source_0.set_center_freq(939000000, 0)
        self.multi_rtl_source_0.set_gain_mode(False, 0)
        self.multi_rtl_source_0.set_sync_gain(10, 1)
        self.multi_rtl_source_0.set_gain(10, 1)
        self.multi_rtl_source_0.set_center_freq(939000000, 1)
        self.multi_rtl_source_0.set_gain_mode(False, 1)
        self.blocks_head_0_0 = blocks.head(gr.sizeof_gr_complex*1, 10000000000)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 10000000000)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'fname_ch1', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'fname_ch0', False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.multi_rtl_source_0, 0), (self.blocks_head_0, 0))
        self.connect((self.multi_rtl_source_0, 1), (self.blocks_head_0_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate



def main(top_block_cls=mutlirtl_rx_to_cfile_2chan, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
