# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License
#
# Copyright (c) 2012, 2013, Leo Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
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

# pylint: disable=I0011,C0301,C0103,W0105

"""External Corpus Tools Config Module

This module define the class CorpusToolsConfig to access the configuration of external corpus tools.
The instance will read the system-wide and user configuration automatically, and you can specify
a configuration file to load.

"""

import os.path
import ConfigParser


class CorpusToolsConfig(object):
    """Configuration to store external tools info.

    The instance can be initialized by reading three configuration files:
    system-wide, user default and optional specified file.
    Can initialize with specified file as parameter, or read the file after initialization.

    Configuration file foramt: ini (key=value) style.

    """

    SYSTEM_CONFIG = "/etc/corpustools.conf"
    """System wide configuration."""

    USER_CONFIG = "~/.corpustools.conf"
    """User default configuration."""

    def __init__(self, filename=None):
        """Initialize external tools configuration instance.

        Read the system wide, default user configuration and user specified configuration
        if parameter filename given.

        """
        self.config = ConfigParser.SafeConfigParser()
        configfiles = [CorpusToolsConfig.SYSTEM_CONFIG,
                       os.path.expanduser(CorpusToolsConfig.USER_CONFIG)]

        if filename is not None:
            configfiles.append(os.path.abspath(os.path.expanduser(filename)))

        for configfile in configfiles:
            self.readfile(configfile)

    def readfile(self, filename):
        """Read the configuration from file."""
        # If failed to open config file, the parser will ignore that file, so I don't catch the IOError.
        # But we still need to catch the ConfigParser.Error in case any config file is broken.
        try:
            self.config.read(filename)
        except ConfigParser.Error as e:
            print e

    def sections(self):
        """Return section list of configuration."""
        return self.config.sections()

    def options(self, section):
        """Return a list of options in specified section, or None if section not found."""
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
        """A convenient function for introspecting config instance in development."""
        for section in self.config.sections():
            print "[" + section + "]"
            for name, value in self.config.items(section):
                print name + " = " + value
            print ""
