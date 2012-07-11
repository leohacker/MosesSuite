# -*- encoding: utf-8 -*-

# pylint: disable=C0301,C0103,C0111
# pylint: disable-msg=R0902
# pylint: disable-msg=W0201

"""Config module for corpus tools.

This module define the class CorpusToolsConfig to access the configuration of
corpus tools. The instance will read the system-wide and user configuration
automatically, then you specify a configuration file to read.

CleanConfig define the configuration of clean steps.
"""

import errno
import json
import os
import sys
from os import path
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
                       path.expanduser(CorpusToolsConfig.USER_CONFIG)]

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

    #
    def __getitem__(self, inquire_str):
        if len(inquire_str.split('.')) != 2:
            return None
        section, option = inquire_str.split('.')
        return self.config.get(section, option) if self.config.has_option(section, option) else None

    def dump(self):
        for section in self.config.sections():
            print "[" + section + "]"
            for name, value in self.config.items(section):
                print name + " = " + value
            print ""


class CleanConfig(object):
    def __init__(self, filename=None):
        self._steps = None
        if filename is not None:
            try:
                fp = open(filename, 'r')
                self._steps = json.load(fp)
            except IOError as e:
                print e
            except ValueError as e:
                print e

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, step_list):
        self._steps = step_list

    # TODO: check more situations.
    def validate_steps(self):
        return False if self._steps is None else True

    @property
    def corpus_name(self):
        """The corpus filename without language extension."""
        return self._corpus_name

    @corpus_name.setter
    def corpus_name(self, value):
        self._corpus_name = value

    @property
    def source_lang(self):
        return self._source_lang

    @source_lang.setter
    def source_lang(self, value):
        self._source_lang = value

    @property
    def target_lang(self):
        return self._target_lang

    @target_lang.setter
    def target_lang(self, value):
        self._target_lang = value

    @property
    def infile_dir(self):
        """The directory to store the corpus files should be cleaned."""
        return self._infile_dir

    @infile_dir.setter
    def infile_dir(self, value):
        self._infile_dir = value

    @property
    def outfile_dir(self):
        """The directory to store the cleaned corpus files."""
        return self._outfile_dir

    @outfile_dir.setter
    def outfile_dir(self, value):
        self._outfile_dir = value

    @property
    def working_dir(self):
        """The working directory for corpus clean tool to store intermediate files."""
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value):
        self._working_dir = value

    @property
    def log(self):
        """The log file for clean steps."""
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    def validate_paths(self):
        """Check the existence of files and directories specified in clean configuration."""
        result = True

        if not path.isdir(self.infile_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.infile_dir + "\n")
            result = False

        if not path.isdir(self.outfile_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.outfile_dir + "\n")
            result = False

        if not path.isdir(self.working_dir):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + self.working_dir + "\n")
            result = False

        source_path = path.join(self.infile_dir, '.'.join([self.corpus_name, self.source_lang]))
        target_path = path.join(self.infile_dir, '.'.join([self.corpus_name, self.target_lang]))
        if not path.isfile(source_path):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + source_path + "\n")
            result = False
        if not path.isfile(target_path):
            sys.stderr.write(os.strerror(errno.ENOENT) + ": " + target_path + "\n")
            result = False

        try:
            fp = open(self.log, 'w')
            fp.close()
        except IOError as e:
            print e
            result = False

        return result

    def corpus_w(self, lang, ext=None):
        """Return corpus name with specified lang and ext in working directory."""
        assert lang == self.source_lang or lang == self.target_lang
        namelist = [self.corpus_name, lang]
        if ext is not None:
            namelist.insert(1, ext)
        return path.join(self.working_dir, '.'.join(namelist))
