#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, Leo Jiang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author:   Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301

"""ZString Sequence Clean Module

Support conversion for Adobe's ZString escape sequence.
"""

ESCAPESEQ_TABLE = {     # zstring1.5
    # ur"\\" : u"\u005C",     # REVERSE SOLIDUS
    # ur"\"" : u"\u0022",     # QUOTATION MARK  APL quote
    # ur"\n" : u"\u000A",     # LINE FEED
    # ur"\r" : u"\u000D",     # CARRIAGE RETURN
    # ur"\t" : u"\u0009",     # HORIZONTAL TABULATION
    # ur"\b" : u"\u0008",     # BACK SPACE
    # ur"\v" : u" ",
    # ur"\f" : u" ",

    # ur"^^" : u"\u005E",     # ^ CIRCUMFLEX ACCENT
    ur"^Q" : u"\u0022",     # " QUOTATION MARK  APL quote
    # ur"^[" : u"\u201C",     # “ LEFT DOUBLE QUOTATION MARK  DOUBLE TURNED COMMA QUOTATION MARK
    # ur"^]" : u"\u201D",     # ” RIGHT DOUBLE QUOTATION MARK DOUBLE COMMA QUOTATOIN MARK
    # ur"^{" : u"\u2018",     # ‘ LEFT SINGLE QUOTATION MARK  SINGLE TURNED COMMA QUOTATION MARK
    # ur"^}" : u"\u2019",     # ’ RIGHT SINGLE QUOTATION MARK SINGLE COMMA QUOTATION MARK
    # ur"^C" : u"\u00A9",     # © COPYRIGHT SIGN
    # ur"^R" : u"\u00AE",     # ® REGISTERED SIGN REGISTERED TRADE MARK SIGN
    # ur"^T" : u"\u2122",     # ™ TRADEMARK SIGN
    # ur"^D" : u"\u00B0",     # ° DEGREE SIGN
    # ur"^B" : u"\u2022",     # • BULLET  black small circle
    # ur"^#" : u"\u2318",     # ⌘ PLACE OF INTEREST SIGN  COMMAND KEY
    # ur"^!" : u"\u00AC",     # ¬ NOT SIGN
    # ur"^|" : u"\u2206",     # ∆ INCREMENT   Laplace operator forward difference
    # ur"^S" : u"\u2211",     # ∑ N-ARY SUMMATION summation sign

    ur"#{endl}"     : u"\u000A", # \n
    ur"#{tab}"      : u"\u0009", # \t  horizontal tabulation
    ur"#{cr}"       : u"\u000D", # \r  carriage return
    ur"#{lf}"       : u"\u000A", # \n  line feed
    ur"#{quot}"     : u"\u0022", # "   U+0022  quotation mark = APL quote
    ur"#{amp}"      : u"\u0026", # &   U+0026  ampersand
    ur"#{lt}"       : u"\u003C", # <   U+003C  less-than sign
    ur"#{gt}"       : u"\u003E", # >   U+003E  greater-than sign
    ur"#{equal}"    : u"=",

    ur"#{nbsp}"     : u"\u00A0", #     U+00A0  no-break space = non-breaking space
    ur"#{iexcl}"    : u"\u00A1", # ¡   U+00A1  inverted exclamation mark
    ur"#{cent}"     : u"\u00A2", # ¢   U+00A2  cent sign
    ur"#{pound}"    : u"\u00A3", # £   U+00A3  pound sign
    ur"#{curren}"   : u"\u00A4", # ¤   U+00A4  currency sign
    ur"#{yen}"      : u"\u00A5", # ¥   U+00A5  yen sign = yuan sign
    ur"#{brvbar}"   : u"\u00A6", # ¦   U+00A6  broken bar = broken vertical bar
    ur"#{sect}"     : u"\u00A7", # §   U+00A7  section sign
    ur"#{uml}"      : u"\u00A8", # ¨   U+00A8  diaeresis = spacing diaeresis
    ur"#{copy}"     : u"\u00A9", # ©   U+00A9  copyright sign
    ur"#{ordf}"     : u"\u00AA", # ª   U+00AA  feminine ordinal indicator
    ur"#{laquo}"    : u"\u00AB", # «   U+00AB  left-pointing double angle quotation mark
    ur"#{not}"      : u"\u00AC", # ¬   U+00AC  not sign
    ur"#{shy}"      : u"\u00AD", #  ­   U+00AD  soft hyphen = discretionary hyphen
    ur"#{reg}"      : u"\u00AE", # ®   U+00AE  registered sign = registered trade mark sign
    ur"#{macr}"     : u"\u00AF", # ¯   U+00AF  macron = spacing macron = overline
    ur"#{deg}"      : u"\u00B0", # °   U+00B0  degree sign
    ur"#{plusmn}"   : u"\u00B1", # ±   U+00B1  plus-minus sign = plus-or-minus sign
    ur"#{sup2}"     : u"\u00B2", # ²   U+00B2  superscript two = superscript digit two
    ur"#{sup3}"     : u"\u00B3", # ³   U+00B3  superscript three = superscript digit three
    ur"#{acute}"    : u"\u00B4", # ´   U+00B4  acute accent = spacing acute
    ur"#{micro}"    : u"\u00B5", # µ   U+00B5  micro sign
    ur"#{para}"     : u"\u00B6", # ¶   U+00B6  pilcrow sign = paragraph sign
    ur"#{middot}"   : u"\u00B7", # ·   U+00B7  middle dot = Georgian comma
    ur"#{cedil}"    : u"\u00B8", # ¸   U+00B8  cedilla = spacing cedilla
    ur"#{sup1}"     : u"\u00B9", # ¹   U+00B9  superscript one = superscript digit one
    ur"#{ordm}"     : u"\u00BA", # º   U+00BA  masculine ordinal indicator
    ur"#{raquo}"    : u"\u00BB", # »   U+00BB  right-pointing double angle quotation mark
    ur"#{frac14}"   : u"\u00BC", # ¼   U+00BC  vulgar fraction one quarter
    ur"#{frac12}"   : u"\u00BD", # ½   U+00BD  vulgar fraction one half
    ur"#{frac34}"   : u"\u00BE", # ¾   U+00BE  vulgar fraction three quarters
    ur"#{iquest}"   : u"\u00BF", # ¿   U+00BF  inverted question mark
    ur"#{Agrave}"   : u"\u00C0", # À   U+00C0  latin capital letter A with grave = latin capital letter A grave
    ur"#{Aacute}"   : u"\u00C1", # Á   U+00C1  latin capital letter A with acute
    ur"#{Acirc}"    : u"\u00C2", # Â   U+00C2  latin capital letter A with circumflex
    ur"#{Atilde}"   : u"\u00C3", # Ã   U+00C3  latin capital letter A with tilde
    ur"#{Auml}"     : u"\u00C4", # Ä   U+00C4  latin capital letter A with diaeresis
    ur"#{Aring}"    : u"\u00C5", # Å   U+00C5  latin capital letter A with ring above = latin capital letter A ring
    ur"#{AElig}"    : u"\u00C6", # Æ   U+00C6  latin capital letter AE = latin capital ligature AE
    ur"#{Ccedil}"   : u"\u00C7", # Ç   U+00C7  latin capital letter C with cedilla
    ur"#{Egrave}"   : u"\u00C8", # È   U+00C8  latin capital letter E with grave
    ur"#{Eacute}"   : u"\u00C9", # É   U+00C9  latin capital letter E with acute
    ur"#{Ecirc}"    : u"\u00CA", # Ê   U+00CA  latin capital letter E with circumflex
    ur"#{Euml}"     : u"\u00CB", # Ë   U+00CB  latin capital letter E with diaeresis
    ur"#{Igrave}"   : u"\u00CC", # Ì   U+00CC  latin capital letter I with grave
    ur"#{Iacute}"   : u"\u00CD", # Í   U+00CD  latin capital letter I with acute
    ur"#{Icirc}"    : u"\u00CE", # Î   U+00CE  latin capital letter I with circumflex
    ur"#{Iuml}"     : u"\u00CF", # Ï   U+00CF  latin capital letter I with diaeresis
    ur"#{ETH}"      : u"\u00D0", # Ð   U+00D0  latin capital letter ETH
    ur"#{Ntilde}"   : u"\u00D1", # Ñ   U+00D1  latin capital letter N with tilde
    ur"#{Ograve}"   : u"\u00D2", # Ò   U+00D2  latin capital letter O with grave
    ur"#{Oacute}"   : u"\u00D3", # Ó   U+00D3  latin capital letter O with acute
    ur"#{Ocirc}"    : u"\u00D4", # Ô   U+00D4  latin capital letter O with circumflex
    ur"#{Otilde}"   : u"\u00D5", # Õ   U+00D5  latin capital letter O with tilde
    ur"#{Ouml}"     : u"\u00D6", # Ö   U+00D6  latin capital letter O with diaeresis
    ur"#{times}"    : u"\u00D7", # ×   U+00D7  multiplication sign
    ur"#{Oslash}"   : u"\u00D8", # Ø   U+00D8  latin capital letter O with stroke = latin capital letter O slash
    ur"#{Ugrave}"   : u"\u00D9", # Ù   U+00D9  latin capital letter U with grave
    ur"#{Uacute}"   : u"\u00DA", # Ú   U+00DA  latin capital letter U with acute
    ur"#{Ucirc}"    : u"\u00DB", # Û   U+00DB  latin capital letter U with circumflex
    ur"#{Uuml}"     : u"\u00DC", # Ü   U+00DC  latin capital letter U with diaeresis
    ur"#{Yacute}"   : u"\u00DD", # Ý   U+00DD  latin capital letter Y with acute
    ur"#{THORN}"    : u"\u00DE", # Þ   U+00DE  latin capital letter THORN
    ur"#{szlig}"    : u"\u00DF", # ß   U+00DF  latin small letter sharp s = ess-zed
    ur"#{agrave}"   : u"\u00E0", # à   U+00E0  latin small letter a with grave = latin small letter a grave
    ur"#{aacute}"   : u"\u00E1", # á   U+00E1  latin small letter a with acute
    ur"#{acirc}"    : u"\u00E2", # â   U+00E2  latin small letter a with circumflex
    ur"#{atilde}"   : u"\u00E3", # ã   U+00E3  latin small letter a with tilde
    ur"#{auml}"     : u"\u00E4", # ä   U+00E4  latin small letter a with diaeresis
    ur"#{aring}"    : u"\u00E5", # å   U+00E5  latin small letter a with ring above = latin small letter a ring
    ur"#{aelig}"    : u"\u00E6", # æ   U+00E6  latin small letter ae = latin small ligature ae
    ur"#{ccedil}"   : u"\u00E7", # ç   U+00E7  latin small letter c with cedilla
    ur"#{egrave}"   : u"\u00E8", # è   U+00E8  latin small letter e with grave
    ur"#{eacute}"   : u"\u00E9", # é   U+00E9  latin small letter e with acute
    ur"#{ecirc}"    : u"\u00EA", # ê   U+00EA  latin small letter e with circumflex
    ur"#{euml}"     : u"\u00EB", # ë   U+00EB  latin small letter e with diaeresis
    ur"#{igrave}"   : u"\u00EC", # ì   U+00EC  latin small letter i with grave
    ur"#{iacute}"   : u"\u00ED", # í   U+00ED  latin small letter i with acute
    ur"#{icirc}"    : u"\u00EE", # î   U+00EE  latin small letter i with circumflex
    ur"#{iuml}"     : u"\u00EF", # ï   U+00EF  latin small letter i with diaeresis
    ur"#{eth}"      : u"\u00F0", # ð   U+00F0  latin small letter eth
    ur"#{ntilde}"   : u"\u00F1", # ñ   U+00F1  latin small letter n with tilde
    ur"#{ograve}"   : u"\u00F2", # ò   U+00F2  latin small letter o with grave
    ur"#{oacute}"   : u"\u00F3", # ó   U+00F3  latin small letter o with acute
    ur"#{ocirc}"    : u"\u00F4", # ô   U+00F4  latin small letter o with circumflex
    ur"#{otilde}"   : u"\u00F5", # õ   U+00F5  latin small letter o with tilde
    ur"#{ouml}"     : u"\u00F6", # ö   U+00F6  latin small letter o with diaeresis
    ur"#{divide}"   : u"\u00F7", # ÷   U+00F7  division sign
    ur"#{oslash}"   : u"\u00F8", # ø   U+00F8  latin small letter o with stroke, = latin small letter o slash
    ur"#{ugrave}"   : u"\u00F9", # ù   U+00F9  latin small letter u with grave
    ur"#{uacute}"   : u"\u00FA", # ú   U+00FA  latin small letter u with acute
    ur"#{ucirc}"    : u"\u00FB", # û   U+00FB  latin small letter u with circumflex
    ur"#{uuml}"     : u"\u00FC", # ü   U+00FC  latin small letter u with diaeresis
    ur"#{yacute}"   : u"\u00FD", # ý   U+00FD  latin small letter y with acute
    ur"#{thorn}"    : u"\u00FE", # þ   U+00FE  latin small letter thorn
    ur"#{yuml}"     : u"\u00FF", # ÿ   U+00FF  latin small letter y with diaeresis

    ur"#{OElig}"    : u"\u0152", # Œ   U+0152  latin capital ligature OE
    ur"#{oelig}"    : u"\u0153", # œ   U+0153  latin small ligature oe
    ur"#{Scaron}"   : u"\u0160", # Š   U+0160  latin capital letter S with caron
    ur"#{scaron}"   : u"\u0161", # š   U+0161  latin small letter s with caron
    ur"#{Yuml}"     : u"\u0178", # Ÿ   U+0178  latin capital letter Y with diaeresis
    ur"#{circ}"     : u"\u02C6", # ˆ   U+02C6  modifier letter circumflex accent
    ur"#{tilde}"    : u"\u02DC", # ˜   U+02DC  small tilde
    ur"#{ensp}"     : u"\u2002", #     U+2002  en space
    ur"#{emsp}"     : u"\u2003", #     U+2003  em space
    ur"#{thinsp}"   : u"\u2009", #     U+2009  thin space
    ur"#{zwnj}"     : u"\u200C", # ‌   U+200C  zero width non-joiner
    ur"#{zwj}"      : u"\u200D", # ‍   U+200D  zero width joiner
    ur"#{lrm}"      : u"\u200E", # ‎   U+200E  left-to-right mark
    ur"#{rlm}"      : u"\u200F", # ‏   U+200F  right-to-left mark
    ur"#{ndash}"    : u"\u2013", # –   U+2013  en dash
    ur"#{mdash}"    : u"\u2014", # —   U+2014  em dash
    ur"#{lsquo}"    : u"\u2018", # ‘   U+2018  left single quotation mark
    ur"#{rsquo}"    : u"\u2019", # ’   U+2019  right single quotation mark
    ur"#{sbquo}"    : u"\u201A", # ‚   U+201A  single low-9 quotation mark
    ur"#{ldquo}"    : u"\u201C", # “   U+201C  left double quotation mark
    ur"#{rdquo}"    : u"\u201D", # ”   U+201D  right double quotation mark
    ur"#{bdquo}"    : u"\u201E", # „   U+201E  double low-9 quotation mark
    ur"#{dagger}"   : u"\u2020", # †   U+2020  dagger
    ur"#{Dagger}"   : u"\u2021", # ‡   U+2021  double dagger
    ur"#{permil}"   : u"\u2030", # ‰   U+2030  per mille sign
    ur"#{lsaquo}"   : u"\u2039", # ‹   U+2039  single left-pointing angle quotation mark
    ur"#{rsaquo}"   : u"\u203A", # ›   U+203A  single right-pointing angle quotation mark
    ur"#{euro}"     : u"\u20AC"  # €   U+20AC  euro sign
}

import codecs
import os
import re
from xml.sax import saxutils

def validate(step):
    return True

def run(clean_config, corpustool_config, step):     # pylint: disable=I0011,W0613
    """entry function."""
    zstring_dict = ESCAPESEQ_TABLE

    filename = os.path.join(clean_config.working_dir, clean_config.corpus_filename())
    filename_ext = os.path.join(clean_config.working_dir, clean_config.corpus_filename(step["ext"]))

    infp = codecs.open(filename, 'r', 'UTF-8')
    outfp = codecs.open(filename_ext, 'w', 'UTF-8')

    for line in infp:
        [source, target] = line.split(u'\t')
        source = zstring_unescape(source, zstring_dict)
        target = zstring_unescape(target, zstring_dict)
        outfp.write(u'\t'.join([source.strip(), target.strip()]) + os.linesep)

    infp.close()
    outfp.close()


def zstring_unescape(line, zdict):
    """unescape the zstring name form and number form of escape sequence."""
    line = u" ".join(saxutils.unescape(line, zdict).splitlines())
    pattern = ur'#\{U\+([0-9a-fA-F]{4})\}'
    line = re.sub(pattern,
                  lambda m: unichr(int(m.group(1), 16)),
                  line)
    return u" ".join(line.splitlines())
