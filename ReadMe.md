to start, run main.py file

writen by Mattanya Frank in 2022
for more details mattanyafrank@gmail.com


project settings are cotrold by a json file called :
"settings.json"
 the file looks like this:
{
  "address": "127.0.0.1", //Ip address
  "port": 5000,
  "ErrorLogFile":"Log.csv",
  "file_path": "DataImport",   // the path of the answers data directory
  "massegeToSent":{
    "patient":{
      "PID": "", "APID":"", "NAME":"","MN":"","BD":"","SEX":"","DCODE":"","HT":"","WT":"","ADMS":"","LC":"","DTR": ""
    }, // patient parameters for the request
    "order":{
      "ONO": "","RQDT":"","TESTID": "","PRI": "", "CLDT": "" ,"CVLM": "", "ACCD": "","RCINF": "","RCDT": "","SRC": "","DTR": "", "PSID":""
    }    // order parameters for the request
  } // request parameters
}
