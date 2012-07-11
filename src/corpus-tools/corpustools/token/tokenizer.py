# -*- encoding: utf-8 -*-
# pylint: disable=C0301,C0111

import errno
import sys
from corpustools.langcode import LangCode

# We handle the config parsing in this file and dispatch the tokenize
# request to other modules which implement the tokenziation or as a adapter
# to external tokenizer/segmenter tool.
def tokenize(clean, tools, step, lang):
    xxlang = LangCode(lang).xx_XX()
    module_name = "corpustools.token." + step["tool"][xxlang]["name"]
    try:
        __import__(module_name)
        module = sys.modules[module_name]
        module.tokenize(clean, tools, step, lang)
    except ImportError as e:
        print e
        sys.exit(errno.EPERM)


def run(clean, tools, step):
    tokenize(clean, tools, step, clean.source_lang)
    tokenize(clean, tools, step, clean.target_lang)
