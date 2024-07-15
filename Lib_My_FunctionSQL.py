
##--------------------------------------------------------
###  My Lib
##   Created : suthisak
##---------------------------------------------------------

import pathlib
import sqlite3


def Print_Code(mytext):
    #--   รูปแบบค่าที่รับมา = "จังหวัดพิษณุโลก[65]"
    #--   ค่าที่ได้ = 65
    line_start = mytext.find("[") +1
    line_end   = mytext.find("]")
    XCode = mytext[line_start:line_end]
    return str(XCode)
#
def Print_Text(mytext):
    # --   รูปแบบค่าที่รับมา = "จังหวัดพิษณุโลก[65]"
    # --   ค่าที่ได้ = จังหวัดพิษณุโลก
    line_start = mytext.find("[")
    XText= mytext[0:line_start]
    return str(XText)
#

def ReVerse_Print_Code(mytext):
    #--   รูปแบบค่าที่รับมา = "65[จังหวัดพิษณุโลก]"
    #--   ค่าที่ได้ = 65
    line_start = 0
    line_end   = mytext.find("[")
    XCode = mytext[line_start:line_end]
    return str(XCode)
def ReVerse_Print_Text(mytext):
    # --   รูปแบบค่าที่รับมา = "65[จังหวัดพิษณุโลก]"
    # --   ค่าที่ได้ = จังหวัดพิษณุโลก
    line_start = mytext.find("[")+1
    line_end   = mytext.count("")-2
    XText= mytext[line_start:line_end]
    return str(XText)

##-------------------------------------------------------
## Connection Database
##-------------------------------------------------------
def connectSqlite():
    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
    sqliteConnection = sqlite3.connect(DataPath)
    Mycursor = sqliteConnection.cursor()
    return Mycursor


#########################################################################################
## --  การค้นหา แบบ Autocomplete ----------------------------------------------------------
## คำสั่ง
# -- เรียก ฟังก์ชั่นด้านล่าง ก่อน
#  results list_ProvinceName()
#  completer = QCompleter(results)
#  self.lineEditSearch.setCompleter(completer)
#######################################################################################
#########################################################################################
#   การ Add Item
#   comboBoxName
# -- เรียก ฟังก์ชั่นด้านล่าง ก่อน
#  results list_ProvinceName()
#  xresults = MyLib.comboBox_ProvinceName()
#  self.comboBoxName.addItems(xresults)
##
#########################################################################################
    #     self.initUI()
    #     self.comboBoxName.activated.connect(self.activated)
    #     self.comboBoxName.currentTextChanged.connect(self.text_changed)
    #     self.comboBoxName.currentIndexChanged.connect(self.index_changed)
    #
    # def activated(Self, index):
    #     print("Activated index:", index)
    #
    # def text_changed(self, s):
    #     print("Text changed:", s)
    #
    # def index_changed(self, index):
    #     print("Index changed", index)
    #
    # def initUI(self):
    #     xresults = MyLib.list_ProvinceName()
    #     self.comboBoxName.addItems(xresults)



###--------------------------------------------
##   จังหวัด
##---------------------------------------------
def list_ProvinceName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "select DISTINCT SUBSTR(CATM,1,2) ,CHANGWAT_NAME FROM l_catm ORDER BY CHANGWAT_NAME"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##----   ค่าที่แสดงผล =  พิษณุโลก[65]
    return Result

###--------------------------------------------
##   อำเภอ
##---------------------------------------------
def list_AmpurName(codechang):
    province_id = "'"+str(codechang)+"'"
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "select DISTINCT SUBSTR(CATM,1,4) ,AMPHUR_NAME FROM l_catm WHERE SUBSTR(CATM,1,2) = '"+codechang+"' ORDER BY SUBSTR(CATM,1,4)"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##----   ค่าที่แสดงผล =  พิษณุโลก[6500]
    return Result

###--------------------------------------------
##   ตำบล
##---------------------------------------------
def list_TumbonName(codeampur):
    ampur_id = "'"+str(codeampur)+"'"
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "select DISTINCT SUBSTR(CATM,1,6) ,TUMBON_NAME FROM l_catm WHERE SUBSTR(CATM,1,4) = '"+codeampur+"' ORDER BY SUBSTR(CATM,1,6)"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##----   ค่าที่แสดงผล =  พิษณุโลก[650000]
    return Result



def list_R_ProvinceCode():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "select DISTINCT SUBSTR(CATM,1,2) ,CHANGWAT_NAME FROM l_catm ORDER BY SUBSTR(CATM,1,2)"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}[{row[1]}]")
        ##----   ค่าที่แสดงผล =  65[พิษณุโลก]
    return Result










###--------------------------------------------
##   hospital  โรงพยาบาล                      ##
##---------------------------------------------
def list_HospitalName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT HMAIN,HNAME FROM l_hospital ORDER BY HNAME"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##-----ค่าที่แสดง = คลินิกรักฟัน[40631]
    return Result

def list_R_HospitalCode():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT HMAIN,HNAME FROM l_hospital ORDER BY HMAIN"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}[{row[1]}]")
        ##-----ค่าที่แสดง = 08333[รพ.สต.บ่อพลับ]
    return Result

###--------------------------------------------
##   อาชีพ                       ##
##---------------------------------------------
def list_OccupationName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT occupacode,occupaname FROM l_occupation ORDER BY occupaname"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##-----ค่าที่แสดง = เกษตรกร[0001]
    return Result

def list_R_OccupationCode():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT occupacode,occupaname FROM l_occupation ORDER BY occupacode"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}[{row[1]}]")
        ##-----ค่าที่แสดง = 0001[เกษตรกร]
    return Result

###--------------------------------------------
##   สิทธิการรักษาพบาบาล                         ##
##---------------------------------------------
def list_RightName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT right_main_code,right_main_desc FROM l_right_pttype ORDER BY right_main_desc"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}({row[0]})")
        ##-----ค่าที่แสดง = บุคคลผู้มีปัญหาสถานะและสิทธิ[S]
    return Result

def list_R_RightCode():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT right_main_code,right_main_desc FROM l_right_pttype ORDER BY right_main_code"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}[{row[1]}]")
        ##-----ค่าที่แสดง = S[บุคคลผู้มีปัญหาสถานะและสิทธิ]
    return Result

###--------------------------------------------
##   คำนำหน้าชื่อ                     ##
##---------------------------------------------
def list_TitleName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT TITLECODE,TITLENAME FROM l_titles ORDER BY TITLENAME"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##-----ค่าที่แสดง = บุคคลผู้มีปัญหาสถานะและสิทธิ[S]
    return Result

def list_R_TitleCode():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "SELECT DISTINCT TITLECODE,TITLENAME FROM l_titles ORDER BY TITLECODE"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[0]}[{row[1]}]")
        ##-----ค่าที่แสดง = S[บุคคลผู้มีปัญหาสถานะและสิทธิ]
    return Result


#########################################################################################
#   การ Add Item
#   comboBoxName
#########################################################################################
def comboBox_ProvinceName():
    Result=[]   #-- ประการค่าเป็น List
    Mycursor = connectSqlite()
    query = "select DISTINCT SUBSTR(CATM,1,2) ,CHANGWAT_NAME FROM l_catm ORDER BY CHANGWAT_NAME"
    Mycursor.execute(query)
    results = Mycursor.fetchall()
    for row in results:
        Result.append(f"{row[1]}[{row[0]}]")
        ##----   ค่าที่แสดงผล =  พิษณุโลก[65]
    return Result



# codechang = 65
x = list_AmpurName("พิษณุโลก")
print(x)

# y = list_Province()
# print(y)