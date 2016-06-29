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

MAIN_TMPL = """\
<?xml version="1.0"?>
<block>
  <name>Multi-RTL Source</name>
  <key>multi_rtl_source</key>
  <category>Multi-RTL</category>
  <throttle>1</throttle>
  <import>import multi_rtl</import>
  <make>multi_rtl.multi_rtl_source(sample_rate=\$sample_rate, num_channels=\$nchan, ppm=\$corr, sync_center_freq=\$sync_freq, rtlsdr_id_strings= [ 
  #for $n in range($max_nchan)  
  \$id_string$(n), 
  #end for 
  ])
#for $n in range($max_nchan)
    \#if \$nchan() > $n
self.\$(id).set_sync_gain(\$sync_gain$(n), $n)
self.\$(id).set_gain(\$gain$(n), $n)
self.\$(id).set_center_freq(\$freq$(n), $n)
self.\$(id).set_gain_mode(\$gain_mode$(n), $n)
    \#end if
#end for
  </make>
  <callback>set_freq_corr(\$corr)</callback>
  <callback>set_sync_center_freq(\$sync_freq)</callback>  
#for $n in range($max_nchan)
  <callback>set_center_freq(\$freq$(n), $n)</callback>
  <callback>set_gain(\$gain$(n), $n)</callback>
  <callback>set_gain_mode(\$gain_mode$(n), $n)</callback>
  <callback>set_sync_gain(\$sync_gain$(n), $n)</callback>
#end for
  
  <param>
    <name>Sample Rate (sps)</name>
    <key>sample_rate</key>
    <value>samp_rate</value>
    <type>real</type>
  </param>
  
  <param>
  <name>Freq. Corr. (ppm)</name>
    <key>corr</key>
    <value>0</value>
    <type>real</type>
  </param>
  <param>
    <name>Sync Frequency (Hz)</name>
    <key>sync_freq</key>
    <value>100e6</value>
    <type>real</type>
    <tab>Synchronization</tab>
  </param>

  <param>
    <name>Num Channels</name>
    <key>nchan</key>
    <value>1</value>
    <type>int</type>
    #for $n in range(1, $max_nchan+1)
    <option>
      <name>$(n)</name>
      <key>$n</key>
    </option>
    #end for
  </param>  
  
  $params
  
  <check>$max_nchan >= \$nchan</check>
  <check>\$nchan > 0</check>
  <source>
    <name>out</name>
    <type>complex</type>
    <nports>\$nchan</nports>
  </source>
  <doc>
    The multi_rtl_source block
  </doc>  
  
</block>
"""

PARAMS_TMPL = """
  <param>
    <name>Ch$(n): Sync RF Gain (dB)</name>
    <key>sync_gain$(n)</key>
    <value>10</value>
    <type>real</type>
    <hide>\#if \$nchan() > $n then 'part' else 'all'#</hide>
    <tab>Synchronization</tab>
  </param>
  <param>
    <name>Ch$(n): Frequency (Hz)</name>
    <key>freq$(n)</key>
    <value>100e6</value>
    <type>real</type>
    <hide>\#if \$nchan() > $n then 'none' else 'all'#</hide>
    <tab>RF Options</tab>
  </param>
  <param>
    <name>Ch$(n): RF Gain (dB)</name>
    <key>gain$(n)</key>
    <value>10</value>
    <type>real</type>
    <hide>\#if \$nchan() > $n then 'part' else 'all'#</hide>
    <tab>RF Options</tab>
  </param>
  <param>
    <name>Ch$(n): Gain Mode</name>
    <key>gain_mode$(n)</key>
    <value>False</value>
    <type>bool</type>
    <hide>\#if \$nchan() > $n then 'part' else 'all'#</hide>
    <option>
      <name>Manual</name>
      <key>False</key>
    </option>
    <option>
      <name>Automatic</name>
      <key>True</key>
    </option>
    <tab>RF Options</tab>
  </param>
  <param>
    <name>Ch$(n): ID string</name>
    <key>id_string$(n)</key>
    <value>"$(n)"</value>
    <type>string</type>
    <hide>\#if \$nchan() > $n then 'part' else 'all'#</hide>
  </param>
"""

def parse_tmpl(_tmpl, **kwargs):
  from Cheetah import Template
  return str(Template.Template(_tmpl, kwargs))

max_num_mboards = 8
max_num_channels = max_num_mboards*4

import os.path

if __name__ == '__main__':
  import sys
  for file in sys.argv[1:]:
    head, tail = os.path.split(file)

    if tail.startswith('multi_rtl_source'):
      title = 'multi-rtl'
      prefix = 'multi_rtl'        
    else: raise Exception, 'file %s has wrong syntax!'%tail

    params = ''.join([parse_tmpl(PARAMS_TMPL, n=n) for n in range(max_num_channels)])
    
    open(file, 'w').write(parse_tmpl(MAIN_TMPL,
      max_nchan=max_num_channels,
      params=params,
    ))
