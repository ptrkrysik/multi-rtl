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

    
  
if __name__ == "__main__":
    samp_rate = 1625000/6*4
    N = int(2*samp_rate)
    blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, N)
    blocks_head_1 = blocks.head(gr.sizeof_gr_complex*1, N)
    file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "temp1", False)
    file_sink_0.set_unbuffered(True)
    file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, "temp2", False)
    file_sink_1.set_unbuffered(True)
    multi_rtl_source_0 = multi_rtl.multi_rtl_source(samp_rate=samp_rate, ppm=-7, sync_fc=100e6)
#    nsink = blocks.null_sink(gr.sizeof_gr_complex*1)
#    nsink2 = blocks.null_sink(gr.sizeof_gr_complex*1)

    tb = gr.top_block()    
    tb.connect((multi_rtl_source_0,0),(blocks_head_0,0))
    tb.connect((multi_rtl_source_0,1),(blocks_head_1,0))
    tb.connect((blocks_head_0,0),(file_sink_0,0))
    tb.connect((blocks_head_1,0),(file_sink_1,0))
    tb.start()
    tb.wait()
