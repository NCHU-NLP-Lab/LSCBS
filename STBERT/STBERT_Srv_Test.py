# coding=utf-8

# No model, for server development test
import socket
import json
import traceback

bind_ip = "127.0.0.1"
bind_port = 1026

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print ("[*] Listening on %s:%d " % (bind_ip,bind_port))

while True:
    client,addr = server.accept()
    print('Connected by ', addr)

    try:
        data = client.recv(32768)
        query = data.decode()
        print("Client recv data : %s " % (query))
        TranData = json.loads(query)
        print(TranData)
        if (TranData['type'] == 0):
            print(TranData['msg'])
            print('Similar Done')
            request = 'Type1 Fin'
            print('GetSimilar ', request)
            client.send(request.encode())
        elif (TranData['type'] == 1):
            print(TranData['id'])
            print('Get judgement Done')
            request = 'Type2 Fin'
            #request = json.dumps(s, cls=AdvancedJSONEncoder)
            print('judgement ', request)
            client.send(request.encode())

    except Exception as e:
        print(e)
        traceback.print_exc()
        s = b'Fail'
        client.send(s)
