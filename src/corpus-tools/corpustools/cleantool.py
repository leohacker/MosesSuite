#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# pylint: disable=C0301,C0111

"""Corpus Clean Tool

Clean aligned corpus files according to user specified configuration.
"""

import errno
import shutil
import sys
from os import path

from optparse import OptionParser
from corpustools.config import CorpusToolsConfig
from corpustools.config import CleanConfig


def main(argv=sys.argv):    # pylint: disable=W0102
    config = argv2conf(argv)
    clean_corpus(config)


def argv2conf(argv):
    usage = "Usage: %prog [options] corpus_directory corpus_filename src_lang tgt_lang clean_step_config"
    num_args = 5
    version = "%prog 0.2 (c) 2012 Leo Jiang <leo.jiang.dev@gmail.com>"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-c", "--config", metavar="FILE", dest="config",
                      type="string", help="specified corpus tools config")
    parser.add_option("-w", "--working-dir", metavar="DIR", dest="working_dir",
                      type="string", help="working directory")
    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")
    parser.add_option("-l", "--log", metavar="FILE", dest="log",
                      type="string", help="log file")

    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    # corpus tools config(tools_config) is initialized with system and user config,
    # then some settings are overrided by config file specified thru command line option.
    tools_config = CorpusToolsConfig()
    if options.config is not None:
        tools_config.readfile(path.abspath(options.config))

    # clean tool depends on external tools/scripts, at least moses scripts.
    if len(tools_config.sections()) == 0:
        sys.stderr.write("Corpus tools config files not exist or broken. Please check the system and user config files.\n")
        sys.stderr.write("System: " + tools_config.SYSTEM_CONFIG + "\n")
        sys.stderr.write("User:   " + tools_config.USER_CONFIG + "\n")
        sys.exit(errno.EINVAL)

    steps_filename = args[4]
    clean_config = CleanConfig(path.abspath(steps_filename))
    if clean_config.validate_steps() is False:
        sys.stderr.write("Failed to read clean steps definition.\n")
        sys.exit(errno.EINVAL)

    clean_config.corpus_name = args[1]
    clean_config.source_lang = args[2]
    clean_config.target_lang = args[3]
    clean_config.infile_dir  = path.abspath(args[0])
    clean_config.outfile_dir = clean_config.infile_dir if options.output_dir is None else path.abspath(options.output_dir)
    clean_config.working_dir = clean_config.infile_dir if options.working_dir is None else path.abspath(options.working_dir)

    clean_config.log = path.abspath(options.log) if options.log is not None else \
                        path.join(clean_config.working_dir, '.'.join([clean_config.corpus_name, "clean", "log"]))

    if clean_config.validate_paths() is False:
        sys.exit(errno.ENOENT)

    return clean_config


def clean_corpus(config):
    source_corpus = path.join(config.infile_dir, '.'.join([config.corpus_name, config.source_lang]))
    target_corpus = path.join(config.infile_dir, '.'.join([config.corpus_name, config.target_lang]))

    # prepare the corpus in working directory.
    if not path.samefile(config.infile_dir, config.working_dir):
        shutil.copy(source_corpus, config.working_dir)
        shutil.copy(target_corpus, config.working_dir)

    for step in config.steps:
        print step["name"]

if __name__ == "__main__":
    sys.exit(main(sys.argv))
