#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Test Sync
# Generated: Wed Jan 13 22:44:34 2016
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
        self.samp_rate = samp_rate = 1625000/6.0*4

        ##################################################
        # Blocks
        ##################################################
        self.multi_rtl_source_1 = multi_rtl.multi_rtl_source(sample_rate=samp_rate, num_channels=2, ppm=-7, sync_center_freq=939.4e6, rtlsdr_id_strings= [ 
          "0", 
          "1", 
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
        self.multi_rtl_source_1.set_sync_gain(25, 0)
        self.multi_rtl_source_1.set_gain(30, 0)
        self.multi_rtl_source_1.set_center_freq(939.4e6, 0)
        self.multi_rtl_source_1.set_sync_gain(25, 1)
        self.multi_rtl_source_1.set_gain(30, 1)
        self.multi_rtl_source_1.set_center_freq(939.4e6, 1)
          
        self.blocks_head_1_0 = blocks.head(gr.sizeof_gr_complex*1, int(5*samp_rate))
        self.blocks_head_1 = blocks.head(gr.sizeof_gr_complex*1, int(5*samp_rate))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, 1024)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/piotr/Odbiornik_gsm/multi_rtl/examples/temp2", False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "/home/piotr/Odbiornik_gsm/multi_rtl/examples/temp1", False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_1, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.blocks_head_1_0, 0), (self.blocks_file_sink_0_0, 0))    
        self.connect((self.multi_rtl_source_1, 0), (self.blocks_head_1, 0))    
        self.connect((self.multi_rtl_source_1, 1), (self.blocks_head_1_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_head_1.set_length(int(5*self.samp_rate))
        self.blocks_head_1_0.set_length(int(5*self.samp_rate))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = test_sync()
    tb.start()
    tb.wait()
