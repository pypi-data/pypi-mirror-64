# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2020 Kevin Walchko
# see LICENSE for full details
##############################################
import pickle

class PickleJar(object):
    def __init__(self, fname, buffer_size=500):
        self.fd = open(fname, 'wb')
        self.buffer = {}
        self.buffer_size = buffer_size
        self.counter = 0

    def __del__(self):
        self.close()

    def push(self, topic, data):
        # self.buffer.append(data)
        if topic not in self.buffer:
            self.buffer[topic] = []
        self.buffer[topic].append(data)
        self.counter += 1
        if self.counter > self.buffer_size:
            self.write()
            self.counter = 0

    def write(self):
        for d in self.buffer:
            pickle.dump(d, self.fd)
        self.buffer = {}

    def close(self):
        self.fd.close()
