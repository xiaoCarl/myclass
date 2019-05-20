import json
import os

"""
input_data=[ 
                {
                 SERIAL:serial,
                 INTERFACE_TYPE: sas/sata,
                 data:[.....]},
                {},...]
"""
def get_hd_data(file):
    f = open(file)
    hdds_data =  json.load(f)                      
    
    input_data = []
    disknum=0

    for diskno in hdds_data['DISK_INFO']:
        input_data.append({}) 

        hd_data = diskno
        input_data[disknum]["SERIAL"] = hd_data["SERIAL"]
        input_data[disknum]["INTERFACE_TYPE"] = hd_data["INTERFACE_TYPE"]
        input_data[disknum]["data"]=[] 
          
        if hd_data["INTERFACE_TYPE"] == "SAS":
            for key in sas_info() : 
                if hd_data.get(key,0) == "*":        # if key.value='*', set this key.value=0
                    input_data[disknum]["data"].append(0)
                else:
                    input_data[disknum]["data"].append(hd_data.get(key,0))
        elif hd_data["INTERFACE_TYPE"] == "SATA":
            for key in sata_info() : 
                if hd_data.get(key,0) == "*":
                    input_data[disknum]["data"].append(0)
                else:
                    input_data[disknum]["data"].append(hd_data.get(key,0))
        else:
            print("Error interface type.")
        
        input_data[disknum]["data"] = list(map(lambda x : float(x) , input_data[disknum]["data"]))  #
        disknum +=1

    return input_data


def sas_info():
    return ["CAPACITY","RORATION","VENDOR","MEDIUM_TYPE","SAS_LIFE_TIME","SAS_TEMP",    \
            "SAS_START_COUNT","SAS_GLIST", "SAS_TOTAL_READ", "SAS_READ_ERR",            \
            "SAS_TOTAL_WRITE", "SAS_WRITE_ERR", "SAS_TOTAL_VERIFY", "SAS_VERIFY_ERR",   \
            "RRQMPS", "WRQMPS", "RPS", "WPS", "RKBPS", "WKBPS", "AVGRQ_SZ", "AVGQU_SZ", \
            "AWAIT",  "SVCTM", "UTIL"]

def sata_info():
    return ["SATA_ATTR1_VALUE","SATA_ATTR1_RAW","SATA_ATTR3_VALUE","SATA_ATTR3_RAW",
            "SATA_ATTR4_VALUE","SATA_ATTR4_RAW","SATA_ATTR5_VALUE","SATA_ATTR5_RAW",
            "SATA_ATTR7_VALUE","SATA_ATTR7_RAW","SATA_ATTR9_VALUE","SATA_ATTR9_RAW",
            "SATA_ATTR10_VALUE","SATA_ATTR10_RAW","SATA_ATTR12_VALUE","SATA_ATTR12_RAW",
            "SATA_ATTR187_VALUE","SATA_ATTR187_RAW","SATA_ATTR188_VALUE","SATA_ATTR188_RAW",
            "SATA_ATTR189_VALUE","SATA_ATTR189_RAW","SATA_ATTR190_VALUE","SATA_ATTR190_RAW",
            "SATA_ATTR194_VALUE","SATA_ATTR194_RAW","SATA_ATTR195_VALUE","SATA_ATTR195_RAW",
            "SATA_ATTR196_VALUE","SATA_ATTR196_RAW","SATA_ATTR197_VALUE","SATA_ATTR197_RAW",
            "SATA_ATTR198_VALUE","SATA_ATTR198_RAW","SATA_ATTR240_VALUE","SATA_ATTR240_RAW",
            "RRQMPS", "WRQMPS", "RPS", "WPS", "RKBPS", "WKBPS", "AVGRQ_SZ", "AVGQU_SZ",
            "AWAIT",  "SVCTM", "UTIL"]


def get_all_data(filepath):
    sasdatalist,satadatalist = [],[]
    files = os.listdir(filepath)
    for f in files:
        jsonfile= os.path.join(filepath,f)
        all_data = get_hd_data(jsonfile)
        for hd_data in all_data:
            if hd_data["INTERFACE_TYPE"] == "SAS":
                sasdatalist.append(hd_data["data"])
            elif hd_data["INTERFACE_TYPE"] == "SATA":
                satadatalist.append(hd_data["data"])
    return sasdatalist,satadatalist


if __name__ == '__main__':

#    data = get_hd_data("disk_info.json")
    sasdatalist,satadatalist = get_all_data("data")

    print("....................SAS HD INFO..............")
    for hd_data in sasdatalist:
         print(hd_data)
    print("....................SATA HD INFO..............")
    for hd_data in satadatalist:
         print(hd_data)


"""
{"DATE":"2019-05-06/05:21:54","SERIAL":"ZA1522WE0000R711VQZQ","CAPACITY":"15628053168",
"VENDOR":"SEAGATE","MODEL":"ST8000NM0075","FW":"E002","RORATION":"0x1c20","INTERFACE_TYPE":"SAS",
"MEDIUM_TYPE":"HDD","HEALTH":"*","SAS_LIFE_TIME":"*","SAS_TEMP":"37","SAS_START_COUNT":"76",
"SAS_GLIST":"0","SAS_TOTAL_READ":"117.957","SAS_READ_ERR":"0","SAS_TOTAL_WRITE":"24.858",
"SAS_WRITE_ERR":"0","SAS_TOTAL_VERIFY":"*","SAS_VERIFY_ERR":"*",

"SATA_ATTR1_VALUE":"*","SATA_ATTR1_RAW":"*","SATA_ATTR3_VALUE":"*","SATA_ATTR3_RAW":"*",
"SATA_ATTR4_VALUE":"*","SATA_ATTR4_RAW":"*","SATA_ATTR5_VALUE":"*","SATA_ATTR5_RAW":"*",
"SATA_ATTR7_VALUE":"*","SATA_ATTR7_RAW":"*","SATA_ATTR9_VALUE":"*","SATA_ATTR9_RAW":"*",
"SATA_ATTR10_VALUE":"*","SATA_ATTR10_RAW":"*","SATA_ATTR12_VALUE":"*","SATA_ATTR12_RAW":"*",
"SATA_ATTR187_VALUE":"*","SATA_ATTR187_RAW":"*","SATA_ATTR188_VALUE":"*","SATA_ATTR188_RAW":"*",
"SATA_ATTR189_VALUE":"*","SATA_ATTR189_RAW":"*","SATA_ATTR190_VALUE":"*","SATA_ATTR190_RAW":"*",
"SATA_ATTR194_VALUE":"*","SATA_ATTR194_RAW":"*","SATA_ATTR195_VALUE":"*","SATA_ATTR195_RAW":"*",
"SATA_ATTR196_VALUE":"*","SATA_ATTR196_RAW":"*","SATA_ATTR197_VALUE":"*","SATA_ATTR197_RAW":"*",
"SATA_ATTR198_VALUE":"*","SATA_ATTR198_RAW":"*","SATA_ATTR240_VALUE":"*","SATA_ATTR240_RAW":"*",

"RRQMPS":"0.00","WRQMPS":"0.00","RPS":"911.00","WPS":"24576.00","RKBPS":"116608.00","WKBPS":"98304.00",
"AVGRQ_SZ":"16.86","AVGQU_SZ":"1724.45","AWAIT":"70.53","SVCTM":"0.04","UTIL":"99.50"}

"""