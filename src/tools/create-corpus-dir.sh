#!/bin/bash

# Create the directory hierarchy of corpus for language pair.

# This script is part of Moses Suite.
# Author:       Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright:    Leo Jiang 2012
# License:      GPL

E_BARARGS=65

if [ $# -ne 2 ]; then
    echo "Usage: `basename $0` src-lang target-lang"
    exit $E_BARARGS
fi

src=$( echo "$1" | tr '[:lower:]' '[:upper:]' )
target=$( echo "$2" | tr '[:lower:]' '[:upper:]' )

LANGDIR=/data/corpus/${src}-${target}
if [ -d "$LANGDIR" ]; then
    echo "Directory ${LANGDIR} already exists."
    exit 0
fi

mkdir -p ${LANGDIR}/{training,tuning,recaser,evaluation}
cd /data/corpus/
ln -s ${src}-${target} ${target}-${src}
