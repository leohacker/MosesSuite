# -*- coding: utf-8 -*-

# pylint: disable=C0301,C0111

"""
Lang Code Module.

Normalize the language code, and convert them from one form to another.
"""

import locale


class LangCode(object):
    def __init__(self, langcode):
        """LangCode Constructor.
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
        return self._langcode.lower().split('_')[0] if self._langcode is not None else None

    def xx_XX(self):
        return '_'.join([self._langcode.lower().split('_')[0],
                         self._langcode.upper().split('_')[1]]) if self._langcode is not None else None

    def _XX_dash_XX(self):
        return '-'.join(self._langcode.upper().split('_')) if self._langcode is not None else None

    def TMX_form(self):
        return self._XX_dash_XX()
