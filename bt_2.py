#!/usr/bin/python
import bluetooth
import csv, json, sys
import sys
print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("found %d devices" % len(nearby_devices))
for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))


def StartBTServer():
    srv = BT()
    mac = 'FC:A8:9A:00:32:23' # The address from the HC-05 sensor
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
                if len(data) == 0:
                    btDeviceList = srv.Discover()
                    srv.DumpDevices(btDeviceList)
                    mac = btDeviceList[0][0]
                    name = btDeviceList[0][1]
                    print('Connecting to first BT device found: {0}, MAC: {1}'.format(name, mac))
                    srv.Connect(mac)
                print(ar_obj)
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
        result = bluetooth.lookup_name('FC:A8:9A:00:32:23', timeout=3)
        while True:
            if (result != None):
                try:
                    print('Attempting Connection...')
                    self.btSocket.connect((mac, port))
                except bluetooth.btcommon.BluetoothError:
                    self.BindListen()
            return result

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
    try:
        StartBTServer()

    except ValueError as e:
        pass
        print("Searching for devices...")
        search_time = 10
        nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True, lookup_names=True)
        print("found %d devices" % len(nearby_devices))

        if len(nearby_devices) > 0:
            print("Found %d devices!" % len(nearby_devices))
        else:
            print("No devices found! Please check your Bluetooth device and restart the arduino colar!")
        exit(0)
