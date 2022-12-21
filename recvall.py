
import time

try:
    from functions import *
except Exception as err:
    print(err, 'methodName="import"')

global Machine

def reload_data() -> list:
    m = getData("massegeToSent", jsonFile=getData("propperties"))
    return [getData("file_path"), m["patient"].values(), m["order"].values()]

def proses(Userdata):
    data = []
    b = False
    while not b:
        file_path = Userdata[0]
        #sendPakege(Userdata)
        data = recivePackege()
        b = not (False in data)
    saveData(file_path, data, mode="txt")
    return

def mainloop(Userdata, loop) -> None:
    print(proses(Userdata))
    return

def main(Userdata) -> None:
    loop = False
    if len(Userdata) < 3:
        print("using json file")
        Userdata = reload_data()
        loop = True
    mainloop(Userdata, loop)
    return

if __name__ == '__main__':
    print("starting:")
    time.sleep(0.1)
    Userdata = []
    try:
        Userdata = [sys.argv[0],sys.argv[1:]]

    except Exception as err:
        Log(err, methodName="main")

    finally:
       
        try:
            main(Userdata)
        except Exception as err:
            Log(err, methodName="main")
