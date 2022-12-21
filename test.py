import socket
from astm.constants import *
server =("127.0.0.1",8080)
Host = socket.socket()
Host.bind(server)
Host.listen(1)
cli,_ = Host.accept()
cli.send(NCK)
