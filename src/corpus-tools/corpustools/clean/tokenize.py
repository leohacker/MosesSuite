# −*− coding: utf−8 −*−

"""Tokenize module in corpus clean tools."""
# pylint: disable=I0011,C0301,C0103

import errno
import shutil
import sys
from corpustools.lib.langcode import LangCode


def tokenize(clean, tools, step, lang):
    """Tokenize the corpus files in corpus clean working directroy.

    Actually, this function works as router to dispatch the request to tokenizers in token subpackage.
    The modules in token subpackage are adapters to external tokenizer tools.

    Args

        :clean:     corpus clean configuration.
        :tools:     external tools configuration.
        :step:      clean step.
        :lang:      specify the language of which corpus be tokenize.
    """
    xxlang = LangCode(lang).xx_XX()
    module_name = "corpustools.token." + step["tool"][xxlang]["name"]
    try:
        __import__(module_name)
        module = sys.modules[module_name]
        module.tokenize(clean.corpus_w(lang), clean.corpus_w(lang, step["ext"]), lang, tools, step)
        shutil.copy(clean.corpus_w(lang, step["ext"]), clean.corpus_w(lang))
    except ImportError as e:
        print e
        sys.exit(errno.EPERM)


def run(clean, tools, step):
    """Clean module interface function, run tokenization for corpus files."""
    tokenize(clean, tools, step, clean.source_lang)
    tokenize(clean, tools, step, clean.target_lang)
