import sys
import pathlib
import datetime
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt6.QtGui import QIcon, QAction ,QPixmap
from PyQt6 import QtCore
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice     ## การแปลงรูป เป็น Bit
from configparser import ConfigParser
#-------------------
import mysql.connector          ## Mydel-connect-python
import Lib_Encoding as My_Lib
# Load Lib การอ่านบัตร Smartcard ชื่อไฟล์ Lib_ReadSmartCard.py  --------------
from Lib_ReadSmartCard import textCard, photoCard, resizeImg
# Load Lib การอ่านบัตร Smartcard เพื่อตรวจสอบว่ามีเครือ่งอ่าน หรือมีบัตร หรือเปล่า
from smartcard.System import readers
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
# Load Lib My Lib -----------------------------------------------------
import Lib_MyLib as MyLib
import Lib_MyLib_DateTime as MyLDate
# Database -------------------
import sqlite3
#---- เรียกหน้าจอค้นหาข้อมูลเข้ามาใช้งาน -----
from register_personSearch import Register_SearchpersonWindow  # หน้าต่างค้นหา
from config_camera import Camera_Window                        # หน้าต่างถ่ายรูป


class Register_personWindow(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(Register_personWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/register_screen.ui", self)
        ### --- กำหนดค่า พ.ศ.  และ อายุ ใส่ ComboBox ---------
        # --- Year -----------------------------------------------------
        self.comboBoxBIrth_Year.clear()
        lookYear = MyLib.Lookup_Year()  # -- รับค่า List Year ปีปัจจุบัน ถอยไปอีก 110 ปี ---
        self.comboBoxBIrth_Year.addItems(lookYear)
        # --- Age -----------------------------------------------------
        self.comboBoxAge_Year.clear()
        lookAgeYear = MyLib.Lookup_Age()  # -- รับค่า List Age  0-119  ---
        self.comboBoxAge_Year.addItems(lookAgeYear)


        self.ClearData()                                            ## Clear หน้าจอ และกำหนดค่าเบื้องต้น
        # -----------------------------------------
        self.pushButtonClearScreen.clicked.connect(self.ClearData)  ## Clear Screen --- pushButtonClearScreen
        # -----------------------------------------
        self.comboBoxBIrth_Year.currentTextChanged.connect(self.calculate_Age)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม  comboBoxBIrth_Year
        self.comboBoxAge_Year.currentTextChanged.connect(self.calculate_Year_Birth)  ## คำนวนค่าเมื่อ มีการกดปุ่ม  comboBoxBIrth_Year
        #------- Combobox จังหวัด อำเภอ ที่อยู่ของผู้ป่วย  -----------
        self.comboBoxPtChangwat.currentTextChanged.connect(self.Combo_Pt_Changwat)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม
        self.comboBoxPtAmphur.currentTextChanged.connect(self.Combo_Pt_Amphur)      ## คำนวนค่าเมื่อ มีการกดปุ่ม
        #------- ตรวจสอบการ checkBox  ---  ที่อยู่ เดียวกับ ที่ของผู้ป่วยรึไม่.
        self.checkBox_Address.checkStateChanged.connect(self.checkBox_Chk_ADD)

        # ------- Combobox จังหวัด อำเภอ ที่อยู่ของญาติของผู้ป่วย  -----------
        self.comboBoxF_changwat.currentTextChanged.connect(self.ComboFriend_Changwat)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม
        self.comboBoxF_Amphur.currentTextChanged.connect(self.ComboFriend_Amphur)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม


        self.pushButtonSearch.clicked.connect(self.OpenWindowsSearch_Register)  ##--- ปุ่มค้นหา จาก register_personSearch.py
        self.pushButtonTakePoTo.clicked.connect(self.OpenWindowsSearch_Photo)  ##--- ปุ่มถ่ายรูป config_camera.py

        self.pushButtonREadSmartCard.clicked.connect(self.Read_SmartCard)
        self.pushButtonSaveRegister.clicked.connect(self.Save_Register)
        ####################################################################
        self.pushButtonDelete.clicked.connect(self.Delete_Register)             ## ลบข้อมูลทิ้งแบบถาวร

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/writer-male-48.png'
        self.setWindowTitle('Register Person Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()
        #pass


    def Delete_Register(self):
        if (len(self.lineCID.text()) == 0):
            QMessageBox.information(self, "Warning", " ไม่พบข้อมูลที่ต้องการลบ กรุณาค้นหาข้อมูลก่อน ",
                                    QMessageBox.StandardButton.Ok)
        else:
            if (self.pushTypeKey.text() == 'KeyIN') or (self.pushTypeKey.text() == 'SmartCard'):
                QMessageBox.information(self, "Warning", " การทำงานอยู่ในระหว่างการคีย์ข้อมูล ไม่สามารถลบข้อมูลได้ ",
                                        QMessageBox.StandardButton.Ok)
            else:
                DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
                sqliteConnection = sqlite3.connect(DataPath)
                cursor = sqliteConnection.cursor()
                query = "SELECT idcard,picture_smartcard,picture_camera FROM person WHERE idcard = '" + self.lineCID.text() + "'"
                cursor.execute(query)
                Rec_user = cursor.fetchone()
                sqliteConnection.commit()
                sqliteConnection.close()
                if not Rec_user:
                    QMessageBox.information(self, "Warning", " ไม่พบข้อมูลที่ต้องการลบ..กรุณาลองค้นหาดูอีกครั้ง ",
                                            QMessageBox.StandardButton.Ok)
                else:
                    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
                    sqliteConnection = sqlite3.connect(DataPath)
                    cursor = sqliteConnection.cursor()
                    query = "DELETE FROM person WHERE idcard = '" + self.lineCID.text() + "'"
                    # cursor.execute(query)
                    selected_option = QMessageBox.warning(self, "Warning",
                                                          "ต้องการลงข้อมูลที่อยู่หน้าจอนี้หรือไม่ กรุณา Yes เพื่อยืนยัน?",
                                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
                    if selected_option == QMessageBox.StandardButton.Yes:
                        cursor.execute(query)    ## ลบฐาน Person

                        queryPhoto = "DELETE FROM person_picture WHERE idcard = '" + self.lineCID.text() + "'"
                        cursor.execute(queryPhoto) ## ลบฐาน person_picture

                        sqliteConnection.commit()
                        sqliteConnection.close()
                        QMessageBox.information(self, "Warning", "ข้อมูลถูกลบเรียบร้อยแล้ว....",
                                                QMessageBox.StandardButton.Ok)
                        self.ClearData()
                    else:
                        QMessageBox.information(self, "Warning", "ข้อมูลถูกยกเลิกเรียบร้อยแล้ว....(ไม่มีการลบข้อมูล)",
                                                QMessageBox.StandardButton.Ok)
                        self.ClearData()


    def Edit_message(self):
        ## self.ReturnCID  -- รับค่ามาจาก windows 2 (Search Register)
        #print("Mode Edit")
        #print(self.ReturnCID)
        if not self.ReturnCID:
            QMessageBox.warning(self, "Warning", " กรอกข้อความที่ต้องการค้นหา [บางส่วนของชื่อ หรือ นามสกุล] ",
                                    QMessageBox.StandardButton.Ok)
        else:
            TextSearch = self.ReturnCID             # self.lineSearchName.text()
            TextSearch = TextSearch.replace(" ", "")
            # ---- Search ---------------------
            self.ClearData()  ## Clear หน้าจอ และกำหนดค่าเบื้องต้น
            self.pushTypeKey.setText('Search')
            # ---- Search ---------------------
            DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
            sqliteConnection = sqlite3.connect(DataPath)
            cursor = sqliteConnection.cursor()
            query = "SELECT * FROM person WHERE idcard = '" + TextSearch + "'"
            cursor.execute(query)
            Rec_user = cursor.fetchone()
            #print(Rec_user)
            if not Rec_user:
                QMessageBox.information(self, "Warning", " ไม่พบข้อมูลที่ค้นหา.. กรุณาลองใหม่ ",
                                            QMessageBox.StandardButton.Ok)
            else:
                XCid           = self.lineCID.setText("")

                pcucodeperson  = Rec_user[1]
                housecode      = Rec_user[2]
                prename         = Rec_user[3]
                fname           = Rec_user[4]
                lnameX           = Rec_user[5]
                birth           = Rec_user[6]
                BirthYrar, BirthMonth, BirthDay = MyLib.Check_BirthDay_Search(birth)
                #print(birth)
                #print(BirthYrar)
                #print(BirthMonth)
                #print(BirthDay)
                sex             = Rec_user[7]
                idcard          = Rec_user[8]
                bloodgroup      = Rec_user[9]
                bloodrh         = Rec_user[10]
                allergic        = Rec_user[11]
                drug_allergic   = Rec_user[12]
                marystatus      = Rec_user[13]
                educate         = Rec_user[14]
                occupa          = Rec_user[15]
                nation          = Rec_user[16]
                Race            = Rec_user[17]
                mobile          = Rec_user[18]
                address         = Rec_user[19]
                add_mu          = Rec_user[20]
                add_changwat    = Rec_user[21]
                add_amphur      = Rec_user[22]
                add_tumbon      = Rec_user[23]
                relative        = Rec_user[24]
                relative_tel    = Rec_user[25]
                relative_relation = Rec_user[26]
                relative_add    = Rec_user[27]
                relative_add_mu = Rec_user[28]
                relative_add_changwat = Rec_user[29]
                #print(relative_add_changwat)
                relative_add_amphur = Rec_user[30]
                #print(relative_add_amphur)
                relative_add_tumbon = Rec_user[31]
                #print(relative_add_tumbon)
                right_health        = Rec_user[32]
                #print("Load complete")
                ##-- Title Name --
                index_titlaName = self.comboBoxTitle.findText(prename)
                if index_titlaName != -1:
                    self.comboBoxTitle.setCurrentIndex(index_titlaName)
                else:
                    self.comboBoxTitle.setCurrentIndex(0)
                ##-- FName --
                self.lineFName.setText(fname)
                ##-- LName --
                self.lineLName.setText(lnameX)
                ##-- BirthDate --
                # --- Year -----------------------------------------------------
                # self.comboBoxBIrth_Year.clear()
                # lookYear = MyLib.Lookup_Year()  # -- รับค่า List Year ปีปัจจุบัน ถอยไปอีก 110 ปี ---
                # self.comboBoxBIrth_Year.addItems(lookYear)

                index_BIrth_Year = self.comboBoxBIrth_Year.findText(BirthYrar)
                if index_BIrth_Year != -1:
                    self.comboBoxBIrth_Year.setCurrentIndex(index_BIrth_Year)
                else:
                    self.comboBoxBIrth_Year.setCurrentIndex(0)

                # --- Month -----------------------------------------------------
                index_BIrth_Month = self.comboBoxBIrth_Month.findText(BirthMonth)
                if index_BIrth_Month != -1:
                    self.comboBoxBIrth_Month.setCurrentIndex(index_BIrth_Month)
                else:
                    self.comboBoxBIrth_Month.setCurrentIndex(0)
                # --- Day -----------------------------------------------------
                index_BIrth_Day = self.comboBoxBIrth_Day.findText(BirthDay)
                if index_BIrth_Month != -1:
                    self.comboBoxBIrth_Day.setCurrentIndex(index_BIrth_Day)
                else:
                    self.comboBoxBIrth_Day.setCurrentIndex(0)
                # --- AGe Year--------------------------------------------------
                #print("show age")
                # ##### คำนวนอายุ #####
                today = datetime.date.today()
                thaiyear = today.year + 543
                # # # print(thaiyear)
                AgeYear = str(thaiyear - int(self.comboBoxBIrth_Year.currentText()))
                # # # print(AgeYear)
                # # ##### คำนวนอายุ #####
                # self.comboBoxAge_Year.clear()
                # lookAgeYear = MyLib.Lookup_Age()  # -- รับค่า List Age  0-119  ---
                # self.comboBoxAge_Year.addItems(lookAgeYear)
                index_Age = self.comboBoxAge_Year.findText(AgeYear)
                if index_Age != -1:
                      self.comboBoxAge_Year.setCurrentIndex(index_Age)
                else:
                      self.comboBoxAge_Year.setCurrentIndex(0)

                #print("show cal Age")
                #################
                ##-- Sex -----
                index_Sex = self.comboBoxSex.findText(sex)
                if index_Sex != -1:
                    self.comboBoxSex.setCurrentIndex(index_Sex)
                else:
                    self.comboBoxSex.setCurrentIndex(0)
                ##-- CID -----
                self.lineCID.setText(idcard)  # เลช 13 หลัก
                ##-- bloodgroup -----
                index_blood = self.comboBoxBlood.findText(bloodgroup)
                if index_blood != -1:
                    self.comboBoxBlood.setCurrentIndex(index_blood)
                else:
                    self.comboBoxBlood.setCurrentIndex(0)
                ##-- bloodrh -----
                ##################
                ##-- allergic -----
                index_allergic = self.comboBoxDrugAll.findText(allergic)
                if index_allergic != -1:
                    self.comboBoxDrugAll.setCurrentIndex(index_allergic)
                else:
                    self.comboBoxDrugAll.setCurrentIndex(0)
                ##-- drug_allergic -----
                self.lineDrugAll.setText(drug_allergic)
                ##-- marystatus -----
                index_marystatus = self.comboBoxMarry.findText(marystatus)
                if index_marystatus != -1:
                    self.comboBoxMarry.setCurrentIndex(index_marystatus)
                else:
                    self.comboBoxMarry.setCurrentIndex(0)
                ##-- educate -----
                index_educate = self.comboBoxeducation.findText(educate)
                if index_educate != -1:
                    self.comboBoxeducation.setCurrentIndex(index_educate)
                else:
                    self.comboBoxeducation.setCurrentIndex(0)
                ##-- occupa -----
                index_occupa = self.comboBoxOcc.findText(occupa)
                if index_occupa != -1:
                    self.comboBoxOcc.setCurrentIndex(index_occupa)
                else:
                    self.comboBoxOcc.setCurrentIndex(0)
                ##-- nation -----
                index_nation = self.comboBoxNation.findText(nation)
                if index_nation != -1:
                    self.comboBoxNation.setCurrentIndex(index_nation)
                else:
                    self.comboBoxNation.setCurrentIndex(0)
                ##-- Race -----
                index_Race = self.comboBoxRace.findText(Race)
                if index_Race != -1:
                    self.comboBoxRace.setCurrentIndex(index_Race)
                else:
                    self.comboBoxRace.setCurrentIndex(0)
                #print("index_Race")
                ##-- mobile -----
                self.lineTellPt.setText(mobile)
                ##-- address -----
                self.lineAdd_Ban.setText(address)
                ##-- add_mu -----
                self.lineAdd_Mu.setText(add_mu)
                ##-- Build Data to Select changwat Amphur Tumbon-----
                lookChangwat = MyLib.list_ProvinceName()
                lookAmphur = MyLib.list_AmpurName(add_changwat)  # --  แสดงอำเภอ ใน จังหวัด นั้น ๆ
                lookTombon = MyLib.list_TumbonName(add_changwat, add_amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ
                #print("lookAmphur")
                self.comboBoxPtChangwat.clear()
                self.comboBoxPtChangwat.addItems(lookChangwat)
                self.comboBoxPtAmphur.clear()
                self.comboBoxPtAmphur.addItems(lookAmphur)
                self.comboBoxPtTumbon.clear()
                self.comboBoxPtTumbon.addItems(lookTombon)
                #print("Add Item")
                ##-- add_changwat -----
                # --- Changwat ------------------------------------------------
                index_changwat = self.comboBoxPtChangwat.findText(add_changwat)  # รับค่าจังหวัด ด้านบน
                if index_changwat != -1:
                    self.comboBoxPtChangwat.setCurrentIndex(index_changwat)
                else:
                    self.comboBoxPtChangwat.setCurrentIndex(0)
                ##-- add_amphur -----
                # --- Amphur ------------------------------------------------
                index_Amphur = self.comboBoxPtAmphur.findText(add_amphur)  # รับค่าอำเภอ ด้านบน
                if index_Amphur != -1:
                    self.comboBoxPtAmphur.setCurrentIndex(index_Amphur)
                else:
                    self.comboBoxPtAmphur.setCurrentIndex(0)
                ##-- add_tumbon -----
                # --- Tumbon ------------------------------------------------
                index_Tumbon = self.comboBoxPtTumbon.findText(add_tumbon)  # รับค่าตำบล ด้านบน
                if index_Amphur != -1:
                    self.comboBoxPtTumbon.setCurrentIndex(index_Tumbon)
                else:
                    self.comboBoxPtTumbon.setCurrentIndex(0)

                #print("show address")
                ##-- relative -----
                self.lineFriendPt.setText(relative)
                ##-- relative_tel -----
                self.lineTellFriendPt.setText(relative_tel)
                ##-- relative_relation -----
                ##-- relative_add -----
                self.lineFAdd_Ban.setText(relative_add)
                ##-- relative_add_mu -----
                self.lineFAdd_Mu.setText(relative_add_mu)
                ## ---------- Build Data To Select Changwat Amphun Tumbon -----
                #print("show end address")
                # ---- ที่อยู่ผู้ป่วย ---
                PlookChangwat = MyLib.list_ProvinceName()
                self.comboBoxF_changwat.clear()
                self.comboBoxF_changwat.addItems(PlookChangwat)
                #print("p1")
                if relative_add_amphur is not None:
                    PlookAmphur = MyLib.list_AmpurName(relative_add_changwat)  # --  แสดงอำเภอ ใน จังหวัด นั้น ๆ
                    self.comboBoxF_Amphur.clear()
                    self.comboBoxF_Amphur.addItems(PlookAmphur)
                #print("p2")
                if relative_add_tumbon is not None:
                    PlookTombon = MyLib.list_TumbonName(relative_add_changwat, relative_add_amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ
                    #print("p3")
                    self.comboBoxF_Tumbon.clear()
                    self.comboBoxF_Tumbon.addItems(PlookTombon)
                #print("Add Friend")
                ##-- relative_add_changwat -----
                index_Pchangwat = self.comboBoxF_changwat.findText(relative_add_changwat)  # รับค่าจังหวัด ด้านบน
                if index_changwat != -1:
                    self.comboBoxF_changwat.setCurrentIndex(index_Pchangwat)
                else:
                    self.comboBoxF_changwat.setCurrentIndex(0)
                ##-- relative_add_amphur -----
                index_PAmphur = self.comboBoxF_Amphur.findText(relative_add_amphur)  # รับค่าจอำเภอ ด้านบน
                if index_changwat != -1:
                    self.comboBoxF_Amphur.setCurrentIndex(index_PAmphur)
                else:
                    self.comboBoxF_Amphur.setCurrentIndex(0)
                ##-- relative_add_tumbon -----
                index_PTumbon = self.comboBoxF_Tumbon.findText(relative_add_tumbon)  # รับค่าตำบล ด้านบน
                if index_changwat != -1:
                    self.comboBoxF_Tumbon.setCurrentIndex(index_PTumbon)
                else:
                    self.comboBoxF_Tumbon.setCurrentIndex(0)
                ##-- right_health -----
                index_right = self.comboBoxRight.findText(right_health)  # สิทธิ
                if index_changwat != -1:
                    self.comboBoxRight.setCurrentIndex(index_right)
                else:
                    self.comboBoxRight.setCurrentIndex(0)
                ##-- relative_relation -----
                index_relative = self.comboComitPt.findText(relative_relation)  # การเกี่ยวข้อง ของบุคคลที่เกียวข้องเพื่อให้ข่าวสารผู้ป่วย
                if index_changwat != -1:
                    self.comboComitPt.setCurrentIndex(index_relative)
                else:
                    self.comboComitPt.setCurrentIndex(0)




    ################################################################################################################
    #######                              เปิดหน้าต่าง การค้นหาข้อมูล                                                 ######
    ################################################################################################################
    def OpenWindowsSearch_Register(self):
        if not self.lineSearchName.text():
            QMessageBox.warning(self, "Warning", " กรอกข้อความที่ต้องการค้นหา [บางส่วนของชื่อ หรือ นามสกุล] ",
                                    QMessageBox.StandardButton.Ok)
        else:
            #---- Search ---------------------
            self.pushTypeKey.setText('Search')
            # ---- Search ---------------------
            MessageSearch = self.lineSearchName.text()
            self.window2 = Register_SearchpersonWindow()     #-- เรียกหน้าจอที่ 2  Search Windows
            #self.window2.ReturnMessageSearch = "default"
            #--- Run----
            self.window2.lineEditSearch.setText(MessageSearch)      #-- ส่งค่าไปยัง หน้าต่างค้นหา
            self.window2.search_person()                            #-- ประมวลผลค้นหาตรงหน้าต่างค้นหา
            # --- Run----
            #print("xxxxx")
            self.window2.exec()
            try:
                self.ReturnMess = self.window2.ReturnMessageSearch
                print("Try")
                print(self.ReturnMess)
            except OSError as err:
                print("OS error:", err)
            except ValueError:
                print("Could not convert data to an integer.")
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
            finally:
                #--- ตรวจสอบค่าคืนกลับ  -----------
                if self.ReturnMess == "Defult":   #-- Defult เป็นค่าที่รับมา จาก Search เพื่อตรวจสอบว่า ส่งข้อมูลมาเป็นค่าอะไร หรือ ออกจากหน้าจอเฉย ๆ
                     QMessageBox.critical(self, "Critical", " พบปัญหาการค้นหา ไม่มีการเลือกรายชื่อผู้รับบริการ ",
                                          QMessageBox.StandardButton.Ok)
                else:
                     #self.lineCID.setText(self.ReturnMess)  # -- ส่งค่ากลับมายัง หน้าหลัก
                     #print("send Data Complete")
                    self.ReturnCID = self.ReturnMess
                    print("finally")
                    print(self.ReturnCID)
                    self.Edit_message()

    ################################################################################################################
    #######                              เปิดหน้าต่าง การถ่ายรูป                                                     ######
    ################################################################################################################
    def OpenWindowsSearch_Photo(self):
        self.windowPhoto = Camera_Window()  # -- เรียกหน้าจอที่ 2  Search Windows
        ## self.windowPhoto.search_person()  # -- ประมวลผลค้นหาตรงหน้าต่างค้นหา
        # --- Run----
        self.windowPhoto.exec()
        path = "temp/camera_image.png"
        pixmap = QPixmap(path)
        self.labelCmaera.resize(148, 165)
        self.labelCmaera.setPixmap(pixmap)
        self.labelCmaera.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)



    def check_SmartCard(self):   ## มีการประกาศค่า self.code_error = YE  NE  เพื่อทำงานต่อ
        try:
            SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]  # Check card
            THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]
            CMD_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]  # CID
            # Get all the available readers
            readerList = readers()
            readerSelectIndex = 0  # int(input("Select reader[0]: ") or "0")
            reader = readerList[readerSelectIndex]
            connection = reader.createConnection()

            cardtype = AnyCardType()
            cardrequest = CardRequest(timeout=1, cardType=cardtype)
            cardservice = cardrequest.waitforcard()
            cardservice.connection.connect()

            connection.connect()
            atr = connection.getATR()
        except Exception as e:
            print('Error = ', e)
            self.code_error = 'YE'
            # self.show_error()
            #print(self.code_error)
        else:
             #print("Driver OK")
             self.code_error = 'NE'
             #print(self.code_error)
             pass

    def Read_SmartCard(self):
        ##self.ClearData()    ######################## ล้างข้อมูล ###############################
        self.pushTypeKey.setText('SmartCard')
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXX")
        self.check_SmartCard()
        if self.code_error == 'YE':    # ตรวจสอบค่า การตรวจว่า มีบัตร และ เครื่องอ่าน หรือไม่..............
            #print("หยุดการทำงา")
            self.lineCID.setText("")           # เลช 13 หลัก
            self.lineFName.setText("")
            self.lineLName.setText("")
            self.lineAdd_Ban.setText("")
            self.lineAdd_Mu.setText("")
            # ---------------
            path = "temp/" + "user.png"
            pixmap = QPixmap(path)
            self.labelSmartcard.resize(148, 165)
            self.labelSmartcard.setPixmap(pixmap)
            self.labelSmartcard.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            QMessageBox.warning(self, "Warning", "กรุณาตรวจสอบเครื่องอ่านบัตร และการเสียบบัตร ",
                                    QMessageBox.StandardButton.Ok)


        else:
            #print("ไม่หยุดการทำงา")
            try:
                fileName = a = textCard()
                photoCard(fileName)  # รับอากิวเมน fileName ที่เป็น array โดย photoCard()ทำหน้าที่ดึงรูปและบันทึก
                resizeImg(fileName)  # resizeImg()ทำหน้าที่ปรับขนาดรูปและบันทึก
                path = "temp/" + a[0] + ".png"
                pixmap = QPixmap(path)

                self.labelSmartcard.resize(148, 165)
                self.labelSmartcard.setPixmap(pixmap)
                self.labelSmartcard.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                 #nameText = nameText.replace("#", " ")
                ####  จัดการค่าตัวแปร ที่อ่านมาจากบัตร SmartCard --------
                SerName,FName,LName  = MyLib.Cut_name_smartcard(a[1])
                ban, mu, tumbon, amphur, changwat = MyLib.Cut_Address_smartcard(a[11])
                Sex = a[5]
                BirhtDate = a[3]
                BirthYrar,BirthMonth,BirthDay = MyLib.Check_BirthDay_Smartcard(BirhtDate)
                # print(BirthYrar)
                # print(BirthMonth)
                # print(BirthDay)
                ## ----  แสดงผลข้อมูลทั่วไป  -----------------------
                self.lineCID.setText(a[0])  # เลช 13 หลัก
                # self.lineEdit2.setText(a[1])
                self.lineFName.setText(FName)
                self.lineLName.setText(LName)
                self.lineAdd_Ban.setText(ban)
                self.lineAdd_Mu.setText(mu)
                ####  จัดการค่าตัวแปร ที่อ่านมาจากบัตร SmartCard --------
                #--- Sername ---------------
                index_titlaName = self.comboBoxTitle.findText(str(SerName))
                if index_titlaName != -1:
                      self.comboBoxTitle.setCurrentIndex(index_titlaName)
                else:
                      self.comboBoxTitle.setCurrentIndex(0)
                # --- Sex -----------------
                index_Sex = self.comboBoxSex.findText(str(Sex))
                if index_Sex != -1:
                      self.comboBoxSex.setCurrentIndex(index_Sex)
                else:
                      self.comboBoxSex.setCurrentIndex(0)
                # --- nationality ---------
                self.comboBoxNation.setCurrentIndex(1)
                # --- race ----------------
                self.comboBoxRace.setCurrentIndex(1)
                ############### การกำหนดค่าให้ ComboBox #####################
                lookYear     = MyLib.Lookup_Year()              #-- รับค่า List Year ปีปัจจุบัน ถอยไปอีก 110 ปี ---
                lookAgeYear  = MyLib.Lookup_Age()               #-- รับค่า List Age  0-119  ---
                lookChangwat = MyLib.list_ProvinceName()
                lookAmphur   = MyLib.list_AmpurName(changwat)   #--  แสดงอำเภอ ใน จังหวัด นั้น ๆ
                lookTombon   = MyLib.list_TumbonName(changwat,amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ

                #print(lookAmphur)
                self.comboBoxBIrth_Year.addItems(lookYear)
                self.comboBoxAge_Year.addItems(lookAgeYear)
                #---- ที่อยู่ผู้ป่วย ---
                self.comboBoxPtChangwat.addItems(lookChangwat)
                self.comboBoxPtAmphur.addItems(lookAmphur)
                self.comboBoxPtTumbon.addItems(lookTombon)

                #print(lookTombon)
                # --- Year -----------------------------------------------------
                index_BIrth_Year = self.comboBoxBIrth_Year.findText(BirthYrar)
                if index_BIrth_Year != -1:
                    self.comboBoxBIrth_Year.setCurrentIndex(index_BIrth_Year)
                else:
                    self.comboBoxBIrth_Year.setCurrentIndex(0)
                ##### คำนวนอายุ #####
                today = datetime.date.today()
                thaiyear = today.year + 543
                #print(thaiyear)
                AgeYear  = str(thaiyear - int(self.comboBoxBIrth_Year.currentText()))
                #print(AgeYear)
                ##### คำนวนอายุ #####
                # --- Month -----------------------------------------------------
                index_BIrth_Month = self.comboBoxBIrth_Month.findText(BirthMonth)
                if index_BIrth_Month != -1:
                    self.comboBoxBIrth_Month.setCurrentIndex(index_BIrth_Month)
                else:
                    self.comboBoxBIrth_Month.setCurrentIndex(0)
                # --- Day -----------------------------------------------------
                index_BIrth_Day = self.comboBoxBIrth_Day.findText(BirthDay)
                if index_BIrth_Month != -1:
                    self.comboBoxBIrth_Day.setCurrentIndex(index_BIrth_Day)
                else:
                    self.comboBoxBIrth_Day.setCurrentIndex(0)
                # --- AGe Year--------------------------------------------------
                index_Age = self.comboBoxAge_Year.findText(AgeYear)
                if index_Age != -1:
                    self.comboBoxAge_Year.setCurrentIndex(index_Age)
                else:
                    self.comboBoxAge_Year.setCurrentIndex(0)
                # --- Changwat ------------------------------------------------
                index_changwat = self.comboBoxPtChangwat.findText(changwat)     # รับค่าจังหวัด ด้านบน
                if index_changwat != -1:
                    self.comboBoxPtChangwat.setCurrentIndex(index_changwat)
                else:
                    self.comboBoxPtChangwat.setCurrentIndex(0)
                # --- Amphur ------------------------------------------------
                index_Amphur = self.comboBoxPtAmphur.findText(amphur)                 # รับค่าอำเภอ ด้านบน
                if index_Amphur != -1:
                    self.comboBoxPtAmphur.setCurrentIndex(index_Amphur)
                else:
                    self.comboBoxPtAmphur.setCurrentIndex(0)
                # --- Tumbon ------------------------------------------------
                index_Tumbon = self.comboBoxPtTumbon.findText(tumbon)  # รับค่าตำบล ด้านบน
                if index_Amphur != -1:
                    self.comboBoxPtTumbon.setCurrentIndex(index_Tumbon)
                else:
                    self.comboBoxPtTumbon.setCurrentIndex(0)
            except:
                try:  # แสดงสถานะเตือนกณีไม่มีข้อมูล

                    self.lineCID.setText(a["ไม่มีข้อมูล"])
                    # self.lineEdit2.setText(a["ไม่มีข้อมูล"])
                    self.lineFName.setText(a["ไม่มีข้อมูล"])
                    self.lineLName.setText(a["ไม่มีข้อมูล"])
                    self.lineAdd_Ban.setText(a["ไม่มีข้อมูล"])
                    self.lineAdd_Mu.setText("ไม่มีข้อมูล")
                except:
                    pass

    def SearchIDCard(self):                 ## การตรวจสอบเลข 13 หลัก
        TextSearch = self.lineCID.text()
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT idcard FROM person WHERE idcard = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        return Rec_user

    def convertToBinaryData(self,cid):
        filename = str(pathlib.Path(__file__).parent.absolute()) + '/temp/'+cid+'.png'
        # filename = 'temp/saved_image.png'
        with open(filename,'rb') as file:
            photo = file.read()
        return photo

    def convertToBinaryDataCamera(self):
        filename = str(pathlib.Path(__file__).parent.absolute()) + '/temp/camera_image.png'
        # filename = 'temp/saved_image.png'
        with open(filename,'rb') as file:
            photo = file.read()
        return photo

    def Save_Register(self):
        # COnnection DataBase -----------------
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        Mycursor = sqliteConnection.cursor()
        #--- ถอดค่าตัวแปร ออกมาให้เหมาะสมกับการบันทึกข้อมูล -------
        ### Check Picture----------
        #pixmap = QPixmap().loadFromData(...)
        Spixmap = self.labelSmartcard.pixmap()
        if self.labelSmartcard.pixmap() is not None and not self.labelSmartcard.pixmap().isNull():
            Xpicture_smartcard = "True"
        else:
            Xpicture_smartcard = "False"
        Cpixmap = self.labelCmaera.pixmap()
        if self.labelCmaera.pixmap() is not None and not self.labelCmaera.pixmap().isNull():
            Xpicture_camera = "True"
        else:
            Xpicture_camera = "False"


        Xcheck_smartcard = self.pushTypeKey.text()
        Xpcucodeperson   = "12345"
        Xprename         = self.comboBoxTitle.currentText()
        Xfname           = self.lineFName.text()
        Xlname           = self.lineLName.text()
        Xidcard          = self.lineCID.text()
        Xsex             = self.comboBoxSex.currentText()
        Xbloodgroup      = self.comboBoxBlood.currentText()
        XYear            = self.comboBoxBIrth_Year.currentText()
        xxmonth          = self.comboBoxBIrth_Month.currentText()
        XMonth           = MyLDate.ReturnThaiMonthToEng(xxmonth)      # Lib = Lib_MyLib_DateTime
        xDay             = self.comboBoxBIrth_Day.currentText()
        XBirthDayEng     = MyLDate.ThaiDateTOEng(XYear,XMonth,xDay)    # Lib = Lib_MyLib_DateTime
        #---------
        XMarry      = self.comboBoxMarry.currentText()
        XNation     = self.comboBoxNation.currentText()
        XRace       = self.comboBoxRace.currentText()
        XOcc        = self.comboBoxOcc.currentText()
        Xeducation  =  self.comboBoxeducation.currentText()
        XDrugAll    = self.comboBoxDrugAll.currentText()
        XnameDrugAll  =  self.lineDrugAll.text()
        #---------
        Xmobile     = self.lineTellPt.text()
        XAdd_Ban    = self.lineAdd_Ban.text()
        XAdd_Mu     = self.lineAdd_Mu.text()
        XPtChangwat = self.comboBoxPtChangwat.currentText()
        XPtAmphur   = self.comboBoxPtAmphur.currentText()
        XPtTumbon   = self.comboBoxPtTumbon.currentText()
        XFriendPt   = self.lineFriendPt.text()
        XTellFriendPt = self.lineTellFriendPt.text()
        XComitPt    = self.comboComitPt.currentText()
        XFAdd_Ban   = self.lineFAdd_Ban.text()
        print(XFAdd_Ban)
        XFAdd_Mu    = self.lineFAdd_Mu.text()
        XF_changwat = self.comboBoxF_changwat.currentText()
        XF_Amphur   = self.comboBoxF_Amphur.currentText()
        XF_Tumbon   = self.comboBoxF_Tumbon.currentText()
        XRight      = self.comboBoxRight.currentText()

        XregisterDate = MyLDate.Date_register()

        if (Xcheck_smartcard == "KeyIN") or (Xcheck_smartcard == "SmartCard"):    ## เป็นการเพิ่มข้อมูลใหม่ -------
            print("CHeck 1")
            CheakCIDcard = self.SearchIDCard()  ## ตรวจสอบเลข 13 หลักซ้ำซ้อน
            if CheakCIDcard:
                QMessageBox.warning(self, "Warning",
                                        "มีการบันทึกเลขบัตรประชาชนซ้ำซ้อน.. ไม่สามารถบันทึกข้อมูลได้ กรุณาตรวจสอบแก้ไข",
                                        QMessageBox.StandardButton.Ok)
            else:
                if ((len(self.lineFName.text()) == 0) or (len(self.lineLName.text()) == 0)
                        or (len(self.lineTellPt.text()) == 0)):
                    QMessageBox.warning(self, "Warning",
                                            "กรุณากรอกข้อมูลชื่อ หรือ นามสกุล  และ ** เบอร์โทร **  ให้ครบถ้วน",
                                            QMessageBox.StandardButton.Ok)

                else:

                    query = '''
                            INSERT INTO person (check_smartcard,pcucodeperson, prename, fname ,lname ,idcard,sex,bloodgroup,birth
                            ,nation,Race,occupa,educate,allergic,drug_allergic,marystatus,mobile,address,add_mu,add_changwat
                            ,add_amphur,add_tumbon,relative,relative_tel,relative_relation,relative_add,relative_add_mu
                            ,relative_add_changwat,relative_add_amphur,relative_add_tumbon,register_date,right_health
                            ,picture_smartcard,picture_camera)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            
                            '''

                    Mycursor.execute(query, (Xcheck_smartcard,Xpcucodeperson, Xprename, Xfname ,Xlname ,Xidcard,Xsex,Xbloodgroup,XBirthDayEng
                                             ,XNation,XRace,XOcc,Xeducation,XDrugAll,XnameDrugAll,XMarry,Xmobile,XAdd_Ban,XAdd_Mu
                                             ,XPtChangwat,XPtAmphur,XPtTumbon,XFriendPt,XTellFriendPt,XComitPt,XFAdd_Ban,XFAdd_Mu
                                             ,XF_changwat,XF_Amphur,XF_Tumbon,XregisterDate,XRight,Xpicture_smartcard,Xpicture_camera))
                    ################################################################################################
                    #####  เก็บรูปเข้า DataBase  ####

                    if (Xcheck_smartcard == "SmartCard") and (Xpicture_smartcard == "True"):
                        query2 = "INSERT INTO person_picture (idcard,pt_picture) VALUES (?,?)"
                        empPhoto = self.convertToBinaryData(Xidcard)
                        Mycursor.execute(query2,(Xidcard,empPhoto))


                    if (Xcheck_smartcard == "KeyIN") and (Xpicture_camera == "True"):
                        query2 = "INSERT INTO person_picture (idcard,pt_picture) VALUES (?,?)"
                        CempPhoto = self.convertToBinaryDataCamera()
                        Mycursor.execute(query2,(Xidcard,CempPhoto))


                    Mycursor.connection.commit()
                    Mycursor.connection.close()
                    self.ClearData()
                    QMessageBox.information(self, "information", f"บันทึกข้อมูลเพิ่มใหม่ {Xfname} {Xlname} สำเร็จ...",
                                            QMessageBox.StandardButton.Ok)

        else:   #----- เป็นบันทึกการแก้ไขข้อมูล  --------
            print("CHeck 2")
            CheakCIDcard = self.SearchIDCard()  ## ตรวจสอบเลข 13 หลัก
            if not CheakCIDcard:
                QMessageBox.warning(self, "Warning",
                                    "พบปัญหาเกียวกับฐานข้อมูล ในส่วนของเลขบัตรประชาชน 13 หลัก [Error Code Register 001]",
                                    QMessageBox.StandardButton.Ok)
            else:
                print(XFAdd_Ban)
                query = '''
                            UPDATE person SET prename=?, fname=? ,lname=?,sex=?,bloodgroup=?,birth=?
                                    ,nation=?,Race=?,occupa=?,educate=?,allergic=?,drug_allergic=?
                                    ,marystatus=?,mobile=?,address=?,add_mu=?,add_changwat=?
                                    ,add_amphur=?,add_tumbon=?,relative=?,relative_tel=?,relative_relation=?
                                    ,relative_add=?,relative_add_mu=?,relative_add_changwat=?,relative_add_amphur=?
                                    ,relative_add_tumbon=?,right_health=? 
                                    WHERE pcucodeperson=? and idcard=?
                           '''

                Mycursor.execute(query, (
                                Xprename, Xfname, Xlname, Xsex, Xbloodgroup, XBirthDayEng
                                , XNation, XRace, XOcc, Xeducation, XDrugAll, XnameDrugAll, XMarry, Xmobile, XAdd_Ban, XAdd_Mu
                                , XPtChangwat, XPtAmphur, XPtTumbon, XFriendPt, XTellFriendPt, XComitPt, XFAdd_Ban, XFAdd_Mu
                                , XF_changwat, XF_Amphur, XF_Tumbon, XRight, Xpcucodeperson, Xidcard))
                Mycursor.connection.commit()
                Mycursor.connection.close()
                self.ClearData()
                QMessageBox.information(self, "information", f"บันทึกการแก้ไขข้อมูลของ {Xfname} {Xlname} สำเร็จ",
                                        QMessageBox.StandardButton.Ok)



    def checkBox_Chk_ADD(self):
        XcheckBox_Address = self.checkBox_Address.isChecked()
        if  XcheckBox_Address == True:
            changwat = self.comboBoxPtChangwat.currentText()
            amphur   = self.comboBoxPtAmphur.currentText()
            tumbon   = self.comboBoxPtTumbon.currentText()
            lookChangwat = MyLib.list_ProvinceName()
            lookAmphur = MyLib.list_AmpurName(changwat)  # --  แสดงอำเภอ ใน จังหวัด นั้น ๆ
            lookTombon = MyLib.list_TumbonName(changwat, amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ
            # ----  ใส่ List ที่อยู่ เข้า ใน Combobox ของญาติผู้ป่วย  -----
            self.comboBoxF_changwat.clear()
            self.comboBoxF_changwat.addItems(lookChangwat)
            self.comboBoxF_Amphur.clear()
            self.comboBoxF_Amphur.addItems(lookAmphur)
            self.comboBoxF_Tumbon.clear()
            self.comboBoxF_Tumbon.addItems(lookTombon)

            # --- Changwat ------------------------------------------------
            index_changwat = self.comboBoxF_changwat.findText(changwat)  # รับค่าจังหวัด ด้านบน
            if index_changwat != -1:
                self.comboBoxF_changwat.setCurrentIndex(index_changwat)
            else:
                self.comboBoxF_changwat.setCurrentIndex(0)
            # --- Amphur ------------------------------------------------
            index_Amphur = self.comboBoxF_Amphur.findText(amphur)  # รับค่าอำเภอ ด้านบน
            if index_Amphur != -1:
                self.comboBoxF_Amphur.setCurrentIndex(index_Amphur)
            else:
                self.comboBoxF_Amphur.setCurrentIndex(0)
            # --- Tumbon ------------------------------------------------
            index_Tumbon = self.comboBoxF_Tumbon.findText(tumbon)  # รับค่าตำบล ด้านบน
            if index_Amphur != -1:
                self.comboBoxF_Tumbon.setCurrentIndex(index_Tumbon)
            else:
                self.comboBoxF_Tumbon.setCurrentIndex(0)

            self.lineFAdd_Ban.setText(self.lineAdd_Ban.text())
            self.lineFAdd_Mu.setText(self.lineAdd_Mu.text())
        else:
            self.comboBoxF_changwat.setCurrentIndex(0)
            self.comboBoxF_Amphur.clear()
            self.comboBoxF_Tumbon.clear()
            self.lineFAdd_Ban.clear()
            self.lineFAdd_Mu.clear()


    def Combo_Pt_Changwat(self):
        changwat = self.comboBoxPtChangwat.currentText()
        XlookAmphur = MyLib.list_AmpurName(changwat)  # --  แสดงอำเภอ ใน จังหวัด นั้น ๆ
        self.comboBoxPtAmphur.clear()
        self.comboBoxPtAmphur.addItems(XlookAmphur)

    def ComboFriend_Changwat(self):
        changwat = self.comboBoxF_changwat.currentText()
        XlookAmphur = MyLib.list_AmpurName(changwat)  # --  แสดงอำเภอ ใน จังหวัด นั้น ๆ
        self.comboBoxF_Amphur.clear()
        self.comboBoxF_Amphur.addItems(XlookAmphur)


    def Combo_Pt_Amphur(self):
        changwat = self.comboBoxPtChangwat.currentText()
        amphur = self.comboBoxPtAmphur.currentText()
        XlookTombon = MyLib.list_TumbonName(changwat, amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ
        self.comboBoxPtTumbon.clear()
        self.comboBoxPtTumbon.addItems(XlookTombon)

    def ComboFriend_Amphur(self):
        changwat = self.comboBoxF_changwat.currentText()
        amphur   = self.comboBoxF_Amphur.currentText()
        XlookTombon = MyLib.list_TumbonName(changwat, amphur)  # --  แสดงตำบล ใน อำเภอ จังหวัด นั้น ๆ
        self.comboBoxF_Tumbon.clear()
        self.comboBoxF_Tumbon.addItems(XlookTombon)


    def calculate_Age(self):         ## ทำงาน เมื่อ ComboBox  comboBoxBIrth_Year มีการกดปุม เลือกค่า
        ##### คำนวนอายุ #####
        today = datetime.date.today()
        thaiyear = today.year + 543
        # print(thaiyear)
        AgeYear = str(thaiyear - int(self.comboBoxBIrth_Year.currentText()))
        # --- AGe Year--------------------------------------------------
        index_Age = self.comboBoxAge_Year.findText(AgeYear)
        if index_Age != -1:
            self.comboBoxAge_Year.setCurrentIndex(index_Age)
        else:
            self.comboBoxAge_Year.setCurrentIndex(0)
        ##### คำนวนอายุ #####

    def calculate_Year_Birth(self):
        today = datetime.date.today()
        thaiyear   = today.year + 543
        Year_Birth = str(thaiyear - int(self.comboBoxAge_Year.currentText()))
        # --- Birth Year--------------------------------------------------
        indexYear_Age = self.comboBoxBIrth_Year.findText(Year_Birth)
        if indexYear_Age != -1:
            self.comboBoxBIrth_Year.setCurrentIndex(indexYear_Age)
            self.comboBoxBIrth_Month.setCurrentIndex(0)
            self.comboBoxBIrth_Day.setCurrentIndex(0)
        else:
            self.comboBoxBIrth_Year.setCurrentIndex(0)
            self.comboBoxBIrth_Month.setCurrentIndex(0)
            self.comboBoxBIrth_Day.setCurrentIndex(0)


    def ClearData(self):   # pushButtonClearScreen
        self.lineCID.clear()

        #self.comboBoxTitl.clear()
        self.comboBoxTitle.setCurrentIndex(0)
        self.lineFName.clear()
        self.lineLName.clear()
        #self.comboBoxSex.clear()
        self.comboBoxSex.setCurrentIndex(0)
        #self.comboBoxBIrth_Year.clear()   ###   กำหนดค่าเริ่มต้นให้กับ หน้าจอ
        #self.comboBoxBIrth_Year.clear()
        # lookYear = MyLib.Lookup_Year()  # -- รับค่า List Year ปีปัจจุบัน ถอยไปอีก 110 ปี ---
        # self.comboBoxBIrth_Year.addItems(lookYear)
        self.comboBoxBIrth_Year.setCurrentIndex(0)

        #self.comboBoxBIrth_Month.clear()
        self.comboBoxBIrth_Month.setCurrentIndex(0)
        #self.comboBoxBIrth_Day.clear()
        self.comboBoxBIrth_Day.setCurrentIndex(0)
        #self.comboBoxAge_Year.clear()   ###   กำหนดค่าเริ่มต้นให้กับ หน้าจอ
        #self.comboBoxAge_Year.clear()
        # lookAgeYear = MyLib.Lookup_Age()  # -- รับค่า List Age  0-119  ---
        # self.comboBoxAge_Year.addItems(lookAgeYear)
        self.comboBoxAge_Year.setCurrentIndex(0)
        #
        # self.comboBoxMarry.clear()
        self.comboBoxMarry.setCurrentIndex(0)
        #self.comboBoxNation.clear()
        self.comboBoxNation.setCurrentIndex(0)
        # self.comboBoxRace.clear()
        self.comboBoxRace.setCurrentIndex(0)
        #self.comboBoxOcc.clear()
        self.comboBoxOcc.setCurrentIndex(0)
        #self.comboBoxeducation.clear()
        self.comboBoxeducation.setCurrentIndex(0)
        #self.comboBoxBlood.clear()
        self.comboBoxBlood.setCurrentIndex(0)
        #self.comboBoxDrugAll.clear()
        self.comboBoxDrugAll.setCurrentIndex(0)
        # self.comboBoxRight.clear()
        self.comboBoxRight.setCurrentIndex(0)
        #
        self.lineDrugAll.clear()
        self.lineTellPt.clear()
        self.lineAdd_Ban.clear()
        self.lineAdd_Mu.clear()
        self.comboBoxPtChangwat.clear()           ###   กำหนดค่าเริ่มต้นให้กับ หน้าจอ
        lookChangwat = MyLib.list_ProvinceName()
        self.comboBoxPtChangwat.clear()
        self.comboBoxPtChangwat.addItems(lookChangwat)
        self.comboBoxPtChangwat.setCurrentIndex(0)

        self.comboBoxPtAmphur.clear()
        # self.comboBoxPtAmphur.setCurrentIndex(0)
        self.comboBoxPtTumbon.clear()
        # self.comboBoxPtTumbon.setCurrentIndex(0)
        self.lineFriendPt.clear()
        self.lineTellFriendPt.clear()
        #self.comboComitPt.clear()
        self.comboComitPt.setCurrentIndex(0)
        #----------
        self.checkBox_Address.setChecked(False)
        # ----------
        self.lineFAdd_Ban.clear()
        # ----------
        self.lineFAdd_Mu.clear()
        # ----------
        self.comboBoxF_changwat.clear()               ###   กำหนดค่าเริ่มต้นให้กับ หน้าจ
        lookChangwat = MyLib.list_ProvinceName()
        self.comboBoxF_changwat.clear()
        self.comboBoxF_changwat.addItems(lookChangwat)
        self.comboBoxF_changwat.setCurrentIndex(0)

        self.comboBoxF_Amphur.clear()
        #self.comboBoxF_Amphur.setCurrentIndex(0)
        self.comboBoxF_Tumbon.clear()
        #self.comboBoxF_Tumbon.setCurrentIndex(0)
        # #---------- ล้างข้อมูล -------
        self.labelSmartcard.clear()    # ลบรูปที่หน้าจอ
        self.labelCmaera.clear()    # ลบรูปที่หน้าจอ

        self.lineSearchName.clear()
        self.pushTypeKey.setText('KeyIN')    #--  แสดงข้อมูล คีย์เข้า หรือ เกิดจาก อ่านบัตร SmartCard หรือ การค้นหาข้อมูล
        # เพื่อนำข้อมูล ไป แสดง สถานนะ ว่า  InSert UpDate Delete


def register_main():
    app = QApplication(sys.argv)
    ex = Register_personWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    register_main()