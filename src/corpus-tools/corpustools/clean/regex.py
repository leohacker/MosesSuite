# -*- coding: utf-8 -*-

import codecs
import re


def run(clean, tools, step):
    ext = step["ext"]
    relist = step["list"]

    source_fp = codecs.open(clean.corpus_w(clean.source_lang), 'r', 'utf-8')
    target_fp = codecs.open(clean.corpus_w(clean.target_lang), 'r', 'utf-8')
    source_ext_fp = codecs.open(clean.corpus_w(clean.source_lang, ext), 'w', 'utf-8')
    target_ext_fp = codecs.open(clean.corpus_w(clean.target_lang, ext), 'w', 'utf-8')

    for source_line, target_line in zip(source_fp, target_fp):
        source_line, target_line = relist_clean(source_line, target_line, relist)
        if len(source_line) != 0 and len(target_line) != 0:
            source_ext_fp.write(source_line)
            target_ext_fp.write(target_line)

    source_fp.close()
    target_fp.close()
    source_ext_fp.close()
    target_ext_fp.close()


def relist_clean(source, target, relist):
    for re_step in relist:
        source = source.strip()
        target = target.strip()
        if len(source) == 0 or len(target) == 0:
            return source, target

        action = re_step["action"]
        apply_to = re_step["apply_to"]

        if action == "delete_line":
            match_re = re_step["match"]
            source, target = re_del(source, target, match_re, apply_to)
            continue

        if action == "replace":
            match_re = re_step["match"]
            repl_re = re_step["replace"]
        elif action == "delete":
            match_re = re_step["match"]
            repl_re = ur''
        source, target = re_repl(source, target, match_re, repl_re, apply_to)

    return source.strip(), target.strip()


def re_del(source, target, match_re, apply_to):
    if apply_to == "source" or apply_to == "both":
        if re.match(match_re, source):
            source = u''
    if apply_to == "target" or apply_to == "both":
        if re.match(match_re, target):
            target = u''
    return source, target


def re_repl(source, target, match_re, repl_re, apply_to):
    if apply_to == "source" or apply_to == "both":
        source = re.sub(match_re, repl_re, source)
    if apply_to == "target" or apply_to == "both":
        target = re.sub(match_re, repl_re, target)
    return source, target
