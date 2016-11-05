#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Nov  4 18:48:57 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from chn_recv import chn_recv  # grc-generated hier_block
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import igate
import sip
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.rf_samp_rate = rf_samp_rate = samp_rate*32
        self.rf_gain = rf_gain = 30
        self.freq = freq = 144.8e6

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_range = Range(0, 100, 1, 30, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "rf_gain", "counter_slider", float)
        self.top_layout.addWidget(self._rf_gain_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(rf_samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq+200e3, 0)
        self.uhd_usrp_source_0.set_gain(rf_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq+200e3, #fc
        	rf_samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(True)
        
        
          
        self.igate_debug_print_msg_0 = igate.debug_print_msg()
        self.igate_aprs_pkt_gen_0 = igate.aprs_pkt_gen(3.0, 'SA6BBC-10', 'APN123', '', 240, 3, 'something')
        self.igate_aprs_append_path_0 = igate.aprs_append_path('qAR,SA6BBC-10')
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(rf_samp_rate / samp_rate, (firdes.low_pass(1, rf_samp_rate, 12500, 2000)), -200e3, rf_samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.chn_recv_0 = chn_recv(
            samp_rate=samp_rate,
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.chn_recv_0, 'out'), (self.igate_aprs_append_path_0, 'in'))    
        self.msg_connect((self.igate_aprs_append_path_0, 'out'), (self.igate_debug_print_msg_0, 'in'))    
        self.msg_connect((self.igate_aprs_pkt_gen_0, 'out'), (self.igate_debug_print_msg_0, 'in'))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.chn_recv_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_rf_samp_rate(self.samp_rate*32)
        self.chn_recv_0.set_samp_rate(self.samp_rate)

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.rf_samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(self.freq+200e3, self.rf_samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.low_pass(1, self.rf_samp_rate, 12500, 2000)))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.uhd_usrp_source_0.set_gain(self.rf_gain, 0)
        	

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq+200e3, 0)
        self.qtgui_sink_x_0.set_frequency_range(self.freq+200e3, self.rf_samp_rate)


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
