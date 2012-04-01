#!/bin/bash

# This file is part of Moses Suite.
# Author: Leo Jiang <leo.jiang.dev@gmail.com>
# Copyright 2012 Leo Jiang
# under GPL License.

E_BARARGS=65

if [ $# -ne 2 ]; then
    echo "Usage: `basename $0` src-lang target-lang"
    exit $E_BARARGS
fi

src=$( echo "$1" | tr '[:lower:]' '[:upper:]' )
target=$( echo "$2" | tr '[:lower:]' '[:upper:]' )

mkdir -p /data/corpus/${src}-${target}/{training,tuning,recaser,evaluation}
cd /data/corpus/
ln -s ${src}-${target} ${target}-${src}
