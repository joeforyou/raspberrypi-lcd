Step 1.
login to raspberry pi as pi

Step 2.
sudo nano /etc/apt/sources.list

#deb m http://repo.volumio.org/apt/ m jessie main contrib
deb m http://mirrordirector.raspbian.org/raspbian/ m jessie main
#deb-src m http://mirrordirector.raspbian.org/raspbian/ m wheezy main


Step 3.
add at end:
sudo nano /etc/modules

i2c-bcm2708
i2c-dev

Step 4.
Then install the PiFace libraries:

login as root

apt-get update;apt-get install git python-smbus i2c-tools python-dev gcc

git clone git://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git 

Step 5.
# Install python-mpd2 library

sudo apt-get update
sudo apt-get install python-setuptools
git clone git://github.com/Mic92/python-mpd2.git
cd python-mpd2
sudo python setup.py install

Step 6.
# Copy  my files in 
Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate

chmod ugo+x *.py

Step 7.
# Enjoy

./launcher.py