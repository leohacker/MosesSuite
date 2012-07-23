# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301

"""predicate clean module."""

def predicate(source, target, constraint):
    """Return False if the distance between source and target is beyond the limit."""
    len_s = len(source.split(' '))
    len_t = len(target.split(' '))
    if abs(len_s - len_t) > constraint["diff"]:
        return False
    else:
        return True
