# -*- encoding: utf-8 -*-

# pylint: disable=C0301,C0111

"""
Filter the sentences according to sentence ratio.
"""
def predicate(source, target, constraint):
    len_s = len(source.split(' '))
    len_t = len(target.split(' '))
    ratio = (float(len_s) / len_t) if len_s > len_t else (float(len_t) / len_s)
    if ratio > constraint["ratio"]:
        return False
    else:
        return True
