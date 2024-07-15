
import sys
import os
import pathlib
import cv2
import datetime
import sqlite3
#from datetime import datetime


## ---  ตรวจสอบ File ui  In Folder /ui
def CheckFile_FolderUi(MyFileUi):
    # ------- CheckFile_FolderUi("ชื่อไฟล์.ui")
    #--------  ถ้ามีไฟล์ return True ----------
    folder_path = "ui"
    file_name = MyFileUi     #### Ex. "cam.ui"
    if os.path.isdir(folder_path):
          file_path = os.path.join(folder_path, file_name)
          if os.path.isfile(file_path):
            return True
          else:
            return False
    else:
        return False

#-----------------------------------------------------
# --- ตรวจสอบการพร้อมใช้ของกล้องที่พ่วงกับคอมพิวเตอร์  -----------
def check_cameras(max_cameras=1):
    ## ------ สามารถตรวจสอบเครื่อง ได้หลายเครื่อง
    ## ------ ถ้าให้ตรวจหลายเครื่อง ให้ เอาค่า return ออก เพื่อให้ พิมพ์ค่าออกมา
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            #print(f"Camera {i} is available.")
            return  True
            cap.release()

        else:
            return  False
            #print(f"Camera {i} is not available.")

#-----------------------------------------------------
#--- การตัดคำ  คำนำหน้าชื่อ ชือ และนามสกุล เพื่อบันทึกลงฐานข้อมูล
def Cut_name_smartcard(nameSmartcard):
    line_space1 = nameSmartcard.find(" ")
    line_space2 = nameSmartcard.find("  ")
    line_end = len(nameSmartcard)
    sername = nameSmartcard[0:line_space1]
    fname = nameSmartcard[line_space1 + 1:line_space2]
    lname = nameSmartcard[line_space2 + 2:line_end]
    return sername,fname,lname

#-----------------------------------------------------
#--- การตัดคำ  ที่อยู่ หมู่ ตำบล อำเภอ และ จังหวัด
def Cut_Address_smartcard(addressSmartcard):
    ## ----  ค่าที่ได้มา = "142 หมู่ที่ 3    ตำบลมะต้อง อำเภอพรหมพิราม จังหวัดพิษณุโลก"
    line_Mu = addressSmartcard.find("หมู่ที่")
    line_tombon = addressSmartcard.find("ตำบล")
    line_amphur = addressSmartcard.find("อำเภอ")
    line_changwat = addressSmartcard.find("จังหวัด")
    Line_total = len(addressSmartcard)

    ban = addressSmartcard[0:line_Mu]
    ban = ban.replace("#", " ")
    #print(ban)
    mu = addressSmartcard[line_Mu + 8:line_tombon]
    mu = mu.replace("#", "")
    #print(mu)
    tumbon = addressSmartcard[line_tombon + 4:line_amphur]
    tumbon = tumbon.replace("#", "")
    #print(tumbon)
    amphur = addressSmartcard[line_amphur + 5:line_changwat]
    amphur = amphur.replace("#", "")
    #print(amphur)
    changwat = addressSmartcard[line_changwat + 7:Line_total]
    changwat = changwat.replace("#", "")
    #print(changwat)
    return  ban,mu,tumbon,amphur,changwat

#----------------------------------------------------------------
#---  กำหนด ปี พ.ศ. ใน ComBoBOx -- ให้เลือก
#---
def Lookup_Year():
    today = datetime.date.today()
    year = today.year
    thaiyear = today.year +543
    lookYear=[]
    for i in range(1, 110):
        lookYear.append(str(thaiyear))
        thaiyear-=1
    return lookYear

#----------------------------------------------------------------
#---  กำหนด อายุ ใน ComBoBOx -- ให้เลือก  ตั้งแต่ 0 - 120 ปี
#---
def Lookup_Age():
    lookAge=[]
    TStart = 0
    for i in range(0, 120):
        lookAge.append(str(TStart))
        TStart+=1
    return lookAge
#----------------------------------------------------------------
#---  ตรวจสอบ วันเดือนปีเงิน จากข้อมูลที่อ่านบัตร SmartCard
#---
def Check_BirthDay_Smartcard(birthdate):
    if len(birthdate)==8:
        BirthYrar  = birthdate[0:4]
        BirthMonth = birthdate[4:6]
        BirthDay   = birthdate[6:8]
        #print("Read Smartcard")
    else:
        #print("No Read Smartcard")
        BirthYrar = birthdate[0:4]
        index_BirthYrar = len(BirthYrar)
        if index_BirthYrar == 4:
            BirthYrar  = birthdate[0:4]
            BirthMonth = "00"
            BirthDay   = "00"
        else:
            BirthYrar = '0000'
            BirthMonth = '00'
            BirthDay = '00'
    Month =['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฏาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
    BMonth = Month[int(BirthMonth)-1]
    return BirthYrar,BMonth,str(int(BirthDay))

def Check_BirthDay_Search(birthdate):
    if len(birthdate)<8:
        BirthYrar  = "2567"
        BirthMonth = "01"
        BirthDay   = "01"
    else:
        BirthYrar = str(int(birthdate[0:4])+543)
        BirthMonth = int(birthdate[5:7])
        BirthDay = str(int(birthdate[8:10]))
    Month =['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฏาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
    BMonth = Month[int(BirthMonth)-1]
    return BirthYrar,BMonth,BirthDay


##---- การแปลงเดือนภาษาไทย ให้ เป็น เดือน  Eng  ---------
# def ReturnThaiMonthToEng(month):
#     xMonth = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฏาคม', 'สิงหาคม', 'กันยายน',
#              'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
#     matched_indexes = []
#     i = 0
#     length = len(xMonth)
#     while i < length:
#         if month == xMonth[i]:
#             matched_indexes.append(i)
#         i += 1
#     EngMonth = matched_indexes[0]+1
#     return EngMonth



#----------------------------------------------------------------
#----------------------------------------------------------------
#----------------------------------------------------------------
##-------------------------------------------------------
## Connection Database
##-------------------------------------------------------
def MyconnectSqlite():
    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
    sqliteConnection = sqlite3.connect(DataPath)
    Mycursor = sqliteConnection.cursor()
    return Mycursor

##-------------------------------------------------------
## Connection Database Select Province
def list_ProvinceName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = MyconnectSqlite()
    query = "select DISTINCT CHANGWAT_NAME FROM l_catm ORDER BY CHANGWAT_NAME"
    Mycursor.execute(query)
    Result.append("== เลือกจังหวัด ==")
    results = Mycursor.fetchall()
    Mycursor.connection.close()
    for row in results:
        Result.append(f"{row[0]}")
        ##----   ค่าที่แสดงผล =  พิษณุโลก
    return Result

#-- ค้นหารหัสจังหวัด จากชื่อจังหวัด ---
def Search_CodeChangwat(changwat):
    Mycursor = MyconnectSqlite()
    query = "select DISTINCT substr(CATM,1,2)||'00' as Code,CHANGWAT_NAME FROM l_catm WHERE CHANGWAT_NAME = '"+changwat+"'"
    Mycursor.execute(query)
    results = Mycursor.fetchone()
    result = results[0]
    Mycursor.connection.close()
    return result




def list_AmpurName(changwat):
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = MyconnectSqlite()
    query = "select DISTINCT AMPHUR_NAME FROM l_catm WHERE CHANGWAT_NAME = '"+changwat+"' ORDER BY SUBSTR(CATM,1,4)"
    Mycursor.execute(query)
    Result.append("== เลือกอำเภอ ==")
    results = Mycursor.fetchall()
    Mycursor.connection.close()
    for row in results:
        Result.append(f"{row[0]}")
        ##----   ค่าที่แสดงผล = ชื่อ อำเภอ ภายในจังหวัด นั้น ๆ
    return Result

def list_TumbonName(changwat,amphur):
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = MyconnectSqlite()
    query = "select DISTINCT TUMBON_NAME FROM l_catm WHERE CHANGWAT_NAME = '"+changwat+"' AND AMPHUR_NAME = '"+amphur+"' ORDER BY SUBSTR(CATM,1,6)"
    Mycursor.execute(query)
    Result.append("== เลือกตำบล ==")
    results = Mycursor.fetchall()
    Mycursor.connection.close()
    for row in results:
        Result.append(f"{row[0]}")
        ##----   ค่าที่แสดงผล = ชื่อ ตำบล  ภายใน อำเภอ และ จังหวัด นั้น ๆ
    return Result

#---------------------------------------------------------
#---  แปลง ปี เดือน วัน ให้ อยู่ในรูปแบบ Date เพื่อบันทึกเข้า dataBase ------------------------

# def ThaiDateTOEng(thaiyear,month,day):
#     xEngYear = str(int(thaiyear) - 543)
#     # Define the string containing the date  Ex date_string = "2024-06-23"
#     str_EngDate = xEngYear+"-"+month+"-"+day
#     # Convert the string to a datetime object
#     date_eng = datetime.strptime(str_EngDate, "%Y-%m-%d")
#     return date_eng


##-------------------------------------------
## ค้นหา Texe เพื่อดูสถานะว่า มีการ Login หรือไม่ --------
def Search_Text(text,Searchtext):
    Xtext = text
    XSearchtext = Searchtext
    result = Xtext.find(XSearchtext)
    ## --- ถ้าไม่พบข้อความจะ ให้ค่า เท่ากับ -1  = ส่งค่อออกไป เป็น False
    if result == -1:
        resultSearch = False
    else:
        resultSearch = True
    return resultSearch
#-----------ตรวจสอบการ Login ของ ระบบ โดยผล Type ของ User ------------------
def Check_Login(text):
    Xtext = text
    XSearchtext1 = "Admin"
    XSearchtext2 = "User"
    result1 = Xtext.find(XSearchtext1)
    result2 = Xtext.find(XSearchtext2)
    ## --- ถ้าไม่พบข้อความจะ ให้ค่า เท่ากับ -1  = ส่งค่อออกไป เป็น False
    if (result1 == -1) and (result2 == -1):
        resultSearch = False
    else:
        resultSearch = True
    return resultSearch




# xxxx = Search_CodeChangwat("พิษณุโลก")
# print(xxxx)
