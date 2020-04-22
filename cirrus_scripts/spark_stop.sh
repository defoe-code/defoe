#!/bin/bash
set -x 

filename=$HOME/bash_scripts/worker.log
fileItemString=$(cat  $filename |tr "\n" " ")
readarray -t fileItemString < $filename
declare -p fileItemString

echo $fileItemString
for i in "${fileItemString[@]}"
do
        echo "ssh $i killall java"
        ssh $i "killall java"
done

filename=$HOME/bash_scripts/master.log
fileItemString=$(cat  $filename |tr "\n" " ")
readarray -t fileItemString < $filename
declare -p fileItemString

echo $fileItemString
for i in "${fileItemString[@]}"
do
        echo "ssh $i killall java"
        ssh $i "killall java"
done
