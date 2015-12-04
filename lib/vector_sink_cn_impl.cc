/* -*- c++ -*- */
/*
 * Copyright 2004,2008,2010,2013 Free Software Foundation, Inc.
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

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <vector_sink_cn_impl.h>
#include <gnuradio/io_signature.h>
#include <algorithm>
#include <iostream>

namespace gr {
  namespace multi_rtl {

    vector_sink_cn::sptr
    vector_sink_cn::make(int vlen, bool finite, int nsamp, feval * fullness_norifier)
    {
      return gnuradio::get_initial_sptr
        (new vector_sink_cn_impl(vlen, finite, nsamp, fullness_norifier));
    }

    vector_sink_cn_impl::vector_sink_cn_impl(int vlen, bool finite, int nsamp, feval * fullness_norifier)
    : sync_block("vector_sink_c",
                    io_signature::make(1, 1, sizeof(gr_complex) * vlen),
                    io_signature::make(0, 0, 0)),
    d_vlen(vlen), d_finite(finite), d_nsamp(nsamp), d_samp_couter(0), d_fullness_norifier(fullness_norifier)
    {
    }

    vector_sink_cn_impl::~vector_sink_cn_impl()
    {}

    std::vector<gr_complex>
    vector_sink_cn_impl::data() const
    {
      return d_data;
    }

    std::vector<tag_t>
    vector_sink_cn_impl::tags() const
    {
      return d_tags;
    }

    int
    vector_sink_cn_impl::work(int noutput_items,
                      gr_vector_const_void_star &input_items,
                      gr_vector_void_star &output_items)
    {
      gr_complex *iptr = (gr_complex*)input_items[0];

      if((!d_finite) || (d_samp_couter < d_nsamp)){
          for(int i = 0; (i < noutput_items * d_vlen); i++){
            d_data.push_back (iptr[i]);
            d_samp_couter++;
            if(d_finite && (d_samp_couter>=d_nsamp)){
                if(d_fullness_norifier!=NULL){
                    d_fullness_norifier->calleval();
                }
                break;
            }
          }
          
          std::vector<tag_t> tags;
          get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + noutput_items);
          d_tags.insert(d_tags.end(), tags.begin(), tags.end());
      }
      return noutput_items;
    }

  } /* namespace multi_rtl */
} /* namespace gr */
