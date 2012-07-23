# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301

"""Predicate clean module"""
def predicate(source, target, constraint):
    """
    Return False if the sentences ratio is beyond the threshold.

    The available threshold of moses system is 9.
    """
    len_s = len(source.split(' '))
    len_t = len(target.split(' '))
    ratio = (float(len_s) / len_t) if len_s > len_t else (float(len_t) / len_s)
    if ratio > constraint["ratio"]:
        return False
    else:
        return True
