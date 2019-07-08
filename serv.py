import bluetooth

hostMACAddress = '98:D3:31:40:4A:07'
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)


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
        return datas
    except ValueError as e:
        return None  # or: raise

data = ""
while True:
    client, clientInfo = s.accept()
    try:
        while True:
            data += client.recv(size)
            data_end = data.find(']')
            if data_end != -1:
                rec = data[:data_end]
                print(parse(data))
                client.send("1")
                data = data[data_end + 1:]
                client.send("0")
    except:
        print("Closing socket")
        client.close()
s.close()