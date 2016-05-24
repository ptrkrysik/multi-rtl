INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MULTI_RTL multi_rtl)

FIND_PATH(
    MULTI_RTL_INCLUDE_DIRS
    NAMES multi_rtl/api.h
    HINTS $ENV{MULTI_RTL_DIR}/include
        ${PC_MULTI_RTL_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MULTI_RTL_LIBRARIES
    NAMES multi_rtl
    HINTS $ENV{MULTI_RTL_DIR}/lib
        ${PC_MULTI_RTL_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MULTI_RTL DEFAULT_MSG MULTI_RTL_LIBRARIES MULTI_RTL_INCLUDE_DIRS)
MARK_AS_ADVANCED(MULTI_RTL_LIBRARIES MULTI_RTL_INCLUDE_DIRS)

