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

def run(clean, tools, step):    # pylint: disable=I0011,W0613
    """entry function."""
    urlclean = URLClean(clean, step)
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

    def run(self):
        """run URL clean process."""
        clean = self.clean
        for lang in [clean.source_lang, clean.target_lang]:
            self.urlclean_file(clean.corpus_w(lang), clean.corpus_w(lang, self.ext))


    def urlclean_file(self, infile, outfile):     # pylint: disable=I0011,R0914
        """Clean url-like text in infile and write the output into outfile."""

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
        pattern = re.compile(url_pattern)

        infp = codecs.open(infile, 'r', 'utf-8')
        outfp = codecs.open(outfile, 'w', 'utf-8')

        for line in infp:
            outfp.write(pattern.sub("$URL", line))

        infp.close()
        outfp.close()
