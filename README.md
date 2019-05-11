# moonboard


## python3.7 

The project need python3.7

Run `scripts/install_py_3.7.sh`. See scripts. to install python 3.7 on raspberry. It take some time...  

Run `sudo pip3.7 install -r requirements.txt` to install requirements. It take some time... 

## Services

The following systemd services are needed

- **moonboard backend service**: backend service to the moonboard app. Add `services/moonboard.service`.  
  
- **nginx service**: Webserver serving the moonboard app. See next section.  

- **optional, app client service**: you can access moonboard app using the rpi browser. To automate it at startup. Add `services/kiosk_browser.service`.  
  
To Add and start a service see `services/install_service.sh`

### Install and setup  nginx

See [Deploy your React & .NET Core Apps on Linux using Nginx and Supervisor](https://hackernoon.com/deploy-your-react-net-core-apps-on-linux-using-nginx-and-supervisor-5a29d0b6ef94)
- install nginx `sudo apt install nginx`. 
- configure nginx:   
    - open file `sudo nano /etc/nginx/sites-available/default`
    - append content  
        ```
        server {
            listen 80 default_server;
            listen [::]:80 default_server;
            # Some comments...
            root /var/www/html;  # STATIC FILE LOCATION
            # Some comments...
            index index.html index.htm index.nginx-debian.html;
            server_name _;
            location / {
                    # Some comments...
                    try_files $uri /index.html;   # ADD THIS
            }
            # Some comments...
        }
        ```  

 - copy react app folder `/buils`  to  `/var/www/html`
 - restart nginx server `sudo systemctl restart nginx.service`. See `scripts/move_build.sh` script.

