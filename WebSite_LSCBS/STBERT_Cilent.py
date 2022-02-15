import socket
import json
import sys
import os

class TranData(object):
    def __init__(self):
        self.type = 0
        self.msg = ""

    def __jsonencode__(self):
        return {'type': self.type, 'msg': self.msg}

class AdvancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()

        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

HOST = os.environ.get("BACKEND_SERVER_ADDR", "127.0.0.1")
PORT = 1025


try:
    #cmd = sys.argv[1]
    #d = TranData()
    #d.msg = cmd
    #request = json.dumps(d, cls=AdvancedJSONEncoder)
    #print(request)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    cmd = str(sys.argv[1])
    d = TranData()
    d.msg = cmd
    request = json.dumps(d, cls=AdvancedJSONEncoder)
    #print(request)
    s.send(request.encode())
    data = s.recv(32768).decode()
    #print("server send : ")
    #print(data)
    s.close()
    SimilarList = json.loads(data)
    print(data)
except Exception as ex:
    print(ex)
#print('Finish')