#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Nov  8 21:54:42 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import igate


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 9600
        self.if_samp_rate = if_samp_rate = samp_rate*4
        self.rf_samp_rate = rf_samp_rate = if_samp_rate*32
        self.freq = freq = 144.8e6

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=samp_rate/100,
                decimation=441,
                taps=None,
                fractional_bw=None,
        )
        self.igate_debug_print_msg_0 = igate.debug_print_msg()
        self.igate_aprs_pkt_gen_0 = igate.aprs_pkt_gen(3.0, 'SA6BBC-10', 'APN123', '', 240, 3, 'something')
        self.igate_aprs_demod_0 = igate.aprs_demod(9600)
        self.igate_aprs_append_path_0 = igate.aprs_append_path('qAR,SA6BBC-10')
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/Users/msikstrom/Desktop/tnctest/tnc_test01.wav', False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.igate_aprs_append_path_0, 'out'), (self.igate_debug_print_msg_0, 'in'))    
        self.msg_connect((self.igate_aprs_demod_0, 'out'), (self.igate_aprs_append_path_0, 'in'))    
        self.msg_connect((self.igate_aprs_pkt_gen_0, 'out'), (self.igate_debug_print_msg_0, 'in'))    
        self.connect((self.blocks_wavfile_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.igate_aprs_demod_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_if_samp_rate(self.samp_rate*4)

    def get_if_samp_rate(self):
        return self.if_samp_rate

    def set_if_samp_rate(self, if_samp_rate):
        self.if_samp_rate = if_samp_rate
        self.set_rf_samp_rate(self.if_samp_rate*32)

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
