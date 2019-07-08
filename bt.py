import bluetooth
from subprocess import Popen, PIPE

print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    print("  %s - %s" % (addr, name))

bd_addr = addr #The address from the HC-05 sensor
port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
search_time = 10

#Therefore, to test if a socket is still connected to an actual device lost connection control
try:
    sock.getpeername()
    still_connected = True
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
    for addr, name in nearby_devices:
        print("%s. %s - %s" % (i, addr, name))
        i = + 1

    device_num = input("Please specify the number of the device you want to track: ")
    # extract out the useful info on the desired device for use later
    addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]
    sock.connect((addr, port))

data = b""
while 1:
	try:
		data += sock.recv(1024)
		data_end = data.find(b'\n')
		if data_end != -1:
			rec = data[:data_end]
			print (data)
			data = data[data_end+1:]
	except KeyboardInterrupt:
		break
sock.close()
