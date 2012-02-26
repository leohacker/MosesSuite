#!/bin/bash
#set -x
echo "Downloading the sample model and verify the moses installation."
wget http://www.statmt.org/moses/downloads/sample-models.tgz
tar xvf sample-models.tgz
cd sample-models
/tools/moses/bin/moses -f phrase-model/moses.ini < phrase-model/in > out
read line < out
if [ "$line" = "this is a small house" ]; then
    echo "Success!"
    echo "Moses installation test Passed."
else
    echo "Moses installation test Failed."
fi
cd - 2&>1 > /dev/null
rm -rf sample-models
rm -f sample-models.tgz
