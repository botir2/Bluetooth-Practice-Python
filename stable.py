import sys
import bluetooth
import json, time

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = server_sock.getsockname()[1]
server_sock.connect(('98:D3:31:40:4A:07',1))
server_sock.bind(("",port))
server_sock.listen(1)


print ("listening on port %d" % port)

uuid = "00001101-0000-1000-8000-00805f9b34fb"
bluetooth.advertise_service(server_sock, "pet_costume", uuid)
client_sock,address = server_sock.accept()
print ("Accepted connection from ",address)


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
data = ""
while True:
    try:
        data += server_sock.recv(1024)
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
client_sock.close()
server_sock.close()

