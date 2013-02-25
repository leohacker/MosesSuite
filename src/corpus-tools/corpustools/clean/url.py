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

"""
URL Clean Module

Clean the URL-like text as I can.
"""

import codecs
import re
import os

def validate(step):
    return True

def run(clean_config, corpustools_config, step):    # pylint: disable=I0011,W0613
    """entry function."""
    urlclean = URLClean(clean_config, step)
    urlclean.run()


class URLClean(object):
    """Class of cleaning the url-like text from corpus.

    """

    PROTOCAL = ['http', 'https', 'ftp', 'ldap']

    GENERAL_ROOT = ['com', 'org', 'net', 'edu', 'gov', 'info', 'int', 'tv' ]
    COUNTRY_ROOT = ['uk', 'eu',
                    'au', 'br', 'ca', 'cn', 'ch', 'cz',
                    'de', 'dk', 'es', 'fi', 'fr', 'gr',
                    'hk', 'hu', 'ie', 'il', 'in', 'it',
                    'jp', 'kr', 'nl', 'no', 'pl', 'pt',
                    'ro', 'ru', 'se', 'sg', 'tr', 'tw',
                    'ua', 'us']

    def __init__(self, clean, step):
        """init function."""
        self.ext = step["ext"]
        self.country = step["country"] if "country" in step else None
        self.clean = clean
        self.logger = step["logger"]
        self.log = step["log"] if "log" in step else None
        self.repl = step["repl"]

        self.pattern = None


    def run(self):
        """run URL clean process."""
        clean = self.clean
        self.prepare_pattern()

        filename = os.path.join(self.clean.working_dir, self.clean.corpus_filename())
        filename_ext = os.path.join(self.clean.working_dir, self.clean.corpus_filename(self.ext))

        infp = codecs.open(filename, 'r', 'UTF-8')
        outfp = codecs.open(filename_ext, 'w', 'UTF-8')

        lineno = 0
        for line in infp:
            lineno = lineno + 1
            [source, target] = line.split(u'\t')
            source = self.urlclean_line(source, lineno)
            target = self.urlclean_line(target, lineno)
            outfp.write(u'\t'.join([source.strip(), target.strip()]) + os.linesep )

        infp.close()
        outfp.close()

    def prepare_pattern(self):
        # prepare the re pattern.
        proto_list = "|".join(self.PROTOCAL)
        groot_list = "|".join(self.GENERAL_ROOT)
        if self.country is not None:
            self.COUNTRY_ROOT.extend(self.country)
        croot_list = "|".join(self.COUNTRY_ROOT)

        proto = ur'((?#Protocal)({proto})://)'.format(proto=proto_list)
        user = ur'(?:\\w+:\\w+@)?'
        address = ur'(([\d]{1,3}\.){3}[\d]{1,3})'
        # qualified domain.
        qdomain = ur'((?#Subdomains)([-\w]+\.)+(?#Rootdomain)({groot}|{croot}))'.format(groot=groot_list,
                                                                                        croot=croot_list)
        # qualified domain and local host domain.
        domain = ur'({proto}?({qdomain}|{ipaddress})|{proto}[-\w]+)'.format(proto=proto,
                                                                        qdomain=qdomain,
                                                                        ipaddress=address)
        port = ur'(?#Port)(:[\d]{2,5})?'
        # RFC 3986
        # I remove the () [] from valid character set. I hate these chars in URL.
        path = ur"(?#Path)(/([-\w.~:/?#\@!$&*+,;=%]*))?"
        suffix = ur"""(?=([{}<>'"()\[\]|]|[.,;?!](?=(\s|$|[{}<>'"()\[\]|]))|(?<![.,;?!])(\s|$)))"""

        url_pattern = ''.join([domain, user, port, path, suffix])
        self.pattern = re.compile(url_pattern)


    def urlclean_line(self, line, lineno):     # pylint: disable=I0011,R0914

        if self.log is not None and self.pattern.search(line):
            if self.log == u'detail':
                for match in self.pattern.finditer(line):
                    self.logger.info(
                        "Line {ln}: {match}".format(ln=lineno,
                                                    match=match.group(0).encode('utf-8'))
                    )
            elif self.log == u'lineno':
                self.logger.info("Line {ln}".format(ln=lineno))

        return self.pattern.sub(self.repl, line)
