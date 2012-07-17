# -*- coding: utf-8 -*-

# pylint: disable=C0301,C0111

"""
Filter the sentences according to distance of length.
"""
def predicate(source, target, constraint):
    len_s = len(source.split(' '))
    len_t = len(target.split(' '))
    if abs(len_s - len_t) > constraint["diff"]:
        return False
    else:
        return True
