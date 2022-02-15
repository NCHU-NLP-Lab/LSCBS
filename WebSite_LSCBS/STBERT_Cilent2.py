import socket
import json
import sys
import os

class TranData(object):
    def __init__(self):
        self.type = 1
        self.id = 0

    def __jsonencode__(self):
        return {'type': self.type, 'id': self.id}

class AdvancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()

        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

HOST = os.environ.get("BACKEND_SERVER_ADDR", "127.0.0.1")
PORT = 1025


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

cmd = int(sys.argv[1])
d = TranData()
d.id = int(cmd)
request = json.dumps(d, cls=AdvancedJSONEncoder)
#print(request)
s.send(request.encode())

data = s.recv(131072).decode()
#print("server send : ")
#print(data)
s.close()

#SimilarList = json.loads(data)
print(data)
#print('Finish')