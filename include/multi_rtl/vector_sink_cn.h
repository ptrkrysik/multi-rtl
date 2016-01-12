/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_MULTI_RTL_VECTOR_SINK_CN_H
#define INCLUDED_MULTI_RTL_VECTOR_SINK_CN_H

#include <multi_rtl/api.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/feval.h>

namespace gr {
  namespace multi_rtl {

    /*!
     * \brief gr_complex sink that writes to a vector
     * \ingroup multi_rtl
     */
    class MULTI_RTL_API vector_sink_cn : virtual public sync_block
    {
    public:
      // gr::blocks::vector_sink_cn::sptr
      typedef boost::shared_ptr<vector_sink_cn> sptr;

      static sptr make(int vlen = 1, bool finite=false, int nsamp=0, int num_channels=1, feval * fullness_norifier=NULL);

      virtual void reset() = 0;
      virtual std::vector< std::vector<gr_complex> > data() const = 0;
      virtual std::vector<tag_t> tags() const = 0;
    };

  } // namespace multi_rtl
} // namespace gr

#endif /* INCLUDED_MULTI_RTL_VECTOR_SINK_CN_H */



