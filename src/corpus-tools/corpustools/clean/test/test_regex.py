# −*− coding: utf−8 −*−
import re
from corpustools.clean import regex

def test_re_clean_repl_unicode_true():
    step = {"action": u"replace",
            "pattern": u"(\\bKorean\\b)",
            "repl": u" \\1 ",
            "unicode": True
            }
    source = u"韩国Korean代表团"
    step["pattern"] = re.compile(step["pattern"], re.UNICODE)
    source = regex.re_clean(source, step)
    assert source == u"韩国Korean代表团"

def test_re_clean_repl_unicode_false():
    step = {"action": u"replace",
            "pattern": u"(\\bKorean\\b)",
            "repl": u" \\1 ",
            "unicode": False
            }
    source = u"韩国Korean代表团"
    step["pattern"] = re.compile(step["pattern"])
    source = regex.re_clean(source, step)
    assert source == u"韩国 Korean 代表团"


def test_re_clean_repl_case_insensitive():
    step = {"action": u"replace",
            "pattern": u"(\\bKOREAN\\b)",
            "repl": u" \\1 ",
            "case_sensitive": False
            }
    source = u"韩国Korean代表团"
    step["pattern"] = re.compile(step["pattern"], re.IGNORECASE)
    source = regex.re_clean(source, step)
    assert source == u"韩国 Korean 代表团"

def test_re_del_line():
    # delete the match sentence in source corpus.
    source = u"English string"
    target = u''
    pattern = u'English'
    pattern = re.compile(pattern)
    source = regex.re_del(source, pattern)
    assert source == target


def test_re_repl():
    # replace the match string in source corpus.
    source = u"English string"
    target = u'Foreign string'
    pattern = u'English'
    repl = u'Foreign'
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == target


def test_re_del():
    # delete the match string.
    source = u"English string"
    target = u' string'
    pattern = u'English'
    repl = u''
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == target


def test_re_repl_backslash():
    # the backslash char in regex.
    source01 = u"{ 2 }"
    source02 = u"{ 1.2 }"
    pattern = u"{ (\\d+) }"
    repl = u'{\\1}'
    pattern = re.compile(pattern)
    source01 = regex.re_repl(source01, pattern, repl)
    source02 = regex.re_repl(source02, pattern, repl)
    assert source01 == u'{2}'
    assert source02 == u'{ 1.2 }'


def test_re_phtag():
    # clean phtag.
    source = ur'<ph x="1">{1}</ph>[domain]<ph x="2">{2}</ph>/<ph x="3">{3}</ph>'
    target = ur'<ph x="1">{1}</ph>[域]<ph x="2">{2}</ph>/<ph x="3">{3}</ph>'
    #pattern = ur'<ph(?:\s+[\w=\"]*)*>(\{\d+\})<\/ph>'
    pattern = u"<ph.*?>({\d+})</ph>"
    repl = ur' \1 '
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    target = regex.re_repl(target, pattern, repl)
    assert source == u" {1} [domain] {2} / {3} "
    assert target == u" {1} [域] {2} / {3} "

def test_re_detoken01():
    source = u"(  )"
    target = u"()"
    pattern = ur"\(\s+\)"
    repl = ur'()'
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == target


def test_re_integer_float():
    # clean integer and float.
    source01 = u"465 -12+23.4 -.23e-10 +19E+2"
    source02 = u"1st"
    pattern = ur"[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
    repl = u''
    pattern = re.compile(pattern)
    source01 = regex.re_repl(source01, pattern, repl)
    source02 = regex.re_repl(source02, pattern, repl)
    assert source01.strip() == u''
    assert source02.strip() == u'st'

def test_re_hex_oct():
    # clean hex and oct.
    source = u"+0x10FFF -0674"
    pattern = ur'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)'
    repl = u''
    pattern = re.compile(pattern)
    source01 = regex.re_repl(source, pattern, repl)
    assert source01.strip() == u''

def test_re_expression():
    # clean expression.
    # TODO: figure out a better re.
    source = u"5786*0674 46 + 57"
    pattern = ur'[\d+\-*/]+'
    repl = u''
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source.strip() == u''

def test_re_date():
    pass

def test_re_us_currency():
    source = u'¥ 3,186,515.39 CNY $ 500,000 USD'
    pattern = ur'\b(\d{1,3})(\,\d{3})*(\.\d+)?\b'
    repl = u''
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == u'¥  CNY $  USD'


def test_re_vertical_line():
    source = u'table | column'
    target = u'table vl column'
    pattern = ur'\|'
    repl = u'vl'
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == target

def test_re_url():
    source = u'goto http://www.sina.com.cn'
    target = u'goto '
    pattern = ur'((?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~\/|\/)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:\/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?)(?=($|<|{))'
    repl = u''
    pattern = re.compile(pattern)
    source = regex.re_repl(source, pattern, repl)
    assert source == target
