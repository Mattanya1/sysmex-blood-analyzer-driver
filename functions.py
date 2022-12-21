from varubols import *

global Machine

print(Machine)
# functions
def create_csv(name):
    open(name,"x").close()
    with open(name,"a") as f:
        f.write("   ,methodName, Error, time\n")
    return

def Log(Error, methodName="Unknown") -> None:
    print(f"Error, {Error}")
    name = getData("ErrorLogFile")
    fileError = f"[Errno 2] No such file or directory: '{name}'"
    t = lambda :time.strftime('%m/%d/%Y %H:%M:%S', time.localtime())
    l=1
    try:
        with open(name,"r") as f:
            l = len(f.read().split(sep="\n"))
    except Exception as error:
        if str(error) == fileError:
            try:
                create_csv(name)
            except:
                raise (f"Couldn't find the log file in place:{name}.\n Try to close it, crate a csv file there or change the 'ErrorLogFile' position\n in the settings file.")
            else:
               print("criating file!")
        else:
            print(f"Error accord while writing to log file:\n{error}")
            with open(name,"a") as f:
                f.write(f"{l}, Log, {str(error)}, {t()}\n")
            print(l)
    finally:
        f = open(name,"r")
        p = f.read()
        f.close()
        s = p.split(sep="\n")
        l = len(s)
        with open(name,"a") as f:
            f.write(f"{l-1}, {methodName}, {str(Error)}, {t()}\n")
        return

def getOrder_Record(ONO,TESTID,PRI, CLDT ,CVLM, ACCD,RCINF,RCDT,SRC,DTR,RQDT, PSID)-> str:
    global Record_NUM
    return f"OBR | {get_NUM(Record_NUM)} | {ONO} | | {TESTID} | {PRI} | {RQDT} | {CLDT} | | {CVLM} | | {ACCD} | {RCINF} | {RCDT} | {SRC} | | | | | | | {DTR} | | {PSID} | | s\n"

def getHeader_Record()-> str:
    return f"H | ^ ~ \ & | | | | | | | | | | | A.2 | {time.strftime('%Y%m%d%H%M', time.localtime())}\n"

def  getPatient_Record(PID, APID, NAME,MN,BD,SEX,DCODE,HT,WT,ADMS,LC,DTR)-> str:
    global PATIENT_NUM
    # Date of Birth in Format: YYYYMMDD
    #Gender M: Male, F: Female, U: Unknown
    #Admission status In/Out
    # args -> PID, APID, NAME,MN,BD,SEX,DCODE,HT,WT,ADMS,LC,DTR
    return f"P |{get_NUM(PATIENT_NUM)}| {PID} | | {APID} | {NAME} | {MN} | {BD} | {SEX} | | | | | {DCODE} | | | {HT} | {WT} | | | | | | | {ADMS} |{LC} | | | | | | | {DTR} \n"

def getEnd_Record(SEQ, PCNT, LCNT) -> str:
    return f"L | {SEQ} | | {PCNT} | {LCNT} \n"

def recive(encoding="utf-8", length=1024) -> bytes:
    returnValue = ""
    try:
        data = Machine.recv(length)
        if data == b"":
            return b"error"
        returnValue +=data.decode(encoding)
    except Exception as err:
        Log(err, methodName="recive")
        print("Error accord: ", err)
        Machine.send(NAK)
    else:
        try:
            Machine.send(ACK)
        except:
            Log("filed in sending ACK", methodName="recive")
            print("oy")
    finally:
        #cond = returnValue.encode(encoding)==EOT
        return returnValue.encode(encoding)

def send(massage, encoding="UTF-8") -> bool:
    def do():
        print("sending:", massage)
        if encoding=="":
            Machine.send(massage)
        else:
            Machine.send(massage.encode(encoding))
    do()
    f = Machine.recv(1)
    print(f)
    return ACK in f

def sendPakege(data, encoding="UTF-8", length=1024) -> None:
    records =[getHeader_Record(),getPatient_Record(*data[1]),getOrder_Record(*data[2])]
    SEQ, PCNT, LCNT = 1, 1, len(records)
    records.append(getEnd_Record(SEQ, PCNT, LCNT))
    records[0] = str(LCNT+1)+ records[0]
    print(records[0])

    massage = [encode_record(r, encoding) for r in records]
    massage[0]= STX+massage[0]
    print(massage)

    try:
        Machine.send(ENQ)
        print("sending")
        for m in massage:
            data = False
            while not data:
                data = send(m, encoding="") # send reterns bool obj(look one def up)!!!

                if not data:
                    print("Error accord while sending data")
                    time.sleep(10)
                elif data:
                    print("ACK")
                else:
                    print("what the hell?!")

    except Exception as err:
        Log(err, methodName="sendPakege")
    Machine.send(EOT)# end of sending
    print("success")
    return


def recivePackege(encoding="UTF-8",length=1024) -> list:
    reternValue = b""
    data = b""
    while data != ENQ:
        data = Machine.recv(1)
        print(data)
    Machine.send(ACK)
    print("receiving")
    while True:
        data = recive()
        #if reternValue==b'\x02' and data!=b"H":continue
        if EOT in data or data ==b"error":# or EOT in data:
            break
        else:
            reternValue += data
        #return recivePackege()
    Machine.send(EOT)
    print(reternValue)
    def temp(r):
        massage = (r.decode()+"\r\n").encode()
        try:
            return decode_message(massage, encoding)
        except Exception as err:
            print ("cheak-Sum Error")
            Log(err, methodName="recivePackege")
            return False
    l1 = map(temp,reternValue.split(sep=b"\r\n"))
    l2 = []
    for i in l1:
        if not i in ["\r\n","\r\n\r\n"]:
            l2.append(i)
    return l2

def saveData(path,data, mode="txt"):
    global Answer_NUM
    text=""
    path = getData("file_path")
    for t in data:
        text += str(t)+'\n'
        try:
           t[1][0][0]
        except:
            print("not P")
        else:
            if t[1][0][0] in ["p","P"]:
                path = f"{path}\\data_{t[1][0][3]}_{time.strftime('%m_%d_%Y', time.localtime())}.{mode}"
    if path == getData("file_path"):
        path = f"{path}\\data{get_NUM(Answer_NUM)}.{mode}"
    if mode=="txt":

        try:
            temp=open(path)
            temp.close()
        except:
            temp = open(path, "x")
            temp.close()

        finally:
            with open(path, "w") as f:
                f.write(text)

    #ToDo elif mode == "xml"
