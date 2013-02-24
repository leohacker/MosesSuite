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
Predicate Module: Length Limit
"""

def validate(step):
    return True

def predicate(source, target, constraint):
    """
    Return True if the length of source and/or target is beyond the limit.

    The length limit for GIZA++ in moses is 100 tokens.

    """

    if "source" in constraint:
        len_s = len(source.split(' '))
        (low, high) = tuple(constraint["source"])
        if len_s < low or len_s > high:
            return True

    if "target" in constraint:
        len_t = len(target.split(' '))
        (low, high) = tuple(constraint["target"])
        if len_t < low or len_t > high:
            return True

    return False
