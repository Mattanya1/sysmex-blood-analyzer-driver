
import json
import time
import sys
import socket

from astm.constants import *
print(ACK)

def getData(key, jsonFile = "settings.json"):
    ret = {}
    while ret == {}:
        j =open(jsonFile,"r")
        t = j.read()
        j.close()
        if t =="":
            time.sleep(10)
        else:
            ret = json.loads(t)[key]
    return ret

def get_NUM(_NUM):
    _NUM += 1
    _NUM %= 9999
    return f"{(4-len(str(_NUM)))*'0'}{_NUM}"

# global data
global PATIENT_NUM
global Record_NUM
global Answer_NUM
global Machine

PATIENT_NUM, Record_NUM, Answer_NUM = 0,0,0

address = getData("address")
port = getData("port")
if __name__ == "function.py" or __name__ == "varubols" or __name__ == '__main__':
    from astm.codec import decode_message, encode_message, encode_record
    print(__name__)
    Host = socket.socket()
    Host.bind((address, port))
    Host.listen(1)
    global Machine
    Machine, _ = Host.accept()
    print(Machine)



