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
import pmt
import sys

class ax25_decode_pp(gr.basic_block):
    """
    docstring for block ax25_decode_pp
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="AX25 decoder",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def forecast(self, noutput_items, ninput_items_required):
        pass

    def general_work(self, input_items, output_items):
        return 0

    def handle_msg(self, msg_pmt):
        meta = pmt.to_python(pmt.car(msg_pmt))
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] invalid message"
        else:
            msg_str = "".join([chr(x) for x in pmt.u8vector_elements(msg)])
            print printpacket(msg_str)
            sys.stdout.flush()

def printpacket(pkt):
    string=""
    idx=0
    v1=1
    lun=len(pkt)
    if lun<8:
        return "ERROR: Packet can't be shorter than 8 bytes (%u)" % len(pkt)
    if (ord(pkt[idx+1]) & 0x01):
        #flexnet header compression
        v1=0
        cmd=(ord(pkt[idx+1]) & 2)!=0
        string="fm ? to "
        i=(ord(pkt[idx+2])>>2) & 0x3f
        if i:
            string+=chr(i+0x20)
        i = ((ord(pkt[idx+2]) << 4) | ((ord(pkt[idx+3]) >> 4) & 0xf)) & 0x3f
        if i:
            string+=chr(i+0x20)
        i = ((ord(pkt[idx+3]) << 2) | ((ord(pkt[idx+4]) >> 6) & 3)) & 0x3f
        if i:
            string+=chr(i+0x20)
        i = ord(pkt[idx+4]) & 0x3f
        if i:
            string+=chr(i+0x20)
        i = (ord(pkt[idx+5]) >> 2) & 0x3f
        if i:
            string+=chr(i+0x20)
        i = ((ord(pkt[idx+5]) << 4) | ((ord(pkt[idx+6]) >> 4) & 0xf)) & 0x3f
        if i:
            string+=chr(i+0x20)
        string+="-%u QSO Nr %u" % (ord(pkt[idx+6]) & 0xf, (ord(pkt[idx+0]) << 6) | (ord(pkt[idx+1]) >> 2))
        idx+=7
        lun-=7
    else:
        #normal header
        if lun<15:
            return "ERROR: Packet can't be shorter than 15 bytes (%u)" % len(pkt)
        if ((ord(pkt[idx+6]) & 0x80) != (ord(pkt[idx+13]) & 0x80)):
            v1=0
            cmd=(ord(pkt[idx+6]) & 0x80)
        string+="fm "
        for i in range(7,13):
            if (ord(pkt[idx+i])&0xfe)!=0x40:
                string+=chr(ord(pkt[idx+i])>>1)
        string+="-%u to " % ((ord(pkt[idx+13])>>1) & 0x0f)
        for i in range(6):
            if (ord(pkt[idx+i])&0xfe)!=0x40:
                string+=chr(ord(pkt[idx+i])>>1)
        string+="-%u" % ((ord(pkt[idx+6])>>1) & 0x0f)
        idx+=14
        lun-=14
        if (not(ord(pkt[idx-1]) & 1)) and (lun >= 7):
            string+=" via "
        while (not(ord(pkt[idx-1]) & 1)) and (lun >= 7):
            for i in range(6):
                if ((ord(pkt[idx+i])&0xfe)!=0x40):
                    string+=chr(ord(pkt[idx+i])>>1)
            string+="-%u" % (ord(pkt[idx+6])>>1 & 0x0f)
            idx+=7
            lun-=7
            if (not(ord(pkt[idx-1]) & 1)) and (lun>=7):
                string+=","
    if (lun==0):
            return string
    i=ord(pkt[idx])
    idx+=1
    lun-=1
    if v1:
        if i & 0x10:
            j="!"
        else:
            j=" "
    else:
        if i & 0x10:
            if cmd:
                j="+"
            else:
                j="-"
        else:
            if cmd:
                j="^"
            else:
                j="v"
    if (not(i & 1)):
        #Info frame
        string+=" I%u%u%c" % ((i >> 5) & 7, (i >> 1) & 7, j)
    elif (i & 2):
        #U frame
        ii=(i & (~0x10))
        if ii==0x03:
            string+=" UI%c" % j
        elif ii==0x2f:
            string+=" SABM%c" % j
        elif ii==0x43:
            string+=" DISC%c" % j
        elif ii==0x0f:
            string+=" DM%c" % j
        elif ii==0x63:
            string+=" UA%c" % j
        elif ii==0x87:
            string+=" FRMR%c" % j
        else:
            string+=" unknown U (0x%x)%c" % (i & (~0x10), j)
    else:
        #supervisory
        ii=(i & 0xf)
        if ii==0x1:
            string+=" RR%u%c" % ((i >> 5) & 7, j)
        elif ii==0x5:
            string+=" RNR%u%c" % ((i >> 5) & 7, j)
        elif ii==0x9:
            string+=" REJ%u%c" % ((i >> 5) & 7, j)
        else:
            string+=" unknown S (0x%x)%u%c" % (i & 0xf, (i >> 5) & 7, j)
    if (lun==0):
        string+="\n"
        return string
    string+=" pid=%02X\n" % ord(pkt[idx])
    idx+=1
    lun-=1
    j=0
    while lun:
        i=ord(pkt[idx])
        idx+=1
        if (i>=32) and (i<128):
            string+=chr(i)
        elif i==13:
            if j:
                string+="\n"
            j=0
        else:
            string+="."
        if i>=32:
            j=1
        lun-=1
    if j:
        string+="\n"
    return string
