import sys
import pathlib
import time
import os
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot # ---  การส่งข้อมูลกลับ
from PyQt6.QtWidgets import *           #QMainWindow, QApplication,QMdiSubWindow
from PyQt6.QtWidgets import *           #QMessageBox
from PyQt6.QtGui import *               # QIcon
from PyQt6.QtCore import Qt
# Database -------------------
import sqlite3
from configparser import ConfigParser
import Lib_Encoding as My_Lib
import Lib_MyLib_DateTime as MyLDate
#-------------------
import mysql.connector          ## Mydel-connect-python

class Super_TranferPersonWindow(QtWidgets.QDialog):  # QWidget  QDialog



    def __init__(self, *args, **kwargs):
        super(Super_TranferPersonWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/tranfer_person.ui", self)
        # --------------Set Gobal Values  Windows ---------------------------
        self.host_ip   = "Null"
        self.user_host = "Null"
        self.pass_host = "Null"
        self.port_host = "Null"
        self.database_name = "Null"
        #---------- Load config -------------------------------
        self.load_Config()

        # self.pushButtonREadSmartCard.clicked.connect(self.Read_SmartCard)
        # self.pushButtonSaveRegister.clicked.connect(self.Save_Register)
        ##-------- กำหนดให้มีการ double_clicked Row ในตาราง  ----------------------------
        # self.tableWidgetUser.cellDoubleClicked.connect(self.cell_was_double_clicked)
        # ##-------- กำหนดให้มีการ การทำงานของปุ่ม เพื่อค้นหาข้อมูล  ----------------------------
        self.pushButtonSearchSqlite.clicked.connect(self.search_personSqlite)
        self.pushButtonDeleteSqlite.clicked.connect(self.Delete_personSqlite)

        self.pushButtonLoadMyPerson.clicked.connect(self.Load_personMysql)
        self.pushButtonMyTOSqlite.clicked.connect(self.SaveMysqlTOSqlite)


        # ## -----  กำหนดขนาดของช่องตาราง  -----------------------------------------------
        # self.tableWidgetUser.setColumnWidth(0, 150)
        # self.tableWidgetUser.setColumnWidth(1, 150)
        # self.tableWidgetUser.setColumnWidth(2, 150)
        # self.tableWidgetUser.setColumnWidth(3, 50)
        # self.tableWidgetUser.setColumnWidth(4, 200)
        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/writer-male-48.png'
        self.setWindowTitle('Tranfer  Person Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()

    def progress(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBar.setValue(i)
            if i == 100:
                self.labelCOMPLETE.setText("Loading Complete")
                self.labelCOMPLETE.setAlignment(Qt.AlignmentFlag.AlignCenter)
    def SaveMysqlTOSqlite(self):

        self.progress()

        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        Mycursor = sqliteConnection.cursor()

        ResultPersom = self.load_MysqlPerson()
        i=0
        if len(ResultPersom) > 0:
            for row in ResultPersom:

                Xpcucodeperson = str(ResultPersom[i][0])
                Xprename = str(ResultPersom[i][2])
                Xfname = str(ResultPersom[i][3])
                Xlname = str(ResultPersom[i][4])

                XBirthDayEng = str(ResultPersom[i][5])
                Xsex = str(ResultPersom[i][6])
                Xidcard = str(ResultPersom[i][7])
                Xbloodgroup = str(ResultPersom[i][8])
                Xbloodhr = str(ResultPersom[i][9])
                XDrugAll = str(ResultPersom[i][10])
                XnameDrugAll = str(ResultPersom[i][11])
                XMarry = str(ResultPersom[i][12])
                Xeducation = str(ResultPersom[i][13])
                # ---------
                XOcc = str(ResultPersom[i][14])
                XNation = str(ResultPersom[i][15])
                XRace = str(ResultPersom[i][16])
                # ---------
                Xmobile = str(ResultPersom[i][17])
                XAdd_Ban = str(ResultPersom[i][18])
                XAdd_Mu = str(ResultPersom[i][19])
                XPtChangwat = str(ResultPersom[i][20])
                XPtAmphur = str(ResultPersom[i][21])
                XPtTumbon = str(ResultPersom[i][22])
                XFriendPt = str(ResultPersom[i][23])
                XTellFriendPt = str(ResultPersom[i][24])
                XComitPt = str(ResultPersom[i][25])
                XUC_Hmain = str(ResultPersom[i][26])
                XUC_Hsub  = str(ResultPersom[i][27])
                XRight = str(ResultPersom[i][28])

                Xcheck_smartcard = "KeyIN"
                XregisterDate = MyLDate.Date_register()
                Xpicture_smartcard = "False"
                Xpicture_camera = "False"

                query = '''
                        INSERT INTO person (pcucodeperson, prename, fname ,lname ,idcard,sex,bloodgroup,birth
                        ,nation,Race,occupa,educate,allergic,drug_allergic,marystatus,mobile,address,add_mu,add_changwat
                        ,add_amphur,add_tumbon,relative,relative_tel,relative_relation,uc_hmain,uc_hsub,right_health
                        ,check_smartcard,register_date,picture_smartcard,picture_camera)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                     '''
                Mycursor.execute(query, (
                 Xpcucodeperson, Xprename, Xfname, Xlname, Xidcard, Xsex, Xbloodgroup, XBirthDayEng
                , XNation, XRace, XOcc, Xeducation, XDrugAll, XnameDrugAll, XMarry, Xmobile, XAdd_Ban, XAdd_Mu
                , XPtChangwat, XPtAmphur, XPtTumbon, XFriendPt, XTellFriendPt, XComitPt,XUC_Hmain,XUC_Hsub, XRight
                ,Xcheck_smartcard,XregisterDate,Xpicture_smartcard,Xpicture_camera))
                i+=1

        Mycursor.connection.commit()
        Mycursor.connection.close()
        self.labelCOMPLETE.setText("Wait For Process..")
        QMessageBox.information(self, "Warning", "บันทึกข้อมูลเรียบร้อยแล้ว....",
                                QMessageBox.StandardButton.Ok)


    def Load_personMysql(self):

        self.progress()

        ResultPersom = self.load_MysqlPerson()
        # print(ResultPersom)
        #print("XXXXXXXXXXXXXXXXXXXXx")
        if len(ResultPersom) > 0:
            #----------------------------------
            for i in reversed(range(self.tableWidgetUser.rowCount())):
                self.tableWidgetUser.removeRow(i)
            ##---------- Remove ------------
            ## User = self.LoadData()
            rowPosition = self.tableWidgetUser.rowCount()
            print(rowPosition)
            #print("BBBBBBBBBBBBBBBBBBBBBBBBB")
            for row in ResultPersom:
                # print(row)
                # print(rowPosition)
                self.tableWidgetUser.insertRow(rowPosition)
                self.tableWidgetUser.setItem(rowPosition, 1, QTableWidgetItem(str(row[0])))
                self.tableWidgetUser.setItem(rowPosition, 2, QTableWidgetItem(str(row[1])))
                self.tableWidgetUser.setItem(rowPosition, 3, QTableWidgetItem(str(row[2])))
                self.tableWidgetUser.setItem(rowPosition, 4, QTableWidgetItem(str(row[3])))
                self.tableWidgetUser.setItem(rowPosition, 5, QTableWidgetItem(str(row[4])))
                self.tableWidgetUser.setItem(rowPosition, 6, QTableWidgetItem(str(row[5])))
                self.tableWidgetUser.setItem(rowPosition, 7, QTableWidgetItem(str(row[6])))
                self.tableWidgetUser.setItem(rowPosition, 8, QTableWidgetItem(str(row[7])))
                self.tableWidgetUser.setItem(rowPosition, 9, QTableWidgetItem(str(row[8])))
                self.tableWidgetUser.setItem(rowPosition, 10, QTableWidgetItem(str(row[9])))
                self.tableWidgetUser.setItem(rowPosition, 11, QTableWidgetItem(str(row[10])))
                self.tableWidgetUser.setItem(rowPosition, 12, QTableWidgetItem(str(row[11])))
                self.tableWidgetUser.setItem(rowPosition, 13, QTableWidgetItem(str(row[12])))
                self.tableWidgetUser.setItem(rowPosition, 14, QTableWidgetItem(str(row[13])))
                self.tableWidgetUser.setItem(rowPosition, 15, QTableWidgetItem(str(row[14])))
                self.tableWidgetUser.setItem(rowPosition, 16, QTableWidgetItem(str(row[15])))
                self.tableWidgetUser.setItem(rowPosition, 17, QTableWidgetItem(str(row[16])))
                self.tableWidgetUser.setItem(rowPosition, 18, QTableWidgetItem(str(row[17])))
                self.tableWidgetUser.setItem(rowPosition, 19, QTableWidgetItem(str(row[18])))
                self.tableWidgetUser.setItem(rowPosition, 20, QTableWidgetItem(str(row[19])))
                self.tableWidgetUser.setItem(rowPosition, 21, QTableWidgetItem(str(row[20])))
                self.tableWidgetUser.setItem(rowPosition, 22, QTableWidgetItem(str(row[21])))
                self.tableWidgetUser.setItem(rowPosition, 23, QTableWidgetItem(str(row[22])))
                self.tableWidgetUser.setItem(rowPosition, 24, QTableWidgetItem(str(row[23])))
                self.tableWidgetUser.setItem(rowPosition, 25, QTableWidgetItem(str(row[24])))
                self.tableWidgetUser.setItem(rowPosition, 26, QTableWidgetItem(str(row[25])))
                self.tableWidgetUser.setItem(rowPosition, 32, QTableWidgetItem(str(row[28])))
                self.tableWidgetUser.setItem(rowPosition, 33, QTableWidgetItem(str(row[26])))
                self.tableWidgetUser.setItem(rowPosition, 34, QTableWidgetItem(str(row[27])))

        QMessageBox.information(self, "Warning", "Load ข้อมูลเรียบร้อยแล้ว....",
                                QMessageBox.StandardButton.Ok)
        self.labelCOMPLETE.setText("Wait For Process..")


    def Delete_personSqlite(self):

        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM person "
        cursor.execute(query)
        Rec_user = cursor.fetchall()
        self.CountRec = len(Rec_user)

        Dquery = "DELETE FROM person "
        selected_option = QMessageBox.warning(self, "Warning",
                                              "ต้องการลบข้อมูลที่อยู่หน้าจอนี้หรือไม่ กรุณา Yes เพื่อยืนยัน?",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if selected_option == QMessageBox.StandardButton.Yes:
            self.progress()
            cursor.execute(Dquery)
            sqliteConnection.commit()
            sqliteConnection.close()
            #------------------------------Delete Data to show.
            for i in reversed(range(self.CountRec)):
                self.tableWidgetUser.removeRow(i)
            #------------------------------Delete Data to show.
            QMessageBox.information(self, "Warning", "ข้อมูลถูกลบเรียบร้อยแล้ว....",
                                    QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Warning", "ข้อมูลถูกยกเลิกเรียบร้อยแล้ว....(ไม่มีการลบข้อมูล)",
                                    QMessageBox.StandardButton.Ok)
        self.labelCOMPLETE.setText("Wait For Process..")

    def search_personSqlite(self):

        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM person "
        cursor.execute(query)
        Rec_user = cursor.fetchall()

        self.progress()

        if len(Rec_user) > 0:
            #----------------------------------
            for i in reversed(range(self.tableWidgetUser.rowCount())):
                self.tableWidgetUser.removeRow(i)
            ##---------- Remove ------------
            ## User = self.LoadData()
            rowPosition = self.tableWidgetUser.rowCount()
            # print(rowPosition)
            for row in Rec_user:
                # print(row)
                # print(rowPosition)
                self.tableWidgetUser.insertRow(rowPosition)
                self.tableWidgetUser.setItem(rowPosition, 0, QTableWidgetItem(str(row[0])))
                self.tableWidgetUser.setItem(rowPosition, 1, QTableWidgetItem(row[1]))
                self.tableWidgetUser.setItem(rowPosition, 2, QTableWidgetItem(row[2]))
                self.tableWidgetUser.setItem(rowPosition, 3, QTableWidgetItem(row[3]))
                self.tableWidgetUser.setItem(rowPosition, 4, QTableWidgetItem(row[4]))
                self.tableWidgetUser.setItem(rowPosition, 5, QTableWidgetItem(row[5]))
                self.tableWidgetUser.setItem(rowPosition, 6, QTableWidgetItem(row[6]))
                self.tableWidgetUser.setItem(rowPosition, 7, QTableWidgetItem(row[7]))
                self.tableWidgetUser.setItem(rowPosition, 8, QTableWidgetItem(row[8]))
                self.tableWidgetUser.setItem(rowPosition, 9, QTableWidgetItem(row[9]))
                self.tableWidgetUser.setItem(rowPosition, 10, QTableWidgetItem(row[10]))
                self.tableWidgetUser.setItem(rowPosition, 11, QTableWidgetItem(row[11]))
                self.tableWidgetUser.setItem(rowPosition, 12, QTableWidgetItem(row[12]))
                self.tableWidgetUser.setItem(rowPosition, 13, QTableWidgetItem(row[13]))
                self.tableWidgetUser.setItem(rowPosition, 14, QTableWidgetItem(row[14]))
                self.tableWidgetUser.setItem(rowPosition, 15, QTableWidgetItem(row[15]))
                self.tableWidgetUser.setItem(rowPosition, 16, QTableWidgetItem(row[16]))
                self.tableWidgetUser.setItem(rowPosition, 17, QTableWidgetItem(row[17]))
                self.tableWidgetUser.setItem(rowPosition, 18, QTableWidgetItem(row[18]))
                self.tableWidgetUser.setItem(rowPosition, 19, QTableWidgetItem(row[19]))
                self.tableWidgetUser.setItem(rowPosition, 20, QTableWidgetItem(row[20]))
                self.tableWidgetUser.setItem(rowPosition, 21, QTableWidgetItem(row[21]))
                self.tableWidgetUser.setItem(rowPosition, 22, QTableWidgetItem(row[22]))
                self.tableWidgetUser.setItem(rowPosition, 23, QTableWidgetItem(row[23]))
                self.tableWidgetUser.setItem(rowPosition, 24, QTableWidgetItem(row[24]))
                self.tableWidgetUser.setItem(rowPosition, 25, QTableWidgetItem(row[25]))
                self.tableWidgetUser.setItem(rowPosition, 26, QTableWidgetItem(row[26]))
                self.tableWidgetUser.setItem(rowPosition, 27, QTableWidgetItem(row[27]))
                self.tableWidgetUser.setItem(rowPosition, 28, QTableWidgetItem(row[28]))
                self.tableWidgetUser.setItem(rowPosition, 29, QTableWidgetItem(row[29]))
                self.tableWidgetUser.setItem(rowPosition, 30, QTableWidgetItem(row[30]))
                self.tableWidgetUser.setItem(rowPosition, 31, QTableWidgetItem(row[31]))
                self.tableWidgetUser.setItem(rowPosition, 32, QTableWidgetItem(row[32]))
                self.tableWidgetUser.setItem(rowPosition, 33, QTableWidgetItem(row[33]))
                self.tableWidgetUser.setItem(rowPosition, 34, QTableWidgetItem(row[34]))
                self.tableWidgetUser.setItem(rowPosition, 35, QTableWidgetItem(row[35]))
                self.tableWidgetUser.setItem(rowPosition, 36, QTableWidgetItem(row[36]))
                self.tableWidgetUser.setItem(rowPosition, 37, QTableWidgetItem(row[37]))
                self.tableWidgetUser.setItem(rowPosition, 38, QTableWidgetItem(row[38]))
                self.tableWidgetUser.setItem(rowPosition, 39, QTableWidgetItem(row[39]))
                self.tableWidgetUser.setItem(rowPosition, 40, QTableWidgetItem(row[40]))

        QMessageBox.information(self, "Warning", "Load ข้อมูลเรียบร้อยแล้ว....",
                                QMessageBox.StandardButton.Ok)
        self.labelCOMPLETE.setText("Wait For Process..")
        # else:
        #     self.tableWidgetUser.removeRow
        #     self.remove_item()

    def load_Config(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        # HOSPITAL
        self.hospitalInfo = config_object["SERVERCONFIG"]
        # Set Values
        self.host_ip = My_Lib.Decoding(self.hospitalInfo["host_ip"])
        self.user_host = My_Lib.Decoding(self.hospitalInfo["user_host"])
        self.pass_host = My_Lib.Decoding(self.hospitalInfo["pass_host"])
        self.port_host = My_Lib.Decoding(self.hospitalInfo["port_host"])
        self.database_name = My_Lib.Decoding(self.hospitalInfo["database_name"])

    def load_MysqlPerson(self):

        #print(self.user_host)
        #print(self.host_ip)

        cnx = mysql.connector.connect(user=self.user_host,
                                      password=self.pass_host,
                                      host=self.host_ip,
                                      database=self.database_name,
                                      port=self.port_host)
        try:
            cursor = cnx.cursor()
            cursor.execute(""" 
                      SELECT pcucodeperson
                          ,hcode
                                ,CASE
                                   WHEN prename = '001' then 'เด็กชาย'
                                     WHEN prename = '002' then 'เด็กหญิง'
                                     WHEN prename = '003' then 'นาย'
                                     WHEN prename = '004' then 'น.ส.'
                                     WHEN prename = '005' then 'นาง'
                                     WHEN substr(prename,1,1) = '8' then 'พระ'
                                     ELSE  'อื่นๆ(มียศ.)'
                                END as prename			
                                ,fname
                                ,lname
                                ,birth
                                ,CASE 
                                     WHEN sex = '1' then 'ชาย'
                                         WHEN sex = '2'then 'หญิง'
                                         ELSE 'เลือกเพศ'
                           END AS sex 
                                ,idcard
                                ,CASE
                                   WHEN bloodgroup = 'A' then 'A'
                                     WHEN bloodgroup = 'B' then 'B'
                                     WHEN bloodgroup = 'O' then 'O'
                                     WHEN bloodgroup = 'AB' then 'AB'
                                     ELSE  'ไม่ทราบ'
                                END as bloodgroup		
                                    ,'' as bloodrh
                                    ,CASE
                                   WHEN allergic = 'ปฏิเสธ' then 'ปฏิเสธการแพ้ยา'
                                     ELSE  'ไม่ทราบ'
                                END as allergic	
                                 ,'' as drug_allergic
                                 ,CASE
                                   WHEN marystatus = '1' then 'โสด'
                                     WHEN marystatus = '2' then 'คู่(สมรส)'
                                     WHEN marystatus = '3' then 'หม้าย'
                                     WHEN marystatus = '4' then 'หย่า'
                                     WHEN marystatus = '5' then 'แยกกันอยู่'
                                     ELSE  'ไม่ทราบ'
                                END as marystatus	
                                ,CASE
                                   WHEN educate = '00' then 'ไม่ได้รับการศึกษา'
                                     WHEN educate = '01' then 'ประถม'
                                     WHEN educate = '02' then 'ประถม'
                                     WHEN educate = '03' then 'มัธยม'
                                     WHEN educate = '04' then 'ปวช./ปวส.'
                                     WHEN educate = '05' then 'ปริญญาตรี'
                                     WHEN educate = '06' then 'ปริญญาโท'
                                     WHEN educate = '09' then 'ไม่ทราบ'
                                     ELSE  'ไม่ทราบ'
                                END as educate	
                                 ,CASE
                                   WHEN occupa = '000' then 'ไม่ทราบ'
                                     WHEN occupa = '001' then 'เกษตรกรรมหรือประมง'
                                     WHEN occupa = '002' then 'รับจ้าง'
                                     WHEN occupa = '003' then 'ค้าขาย'
                                     WHEN occupa = '004' then 'รับราชการ'
                                     WHEN occupa = '008' then 'เกษตรกรรมหรือประมง'
                                     WHEN occupa = '007' then 'ทหารหรือตำรวจ'
                                     WHEN occupa = '009' then 'ครู'
                                     WHEN substr(occupa,1,2) = '22' then 'ทางสาธารณสุข'
                                     WHEN occupa = '9999' then 'ไม่ทราบ'
                                     WHEN occupa = '9002' then 'ในปกครอง'
                                     WHEN occupa = '013' then 'ทางศาสนา'
                                     WHEN occupa = '014' then 'งานบ้าน'
                                     ELSE  'ไม่ทราบ'
                                END as occupa	
                                 ,CASE
                                   WHEN nation = '99' then 'ไทย'
                                     WHEN nation = '000' then 'ไม่ทราบ'
                                     WHEN nation = '002' then 'จีน'
                                     WHEN nation = '045' then 'อินเดีย'
                                     WHEN nation = '046' then 'เวียดนาม'
                                     WHEN nation = '048' then 'พม่า'
                                     WHEN nation = '057' then 'กัมพูชา'
                                     ELSE  'ไม่ทราบ'
                                END as nation	
                                 ,' ' as Race
                                 ,mobile
                                 ,hnomoi as address
                                 ,mumoi as add_mu
                                 ,cprovince.provname as add_changwat
                                 ,cdistrict.distname as add_amphur
                                 ,csubdistrict.subdistname  as add_tumbon
                                 ,case when LENGTH(messengername) > 0 then messengername else 'ไม่ระบุ' END as relative
			                     ,case when LENGTH(messengertel) > 0 then messengertel else 'ไม่ระบุ' END as relative_tel 
                                 ,CASE
                                    WHEN patientrelate is null then 'ไม่ทราบ'
                                        WHEN patientrelate is not null then 'บุคคลครอบครัวเดียวกัน'
                                    END as relative_relation
                                 ,hosmain as uc_hmain
                                 ,hossub as uc_hsub
                                 ,CASE
                                    WHEN crightgroup.rightgroupcode = '1' then 'สิทธิกรมบัญชีกลาง'
                                        WHEN crightgroup.rightgroupcode = '2' then 'สิทธิประกันสังคม'
                                        WHEN crightgroup.rightgroupcode = '3' then 'สิทธิ 30 บาท หลักประกันสุขภาพ'
                                        WHEN crightgroup.rightgroupcode = '4' then 'สิทธิ 30 บาท หลักประกันสุขภาพ'
                                        WHEN crightgroup.rightgroupcode = '5' then 'ต่างด้าว'
                                        WHEN crightgroup.rightgroupcode = '6' then 'ต่างด้าว'
                                        else 'ไม่ทราบ'
                                    END as right_health			 
                                FROM person
                                LEFT JOIN cprovince on cprovince.provcode = person.provcodemoi
                                LEFT JOIN cdistrict on cdistrict.provcode = person.provcodemoi and cdistrict.distcode = person.distcodemoi
                                LEFT JOIN csubdistrict on csubdistrict.provcode = person.provcodemoi and csubdistrict.distcode = person.distcodemoi and csubdistrict.subdistcode = person.subdistcodemoi
                                LEFT JOIN cright on cright.rightcode = person.rightcode
                                LEFT JOIN crightgroup on crightgroup.rightgroupcode = cright.rightgroup          
                                               
                        
                        """)
            result = cursor.fetchall()
            #print("YYYYYYYYYYYYYYYYYYYYYYYYY")
            if result:
                xresult = result
                # return  xresult
            else:
                xresult = "Not Connect"
        finally:
            cnx.close()
            return xresult


    def cell_was_double_clicked(self, row, column):
        self.ReturnMessageSearch = self.tableWidgetUser.item(row, 0).text()
        self.close()
        return self.ReturnMessageSearch



    # def register_main():
# app = QApplication(sys.argv)
# ex = Super_TranferPersonWindow()
# sys.exit(app.exec())
# #
# #
# # if __name__ == '__main__':
# #     register_main()
