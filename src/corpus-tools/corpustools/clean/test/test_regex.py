# −*− coding: utf−8 −*−

from corpustools.clean import regex

def test_re_del001():
    # delete the match sentence in source corpus.
    source_corpus = u"English string"
    target_corpus = u'Foreign string'
    pattern = u'English'
    apply_to = u'source'
    source, target = regex.re_del(source_corpus, target_corpus, pattern, apply_to)
    assert source == u''
    assert target == u'Foreign string'

def test_re_del002():
    # delete the match sentence in target corpus.
    source_corpus = u"English string"
    target_corpus = u'Foreign string'
    pattern = u'string'
    apply_to = u'target'
    source, target = regex.re_del(source_corpus, target_corpus, pattern, apply_to)
    print target
    assert source == u'English string'
    assert target == u''

def test_re_repl001():
    # replace the match string in source corpus.
    source_corpus = u"English string"
    target_corpus = u'Foreign string'
    pattern = u'English'
    repl = u'Foreign'
    apply_to = u'source'
    source, target = regex.re_repl(source_corpus, target_corpus, pattern, repl, apply_to)
    assert source == target_corpus

def test_re_repl002():
    # replace the match string in both corpus.
    source_corpus = u"English string"
    target_corpus = u'Foreign string'
    pattern = u'string'
    repl = u'str'
    apply_to = u'both'
    source, target = regex.re_repl(source_corpus, target_corpus, pattern, repl, apply_to)
    assert source == u'English str'
    assert target == u'Foreign str'

def test_re_repl003():
    # delete the match string.
    source_corpus = u"English string"
    target_corpus = u'Foreign string'
    pattern = u'English'
    repl = u''
    apply_to = u'source'
    source, target = regex.re_repl(source_corpus, target_corpus, pattern, repl, apply_to)
    assert source == u' string'

def test_re_repl004():
    # the backslash char in regex.
    source_corpus = u"{ 2 }"
    target_corpus = u"{ 1.2 }"
    pattern = u"\{ (\\d+) \}"
    repl = u'{\\1}'
    apply_to = u"both"
    source, target = regex.re_repl(source_corpus, target_corpus, pattern, repl, apply_to)
    print source
    print target
    assert source == u'{2}'
    assert target == u'{ 1.2 }'

def test_re_phtag():
    # clean phtag.
    source_corpus = ur'<ph x="1">{1}</ph>[domain]<ph x="2">{2}</ph>/<ph x="3">{3}</ph>'
    target_corpus = ur'<ph x="1">{1}</ph>[域]<ph x="2">{2}</ph>/<ph x="3">{3}</ph>'
    apply_to = u'both'
    #pattern = ur'<ph(?:\s+[\w=\"]*)*>(\{\d+\})<\/ph>'
    pattern = u"<ph.*?>({\d+})</ph>"
    repl = ur' \1 '
    source, target = regex.re_repl(source_corpus, target_corpus, pattern, repl, apply_to)
    print source
    print target
    assert source == u" {1} [domain] {2} / {3} "
    assert target == u" {1} [域] {2} / {3} "

# def test_re_num():
#     # clean integer
#     "^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$"
