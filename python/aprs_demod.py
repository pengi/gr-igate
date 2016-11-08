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

from gnuradio import analog
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import igate
import math

class aprs_demod(gr.hier_block2):
    """
    docstring for block aprs_demod
    """
    def __init__(self, samp_rate):
        gr.hier_block2.__init__(self,
            "APRS demod",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out("out")

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.bit_rate = bit_rate = 1200

        ##################################################
        # Blocks
        ##################################################
        self.igate_clock_recovery_timer_bb_0 = igate.clock_recovery_timer_bb(samp_rate/bit_rate)
        self.igate_aprs_air_to_is_pp_0 = igate.aprs_air_to_is_pp()
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, (firdes.low_pass(1, samp_rate, 1200, 200)), (1200+2200)/2, samp_rate)
        self.digital_map_bb_0 = digital.map_bb(([1,0]))
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(16, 1024)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*5008.0))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.igate_aprs_air_to_is_pp_0, 'in'))
        self.msg_connect((self.igate_aprs_air_to_is_pp_0, 'out'), (self, 'out'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.igate_clock_recovery_timer_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.igate_clock_recovery_timer_bb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 1200, 200)))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*5008.0))

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
