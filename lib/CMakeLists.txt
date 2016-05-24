# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND multi_rtl_sources
    vector_sink_cn_impl.cc )

set(multi_rtl_sources "${multi_rtl_sources}" PARENT_SCOPE)
if(NOT multi_rtl_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT multi_rtl_sources)

add_library(multi_rtl SHARED ${multi_rtl_sources})
target_link_libraries(multi_rtl ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(multi_rtl PROPERTIES DEFINE_SYMBOL "multi_rtl_EXPORTS")

if(APPLE)
    set_target_properties(multi_rtl PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
install(TARGETS multi_rtl
    LIBRARY DESTINATION lib${LIB_SUFFIX} # .so/.dylib file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} # .lib file
    RUNTIME DESTINATION bin              # .dll file
)

########################################################################
# Build and register unit test
########################################################################
include(GrTest)

include_directories(${CPPUNIT_INCLUDE_DIRS})

list(APPEND test_multi_rtl_sources
    ${CMAKE_CURRENT_SOURCE_DIR}/test_multi_rtl.cc
    ${CMAKE_CURRENT_SOURCE_DIR}/qa_multi_rtl.cc
)

add_executable(test-multi_rtl ${test_multi_rtl_sources})

target_link_libraries(
  test-multi_rtl
  ${GNURADIO_RUNTIME_LIBRARIES}
  ${Boost_LIBRARIES}
  ${CPPUNIT_LIBRARIES}
  multi_rtl
)

GR_ADD_TEST(test_multi_rtl test-multi_rtl)
