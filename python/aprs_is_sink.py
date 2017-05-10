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

from gnuradio import gr
from threading import Thread, Event
import pmt
import socket

class aprs_is_sink(gr.sync_block):
    """
    docstring for block aprs_is_sink
    """
    def __init__(self, host, port, callsign, password):
        gr.sync_block.__init__(self,
            name="APRS-IS sink",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self._handle_msg)

        self.d_host = host
        self.d_port = port
        self.d_callsign = callsign
        self.d_password = password

        self.d_socket = None

    def start(self):
        self.d_thread = Thread(
            target = self._thread_main
        )
        self.d_stop = Event()

        print "Connecting to %s:%d" % (self.d_host, self.d_port)

        self.d_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.d_socket.connect((self.d_host, self.d_port))
        self.d_socket.sendall('user %s pass %d\n' % (self.d_callsign, self.d_password))

        self.d_thread.start()
        return True

    def stop(self):
        self.d_stop.set()
        self.d_thread.join()

        if self.d_socket != None:
            self.d_socket.close()
            self.d_socket = None

        return True

    def _handle_msg(self, msg_pmt):
        pkt = pmt.to_python(msg_pmt)
        msg = pack_message(pkt)
        print " >", msg,
        if self.d_socket != None:
            self.d_socket.sendall(msg)
        else:
            print "...no socket"

    def _thread_main(self):
        self.d_socket.settimeout(0.1)
        while not self.d_stop.is_set():
            try:
                data = self.d_socket.recv(1024)
                if data:
                    print "< ", data,
            except:
                pass
            self.d_stop.wait(0.1)

def secure_text(text):
    # TODO: fixme
    return text

def pack_message(pkt):
    lines_info = pkt['info'].splitlines()
    return "%s>%s%s:%s\r\n" % (
        secure_text(pkt['src']),
        secure_text(pkt['dst']),
        secure_text("".join([ ","+x for x in pkt['path']])),
        secure_text(lines_info[0])
    )
