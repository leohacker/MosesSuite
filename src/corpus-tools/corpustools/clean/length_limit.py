# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301

"""predicate clean module."""

def predicate(source, target, constraint):
    """
    Return False if the length of source and/or target is beyond the limit.

    The available limit is 100 tokens for GIZA++ in moses system.
    """

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
