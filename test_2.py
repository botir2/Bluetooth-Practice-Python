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

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

target_name = "HC-6-2" # HC 05/06 arduino bluetooth Device name
port = 1  # RFCOMM SPP connection port
target_address = None

print("Init bluetooth...")
bl = Bluetoothctl()
srv = BT_data_object() #service class
jsondisconnd = {}
jsonconnd = {}
# reailze bluetooth data class
print("Ready!")
bl.power_on()
bl.pairable_on()
bl.agent_on()
bl.default_agent()
bl.start_scan()
start_disc_time = ""
start_conn_time = ""
start_count = 1
last_count = 0
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
        try:
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((target_address, port))
            start_conn_time = datetime.datetime.now()  # start connection time
            jsondisconnd['disconnd'] = start_disc_time
            jsonconnd['connd'] = start_conn_time
            while True:
                try:
                    data += sock.recv(1024)  # recieving data
                except:
                    start_count = 1
                    last_count = 0
                    raise
                data_end = data.find(b']')
                if data_end != -1:
                    rec = data[:data_end]
                    ar_obj = srv.parse(data)
                    #print(start_conn_time)
                    data = data[data_end + 1:]
                    sock.send(json.dumps(jsondisconnd, cls=DateTimeEncoder))
                    sock.send(json.dumps(jsonconnd, cls=DateTimeEncoder))
            server_sock.close()
        except bluetooth.btcommon.BluetoothError as err:
            print("Error catched: " + str(err))
            print(bl.get_device_full_info(target_address))
            if start_count > last_count:
                start_disc_time = datetime.datetime.now()#  # start disconnection time
            print(start_disc_time)
            last_count = 2
            # Error handler
            pass
    else:
        print("could not find target bluetooth device nearby")


