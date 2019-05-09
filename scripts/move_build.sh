#!/bin/bash
echo Beginning move
sudo cp --verbose -a frontend/build/* /var/www/html/
echo restart nginx
sudo systemctl restart nginx.service
