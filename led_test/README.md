sudo apt-get update
sudo apt-get -y install gcc make build-essential git scons swig

# follow: https://developer-blog.net/raspberry-pi-zero-als-led-strip-controller/?cookie-state-change=1602664207125


git clone https://github.com/jgarff/rpi_ws281x.git
sudo pip3 install LightBerries rpi-ws281x-light-show 

sudo python3 strandtest.py

adjust number of led



pins as described elsewhere

TBD

5v over same pwr supply


TBD: disable sound card stuff from blog above



WS2811 