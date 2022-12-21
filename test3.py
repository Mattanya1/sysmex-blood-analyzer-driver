print("start")
import functions
from varubols import *

Userdata = [getData("file_path"), getData("massegeToSent")["patient"].values(),getData("massegeToSent")["order"].values()]
functions.sendPakege(Userdata)
