import bluetooth
import json
import time

bd_addr = 'FC:A8:9A:00:32:23'  # The address from the HC-05 sensor
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))


def parse(json_text):
    try:
        datas = []
        json_object = json.loads(str(json_text))
        datas.append(json_object[0])
        datas.append(json_object[1])
        datas.append(json_object[2])
        datas.append(json_object[3])
        datas.append(json_object[4])
        datas.append(json_object[5])
        datas.append(json_object[7])

        return datas
    except ValueError as e:
        return None  # or: raise

def sentDiscovery():
    sock.send("1")
    sock.send("2")
data = ""
while True:
    try:
        data += sock.recv(1024)
        data_end = data.find(']')
        if data_end != -1:
            rec = data[:data_end]
            print(parse(data))
            sock.send("1")
            data = data[data_end + 1:]
            sock.send("0")
        # data = sock.recv(64)
        # jdata = parse(data)
        # print(data)
        # data = ""
    except KeyboardInterrupt:
        break
sock.close()














