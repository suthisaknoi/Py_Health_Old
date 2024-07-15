import sys
import pathlib
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication,QMdiSubWindow,QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
#----- Lib_MyLib    เป็น Function เพื่อ่ใช้งาน
import Lib_MyLib as MyLib
#------------------
import load_splash as Splash
import Login_App as login_App
import change_password as changPass
##---------Work---------------------
import register_person as RegPerson
##--------About --------------------
import about_dev as DevWindow
import about_application as AboutApp
import config_SmartCard as ReadSmart
##--------Config -------------------
import config_hospital as ConHospital
import config_mysql as ConMySQL
import config_line as ConLine
import config_AddUser as Add_User
##-----------Super Admin ----------
import Super_TranferPerson as TranPerson
import gen_code_useapp as Gen_Code


# import config_SuperAdmin as ConSuper
# import config_register_App as Reg_App



#-----------------

class MainWindows(QtWidgets.QMainWindow): #, QApplication ,QMainWindow

    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("ui/Main_App.ui", self)
        ##==============ประกาศตัวแปร==============================
        self.USERtoLOGIN        = "Null"
        self.USERtoLOGIN_type   = "Null"
        self.USERtoLOGIN_status = "Null"
        self.HCODE_app          = "Null"
        self.HNAME_app          = "Null"
        self.STATUSAPP_ligin    = False


        #-------Load คำสั่งการทำงานครั้งแรกตอนเปิดโปรแกรม   -------------
        self.initUI()


        # -------Load คำสั่งการทำงานครั้งแรกตอนเปิดโปรแกรม   -------------
        self.setWindowTitle('Main Windows')
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        QtWidgets.QWidget.setWindowModality(self,Qt.WindowModality.WindowModal)

        print(self.isModal())
        self.show()

    def initUI(self):   # แสดงปุ่มคลิ๊ก ในเมนู โปรแกรม
        # Exit ----------
        self.ButtonLogoutClick()

        self.actionExit.triggered.connect(self.FClose)                                          # ออกจากโปรแกรม ==
        self.actionDeveloper.triggered.connect(self.Buttonabout_DeveloperClick)                 # เรียกใช้งาน about_Developer.py
        self.actionApplication.triggered.connect(self.Buttonabout_ApplicationClick)             # เรียกใช้งาน about_developer.py
        self.actionTest_Smart_Card.triggered.connect(self.ButtonRead_SmartcardClick)            # เรียกใช้งาน config_SmartCard.py

        self.actionMySql.triggered.connect(self.ButtonConfig_MysqlClick)                        # เรียกใช้งาน config_Mysql.py
        self.actionHospital.triggered.connect(self.ButtonConfig_HospitalClick)                  # เรียกใช้งาน config_hispital.py
        self.actionLine_notify.triggered.connect(self.ButtonLine_notifylClick)                  # เรียกใช้งาน config_Line.py
        self.action_User.triggered.connect(self.ButtonUser_AddlClick)  # เรียกใช้งาน config_Line.py



        #self.actionReguest_Approved_Code.triggered.connect(self.ButtonRequest_ApprovedClick)    # เรียกใช้งาน Request_Approved.py
        #self.actionRegister_Application_2.triggered.connect(self.ButtonPost_register_CodeClick)  # เรียกใช้งาน register_Code.py

        self.actionChangPass.triggered.connect(self.ButtonChangPassClick)  # เรียกใช้งาน change_password.py
        self.actionLogin.triggered.connect(self.ButtonLoginClick)      # เรียกใช้งาน logine.py
        self.actionLogout.triggered.connect(self.ButtonLogoutClick)  # เรียกใช้งาน logout.py

        self.actionPatient.triggered.connect(self.ButtonRegisterPersonClick)  # เรียกใช้งาน logout.py

        ##------Super Admin -----------------------------------
        self.action_Person_Jhcis.triggered.connect(self.ButtonTranferPersonMyTOSqlite)  # เรียกใช้งาน super_tranferPerson.py
        self.actionGen_Code_Approve.triggered.connect(self.ButtonGenCodeApp)  # เรียกใช้งาน super_tranferPerson.py

        #################################
        ##login_windows
        #print(login_windows.CHeckRight)
        #################################

    def FClose(self):
        reply = QMessageBox.question(self, 'Question', 'คุณต้องการออกจากโปรแกรม..ใช่หรือไม่.?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()


    def ButtonLogoutClick(self):
        self.labelNameUser.setText("ผู้เข้าใช้งาน : Null")
        self.labelTypeUser.setText("สิทธิการใช้งาน ของผู้ใช้งาน : Null")
        #self.menuSetting.setEnabled(False)
        #self.menuWork.setEnabled(False)
        self.menuSetting.setEnabled(True)
        self.menuWork.setEnabled(True)
        ## ----- ซ่อน ปุ่มเข้าระบบ------
        self.actionChangPass.setVisible(False)
        self.actionLogout.setVisible(False)
        self.actionLogin.setVisible(True)

    def ButtonGenCodeApp(self):
        self.GecCodeApp = Gen_Code.Gen_CodeWindow()
        self.GecCodeApp.exec()

        
    def ButtonRegisterPersonClick(self):
        self.RegPerson = RegPerson.Register_personWindow()
        self.RegPerson.exec()


    def ButtonTranferPersonMyTOSqlite(self):
        self.TranPersonWindows = TranPerson.Super_TranferPersonWindow()
        self.TranPersonWindows.exec()




    def ButtonLoginClick(self):
        self.loginApp = login_App.login_windows()
        self.loginApp.exec()
        ##--------- ส่งค่าตัวแปร ให้ กับ main_windows --------------
        # self.loginApp.usercid
        # self.loginApp.nameuser
        self.USERtoLOGIN_status = self.loginApp.userstatus
        self.USERtoLOGIN        = self.loginApp.username
        self.USERtoLOGIN_type   = self.loginApp.usertype

        self.labelNameUser.setText("ผู้เข้าใช้งาน : "+self.loginApp.nameuser)
        self.labelTypeUser.setText("สิทธิการใช้งาน ของผู้ใช้งาน : " + self.loginApp.usertype)
        self.STATUSAPP_ligin = MyLib.Check_Login(self.labelTypeUser.text())         #--- ตรวจสอบสถาน type ของ User ที่ login  result_login

        if self.STATUSAPP_ligin == False:
            self.labelNameUser.setText("ผู้เข้าใช้งาน : " + self.loginApp.nameuser)
            self.labelTypeUser.setText("สิทธิการใช้งาน ของผู้ใช้งาน : " + self.loginApp.usertype)
           # QMessageBox.warning(self, "Warning", " Error การ Login ไม่สำเร็จ.. ติดต่อผู้พัฒนาระบบ ",
           #                         QMessageBox.StandardButton.Ok)
        else:
            if not self.USERtoLOGIN_status == "ใช้งาน":
                self.labelTypeUser.setText("สถานะการใช้งานขณะนี้ ถูกระงับการเข้าใช้งาน กรุณาติดต่อผู้ดูแลระบบของท่านเอง")
            else:
                ## ----- ซ่อน ปุ่มเข้าระบบ------
                self.actionChangPass.setVisible(True)
                self.actionLogout.setVisible(True)
                self.actionLogin.setVisible(False)

                if self.loginApp.usertype == "Admin":
                     self.menuSetting.setEnabled(True)
                     self.menuWork.setEnabled(True)
                else:
                     self.menuSetting.setEnabled(False)
                     self.menuWork.setEnabled(True)


    def ButtonChangPassClick(self):
        self.WindowsChangPass = changPass.Change_PasswordWindow()
        self.WindowsChangPass.userToLogin = self.USERtoLOGIN
        self.WindowsChangPass.exec()



    def ButtonUser_AddlClick(self):
        self.windowUser_Add = Add_User.User_assignWindow()
        self.windowUser_Add.exec()


    def Buttonabout_DeveloperClick(self):
        self.windowAbout_Dev = DevWindow.About_DevWindow()
        self.windowAbout_Dev.exec()

    def Buttonabout_ApplicationClick(self):
        self.windowsAbout = AboutApp.About_ApplicationWindow()
        self.windowsAbout.exec()

    def ButtonConfig_HospitalClick(self):
        self.windowConfig_hos = ConHospital.Config_HospitalWindow()
        self.windowConfig_hos.exec()


    def ButtonConfig_MysqlClick(self):
        self.windowConfig_MySQL = ConMySQL.Config_MysqlWindow()
        self.windowConfig_MySQL.exec()

    def ButtonLine_notifylClick(self):
        self.windowLine = ConLine.Config_LineWindow()
        self.windowLine.exec()

    def ButtonRead_SmartcardClick(self):
        self.windowRead_Smartcard = ReadSmart.ReadSmartcard()
        self.windowRead_Smartcard.exec()

    # def ButtonRequest_ApprovedClick(self):
    #     self.windowReg_superAdmin = ConSuper.Config_superadminWindows()
    #     self.windowReg_superAdmin.exec()

    # def ButtonPost_register_CodeClick(self):
    #     self.windowReg_App = Reg_App.Register_AppWindow()
    #     self.windowReg_App.exec()


# app = QtWidgets.QApplication([])
# windows = MainWindows()
# windows.show()
# app.exec_()

def Main():
    app = QApplication(sys.argv)
    splash = Splash.SplashWindow()
    windows = MainWindows()
    splash.show()
    splash.progress()
    splash.close()
    windows.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    Main()
