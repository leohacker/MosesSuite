# -*- coding: utf-8 -*-

import codecs
import re


def run(clean, tools, step):
    ext = step["ext"]
    relist = step["list"]

    compile_relist(relist)

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


def compile_relist(relist):
    for item in relist:
        pattern = item["pattern"]
        flag = 0
        if 'unicode' in item and item["unicode"] == True:
            flag = flag | re.UNICODE
        if 'case_insensitive' in item and item["case_insensitive"] == True:
            flag = flag | re.IGNORECASE
        item["pattern"] = re.compile(pattern, flag)

def relist_clean(source, target, relist):
    for re_step in relist:
        source = source.strip()
        target = target.strip()
        if len(source) == 0 or len(target) == 0:
            return source, target

        if u'apply_to' in re_step:
            if re_step["apply_to"] == u"source":
                source = re_clean(source, re_step)
            elif re_step["apply_to"] == u"target":
                target = re_clean(target, re_step)
        else:
            source = re_clean(source, re_step)
            target = re_clean(target, re_step)
    return source.strip(), target.strip()

def re_clean(sentence, step):
    pattern = step["pattern"]
    if step["action"] == "delete_line":
        return re_del(sentence, pattern)
    else:
        if step["action"] == "replace":
            repl = step["repl"]
        elif step["action"] == "delete":
            repl = u''
        return re_repl(sentence, pattern, repl)


def re_del(sentence, pattern):
    return u'' if pattern.search(sentence) else sentence

def re_repl(sentence, pattern, repl):
    return pattern.sub(repl, sentence)
