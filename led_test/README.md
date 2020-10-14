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



Not able to initialize the driver. Error
PiWS281X Requires the rpi_ws281x C extension.

Install rpi_ws281x with the following shell commands:

    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x

    sudo apt-get install python-dev swig scons
    sudo scons

    cd python
    # If using default system python3
    sudo python3 setup.py build install
    # If using virtualenv, enter env then run
    python setup.py build install

Use bibliopixel.drivers.dummy_driver
^Ckeyboard interrupt received



=> Must be installed :)