import base64
import ping3
#-------------------
import mysql.connector          ## Mydel-connect-python
from configparser import ConfigParser   # config ini File
import pathlib
# Database -------------------
import sqlite3


# load path

def Encoding(MyText):
    sample_string = MyText
    sample_string_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    # print(f"Encoded string: {base64_string}")
    return base64_string

def Decoding(MyTextEncodeind):
    base64_string = MyTextEncodeind
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    Decoding_string = sample_string_bytes.decode("ascii")
    # print(f"Decoded string: {Decoding_string}")
    return Decoding_string


##-----Sample ----------
# x=Encoding("3wr56rer060rt0wrq2rq99rqer1wer97")
# print(x)
# y=Decoding(x)
# print(y)

##-------- ตรวจสอบ IP ของ Server -------------
def ping_ip(ip):
    try:
        response_time = ping3.ping(ip)
        if response_time is None or response_time == False:
            #print(f"Request timed out for {ip}")
            sentmessage = f"Request timed out for {ip}"
            return False,sentmessage
        else:
            sentmessage = f"Ping to {ip} successful, response time: {response_time} seconds"
            #print(f"Ping to {ip} successful, response time: {response_time} seconds")
            return True,sentmessage
    except ping3.errors.PingError as e:
        sentmessage = f"Failed to ping {ip}: {e}"
        #print(f"Failed to ping {ip}: {e}")
        return False,sentmessage

# Example usage
# ip_address = "127.0.0.1"  # Google's public DNS server 61.19.112.123
# x = ping_ip(ip_address)
# if x == True:
#     print("successful")
# else:
#     print("NO successful")

#-----------------------------------------------------
#---   ทดสอบการเชื่อมต่อฐานข้อมูล Mysql --------------------
def testconnect_to_mysql(host, user, password, database,myport):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=myport
        )
        if connection.is_connected():
            sentmessage = 'Connection to MySQL database was successful'
            #print("Connection to MySQL database was successful")
            connection.close()
            return True, sentmessage
        else:
            sentmessage = 'Failed to connect to the database'
            #print("Failed to connect to the database")
            return False, sentmessage
    except mysql.connector.Error as e:
        #print(f"Error: {e}")
        sentmessage = f"Error: {e}"
        return False, sentmessage


# Example usage
# host = "61.19.112.123"
# user = "sa"
# password = "ssa"
# database = "lotto"
# myport = '3306'
#
# result,sentmessage = testconnect_to_mysql(host, user, password, database,myport)
# if result == True:
#     print("Is Connect")
#     print(sentmessage)
# else:
#     print("Is not Connect")
#     print(sentmessage)


def Load_Hospital():
    config_object = ConfigParser()
    config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
    config_object.read(config_file)
    # HOSPITAL
    hospitalInfo = config_object["HOSPITAL"]
    # Set Values
    hcode = hospitalInfo["hcode"]
    hname = hospitalInfo["hcode_name"]
    hprovince_Id = hospitalInfo["province_id"]
    hprovince_Name = hospitalInfo["province_name"]
    return hcode,hname,hprovince_Id,hprovince_Name




def GetData_mysql():
    config_object = ConfigParser()
    config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
    config_object.read(config_file)
    # HOSPITAL
    hospitalInfo = config_object["SERVERCONFIG"]
    # Set Values
    host_ip = Decoding(hospitalInfo["host_ip"])
    user_host = Decoding(hospitalInfo["user_host"])
    pass_host = Decoding(hospitalInfo["pass_host"])
    port_host = Decoding(hospitalInfo["port_host"])
    database_name = Decoding(hospitalInfo["database_name"])

    cnx = mysql.connector.connect(user=user_host,
                                  password=pass_host,
                                  host=host_ip,
                                  database=database_name,
                                  port=port_host)
    try:
        cursor = cnx.cursor()
        cursor.execute("""
                        select pcucodeperson
                         ,pid
                         ,idcard 
                         , mobile
                         ,telephoneperson
                        ,case
                           when mobile is not null then substr(replace(mobile,'-',''),1,10) 
                             else substr(replace(telephoneperson,'-',''),1,10) 
                        end as telephone
                        from person    
                     """)
        result = cursor.fetchall()
        # print("YYYYYYYYYYYYYYYYYYYYYYYYY")
        if result:
            return result
        else:
            return None
    finally:
        cnx.close()
    return None

##----------------- search idcard person_telephone---------------
def Search_idcard(idcard):

    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
    sqliteConnection = sqlite3.connect(DataPath)
    Mycursor = sqliteConnection.cursor()
    # --- Delete Sqlite ------
    Dquery = "select *  FROM person_telephone WHERE idcard = '" + idcard + "'"
    Mycursor.execute(Dquery)
    Rec_user = Mycursor.fetchone()
    if Rec_user==None:
        Mquery = "select MAX(pid)+1 from person_telephone"
        Mycursor.execute(Mquery)
        XRec_user = Mycursor.fetchone()
        Rectype = "NEW"
        pid = XRec_user[0]
        tel = None
    else:
        Rectype = None
        pid = Rec_user[1]
        tel = Rec_user[5]
    return Rectype,pid,tel



# pid,tel = Search_idcard('3200100099141')
# print(tel)
# print(pid)


