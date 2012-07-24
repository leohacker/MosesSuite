# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301,C0103

"""
A module to normalize the language code, and convert them between kinds of forms.
"""

import locale


class LangCode(object):
    """Class LangCode for representing the language code in different context.

    The constructor accept three forms of language code as parameter: xx, xx_XX, xx-XX, case insensitive.
    """

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
