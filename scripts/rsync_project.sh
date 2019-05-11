#!/bin/bash
host=moonboard-1
echo Beginning rsync to  $host

cd /home/esr/Documents

#control
RPI="$host:~/"
EXCLUDE="moonboard/scripts/rsync_exclude.txt"
FOLDERS="moonboard/"

for dir in $FOLDERS
do
rsync -avp --exclude-from=$EXCLUDE $dir $RPI$dir
done
