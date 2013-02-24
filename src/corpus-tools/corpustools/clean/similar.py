#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, Leo Jiang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author:   Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301

"""
Predicate Module: Similar
"""

from nltk.metrics import edit_distance

def validate(step):
    return True

def predicate(source, target, constraint):      # pylint: disable=I0011,W0613
    """Return True if source is similar to target."""
    source = source.strip()
    target = target.strip()
    if constraint["threshold"] == 0:
        if source == target:
            return True
        else:
            return False

    if source == target:
        distance = 0
    elif len(source) == 0 or len(target) == 0:
        distance = float('inf')
    else:
        distance = float(edit_distance(source, target)) / len(source)

    if constraint["log"] == "detail":
        constraint["logger"].info("{0}".format(distance))

    if distance < constraint["threshold"]:
        return True
    return False
