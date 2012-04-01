#! /bin/bash

src=$( echo "$1" | tr '[:lower:]' '[:upper:]' )
target=$( echo "$2" | tr '[:lower:]' '[:upper:]' )

mkdir -p /data/corpus/${src}-${target}/{training,tuning,recaser,evaluation}
cd /data/corpus/
ln -s ${src}-${target} ${target}-${src}
