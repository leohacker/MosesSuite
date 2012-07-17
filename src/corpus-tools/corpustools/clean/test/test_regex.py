# −*− coding: utf−8 −*−

from corpustools.clean import regex

class TestRegex():
    def test_re_del001(self):
        source_corpus = u"English string"
        target_corpus = u'Foreign string'
        match_re = u'English'
        apply_to = u'source'
        source, target = regex.re_del(source_corpus, target_corpus, match_re, apply_to)
        assert source == u''
        assert target == u'Foreign string'

    def test_re_del002(self):
        source_corpus = u"English string"
        target_corpus = u'Foreign string'
        match_re = u'string'
        apply_to = u'target'
        source, target = regex.re_del(source_corpus, target_corpus, match_re, apply_to)
        print target
        assert source == u'English string'
        assert target == u''

    def test_re_repl001(self):
        source_corpus = u"English string"
        target_corpus = u'Foreign string'
        match_re = u'English'
        repl_re = u'Foreign'
        apply_to = u'source'
        source, target = regex.re_repl(source_corpus, target_corpus, match_re, repl_re, apply_to)
        assert source == target_corpus

    def test_re_repl002(self):
        source_corpus = u"English string"
        target_corpus = u'Foreign string'
        match_re = u'string'
        repl_re = u'str'
        apply_to = u'both'
        source, target = regex.re_repl(source_corpus, target_corpus, match_re, repl_re, apply_to)
        assert source == u'English str'
        assert target == u'Foreign str'

    def test_re_repl003(self):
        source_corpus = u"English string"
        target_corpus = u'Foreign string'
        match_re = u'English'
        repl_re = u''
        apply_to = u'source'
        source, target = regex.re_repl(source_corpus, target_corpus, match_re, repl_re, apply_to)
        assert source == u' string'

    def test_re_repl004(self):
        source_corpus = u"{ 2 }"
        target_corpus = u"{ 1.2 }"
        match_re = u"{ (\\d+) }"
        repl_re = u"{\\1}"
        apply_to = u"both"
        source, target = regex.re_repl(source_corpus, target_corpus, match_re, repl_re, apply_to)
        assert source == u'{2}'
        assert target == u'{ 1.2 }'
