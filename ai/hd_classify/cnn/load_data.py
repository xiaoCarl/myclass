import numpy as np
import psycopg2
import random
MAX_FEATURE = 23

def load_sas_data():
    conn = psycopg2.connect(database="diskdb", user="diskdata",password="qwe123",
                     host="10.42.5.193", port="5432") 
    cursor=conn.cursor()

    cursor.execute('select \
            "CAPACITY","RORATION","MEDIUM_TYPE","SAS_TEMP", \
            "SAS_START_COUNT","SAS_GLIST", "SAS_TOTAL_READ", "SAS_READ_ERR",\
            "SAS_TOTAL_WRITE", "SAS_WRITE_ERR", "SAS_TOTAL_VERIFY", "SAS_VERIFY_ERR",\
            "RRQMPS", "WRQMPS", "RPS", "WPS", "RKBPS", "WKBPS", "AVGRQ_SZ", "AVGQU_SZ",\
            "AWAIT",  "SVCTM", "UTIL" \
            from disk_data_table where "INTERFACE_TYPE"=0 and "SAS_TEMP">0' )
    
    saslist=cursor.fetchall()
    
    return_data  = np.zeros((len(saslist),MAX_FEATURE))
    return_lable = []
    
    index = 0
    for sas_data in saslist:
        return_data[index,:] =  sas_data
        return_lable.append( random.randint(0,5)) 
        index +=1

    return_data = np.nan_to_num(return_data)
    return return_data,np.array(return_lable)


if __name__ == '__main__':
    sas,lable=load_sas_data()

    for i in sas:
        print(i)
    print(lable,len(lable))
