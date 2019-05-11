#!/bin/bash
echo copy frontend/build/ folder to to /var/www/html/
sudo cp --verbose -a frontend/build/* /var/www/html/
echo restart nginx
sudo systemctl restart nginx.service
