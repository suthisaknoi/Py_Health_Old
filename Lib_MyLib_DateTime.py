

from datetime import datetime
#---- การแปลงเดือนภาษาไทย ให้ เป็น เดือน  Eng  ---------
def ReturnThaiMonthToEng(month):
    xMonth = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฏาคม', 'สิงหาคม', 'กันยายน',
             'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
    matched_indexes = []
    i = 0
    length = len(xMonth)
    while i < length:
        if month == xMonth[i]:
            matched_indexes.append(i)
        i += 1
    EngMonth = matched_indexes[0]+1
    return str(EngMonth)


#---------------------------------------------------------
#---  แปลง ปี เดือน วัน ให้ อยู่ในรูปแบบ Date เพื่อบันทึกเข้า dataBase ------------------------

def ThaiDateTOEng(thaiyear,month,day):
    xEngYear = str(int(thaiyear) - 543)
    # Define the string containing the date  Ex date_string = "2024-06-23"
    str_EngDate = xEngYear+"-"+month+"-"+day
    # Convert the string to a datetime object
    date_eng = datetime.strptime(str_EngDate, "%Y-%m-%d")
    return date_eng

def Date_register():
    current_dateTime = datetime.now()
    return current_dateTime



# a= Date_register()
# print(a)

# a= ThaiDateTOEng("2567","2","10")
# print(a)
# # # print(BirthMonth)
# # print(BirthDay)


# ###------ รูปแบบ การแสดง อื่น ๆ ------
# now = datetime.datetime.now()
# datetime.time(now.hour, now.minute, now.second)
# now.day
# ืnow.month
# now.year