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

# pylint: disable=I0011,C0301,C0103

"""
LanguageCode Module
"""

import locale


class LanguageCode(object):
    """A class for language code.

    Currently constructor accept three forms of language code as parameter: xx, xx_XX,
    xx-XX, case insensitive. And we can get kinds of forms of language code. So we can
    convert the form of language code.

    """

    def __init__(self, langcode):
        """LanguageCode Constructor.

        Accept three forms of language code: xx, xx_XX, xx-XX, case insensitive.

        """
        # Cut the encoding part and support the form of xx-xx.
        langcode = langcode.split('.')[0].replace('-', '_')
        # Only the legal forms can be recongized and changed by encoding suffix.
        if langcode == locale.normalize(langcode):
            self._langcode = None
        else:
            self._langcode = locale.normalize(langcode).split('.')[0]

    def xx(self):
        """return two chars form of language code."""
        return self._langcode.lower().split('_')[0] if self._langcode is not None else None

    def xx_XX(self):
        """return xx_XX form of language code."""
        return '_'.join([self._langcode.lower().split('_')[0],
                         self._langcode.upper().split('_')[1]]) if self._langcode is not None else None

    def _XX_dash_XX(self):
        """return XX-XX form of language code."""
        return '-'.join(self._langcode.upper().split('_')) if self._langcode is not None else None

    def TMX_form(self):
        """return TMX form (xx-XX) of language code."""
        return '-'.join(self.xx_XX().split('_'))
