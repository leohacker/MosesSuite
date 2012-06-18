#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Corpus Clean Tool

Clean two aligned corpus files according to user specified configuration.
"""

import errno
import os.path
import sys
from optparse import OptionParser
from corpustool.config import CorpusToolsConfig
from corpustool.config import CleanConfig

def main(argv=sys.argv):
    NUM_ARGS = 5
    usage = "Usage: %prog [options] corpus_directory corpus_filename src_lang tgt_lang clean_step_config"
    version = "%prog 1.0 (c) 2012 Leo Jiang <leo.jiang.dev@gmail.com>"
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

    if len(args) != NUM_ARGS :
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=NUM_ARGS)

    # tools_config will be initialized with system and user config, then some settings are overrided by config
    # specified thru command line option.
    tools_config = CorpusToolsConfig()
    if options.config is not None:
        tools_config.readfile(options.config)

    # corpus_clean script depends on external tools/scripts, at least moses scripts.
    if len(tools_config.sections()) == 0:
        sys.stderr.write("No corpus tools configuration works. Please check the system and user config files.\n")
        sys.stderr.write("System: " + tools_config.SYSTEM_CONFIG + "\n")
        sys.stderr.write("User:   " + tools_config.USER_CONFIG + "\n")
        sys.exit(errno.EINVAL)

    steps_filename = args[4]
    clean_config = CleanConfig(steps_filename)
    if not clean_config.has_steps():
        sys.stderr.write("Failed to read clean steps definition.\n")
        sys.exit(errno.EINVAL)

    clean_config.corpus_name = args[1]
    clean_config.source_lang = args[2]
    clean_config.target_lang = args[3]
    clean_config.infile_dir  = args[0]
    clean_config.working_dir = options.working_dir if options.working_dir is not None else clean_config.infile_dir
    clean_config.outfile_dir = options.output_dir if options.output_dir is not None else clean_config.infile_dir

    clean_config.log = options.log if options.log is not None else '.'.join(clean_config.corpus_name, "clean", "log")
    check_config(clean_config)
    clean_corpus(clean_config)

def check_config(config):
    if not os.path.isdir(config.infile_dir):
        sys.stderr.write(os.strerror(errno.ENOENT) + ": " + config.infile_dir + "\n")
        sys.exit(errno.ENOENT)
    if not os.path.isdir(config.outfile_dir):
        sys.stderr.write(os.strerror(errno.ENOENT) + ": " + config.outfile_dir + "\n")
        sys.exit(errno.ENOENT)
    if not os.path.isdir(config.working_dir):
        sys.stderr.write(os.strerror(errno.ENOENT) + ": " + config.working_dir + "\n")
        sys.exit(errno.ENOENT)

    source_path = os.path.join(config.infile_dir, '.'.join(config.corpus_name, config.source_lang))
    target_path = os.path.join(config.infile_dir, '.'.join(config.corpus_name, config.target_lang))
    if not os.path.isfile(source_path):
        sys.stderr.write(os.strerror(errno.ENOENT) + ": " + source_path + "\n")
        sys.exit(errno.ENOENT)
    if not os.path.isfile(target_path):
        sys.stderr.write(os.strerror(errno.ENOENT) + ": " + target_path + "\n")
        sys.exit(errno.ENOENT)

def clean_corpus(config):
    source_corpus = os.path.join(config.infile_dir, '.'.join(config.corpus_name, config.source_lang))
    target_corpus = os.path.join(config.infile_dir, '.'.join(config.corpus_name, config.target_lang))

    # prepare the corpus in working directory.
    if not os.path.samefile(config.infile_dir, config.working_dir):
        shutil.copy(source_corpus, config.working_dir)
        shutil.copy(target_corpus, config.working_dir)

    for step in config.steps:
        print step["name"]

if __name__ == "__main__":
    main()
