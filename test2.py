
import socket
from astm.constants import *

root = socket.socket()
server =("127.0.0.1",5000)
root.connect(server)
print("connected")
data = root.recv(1)
print(data)
root.send(ACK)
data = b""
dl = []
while data != EOT:
    data = root.recv(100)
    dl += [data]
    print(data)
    if data.endswith(b"\n"):
        root.send(ACK)

print("got")
root.send(ENQ)
print(root.recv(1))
print(dl)
for i in dl:
    root.send(i)
    print(root.recv(1))
root.send(EOT)
