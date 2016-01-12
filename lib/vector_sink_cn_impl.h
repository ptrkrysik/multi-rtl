/* -*- c++ -*- */
/*
 * Copyright 2004,2008,2009,2013 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

// WARNING: this file is machine generated. Edits will be overwritten

#ifndef INCLUDED_MULTI_RTL_VECTOR_SINK_CN_IMPL_H
#define INCLUDED_MULTI_RTL_VECTOR_SINK_CN_IMPL_H

#include <multi_rtl/vector_sink_cn.h>


namespace gr {
  namespace multi_rtl {

    class vector_sink_cn_impl : public vector_sink_cn
    {
    private:
      std::vector< std::vector<gr_complex> > d_data;
      std::vector<tag_t> d_tags;
      int d_vlen;
      int d_finite;
      int d_nsamp;
      int d_num_channels;
      int d_samp_counter;
      feval * d_fullness_norifier;

    public:
      vector_sink_cn_impl(int vlen, bool finite, int nsamp, int num_channels, feval * fullness_norifier);
      ~vector_sink_cn_impl();

      void reset();
      std::vector< std::vector<gr_complex> > data() const;
      std::vector<tag_t> tags() const;

      int work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);
    };

  } /* namespace multi_rtl */
} /* namespace gr */

#endif /* INCLUDED_MULTI_RTL_VECTOR_SINK_CN_IMPL_H */
