#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
import pmt
from aprs_is_sink import pack_message

class qa_aprs_is_sink (gr_unittest.TestCase):

    def setUp (self):
        self.msglog = []

    def tearDown (self):
        pass

    def test_001_simple_pack (self):
        stimuli = {
            'src': 'DST2ZZ-3',
            'dst': 'SRC1ZZ-13',
            'path': ['MID1-5*', 'MID2-2'],
            'info': 'stuff'
        }
        expect = "DST2ZZ-3>SRC1ZZ-13,MID1-5*,MID2-2:stuff\r\n"
        self.assertEquals(pack_message(stimuli), expect)

    def test_002_trim_first_line_LF (self):
        stimuli = {
            'src': 'DST2ZZ-3',
            'dst': 'SRC1ZZ-13',
            'path': ['MID1-5*', 'MID2-2'],
            'info': 'stuff and stuff\nboll'
        }
        expect = "DST2ZZ-3>SRC1ZZ-13,MID1-5*,MID2-2:stuff and stuff\r\n"
        self.assertEquals(pack_message(stimuli), expect)

    def test_003_trim_first_line_CR (self):
        stimuli = {
            'src': 'DST2ZZ-3',
            'dst': 'SRC1ZZ-13',
            'path': ['MID1-5*', 'MID2-2'],
            'info': 'stuff and stuff\rboll'
        }
        expect = "DST2ZZ-3>SRC1ZZ-13,MID1-5*,MID2-2:stuff and stuff\r\n"
        self.assertEquals(pack_message(stimuli), expect)
        
    def test_004_binary_safe (self):
        info_bin = range(256)
        info_bin.remove(ord('\n')) # Linebreaks will be removed, se above
        info_bin.remove(ord('\r')) # Linebreaks will be removed, se above
        info = "".join([chr(c) for c in info_bin])
        stimuli = {
            'src': 'DST2ZZ-3',
            'dst': 'SRC1ZZ-13',
            'path': ['MID1-5*', 'MID2-2'],
            'info': info
        }
        expect = "DST2ZZ-3>SRC1ZZ-13,MID1-5*,MID2-2:"+info+"\r\n"
        self.assertEquals(pack_message(stimuli), expect)

if __name__ == '__main__':
    gr_unittest.run(qa_aprs_is_sink, "qa_aprs_is_sink.xml")
