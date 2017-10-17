# Raspberry Pi / OctoPrint GPIO plugin

Currently able to display sensor data on the navbar.

![Screenshot](OctoPrint-Pi-Gpio.png?raw=true)

Tested on Raspberry Pi 3 Model B / OctoPrint 1.3.4.

## Supported periperals

* HTU21D — Temperature and humidity sensor (I²C)

## Setup

1. Connect your hardware as described in the [Wiring](#wiring) section

1. Enable hardware interfaces  
Use `raspi-config` or simply uncomment the corresponding lines in the `/boot/config.txt` file:
   * I²C: `dtparam=i2c_arm=on`

1. Install the plugin

1. Reboot the Pi

## Wiring

### HTU21D

![Wiring](htu21d-wiring.png?raw=true)

## Credits

* Frederic Moutin (https://github.com/l00ma/OctoPrint-roomTemp)
* Adminck (https://s55ma.radioamater.si/2017/05/23/htu21d-raspberry-pi-python-script/)
