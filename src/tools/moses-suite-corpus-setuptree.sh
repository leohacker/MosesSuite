#!/bin/bash

# Create the directory hierarchy of corpus for language pair.

# This script is part of Moses Suite.
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang 2012
# License:      GPL

if [ ! -f "/etc/moses-suite.conf" ]; then
    echo "File /etc/moses-suite.conf not exists."
    echo "Please re-install your moses suite system or create this config file manually."
    exit 0
fi

E_BARARGS=65

if [ $# -ne 2 ]; then
    echo "Usage: `basename $0` src-lang target-lang"
    exit $E_BARARGS
fi

src=$( echo "$1" | tr '[:lower:]' '[:upper:]' )
target=$( echo "$2" | tr '[:lower:]' '[:upper:]' )

source /etc/moses-suite.conf
echo ${MOSES_DATA_ROOT}
CORPUSDIR=${MOSES_DATA_ROOT}/corpus
LANGDIR=${MOSES_DATA_ROOT}/${src}-${target}
if [ -d "$LANGDIR" ]; then
    echo "Directory ${LANGDIR} already exists."
fi

mkdir -p ${LANGDIR}/{training,tuning,recaser,evaluation}
cd ${CORPUSDIR}
ln -s ${src}-${target} ${target}-${src}
