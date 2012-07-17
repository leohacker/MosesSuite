# -*- coding: utf-8 -*-

# pylint: disable=C0301,C0111

def predicate(source, target, constraint):
    if "source" in constraint:
        len_s = len(source.split(' '))
        (low, high) = tuple(constraint["source"])
        if len_s < low or len_s > high:
            return False

    if "target" in constraint:
        len_t = len(target.split(' '))
        (low, high) = tuple(constraint["target"])
        if len_t < low or len_t > high:
            return False

    return True
