#!/usr/bin/python
# encoding=utf8
import time,datetime
import pexpect
import subprocess
import csv, json, sys
import bluetooth_rfkill
import bluetooth
from data_object.BTobject import *
from Bluetoothctl_conn import *

target_name = "HC-6-2" # HC 05/06 arduino bluetooth Device name
port = 1  # RFCOMM SPP connection port
target_address = None

print("Init bluetooth...")
bl = Bluetoothctl()
srv = BT_data_object() #service class
# reailze bluetooth data class
print("Ready!")
bl.power_on()
bl.pairable_on()
bl.agent_on()
bl.default_agent()
bl.start_scan()

print("Scanning for 10 seconds...")
for i in range(1, 11):
    print("Initializing....")
    time.sleep(1)

for device in bl.get_discoverable_devices():
    if target_name == device['name']:
        target_address = device['mac_address']
        break
    else:
        for device in bl.get_paired_devices():
            if target_name == device['name']:
                target_address = device['mac_address']
                break
while True:
    if target_address is not None:
        bluetooth_rfkill.BtAutoPair(target_address)
        print("found target bluetooth device with address ", target_address)
        data = b""
        start_disc_time = ""
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((target_address, port))
            while True:
                try:
                    data += sock.recv(1024)  # recieving data
                except:
                    start_disc_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # start connection time
                    raise
                data_end = data.find(b']')
                if data_end != -1:
                    rec = data[:data_end]
                    ar_obj = srv.parse(data)
                    print(ar_obj)
                    data = data[data_end + 1:]
                    #sock.send(str(elapsed))
            server_sock.close()
        except bluetooth.btcommon.BluetoothError as err:
            print("Error catched: " + str(err))
            print(bl.get_device_full_info(target_address))
            print(start_disc_time)
            # Error handler
            pass
    else:
        print("could not find target bluetooth device nearby")


