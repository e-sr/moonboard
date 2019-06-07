# MOONBOARD BLE

The  moonboard has his own app wich can connect to the [original led box](https://moonclimbing.com/moonboard-led-system.html) thrught BLE.  
In this directory you find informations how setup the same functionality of the box on the pi.

## Moonboard led box information

### BLE Advertising

The original led box advertise itself with the following packet: 

**Advertising:**

|Desc|TYPE|VALUE| |
|--|--|--|--| 
|flags|0x01|0x06| LE General 'Discoverable Mode' and 'BR/EDR Not Supported'
|Tx power level|0x0A|0x00|
|services uiid |0x06|0x9ecadc240ee5a9e093f3a3b50100406e| UART service 

**Scan response**

|Desc|TYPE|VALUE||
|--|--|--|--|
|name|0x09|0x4d6f6f6e626f6172642041|    ascii for: Moonboard A

[See for more info](https://www.bluetooth.com/specifications/assigned-numbers/Generic-Access-Profile/) on GAP types

The advertising interval is about 600 ms.

### BLE services 

The  led box serve the following  BLE services.

1. Device firmware update
2. Device information
3. Nordic UART service: UUID 6e400001-b5a3-f393-e0a9-e50e24dcca9e (see advertising)
4. Eddystone-URL Configuration service 

Communication between app and led box is done by the uart service. The others services are uninportant for our purposes.

### APP => Nordic UART  communication Protocol

The communication is very simple, the app send a sequence of characters describing the problem. The sequence always **start** with `'#l'` and **finish** with `'#'`. Holds information are comma `,` separated. The hold first character describe the hold type. `'S'` for start, `'P'` for moves and `'E'` for end holds. The following char describe the position.
As an Example we can have `'l#S5,P9,P13,E18#'`

The hold positions is a number between 1 and 198. It trasform to the grid position following the strip.  

See the `moonboard_app_protocol.py` for more info.


## Emulated moonboard led box with rpi

The file `ble/moonboard_BLE_service.py` contain the application which do the following:

- register BLE service (as discussed above) using bluez(dbus interface)
- start advertising of the service
- emit a signal on the dbus when a connected device send a new problem to the ble  `Moonboard A` service. The signal contain the problem dictionary as json string.  

The application will show up with the service name `com.moonboard` in the session bus.

The application need access to the system dbus. For that the file `com.moonboard.conf` has to be copied in `/etc/dbus-1/system.d`.  

To start the application at startup the file  `com.moonboard.service` has to be copied in `/usr/share/dbus-1/system-services/`.  

### advertising details

 - 0x07 instead of 0x06 UUID service type
 - ... 

Note that advertising as follow (without scan response) also work:

|Desc|TYPE|VALUE||
|--|--|--|--| 
|services uuid |0x07|0x9ecadc240ee5a9e093f3a3b50100406e| UART service 
|name|0x09|0x4d6f6f6e626f6172642041|    ascii for: Moonboard A

### Simple client

A programm wich subscribe to the com.moonboard

*************
## Other BLE info

### Advertising

[Advertising primer](https://www.argenox.com/a-ble-advertising-primer/)

#### hcitools usage

Setting up advertising in a linux machine  using `hcitools`.  
See Bluetooth specification 5.0 (Core_v5.0.pdf), 7.8.5 LE Set Advertising Parameters command p.1321
- set adv:  
  `sudo hcitool -i hci0 cmd 0x08 0x0008  {adv: 32 byte 0-padded if necessary}`

- set scan response:  
  `sudo hcitool -i hci0 cmd 0x08 0x0009 {adv: 32 byte 0-padded if necessary}`  
  [info scan response](https://stackoverflow.com/questions/46431843/linux-bluez-custom-manufacturing-scan-response-data)

- adv time:    
  `sudo hcitool -i hci0 cmd 0x08 0x0006 {min:2byte} {max:2byte} {connectable:1byte} 00 00 00 00 00 00 00 00 07 00`  
  [info adv time](https://stackoverflow.com/questions/21124993/is-there-a-way-to-increase-ble-advertisement-frequency-in-bluez)

- start adv:  
  `sudo hcitool -i hci0 cmd 0x08 0x000a 01`  
  [info strt adv](https://stackoverflow.com/questions/16151360/use-bluez-stack-as-a-peripheral-advertiser)  

## Bluez DBUS 
[Good introduction](http://smartspacestuff.blogspot.com/2016/02/i-got-figurin-out-dbus-bluez.html)

[API](https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc)