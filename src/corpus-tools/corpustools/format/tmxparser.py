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

# Author: Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0103,R0902,E0202

"""TMX Parser Module"""

import codecs
import os.path
from xml.parsers.expat import ParserCreate
from xml.parsers.expat import ExpatError

from corpustools.lib.languagecode import LanguageCode

class TMXParser(object):
    """TMXParser read TMX file and extract the specified languages sentence align.

    This tmx parser use xml.parsers.expat as xml parser engine.
    """
    def __init__(self):
        self.source_lang = None
        self.target_lang = None
        self.source_filepath = None
        self.target_filepath = None
        self.source = []
        self.target = []

        self._output_dir = None
        self.source_fp = None
        self.target_fp = None

        # The flag 'in_seg' indicate whether current event is happened in seg.
        # Because some tags will be embedded in sentence, we have to keep these tags in seg.
        self.in_seg = False
        self.tuv_lang = None
        self.seg = None

        self.parser = ParserCreate()
        self.parser.buffer_text = True
        self.parser.buffer_size = 4096
        self.parser.returns_unicode = True

        self.parser.StartElementHandler = self.start_element_handler
        self.parser.EndElementHandler = self.end_element_handler
        self.parser.CharacterDataHandler = self.char_data_handler

    @property
    def output_dir(self):
        return self._output_dir


    @output_dir.setter
    def output_dir(self, path):
        if os.path.isdir(path):
            self._output_dir = path


    def parse_file(self, filename, source_lang, target_lang):
        """Expat parser callback function."""
        # open the txm file, needn't to specify the encoding.
        try:
            fp = open(filename, 'r')
        except IOError as e:
            print  e
            return e.errno

        if self.output_dir is None:
            self.output_dir = os.path.dirname(filename)
        stem = os.path.splitext(os.path.basename(filename))[0]

        self.source_lang = LanguageCode(source_lang).TMX_form()
        self.target_lang = LanguageCode(target_lang).TMX_form()
        self.source_filepath = os.path.join(self.output_dir, stem + '.' + LanguageCode(source_lang).xx())
        self.target_filepath = os.path.join(self.output_dir, stem + '.' + LanguageCode(target_lang).xx())
        try:
            self.source_fp = codecs.open(self.source_filepath, 'w', 'utf-8')
            self.target_fp = codecs.open(self.target_filepath, 'w', 'utf-8')
        except IOError as e:
            print  e
            return e.errno

        # whether success or fail, close the files and quit.
        try:
            self.parser.ParseFile(fp)
        except ExpatError as e:
            print "[Error] {0}:".format(os.path.basename(filename)), e
            return e.code
        finally:
            fp.close()
            self.source_fp.close()
            self.target_fp.close()

        return 0


    def start_element_handler(self, name, attributes):
        """Expat parser callback function."""
        if (self.in_seg):
            attrlist = [ attrname + "=" + '"'+ attributes[attrname] +'"' for attrname in attributes.keys()]
            attrstr = " ".join(attrlist)
            tagheader = "<" + name + " " + attrstr + ">"
            self.seg += tagheader
        if (name == u"tu"):
            self.source = []
            self.target = []
        if (name == u"tuv"):
            self.tuv_lang = attributes["xml:lang"]
        if (name == u"seg"):
            self.seg = u""
            self.in_seg = True


    def end_element_handler(self, name):
        """Expat parser callback function."""
        if (name == u"tu"):
            source = u' '.join(self.source).strip()
            target = u' '.join(self.target).strip()
            if len(source) > 0 and len(target) > 0:
                self.source_fp.write(source + os.linesep)
                self.target_fp.write(target + os.linesep)
        if (name == u"tuv"):
            self.tuv_lang = None
        if (name == u"seg"):
            self.in_seg = False
            if self.tuv_lang == self.source_lang:
                self.source.extend(self.seg.splitlines())
            if self.tuv_lang == self.target_lang:
                self.target.extend(self.seg.splitlines())
            self.seg = u""
        if (self.in_seg):
            tagtail = "</" + name + ">"
            self.seg += tagtail


    def char_data_handler(self, data):
        """Expat parser callback function."""
        if self.in_seg:
            self.seg += data
