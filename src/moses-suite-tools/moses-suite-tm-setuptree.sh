#!/bin/bash

# Create directory hierarchy for translation model.
# Project:      Moses Suite
# URL:          http://github.com/leohacker/MosesSuite
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang 2012
# License:      GPL

source moses-suite.functions
if [ $? != 0 ]; then
    echo "Failed to source moses-suite.functions."
    exit 1
fi

source_moses_conf

E_BADARGS=65

if [ $# -ne 3 ]; then
    echo "Usage: `basename $0` src-lang target-lang ID"
    exit $E_BARARGS
fi

src=$( echo "$1" | tr '[:lower:]' '[:upper:]' )
target=$( echo "$2" | tr '[:lower:]' '[:upper:]' )
id=$3

TMS_ROOT=${MOSES_DATA_ROOT}/translation_models
TM_DIR=${TMS_ROOT}/${src}-${target}/$id/
mkdir -p ${TM_DIR}
setup_tm_tree ${TM_DIR}
