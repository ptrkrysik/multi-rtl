"""
Copyright 2012 Free Software Foundation, Inc.

This file is part of GNU Radio

GNU Radio Companion is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

GNU Radio Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

template_main = """\
id: multi_rtl_source
label: Multi-RTL Source
flags: [ throttle, python ]

paramters:
-   id: sample_rate
    label: Sample Rate (sps)
    dtype: real
    default: samp_rate
-   id: corr
    label: Freq. Corr. (ppm)
    dtype: real
    default: 0
-   id: sync_freq
    label: Sync Frequency (Hz)
    category: Synchronization
    dtype: real
    default: 100e6
-   id: nchan
    label: Num Channels
    dtype: int
    default: 1
    options: [ \\
    % for n in range(1, max_nchan):
${n}, \\
    % endfor
${max_nchan} ]
    option_labels: [ \\
    % for n in range(1, max_nchan):
${n}, \\
    % endfor
${max_nchan} ]
${params}

outputs:
-   domain: stream
    label: out
    dtype: complex
    multiplicity: ${"$"}{nchan}

asserts:
-   ${max_nchan} >= ${"$"}{nchan}
-   ${"$"}{nchan} > 0

templates:
    imports: import multi_rtl
    make: |-
        multi_rtl.multi_rtl_source(sample_rate=${"$"}{sample_rate}, num_channels=${"$"}{nchan}, ppm=${"$"}{corr}, sync_center_freq=${"$"}{sync_freq}, rtlsdr_id_strings= [ \\
    % for n in range(max_nchan - 1):
${"$"}{id_string${n}}, \\
    % endfor
${"$"}{id_string${max_nchan-1}} ])
        %for n in range(max_nchan):
        ${"%"} if nchan() > ${n}:
        self.${"$"}{id}.set_sync_gain(${"$"}{sync_gain${n}}, ${n})
        self.${"$"}{id}.set_gain(${"$"}{gain${n}}, ${n})
        self.${"$"}{id}.set_center_freq(${"$"}{freq${n}}, ${n})
        self.${"$"}{id}.set_gain_mode(${"$"}{gain_mode${n}}, ${n})
        ${"%"} endif
        %endfor
    callbacks:
    -   set_freq_corr(${"$"}{corr})
    -   set_sync_center_freq(${"$"}{sync_freq})
    % for n in range(max_nchan):
    -   set_center_freq(${"$"}{freq${n}}, ${n})
    -   set_gain(${"$"}{gain${n}}, ${n})
    -   set_gain_mode(${"$"}{gain_mode${n}}, ${n})
    -   set_sync_gain(${"$"}{sync_gain${n}}, ${n})
    % endfor

documentation: |-
    The multi_rtl_source block

file_format: 1

"""

template_p = """\
-   id: sync_gain${n}
    label: "Ch${n}: Sync RF Gain (dB)"
    category: Synchronization
    dtype: real
    default: 10
    hide: |-
        ${"%"} if nchan() > n:
        part
        ${"%"} else:
        all
        ${"%"} endif
-   id: freq${n}
    label: "Ch${n}: Frequency (Hz)"
    category: RF Options
    dtype: real
    default: 100e6
    hide: |-
        ${"%"} if nchan() > n:
        none
        ${"%"} else:
        all
        ${"%"} endif
-   id: gain${n}
    label: "Ch${n}: RF Gain (dB)"
    category: RF Options
    dtype: real
    default: 10
    hide: |-
        ${"%"} if nchan() > n:
        part
        ${"%"} else:
        all
        ${"%"} endif
-   id: gain_mode${n}
    label: "Ch${n}: Gain Mode"
    category: RF Options
    dtype: bool
    default: False
    hide: |-
        ${"%"} if nchan() > n:
        part
        ${"%"} else:
        all
        ${"%"} endif
    options: [ False, True ]
    option_labels: [ Manual, Automatic ]
-   id: id_string${n}
    label: "Ch${n}: ID string"
    dtype: string
    default: "${n}"
    hide: |-
        ${"%"} if nchan() > n:
        part
        ${"%"} else:
        all
        ${"%"} endif
"""

max_num_mboards = 8
max_num_channels = max_num_mboards*4

from mako.template import Template
import os

if __name__ == '__main__':
    for file in os.sys.argv[1:]:
      head, tail = os.path.split(file)

      if tail.startswith('multi_rtl_source'):
          title = 'multi-rtl'
          prefix = 'multi_rtl'
      else: raise(Exception, 'file %s has wrong syntax!'%tail)

      params = ''.join([Template(template_p).render( n = n ) for n in range(max_num_channels)])

      open(file, 'w').write( Template(template_main).render( max_nchan = max_num_channels, params = params ))
