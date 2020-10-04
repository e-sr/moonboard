#!/bin/bash
FILE=$1
echo "Copy service file $FILE"
cp --verbose $FILE /lib/systemd/system/$FILE
echo "set permission"
chmod 644 /lib/systemd/system/$FILE
echo "restart service"
systemctl daemon-reload
systemctl enable $FILE
systemctl restart $FILE
