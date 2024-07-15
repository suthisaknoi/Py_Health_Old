import sys
import pathlib
import os
import base64
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot # ---  การส่งข้อมูลกลับ
from PyQt6.QtWidgets import *           #QMainWindow, QApplication,QMdiSubWindow
from PyQt6.QtWidgets import *           #QMessageBox
from PyQt6.QtGui import *               # QIcon         # QIcon
# Database -------------------
import sqlite3

#----------------------------
import Lib_Encoding as My_Lib
import Lib_AuthenNHSO as My_LibAuthen
import Lib_MyLib_DateTime as My_LibDate
class authen_ServiceWindow(QtWidgets.QWidget):  # QWidget  QDialog

    def __init__(self, *args, **kwargs):
        super(authen_ServiceWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/authen_service.ui", self)
        # --------------กำหนดค่าเริ่มต้น  ---------------------------
        self.pid = None
        self.fname = None
        self.lname = None
        self.nation = None
        self.birthDate = None
        self.sex = None
        self.mainInscl = None
        self.subInscl = None
        self.age = None
        self.claimType = None    # ประกาศเป็นผลจากการเลือกจาก self.comboBoxClaimType พร้อมส่งออก
        self.image = None
        self.correlationId = None
        #--------------
        self.hospSub_hcode = None
        self.hospSub_hname = None
        self.hospMainOp_hcode = None
        self.hospMainOp_hname = None
        self.hospMain_hcode = None
        self.hospMain_hname = None
        #------------------
        self.check_NEWRec = None   # ตรวจสอบว่าจะบันทึกค่าใหม่ ลงในฐานข้อมูล per_telephone หรือไม่ ถ้า NEW เพิ่มใหม่
        #---------------อ่านค่าบันทึกหน่วยบริการ และ จังหวัด ใน Config.ini -------
        hcode, hname, hprovince_Id, hprovince_Name = My_Lib.Load_Hospital()
        self.hcode          = hcode
        self.hname          = hname
        self.hprovince_Id   = hprovince_Id
        self.hprovince_Name = hprovince_Name
        self.pushButtonHead_label.setText(f"รหัสหน่วยบริการ:{self.hcode} {self.hname} จังหวัด:{self.hprovince_Name}")
        ##-------------ตรวจสอบว่ามีเครื่องอ่านบัตร----------------------
        terminal_name, is_present, sentMessage = My_LibAuthen.get_smartcard()
        self.smart_is_present = is_present        # ส่งค่า พบบัตรอยู่ในเครื่องอ่าน
        self.lineEditSmartCard.setText(f'Smartcard รุ่น : {terminal_name} สถานะ : {sentMessage}')
        ## -------------ตรวจสอบ token ผู้ใช้งาน -------------------
        token, sentmessage = My_LibAuthen.show_token()
        lentoken = len(token)
        token = token[0:lentoken-10]+'xxxxxxxxxx'
        self.lineEditshowToken.setText(f'ตรวจสอบToken : {sentmessage} [{token}]')

        #------ ประมวลผลข้อมูล ปี พ.ศ. เพื่อ ใส่ Combobox ค้นหาข้อมูล วันเดือนปี ที่แสดงข้อมูล ----
        result_lookdate_Service = My_LibAuthen.look_servicedate()
        self.comboBoxdateservise.clear()
        self.comboBoxdateservise.addItems(result_lookdate_Service)

        # ----- load ข้อมูล ลงในตารางแสดงผล ---
        self.load_dataTOtableWidget()  # load ข้อมูลการ Authen มาแสดง

        # ---- การระบุความกว้างของตาราง tableWidgetauthen-------------------
        self.tableWidgetauthen.setColumnWidth(0, 100)
        self.tableWidgetauthen.setColumnWidth(1, 100)
        self.tableWidgetauthen.setColumnWidth(2, 150)
        self.tableWidgetauthen.setColumnWidth(3, 150)
        self.tableWidgetauthen.setColumnWidth(4, 50)
        self.tableWidgetauthen.setColumnWidth(5, 230)
        self.tableWidgetauthen.setColumnWidth(6, 145)
        self.tableWidgetauthen.setColumnWidth(7, 145)
        self.tableWidgetauthen.setColumnWidth(8, 145)

        #self.ReturnMessageSearch = "Defult"
        # ------- Combobox เลือก Claimtype เปลี่ยน ให้ ส่งค่าไปใหม่  -----------
        self.comboBoxClaimType.currentTextChanged.connect(self.ComboClaimtype_Change)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม
        self.comboBoxdateservise.currentTextChanged.connect(self.ComboDateservice_Change)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม


        # # -----------------------------------------
        self.pushButtonSaveAuthen.clicked.connect(self.Save_Authentication)
        self.pushButtotChecksmartcard.clicked.connect(self.check_SmartCard)
        self.pushButtonAuthen.clicked.connect(self.read_smartcard)
        self.pushButtonSyncData.clicked.connect(self.Sync_Database)
        self.pushButtonSycnDate.clicked.connect(self.Sync_DateService)


        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/changPass40.png'
        self.setWindowTitle('Authentication Service Windows')
        self.setWindowIcon(QIcon(image_health))
        # self.show()

    def Save_Authentication(self):
        if (len(self.lineEditcid.text()) == 0):
            QMessageBox.critical(self, "Critical", " กรุณาเสียบบัตร และอ่านบัตร Smart Card เพื่อยืนยันตนเองในการรับบริการ ",
                                    QMessageBox.StandardButton.Ok)
        else:
            if (len(self.lineEditPhone.text()) == 0):
                QMessageBox.critical(self, "Critical",
                                        " ต้องกรอกหมายเลขโทรศัพท์ที่สามารถติดต่อได้ เพื่อยืนยันตนเองในการตรวจสอบการรับบริการ \n ถ้าไม่ทราบให้ใส่ [9999999999] ",
                                        QMessageBox.StandardButton.Ok)
            else:
                ##------ Save to Data base -------
                self.Save_DataAuthen()
                ##------- Load Data  ------------
                self.load_dataTOtableWidget()
                ##------- clear Data  ------------
                self.Clear_Data()
                #   บันทึกข้อมูลการยืนยันตนเองในการเข้ารับบริการ เรียบร้อยแล้ว..




    def Sync_DateService(self):
        result_lookdate_Service = My_LibAuthen.look_servicedate()
        self.comboBoxdateservise.clear()
        self.comboBoxdateservise.addItems(result_lookdate_Service)
        return None


    #---- Sync Mysql field pid idcard mobile teltphone  from person -----
    def Sync_Database(self):
        selected_option = QMessageBox.warning(self, "Warning",
                                              "ต้องการ Sync DataBase Jhcis เพื่อใช้ข้อมูล Telephone  กรุณา Yes เพื่อยืนยัน?",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        if selected_option == QMessageBox.StandardButton.Yes:
            DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
            sqliteConnection = sqlite3.connect(DataPath)
            Mycursor = sqliteConnection.cursor()
            #--- Delete Sqlite ------
            Dquery = "DELETE FROM person_telephone WHERE authen IS NULL OR trim(authen) = '' "
            Mycursor.execute(Dquery)
            sqliteConnection.commit()
            # sqliteConnection.close()
            #print("CCCCCCCCCCCCCCCCCCCCCCCCC")
            #------- Save Data Mysql -----
            ResultPersom = My_Lib.GetData_mysql()
            i = 0
            if len(ResultPersom) > 0:
                #print("XXXXXXXXXXXXXXXXXXXX")
                for row in ResultPersom:
                    xpcucodeperson = str(ResultPersom[i][0])
                    xpid = str(ResultPersom[i][1])
                    xidcard = str(ResultPersom[i][2])
                    xmobile = str(ResultPersom[i][3])
                    xtelephoneperson = str(ResultPersom[i][4])
                    xtelephone = str(ResultPersom[i][5])
                    ###---- หาข้อมูลซ้ำ ไม่บันทึกซ้ำ  -------
                    # result = My_Lib.Search_idcard(xidcard)
                    # if len(result) > 0:
                    #     print("False")
                    # else:
                    #     print("True")
                    query = '''
                            INSERT OR IGNORE INTO person_telephone (pcucodeperson, pid, idcard, mobile, telephoneperson, telephone)
                            VALUES (?,?,?,?,?,?)
                            '''
                    Mycursor.execute(query, (xpcucodeperson, xpid, xidcard, xmobile, xtelephoneperson, xtelephone))
                    i += 1
            Mycursor.connection.commit()
            #Mycursor.connection.close()
            #self.labelCOMPLETE.setText("Wait For Process..")
            QMessageBox.information(self, "Warning", "บันทึกข้อมูลเรียบร้อยแล้ว....",
                                    QMessageBox.StandardButton.Ok)


    def Clear_Data(self):
        self.lineEditcid.clear()
        self.lineEditfname.clear()
        self.lineEditlname.clear()
        self.lineEditsex.clear()
        self.lineEditage.clear()
        self.lineEditright.clear()
        self.lineEditsubright.clear()
        self.lineEditFirst.clear()
        self.lineEditsceond.clear()
        self.lineEditPhone.clear()
        self.label_image.clear()
        self.comboBoxClaimType.clear()
        self.lineEditHN.clear()



    def ComboDateservice_Change(self):
        self.load_dataTOtableWidget()
        return None

    def ComboClaimtype_Change(self):
        self.claimType = My_LibAuthen.look_claimType(self.comboBoxClaimType.currentText())
        return None

    def load_dataTOtableWidget(self):
        dateserv = self.comboBoxdateservise.currentText()
        #print(dateserv)
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = ''' 
            select *
            FROM (
                      select strftime('%d', date(date_authen))||'-'||strftime('%m', date(date_authen))||'-'||cast(cast(strftime('%Y', date(date_authen)) AS INTEGER)+543 as text) as dateservice
                        ,STRFTIME('%H:%M:%S', date_authen) as timeservice
                        ,substr(idcard,1,8)||'xxxxx' as idcard
                        ,fname||' '||lname as namept
                        ,sex
                        ,right_health
                        ,claimtype
                        ,claimcode
                        ,telephone
                    from person_authen  
                    ORDER BY date_authen ASC   
                    ) WHERE  dateservice = '''+"'"+dateserv+"'"
        cursor.execute(query)
        Rec_user = cursor.fetchall()
        #print(Rec_user)
        if len(Rec_user) > 0:
            #-- ล้างข้อมูลในตาราง
            for i in reversed(range(self.tableWidgetauthen.rowCount())):
                self.tableWidgetauthen.removeRow(i)

            rowPosition = self.tableWidgetauthen.rowCount()
            # print(rowPosition)
            for row in Rec_user:
                # print(row)
                # print(rowPosition)
                self.tableWidgetauthen.insertRow(rowPosition)
                self.tableWidgetauthen.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
                self.tableWidgetauthen.setItem(rowPosition, 1, QTableWidgetItem(row[1]))
                self.tableWidgetauthen.setItem(rowPosition, 2, QTableWidgetItem(row[2]))
                self.tableWidgetauthen.setItem(rowPosition, 3, QTableWidgetItem(row[3]))
                self.tableWidgetauthen.setItem(rowPosition, 4, QTableWidgetItem(row[4]))
                self.tableWidgetauthen.setItem(rowPosition, 5, QTableWidgetItem(row[5]))
                self.tableWidgetauthen.setItem(rowPosition, 6, QTableWidgetItem(row[6]))
                self.tableWidgetauthen.setItem(rowPosition, 7, QTableWidgetItem(row[7]))
                self.tableWidgetauthen.setItem(rowPosition, 8, QTableWidgetItem(row[8]))


    def Save_DataAuthen(self):
        #print("yyyyyyyyyyyyy")
        # COnnection DataBase -----------------
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        Mycursor = sqliteConnection.cursor()
        xpid = self.pid
        xfname = self.fname
        xlname = self.lname
        xsex = self.sex
        xhcode = self.hcode  #รับค่าจากด้านบน  รหัสหน่วยบริการ
        # self.hname = hname  #รับค่าจากด้านบน
        ## วันที่รับบริการ
        xregdate = self.registerdate
        xright = self.right_health
        xphone = self.lineEditPhone.text()
        xclaimtype = My_LibAuthen.look_claimType(self.comboBoxClaimType.currentText())
        xcorrelationId = self.correlationId

        xTel   =  self.lineEditPhone.text()
        if len(self.lineEditHN.text())==0:
            xpidHN = 99999
            ApidHN = "99999"
        else:
            xpidHN =  int(self.lineEditHN.text())
            ApidHN =  self.lineEditHN.text()
            # print(xpid)
            # print(xclaimtype)
            # print(xTel)
            # print(xcorrelationId)
            # print(ApidHN)
            # print(xhcode)
        ####################### Authen #############################
        response_data, sentmessage = My_LibAuthen.post_authen_New(xpid, xclaimtype, xTel, xcorrelationId, ApidHN, xhcode)
            # Return = result = Json
            # response_data = "xx"
            # sentmessage = "XX"
        ############################################################
        if response_data == None:
            QMessageBox.information(self, "information", sentmessage,
                                                           QMessageBox.StandardButton.Ok)
        else:
            RclaimCode = response_data['claimCode']
            #RclaimCode = "XXXX"
            query = '''
                    INSERT INTO person_authen (hcode, idcard, date_authen, fname, lname ,sex ,right_health,telephone,claimtype,claimcode)
                    VALUES (?,?,?,?,?,?,?,?,?,?)    
                    '''

            Mycursor.execute(query, (xhcode, xpid, xregdate, xfname, xlname, xsex, xright, xphone, xclaimtype, RclaimCode))
            ## ------------ ปรับปรุงฐานข้อมูล Person_telephone ----------------
            if self.check_NEWRec == "NEW":
                query = '''
                        INSERT INTO person_telephone (pcucodeperson, pid, idcard, telephone, authen )
                        VALUES (?,?,?,?,?)     
                        '''
                xauthen = "True"
                Mycursor.execute(query,(xhcode, xpidHN, xpid, xphone,xauthen ))
            else:
                query = '''
                        UPDATE  person_telephone SET telephone = ? ,authen = ? WHERE idcard = ? 
                        '''
                xauthen = "True"
                Mycursor.execute(query, (xphone, xauthen, xpid))
        ################################################################################################
        Mycursor.connection.commit()
        Mycursor.connection.close()
        #self.ClearData()
        QMessageBox.information(self, "information", f"ยืนยันตนเองของ {xfname} {xlname} สำเร็จ  Claimcode =[{RclaimCode}]",
                                QMessageBox.StandardButton.Ok)


    def read_smartcard(self):
        terminal_name, is_present, sentMessage = My_LibAuthen.get_smartcard()
        if terminal_name == None:
            QMessageBox.warning(self, "Warning",
                                "ไม่พบเครื่องอ่านบัตร หรือ เครื่องอ่านบัตรชำรุด กรุณาให้ผู้ดูแลตรวจสอบ",
                                QMessageBox.StandardButton.Ok)
        else:
            if is_present != True:
                QMessageBox.warning(self, "Warning",
                                    "ไม่พบบัตร Smart Card ในช่องอ่าน หรือ ไม่สามารถอ่านบัตรได้ \n กรุณาให้ผู้ดูแลตรวจสอบ",
                                    QMessageBox.StandardButton.Ok)
            else:
                result = My_LibAuthen.read_smartcardOnline()   # Return = result = Json
                #print(len(result))
                #------ Update ตัวแปร เพื่อนำไปบันทึก ลง DataBase --------
                self.pid = result['pid']
                self.fname = result['fname']
                self.lname = result['lname']
                self.sex = result['sex']
                self.correlationId = result['correlationId']
                #self.hcode = hcode  #รับค่าจากด้านบน
                #self.hname = hname  #รับค่าจากด้านบน
                ## วันที่รับบริการ
                self.registerdate = My_LibDate.Date_register()
                self.right_health = result['mainInscl']

                ##----- ส่งค่าไปแสดงผล ที่หน้าจอ -------------
                self.lineEditcid.setText(result['pid'])
                self.lineEditfname.setText(result['fname'])
                self.lineEditlname.setText(result['lname'])
                self.lineEditsex.setText(result['sex'])
                self.lineEditage.setText(result['age'])
                self.lineEditright.setText(result['mainInscl'])
                self.lineEditsubright.setText(result['subInscl'])
               #
               #  # ----------  imageData ------------------
                image_data = base64.b64decode(result['image'])
                image = QImage()
                image.loadFromData(image_data)
                pixmap = QPixmap.fromImage(image)
                self.label_image.setPixmap(pixmap)
               #  # ----------  imageData ----------------------
               #
               #  #------------self.claimTypes------------------
                ##  เอา List ใส่ comBoBox           ------------
                Result = []  # -- ประการค่าเป็น List
                for item in result['claimTypes']:
                    claimType = item['claimType']
                    claimTypeName = item['claimTypeName']
                    #print(f'[{claimType}]:{claimTypeName}')
                    Result.append(f'[{claimType}]:{claimTypeName}')
                self.comboBoxClaimType.clear()
                self.comboBoxClaimType.addItems(Result)
               # #---------- ส่งตัวแปร ให้เป็นค่า Claimtype -------------
                self.claimType = My_LibAuthen.look_claimType(self.comboBoxClaimType.currentText())
               # #------------------------------------------------
                ##  ถ้าเป็นสิทธิ UCS WEL ให้แสด่งค่า HSUB HMAINOP
                if (result['mainInscl'][1:4] == "UCS") or (result['mainInscl'][1:4] == "WEL"):
                    # print(result['mainInscl'][1:4])
                    # hospSub
                    self.hospSub_hcode = result['hospSub']['hcode']
                    self.hospSub_hname = result['hospSub']['hname']
                    # = hospMainOp
                    self.hospMainOp_hcode = result['hospMainOp']['hcode']
                    self.hospMainOp_hname = result['hospMainOp']['hname']
                    # hospMain
                    self.hospMain_hcode = result['hospMain']['hcode']
                    self.hospMain_hname = result['hospMain']['hname']
                    self.lineEditFirst.setText(f'[{self.hospSub_hcode}]:{self.hospSub_hname}')
                    self.lineEditsceond.setText(f'[{self.hospMainOp_hcode}]:{self.hospMainOp_hname}')
                else:
                    # hospSub
                    self.hospSub_hcode = None
                    self.hospSub_hname = None
                    # = hospMainOp
                    self.hospMainOp_hcode = None
                    self.hospMainOp_hname = None
                    # hospMain
                    self.hospMain_hcode = None
                    self.hospMain_hname = None
                    self.lineEditFirst.setText(f'[-]')
                    self.lineEditsceond.setText(f'[-]')
                    ##--------------ค้นหาฐานSqlite---------------------
                    Rectype,pid,tel = My_Lib.Search_idcard(result['pid'])   # ค้าหาค่ามูลว่ามี idcard หรือไม่
                    self.lineEditHN.setText(str(pid))
                    self.lineEditPhone.setText(tel)
                    ##--------------ค้นหาฐานSqlite---------------------
                    if Rectype=="NEW":    # รับค่าที่แจังว่า เป็นผู้รบบริการรายให่ ให้บันทึกค่าใน person_telephone ไว้ด้วย
                        self.check_NEWRec = "NEW"
                    else:
                        self.check_NEWRec = None

    def check_SmartCard(self):
            terminal_name, is_present, sentMessage = My_LibAuthen.get_smartcard()
            self.smart_is_present = is_present
            self.lineEditSmartCard.setText(f'Smartcard รุ่น : {terminal_name} สถานะ : {sentMessage}')
            return None



app = QApplication(sys.argv)
windows = authen_ServiceWindow()
windows.show()
app.exec()

