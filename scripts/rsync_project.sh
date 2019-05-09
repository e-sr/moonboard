#!/bin/bash
echo Beginning rsync

cd /home/esr/Documents

#control
RPI="moonboard:~/"
EXCLUDE="moonboard/scripts/rsync_exclude.txt"
FOLDERS="moonboard/"

for dir in $FOLDERS
do
rsync -avp --exclude-from=$EXCLUDE $dir $RPI$dir
done
