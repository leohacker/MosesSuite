#!/bin/bash
#set -x
cd /data/engines/sample-models
echo "Verify moses decoder:"
echo "====================="
/tools/moses/bin/moses -f phrase-model/moses.ini < phrase-model/in > ~/out
read line < ~/out
if [ "$line" = "this is a small house" ]; then
    echo "Moses installation test Passed."
else
    echo "Moses installation test Failed."
fi
rm ~/out

echo 
echo 
echo "Verify moses chart decoder:"
echo "==========================="
/tools/moses/bin/moses_chart -f string-to-tree/moses.ini < string-to-tree/in > ~/out.stt
/tools/moses/bin/moses_chart -f tree-to-tree/moses.ini < tree-to-tree/in.xml > ~/out.ttt

