import sys
import pathlib
import os
#-------------------
from PyQt6 import QtWidgets, uic, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication,QMdiSubWindow,QMessageBox
from PyQt6.QtGui import *               # QIcon
# Database -------------------
import sqlite3
#----------------------------
import Lib_Encoding as My_Lib
class Change_PasswordWindow(QtWidgets.QDialog):  # QWidget  QDialog
    def SearchUserName(self,UseName):
        TextSearch = UseName
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app WHERE user_name = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        return Rec_user

    def Save_changPass(self):
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(self.userToLogin)
        if ((len(self.lineEditOld.text()) == 0) or (len(self.lineEditNew.text()) == 0) or (len(self.lineEditConfirm.text()) == 0)):
            QMessageBox.warning(self, "Warning",
                                "กรอกรหัสที่ต้องการเปลี่ยนให้ครบตามข้อกำหนด ทั้ง 3 ช่อง",
                                QMessageBox.StandardButton.Ok)
        else:
            if len(self.lineEditNew.text()) < 6:
                QMessageBox.warning(self, "Warning",
                                    "รหัสใหม่ที่ต้องการเปลี่ยน ต้องมีจำนวนตัวอักษร มากกว่า 6 ตัวอักษรขึ้นไป",
                                    QMessageBox.StandardButton.Ok)
            else:
                checkUser = self.SearchUserName(self.userToLogin)
                Xpass = My_Lib.Decoding(checkUser[4])
                oldpass = self.lineEditOld.text()
                if Xpass != oldpass:
                    QMessageBox.warning(self, "Warning",
                                            "กรอกรหัสผ่านเก่าไม่เหมือนที่ให้เคยไว้ กรุณาลองใหม่..",
                                            QMessageBox.StandardButton.Ok)
                else:
                    if self.lineEditNew.text() != self.lineEditConfirm.text():
                        QMessageBox.warning(self, "Warning",
                                            "รหัสใหม่ และ การยืนยันรหัสใหม่ ไม่เหมือนกัน กรุณากรอกให้ตรงกัน",
                                            QMessageBox.StandardButton.Ok)
                    else:
                        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
                        sqliteConnection = sqlite3.connect(DataPath)
                        cursor = sqliteConnection.cursor()
                        Xpass_user = My_Lib.Encoding(self.lineEditNew.text())
                        Xuser_name = self.userToLogin
                        query = "UPDATE user_app SET pass_user=? WHERE user_name = ?"
                        cursor.execute(query, (Xpass_user, Xuser_name))
                        sqliteConnection.commit()
                        sqliteConnection.close()
                        QMessageBox.information(self, "Warning", " บันทึกข้อมูลชุดใหม่ เรียบร้อยแล้ว ",
                                                QMessageBox.StandardButton.Ok)
                        self.close()


    def __init__(self, *args, **kwargs):
        super(Change_PasswordWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/change_password.ui", self)
        # --------------กำหนดค่าเริ่มต้น  ---------------------------
        self.userToLogin = "Null"

        # self.SearchUserName(username)
        # print(RegisterPerson.MessageSearch)
        #self.ReturnMessageSearch = "Defult"
        # # -----------------------------------------
        #
        # self.pushButtonREadSmartCard.clicked.connect(self.Read_SmartCard)
        self.pushButtonSave.clicked.connect(self.Save_changPass)

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/changPass40.png'
        self.setWindowTitle('Change Password Windows')
        self.setWindowIcon(QIcon(image_health))
        # self.show()

# app = QApplication(sys.argv)
# windows = Change_PasswordWindow()
# windows.show()
# app.exec()

