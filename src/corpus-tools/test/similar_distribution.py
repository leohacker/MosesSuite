#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

factor = int(sys.argv[1])

feq = {}
for i in xrange(factor + 1):
    feq[i] = 0

fp = open("sim.log", 'r')
for line in fp:
    if (line == 'inf'):
        continue
    value = float(line)
    index = int(value * factor)
    if index >= factor:
        index = factor
    feq[index] += 1

print feq
