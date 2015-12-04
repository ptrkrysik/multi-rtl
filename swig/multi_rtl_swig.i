/* -*- c++ -*- */

#define MULTI_RTL_API

%include "gnuradio.i"			// the common stuff
%include "feval.i"

//load generated python docstrings
%include "multi_rtl_swig_doc.i"

%{
#include "multi_rtl/vector_sink_cn.h"
%}

%include "multi_rtl/vector_sink_cn.h"
GR_SWIG_BLOCK_MAGIC2(multi_rtl, vector_sink_cn);
