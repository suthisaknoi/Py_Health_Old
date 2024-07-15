import sys
import os
import pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *  #QMessageBox
from PyQt6.QtGui import *      # QIcon
from PyQt6.QtCore import Qt
import sqlite3
#-------------------
import smtplib, ssl
from email.message import EmailMessage  ## Mail..
#-------------------
import Lib_Encoding as My_Lib
import  Lib_superAdmin as Lib_super
class login_windows(QtWidgets.QDialog):

    def Search_User(self):
        TextSearchUser =self.lineEditUser.text()
        TextSearchPass = self.lineEditPass.text()

        TextSearchUser = TextSearchUser.replace(" ", "")
        TextSearchPass = TextSearchPass.replace(" ", "")

        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        #query = "SELECT * FROM user_app WHERE email = '"+TextSearch+"'"
        query = "SELECT * FROM user_app WHERE user_name = ? and pass_user = ?"
        cursor.execute(query,(TextSearchUser,My_Lib.Encoding(TextSearchPass)))
        #Rec_user = cursor.fetchall()
        Rec_user = cursor.fetchone()
        # print("Rec_user")
        # print(Rec_user)
        return Rec_user

    def CheakLogin_User(self):
        if ((len(self.lineEditUser.text()) == 0) or (len(self.lineEditPass.text()) == 0)):
            QMessageBox.information(self, "Warning", " กรุณากรอก User Name และ Password เพื่อเข้าสู่ระบบงาน ",
                                         QMessageBox.StandardButton.Ok)
        else:
            userSuper,passSuper = Lib_super.pass_superadmin()
            if self.lineEditUser.text() == userSuper and self.lineEditPass.text() == passSuper:
                self.usercid = "9999999999999"
                self.username = "SuperAdmin"
                self.nameuser = "SuperAdmin System developer"
                self.usertype = "SuperAdmin"
                self.userstatus = "ใช้งาน"
                self.CheckStatus = "ใช้งาน"
                self.CHeckRight = "SuperAdmin"
                QMessageBox.information(self, "information", " ่ยินดีต้อนรับ>>Super Admin<<<เข้าสู่ระบบงานสารสนเทศเพื่อการดูแลสุขภาพ ",
                                        QMessageBox.StandardButton.Ok)
                # return self.usercid, self.username, self.nameuser, self.usertype, self.userstatus
                self.close()
            else:
                self.Rec_user   = self.Search_User()
                # print(self.Rec_user)
                if self.Rec_user is None:
                    QMessageBox.information(self, "Warning", " ไม่พบ UserName หรือ Password ผิด.. กรุณาลองใหม่ ",
                                                QMessageBox.StandardButton.Ok)
                else:
                    self.usercid    = self.Rec_user[0]
                    self.username   = self.Rec_user[3]
                    self.nameuser   = self.Rec_user[1]
                    self.usertype   = self.Rec_user[5]
                    self.userstatus = self.Rec_user[6]
                    self.CheckStatus = self.Rec_user[6]
                    self.CHeckRight =  self.Rec_user[5]
                    #print(CheckStatus)
                    if self.CheckStatus=="หยุดการใช้งาน":
                        QMessageBox.critical(self, "critical", " ่ต้องขออภัยท่านถูกระงับเข้าใช้งานในระบบงาน..ติดต่อผู้ดูแลระบบ ",
                                                QMessageBox.StandardButton.Ok)
                        #return self.usercid,self.username,self.nameuser,self.usertype,self.userstatus
                        self.close()
                    else:
                        QMessageBox.information(self, "information", " ่ยินดีต้อนรับเข้าสู่ระบบงานสารสนเทศเพื่อการดูแลสุขภาพ ",
                                            QMessageBox.StandardButton.Ok)
                        #return self.usercid, self.username, self.nameuser, self.usertype, self.userstatus
                        self.close()
        return self.Rec_user

    def SearchUserName(self):
        TextSearch = self.lineEditUser.text()
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app WHERE user_name = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        return Rec_user

    def ForgotPass_User(self):
        if len(self.lineEditUser.text()) == 0:
                QMessageBox.information(self, "Warning", " กรุณากรอก User Name ที่ลงทะเบียนไว้ เพื่อตรวจสอบตัวตน ",
                QMessageBox.StandardButton.Ok)
        else:
            checkUserName = self.SearchUserName()
            if not checkUserName:
                QMessageBox.critical(self, "critical", " ไม่พบ User Name นี้ในฐานข้อมูลสิทธิการเข้าใช้งาน กรุณาตรวจสอบ ",
                                        QMessageBox.StandardButton.Ok)
            else:
                self.checkEmail = checkUserName[2]
                self.checkPassWord = checkUserName[4]
                selected_option = QMessageBox.warning(self, "Warning",
                                                      "ต้องการให้ระบบงาน. ส่งรหัสผ่านให้ทาง Email ที่ให้ไว้หรือไม่..? กรุณา Yes เพื่อยืนยัน?",
                                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
                if selected_option == QMessageBox.StandardButton.Yes:
                    resultSentEmail = self.sent_mail_TOUser()
                    if resultSentEmail:
                        QMessageBox.information(self, "information", "รหัสผ่านของท่านได้ถูกส่งไปให้ใน Email ที่ลงทะเบียนไว้ก่อนหน้านี้แล้ว..",
                                            QMessageBox.StandardButton.Ok)
                    else:
                        QMessageBox.critical(self, "critical",
                                                " Email ไม่สามารถส่งได้ ติดต่อผู้พัฒนา..",
                                                QMessageBox.StandardButton.Ok)
                else:
                    QMessageBox.information(self, "Warning", "ข้อมูลถูกยกเลิกเรียบร้อยแล้ว....(ไม่มีการส่งรหัสผ่านให้ทาง Email)",
                                            QMessageBox.StandardButton.Ok)

    def sent_mail_TOUser(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "testnhso2@gmail.com"  # Enter your address
        ## receiver_email = "suthisak.noi@gmail.com"  # Enter receiver address
        receiver_email = self.checkEmail   #-- อีเมส์ ที่อยู่ที่ที่ได้จากฐานข้อมูลสิทธิ
        password = "ioqzuvntmbsehrup"

        msg = EmailMessage()
        val_xvalKey = self.checkPassWord  # -- เอาค่าใน ฐานข้อมูลสิทธิ
        mytext = "รหัสผ่านที่เข้าใช้งานโปรแกรมระบบสารสนเทศเพื่อสุขภาพ ดังนี้  \n \n \n PassWord : "+val_xvalKey +" \n \n กรุณานำ รหัสนี้ ไปเข้าใช้งานโปรแกรม(Register Application)    \n เมส์นี้เป็นระบบอัตโนมัติ ได้รับแล้ว ไม่ต้องตอบกลับ... ขอบคุณมากครับ"          ## การแปลง Text ให้แสดงเป็นข้อความต่าง ๆ
        msg.set_content(mytext)

        #msg.set_content(mytext)
        msg['Subject'] = "ส่งรหัสรหัสผ่าน สำหรับใช้งานโปรแกรมระบบสารสนเทศเพื่อสุขภาพ..(ลืมรหัสผ่าน)"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
        return True

    def FClose(self):
        reply = QMessageBox.question(self, 'Question', 'คุณต้องการออกจากโปรแกรม..ใช่หรือไม่.?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
    def __init__(self, *args, **kwargs):
        super(login_windows,self).__init__(*args, **kwargs)
        uic.loadUi("ui/login.ui", self)
        ##---------------- กำหนดตัวแปร --------------
        self.usercid  = "Null"
        self.username = "Null"
        self.nameuser = "Null"
        self.usertype = "Null"
        self.userstatus = "Null"
        #------------------------------------------
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  ## เอา Fram หน้าจอออก
        ##-----------------------------------------
        self.Rec_user = []
        # Path DataBase Sqlite #-------------------
        self.DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        isFile = os.path.isfile(self.DataPath)
        if not isFile:
            QMessageBox.information(self, "Warning", "ไม่พบไฟล์ฐานข้อมูล ในการเก็บข้อมูล HealthDB.db ",
                                    QMessageBox.StandardButton.Ok)
        else:
            sqliteConnection = sqlite3.connect(self.DataPath)  # เชื่อมต่อ Database
            try:
                cursor = sqliteConnection.cursor()
                # display version
                query = 'select sqlite_version();'
                cursor.execute(query)
                # get data
                record = cursor.fetchall()
                #self.labelVersionSqlite.setText(f'SQLite Version - {record}')
                self.pushButtonGreen.setEnabled(True)    # กำหนดให้ ไฟสีเขียว แสดง หมายถึงฐานข้อมูลพร้อมใช้งาน
                cursor.close()

            except sqlite3.Error as error:
                self.pushButtonGreen.setEnabled(False)
                print('Error occurred - ', error)
            finally:
                # If the connection was established then close it
                if sqliteConnection:
                    sqliteConnection.close()
                    # print('SQLite Connection closed')
        # Path DataBase Sqlite #-------------------

        self.pushButtonLogin.clicked.connect(self.CheakLogin_User)  ## กดปุ่ม
        self.pushButtonForgotPass.clicked.connect(self.ForgotPass_User)  ## กดปุ่ม
        self.pushButtonClose.clicked.connect(self.FClose)  ## กดปุ่ม
        #self.pushButtonChangPass.clicked.connect(self.)  ## กดปุ่ม
        # self.pushButtonListData.clicked.connect(self.load_Data)  ## กดปุ่ม

        # Display Windows -----
        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/health24.png'
        self.setWindowTitle('Login Windows')
        self.setWindowIcon(QIcon(image_health))
        # self.show()
        # pass
        return


