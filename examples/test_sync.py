#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Test Sync
# Generated: Tue Jan 12 07:35:49 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import multi_rtl


class test_sync(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Sync")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6

        ##################################################
        # Blocks
        ##################################################
        self.multi_rtl_source_0 = multi_rtl.multi_rtl_source(sample_rate=samp_rate, num_channels=2, ppm=-7, sync_center_freq=100e6)
        self.multi_rtl_source_0.set_sync_gain(40, 0)
        self.multi_rtl_source_0.set_gain(25, 0)
        self.multi_rtl_source_0.set_center_freq(939.4e6, 0)
        self.multi_rtl_source_0.set_sync_gain(40, 1)
        self.multi_rtl_source_0.set_gain(25, 1)
        self.multi_rtl_source_0.set_center_freq(939.4e6, 1)
          
        self.blocks_tag_debug_0_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "", ""); self.blocks_tag_debug_0_0.set_display(True)
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "", ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/piotr/Odbiornik_gsm/multi_rtl/examples/temp2", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/piotr/Odbiornik_gsm/multi_rtl/examples/temp1", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.multi_rtl_source_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.multi_rtl_source_0, 1), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.multi_rtl_source_0, 1), (self.blocks_tag_debug_0, 0))    
        self.connect((self.multi_rtl_source_0, 0), (self.blocks_tag_debug_0_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = test_sync()
    tb.start()
    tb.wait()
