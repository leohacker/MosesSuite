# -*- coding: utf-8 -*-

# pylint: disable=C0301,C0103,C0111
# pylint: disable-msg=R0902
# pylint: disable-msg=W0201

"""Config module for corpus tools.

This module define the class CorpusToolsConfig to access the configuration of
corpus tools. The instance will read the system-wide and user configuration
automatically, then you specify a configuration file to read.
"""

import os.path
import ConfigParser


class CorpusToolsConfig(object):
    """Class for reading corpus tools config.

    /etc/corpustools.conf   system wide configuration.
    ~/.corpustools.conf     user configuration.
    -c config               specify the config file in command line.
    """
    SYSTEM_CONFIG = "/etc/corpustools.conf"
    USER_CONFIG = "~/.corpustools.conf"

    def __init__(self):
        """Read the system wide and default user configuration."""
        self.config = ConfigParser.SafeConfigParser()
        configfiles = [CorpusToolsConfig.SYSTEM_CONFIG,
                       os.path.expanduser(CorpusToolsConfig.USER_CONFIG)]

        for configfile in configfiles:
            self.readfile(configfile)

    def readfile(self, filename):
        """Read the configuration from file."""
        # Needn't to catch the IOError when read config because ConfigParser will ignore the file if failed to open/access it.
        # BUT should catch the exception of parser to avoid unexpected termination.
        # e.g. system-wide config is broken, but I can't correct it because of permission.
        try:
            self.config.read(filename)
        except ConfigParser.Error as e:
            print e

    def sections(self):
        return self.config.sections()

    def options(self, section):
        if self.config.has_section(section):
            return self.config.options(section)
        else:
            return None

    def __getitem__(self, keyseq):
        if len(keyseq.split('.')) != 2:
            return None
        section, option = keyseq.split('.')
        return self.config.get(section, option) if self.config.has_option(section, option) else None

    def dump(self):
        for section in self.config.sections():
            print "[" + section + "]"
            for name, value in self.config.items(section):
                print name + " = " + value
            print ""
