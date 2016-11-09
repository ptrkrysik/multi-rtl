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
    vector_sink_cn::make(int vlen, bool finite, int nsamp, int num_channels, feval * fullness_norifier)
    {
      return gnuradio::get_initial_sptr
        (new vector_sink_cn_impl(vlen, finite, nsamp, num_channels, fullness_norifier));
    }

    vector_sink_cn_impl::vector_sink_cn_impl(int vlen, bool finite, int nsamp, int num_channels, feval * fullness_norifier)
    : sync_block("vector_sink_c",
                    io_signature::make(num_channels, num_channels, sizeof(gr_complex) * vlen),
                    io_signature::make(0, 0, 0)),
    d_vlen(vlen), d_finite(finite), d_nsamp(nsamp), d_samp_counter(0), d_fullness_norifier(fullness_norifier), d_num_channels(num_channels)
    {
        int ch;
        d_data.resize(d_num_channels);
        for(ch=0; ch<d_num_channels; ch++){
            d_data[ch].resize(d_nsamp);
//            d_data.push_back(boost::shared_ptr<std::vector<gr_complex> >(new std::vector<gr_complex>(nsamp)));
        }
    }

    void vector_sink_cn_impl::reset(){
        int ch;
        d_samp_counter = 0;
        for(ch=0; ch<d_num_channels; ch++){
            d_data[ch].clear();
        }
    }

    vector_sink_cn_impl::~vector_sink_cn_impl()
    {}

    std::vector< std::vector<gr_complex> >
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
//      gr_complex *iptr = (gr_complex*)input_items[0];
        
      int ch;

      if(d_finite) {
        if(d_samp_counter < d_nsamp){
          bool full=false;
          int samples_to_copy=0;
          if((noutput_items+d_samp_counter) >= d_nsamp){
            int samples_to_copy = d_nsamp-d_samp_counter;
            d_samp_counter=d_samp_counter+samples_to_copy;
            full = true;
          } else {
            samples_to_copy = noutput_items;
            d_samp_counter = d_samp_counter+noutput_items;
          }
                
          for(ch=0; ch<d_num_channels; ch++){
              for(int i = 0; (i < samples_to_copy * d_vlen); i++){
                d_data[ch].push_back (((gr_complex*)input_items[ch])[i]);
              }              
              
                std::vector<tag_t> tags;
                get_tags_in_range(tags, ch, nitems_read(ch), nitems_read(ch) + noutput_items);
                d_tags.insert(d_tags.end(), tags.begin(), tags.end());
          }
          if(full){
              if(d_fullness_norifier!=NULL){
                  d_fullness_norifier->calleval();
              }
          }
        }
      } else {
        for(ch=0; ch<d_num_channels; ch++){
          for(int i = 0; (i < noutput_items * d_vlen); i++){
            d_data[ch].push_back (((gr_complex*)input_items[ch])[i]);
          }              
          
              std::vector<tag_t> tags;
              get_tags_in_range(tags, ch, nitems_read(ch), nitems_read(ch) + noutput_items);
              d_tags.insert(d_tags.end(), tags.begin(), tags.end());
        }
      }
      
      return noutput_items;
    }

  } /* namespace multi_rtl */
} /* namespace gr */
