import bluetooth
import json
import time

def search():
    print("searching....")
    devices = bluetooth.discover_devices(lookup_names=True)
    return devices

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

def conn(addr):

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((addr, 1))
    sock.listen(1)
    port = sock.getsockname()[1]
    uuid = "00001101-0000-1000-8000-00805f9b34fb"
    advertise_service(server_sock, "SampleServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE],
                      )
    print("Waiting for connection on RFCOMM channel %d" % port)   print("Accepted connection from ", client_info)
    print('conneccted..')
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


if __name__ == "__main__":
    while True:
        results = search()
        if (results != None):
            for addr, name in results:
                print("{0} - {1}".format(addr, name))
                conn(addr)
            # endfor
        # endif
        time.sleep(60)
    # endwhile









