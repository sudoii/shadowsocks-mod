#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import sys
import hashlib
import logging

from shadowsocks.common import ord

def create_obfs(method):
    return plain(method)

obfs_map = {
        'plain': (create_obfs,),
        'origin': (create_obfs,),
}

class plain(object):
    def __init__(self, method):
        self.method = method
        self.server_info = None

    def init_data(self):
        return b''

    def get_overhead(self, direction): # direction: true for c->s false for s->c
        return 0

    def get_server_info(self):
        return self.server_info

    def set_server_info(self, server_info):
        self.server_info = server_info

    def client_pre_encrypt(self, buf):
        return buf

    def client_encode(self, buf):
        return buf

    def client_decode(self, buf):
        # (buffer_to_recv, is_need_to_encode_and_send_back)
        return (buf, False)

    def client_post_decrypt(self, buf):
        return buf

    def server_pre_encrypt(self, buf):
        return buf

    def server_encode(self, buf):
        return buf

    def server_decode(self, buf):
        # (buffer_to_recv, is_need_decrypt, is_need_to_encode_and_send_back)
        return (buf, True, False)

    def server_post_decrypt(self, buf):
        return (buf, False)

    def client_udp_pre_encrypt(self, buf):
        return buf

    def client_udp_post_decrypt(self, buf):
        return buf

    def server_udp_pre_encrypt(self, buf, uid):
        return buf

    def server_udp_post_decrypt(self, buf):
        return (buf, None)

    def dispose(self):
        pass

    def get_head_size(self, buf, def_value):
        if len(buf) < 2:
            return def_value
        head_type = ord(buf[0]) & 0x7
        if head_type == 1:
            return 7
        if head_type == 4:
            return 19
        if head_type == 3:
            return 4 + ord(buf[1])
        return def_value
