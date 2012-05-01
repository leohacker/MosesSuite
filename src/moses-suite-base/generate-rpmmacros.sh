#!/bin/bash
# Generate the rpm macros for moses suite packages according to moses suite
# configuration. Keep the config to be consistant between system config and
# rpmmacros.
source moses-suite.conf
touch macros.moses
cat /dev/null > macros.moses
echo "%define moses_suite_root $MOSES_SUITE_ROOT" >> macros.moses
echo "%define moses_data_root $MOSES_DATA_ROOT" >> macros.moses
