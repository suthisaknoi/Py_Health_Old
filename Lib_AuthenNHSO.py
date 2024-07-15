
import requests
import pathlib
import json
# Database -------------------
import sqlite3

#---------- ตรวจสอบเครื่องอ่าน Smart card  -----------------------
#  Name API   /api/smartcard/terminals
#   terminal_name,is_present = get_smartcard()
#   is_present = ตรวจสอบว่าเครื่อง่อานบัตรมีบัตรเสียบอยู่หรือไม่
#   ค่าที่ส่งมา   รูน ยี่ห้อ เครื่องอ่าน และ ความพร้อมในการอ่านบัตร (มีบัตรเสียบคาเครื่องอ่าน)
#
def get_smartcard():
    url = 'http://localhost:8189/api/smartcard/terminals'
    terminal_name = None
    is_present = False
    sentMessage = None
    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            for item in posts:
                terminal_name = item['terminalName']
                is_present = item['isPresent']
            if terminal_name == None:
                sentMessage = "SmartCard Not Connect."
            else:
                sentMessage = "SmartCard is Connect."
            return terminal_name,is_present,sentMessage
        else:
            sentMessage = f'Error: {response.status_code}'
            print('Error:', response.status_code)
            return terminal_name,is_present,sentMessage
    except requests.exceptions.RequestException as e:
        sentMessage = f'Error: {e}'
        print('Error:', e)
        return terminal_name,is_present,sentMessage
 ##-- ตัวอย่างการเรียกใช้งาน ---------
# terminal_name,is_present,sentMessage = get_smartcard()
# print(terminal_name)
# print(is_present)
# print(sentMessage)





#---------- อ่านบัตร Smart card ไม่มีรูปในบัตร -----------------------
# Name API /api/smartcard/read-card-only
# คำสังการใช้งาน
# pid,titleName,fname,lname,birthDate,sex = read_smartcardNoPic()
# ค่าที่ได้ออกมา เป็น รายการตามลำดับ  สามารถเอาตัวแปรไปทำงานต่อไป
def read_smartcardOnlyNoPic():
    url = 'http://localhost:8189/api/smartcard/read-card-only?readImageFlag=false'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            pid = posts['pid']
            titleName = posts['titleName']
            fname = posts['fname']
            lname = posts['lname']
            birthDate = posts['birthDate']
            sex = posts['sex']
            return pid,titleName,fname,lname,birthDate,sex
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None



#---------- ตรวจสอบ การ Authen ครั้งสุดท้าย -----------------------
# Name API /api/nhso-service/latest-authen-code/{pid}
# คำสังการใช้งาน
# pid,titleName,fname,lname,birthDate,sex = read_smartcardNoPic()
# ค่าที่ได้ออกมา เป็น รายการตามลำดับ  สามารถเอาตัวแปรไปทำงานต่อไป
def last_authencode():
    url = 'http://localhost:8189/api/smartcard/read-card-only?readImageFlag=false'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            pid = posts['pid']
            titleName = posts['titleName']
            fname = posts['fname']
            lname = posts['lname']
            birthDate = posts['birthDate']
            sex = posts['sex']
            return pid,titleName,fname,lname,birthDate,sex
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


#---------- ตรวจสอบ ชุดเลข token ของ Authen  -----------------------
# Name API /api/preference
# คำสังการใช้งาน
# defaultTerminal, token = show_token()
# ค่าที่ได้ออกมา เป็น รุ่นเครื่องอ่าน  และ ชุดตัวเลข Token ของหน่วยบริการ
def show_token():
    url = 'http://localhost:8189/api/preference'
    token = "None"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            # print(posts)
            # defaultTerminal = posts['defaultTerminal']
            token = posts['token']
            sentmessage = "พบ Token"
            return token,sentmessage
        else:
            sentmessage = f"ไม่พบ Token Error : {response.status_code}"
            print('Error:', response.status_code)
            return token,sentmessage
    except requests.exceptions.RequestException as e:
        sentmessage = f"ไม่พบ Token Error : {e}"
        print('Error:', e)
        return token,sentmessage
# --  ตัวอย่างการใช้งาน  -------------------------------
# token,sentmessage = show_token()
# print(token)
# print(sentmessage)


#---------- ตรวจสอบ การ Authen ของผู้มารับบริการ  -----------------------
# Name API /api/nhso-service/latest-authen-code/{pid}
# คำสังการใช้งาน
# claimType,claimCode,hcode,claimDateTime,checkDate = check_authen('8671184020680')
# ค่าที่ได้ออกมา เป็น claimtype claimcode hcode ของหน่วยบริการ
def check_authen(cid):
    url = 'http://localhost:8189/api/nhso-service/latest-authen-code/'+cid
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            claimType     = posts['claimType']
            claimCode     = posts['claimCode']
            hcode         = posts['hcode']
            claimDateTime = posts['claimDateTime']
            checkDate     = posts['checkDate']

            return claimType,claimCode,hcode,claimDateTime,checkDate
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


#---------- แสดง การ Authen 5 ครั้งสุดท้าย ของผู้มารับบริการ  -----------------------
# Name API /api/nhso-service/latest-5-authen-code-all-hospital/{pid}
# คำสังการใช้งาน
# data = check_authen5Time('8671184020680')
# ค่าที่ได้ออกมา เป็น claimtype claimcode hcode ของหน่วยบริการ
# print(data)
# print(data[0][0])
# print(data[0][1])
# print(data[0][2])
# print(data[0][3])
# print(data[0][4])

def check_authen5Time(cid):
    url = 'http://localhost:8189/api/nhso-service/latest-5-authen-code-all-hospital/'+cid
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            data1=[]
            data2=[]
            for item in posts:
                data1.clear()
                claimType     = item['claimType']
                claimCode     = item['claimCode']
                hcode         = item['hcode']
                claimDateTime = item['claimDateTime']
                checkDate     = item['checkDate']
                data1.append(claimType)
                data1.append(claimCode)
                data1.append(hcode)
                data1.append(claimDateTime)
                data1.append(checkDate)
                data2.append(data1)
            return data2
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


## -------------- read smartcard Online and Check Right --------------------------
# Name API  /api/smartcard/read
# คำสังการใช้งาน
#  pid,fname,lname,nation,birthDate,sex,mainInscl,subInscl,age,claimTypes,image,correlationId = read_smartcardOnline()
#  การแสดงผล ของการรันโปรแกรม ----------------
#  print(pid)
#  print(fname)
#  print(lname)
#  print(claimTypes[0]['claimType'])
#  print(correlationId)
def read_smartcardOnline():
    url = 'http://localhost:8189/api/smartcard/read?readImageFlag=true'
    hospSub = None
    hospMainOp = None
    hospMain = None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
            ###----- ปรับปรุงใหม่ return เป็น Json ออกไปเลย ------------
            # pid        = posts['pid']
            # fname      = posts['fname']
            # lname      = posts['lname']
            # nation     = posts['nation']
            # birthDate  = posts['birthDate']
            # sex        = posts['sex']
            # mainInscl  = posts['mainInscl']
            # subInscl   = posts['subInscl']
            # age        = posts['age']
            # claimTypes = posts['claimTypes']
            # image      = posts['image']
            # correlationId = posts['correlationId']
            # # if (mainInscl[1:4] == "UCS") or (mainInscl[1:4] == "WEL"):
            # #     print(mainInscl[1:4])
            # #     hospSub    = posts['hospSub']
            # #     hospMainOp = posts['hospMainOp']
            # #     hospMain   = posts['hospMain']
            # #     return pid,fname,lname,nation,birthDate,sex,mainInscl,subInscl,age,claimTypes,image,correlationId,hospSub,hospMainOp,hospMain
            # # else:
            # #     return pid, fname, lname, nation, birthDate, sex, mainInscl, subInscl, age, claimTypes, image, correlationId
            return posts

        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

#------- การสร้าง Json data ------------
#  ตัวแปรที่รรับขึ้นมา -----
#  pid = "3650600299197"
#  claimType = "PG0120001"
#  mobile ="0901975166"
#  correlationId = "1961eaf8-0c7f-4cdb-b3e4-e831e45694dc"
#  hn = "99"
#  hcode =  "11272"
#  รูปแบบการรัน   ------
#  pid,claimType,correlationId,createdDate,claimCode = post_authen(pid, claimType, mobile, correlationId, hn, hcode)

def post_authen(pid,claimType,mobile,correlationId,hn,hcode):
    token = show_token()
    url = 'http://localhost:8189/api/nhso-service/confirm-save'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer '+token
    }
    print(headers)
    # payload = {
    #     "pid": "3650600299197",
    #     "claimType": "PG0130001",
    #     "mobile": "0901975166",
    #     "correlationId": "7a2664d7-a68f-4b97-b72a-8e45afdbdcb0",
    #     "hn": "99",
    #     "hcode": "11272"
    #          }
    payload = {
        "pid": pid,
        "claimType": claimType,
        "mobile": mobile,
        "correlationId": correlationId,
        "hn": hn,
        "hcode": hcode
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print('Request was successful.')
            response_data = response.json()
            pid = response_data.get('pid')
            claimType = response_data.get('claimType')
            correlationId = response_data.get('correlationId')
            createdDate = response_data.get('createdDate')
            claimCode = response_data.get('claimCode')
             #print(f'pid: {pid}, claimType: {claimType}, correlationId: {correlationId}, createdDate: {createdDate}, claimCode: {claimCode}')
            return pid,claimType,correlationId,createdDate,claimCode
        elif response.status_code == 400:
            print('Bad Request:', response.json())
        elif response.status_code == 404:
            print('The requested resource could not be found.')
            return None
        else:
            print('Error:', response.status_code, response.text)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


def post_authen_New(pid, claimType, mobile, correlationId, hn, hcode):
    token = show_token()
    # print(token[0])  # เลือกค่าท่ี่ส่งมาค่าแรก เป็น Token
    # print(pid)
    # print(claimType)
    # print(mobile)
    # print(correlationId)
    # print(hn)
    # print(hcode)
    url = 'http://localhost:8189/api/nhso-service/confirm-save'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer '+token[0]
    }
    payload = {
        "pid": pid,
        "claimType": claimType,
        "mobile": mobile,
        "correlationId": correlationId,
        "hn": hn,
        "hcode": hcode
    }
    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            #print('Request was successful.')
            sentmessage = "Request was successful."
            response_data = response.json()
            #print(f'pid: {pid}, claimType: {claimType}, correlationId: {correlationId}, createdDate: {createdDate}, claimCode: {claimCode}')
            return response_data,sentmessage
        elif response.status_code == 400:
            #print('Bad Request:', response.json())
            sentmessage = f'Bad Request: {response.json()}'
            response_data = None
            return response_data, sentmessage
        elif response.status_code == 404:
            #print('The requested resource could not be found.')
            sentmessage = f'{response.status_code} The requested resource could not be found.'
            response_data = None
            return response_data, sentmessage
        else:
            #print('Error:', response.status_code, response.text)
            sentmessage = f'{response.status_code} The requested resource could not be found.'
            response_data = None
            return response_data, sentmessage
    except requests.exceptions.RequestException as e:
        #print('Error:', e)
        sentmessage = f'Error : {e} '
        response_data = None
        return response_data, sentmessage




# pid = "3650600299197"
# claimType = "PG0130001"
# mobile ="0901975166"
# correlationId = "7a2664d7-a68f-4b97-b72a-8e45afdbdcb0"
# hn = "99999"
# hcode =  "11272"
# #
# json_data = create_json(pid, claimType, mobile, correlationId, hn, hcode)
# #
#
# #
# #
# print(json_data)
# token = show_token()
# print(token)
# # print(claimCode)
#
# pid,claimType,correlationId,createdDate,claimCode = post_authen()



# token,sentmessage = show_token()
# print(token)
# print(sentmessage)
# # print(sentMessage)



#------ เป็นการหารหัส ของ Claimcode ที่อยู่มน combobox--------
#------ เพื่อ ส่งค้นการในการ Authen ------------------------
def look_claimType(claimType):
    #claimType = '[PG0060001]:เข้ารับบริการรักษาทั่วไป (OPD/ IPD/ PP)'   คำตอบ PG0060001
    line_space1 = claimType.find("[")
    line_space2 = claimType.find("]")
    result = claimType[line_space1+1:line_space2]
    return result



#---------- การค้นหาวันที่รับบริการ เพื่อใส่ใน combobox ---------
#
#
#----------------------------------------------------
def look_servicedate():
    Result = []
    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
    sqliteConnection = sqlite3.connect(DataPath)
    cursor = sqliteConnection.cursor()
    query ='''    
           select DISTINCT strftime('%d', date(date_authen))||'-'||strftime('%m', date(date_authen))||'-'||cast(cast(strftime('%Y', date(date_authen)) AS INTEGER)+543 as text) as dateservice
        ,strftime('%d', date(date_authen))||'-'||strftime('%m', date(date_authen))||'-'||cast(cast(strftime('%Y', date(date_authen)) AS INTEGER)+543 as text) as dateservice2
        from person_authen 
            ORDER BY date(date_authen) DESC    
    
            '''
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}")
    return Result


# x= look_servicedate()
# print(x)


