#!/usr/bin/python
import bluetooth
import csv, json, sys
from subprocess import Popen, PIPE
import sys
print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))
for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))


def StartBTServer():
    srv = BT()
    mac = '98:D3:32:10:76:D8' # The address from the HC-05 sensor
    port = 1
    srv.BindListen(mac)
    # sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # sock.connect((bd_addr, port))

    data = b""
    while 1:
        try:
            data += srv.Receive()
            data_end = data.find(b']')
            if data_end != -1:
                rec = data[:data_end]
                ar_obj = srv.parse(data)
                print(ar_obj)
                while data is None:
                    try:
                        print("Searching for devices...")
                        search_time = 30
                        nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True,
                                                                    lookup_names=True)
                        print("found %d devices" % len(nearby_devices))

                        if len(nearby_devices) > 0:
                            print("Found %d devices!" % len(nearby_devices))
                        else:
                            print("No devices found! Please check your Bluetooth device and restart the arduino colar!")
                        exit(0)

                        i = 0  # Just an incrementer for labeling the list entries
                        # Print out a list of all the discovered Bluetooth Devices
                        for mac2, name in nearby_devices:
                            print("%s. %s - %s" % (i, mac2, name))
                            i = + 1
                        srv.Connect(mac2)
                    except SyntaxError:
                        pass

                srv.writeToJSONFile(ar_obj)
                data = data[data_end + 1:]
                srv.Send("1")
        except SyntaxError:
             pass
    print("Searching for devices...")
    nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True, lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    if len(nearby_devices) > 0:
        print("Found %d devices!" % len(nearby_devices))
    else:
        print("No devices found! Please check your Bluetooth device and restart the arduino colar!")
    exit(0)

    i = 0  # Just an incrementer for labeling the list entries
    # Print out a list of all the discovered Bluetooth Devices
    for mac2, name in nearby_devices:
        print("%s. %s - %s" % (i, mac2, name))
        i = + 1
    srv.Connect(mac2)
    srv.Disconnect()


class BT(object):
    def __init__(self, receiveSize=1024):
        self.btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._ReceiveSize = receiveSize

    def __exit__(self):
        self.Disconnect()

    def Connect(self, mac, port=1):
        self.btSocket.connect((mac, port))

    def Disconnect(self):
        try:
            self.btSocket.close()
        except Exception:
            pass

    def parse(self, json_text):
        try:
            datas = []
            json_object = json.loads(str(json_text))
            datas.append(json_object[0])
            datas.append(json_object[1])
            datas.append(json_object[2])
            datas.append(json_object[3])
            datas.append(json_object[4])
            datas.append(json_object[5])
            return datas
        except ValueError as e:
            return None  # or raise
        
    def writeToJSONFile(self, data):
        path = './'
        fileName = 'pet_bh'
        filePathNameExt = './' + path + '/' + fileName + '.txt'
        with open(filePathNameExt, 'w') as fb:
            json.dumps(data, fb)
            fb.write(']')
           

    def Discover(self):
        btDevices = bluetooth.discover_devices(lookup_names=True)
        if (len(btDevices) > 0):
            return btDevices
        else:
            raise Exception('no BT device!')

    def DumpDevices(self, btDeviceList):
        for mac, name in btDeviceList:
            print("BT device name: {0}, MAC: {1}".format(name, mac))

    def BindListen(self, mac, port=1, backlog=1):
        self.btSocket.connect((mac, port))

    def Accept(self):
        client, clientInfo = self.btSocket.accept()
        return client, clientInfo

    def Send(self, data):
        self.btSocket.send(data)

    def Receive(self):
        return self.btSocket.recv(self._ReceiveSize)

    def GetReceiveSize(self):
        return self._ReceiveSize


if __name__ == "__main__":
    StartBTServer()
# def StartBTClient():
#    cli = BT()
#    print('BT Discovery...')
#    btDeviceList = cli.Discover()
#    cli.DumpDevices(btDeviceList)
#    mac = btDeviceList[0][0]
#    name = btDeviceList[0][1]
#    print('Connecting to first BT device found: {0}, MAC: {1}'.format(name, mac))
#    cli.Connect(mac)
#    print('Connected... Enter data or \'exit\' to terminate the connection.')
#    while True:
#        data = raw_input()
#        if (data == 'exit'):
#            break
#        try:
#            cli.Send(data)
#        except Exception as e:
#            print(e.__str__())
#            break
#    cli.Disconnect()


# def GetFirstMAC():
#    proc = Popen(['hcitool', 'dev'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#    output, error = proc.communicate()
#    if (proc.returncode == 0):
#        lines = output.split('\r')
#        for line in lines:
#            if ('hci0' in line):
#                temp = line.split('\t')
#                temp = temp[2].strip('\n')
#                return temp
#        raise Exception('MAC not found')
#    else:
#        raise Exception('Command: {0} returned with error: {1}'.format(cmd, error))


# if __name__ == '__main__':
#    cmd = sys.argv[1]
#    if (cmd == 'server'):
#
#    elif (cmd == 'client'):
#        StartBTClient()
#    else:
#       print("Bluetooth RFCOMM client/server demo")
#       print("Copyright 2014 Nwazet, LLC.")
#       print("Please specify 'client' or 'server'")
# print("This demo assumes a single Bluetooth interface per machine.")
