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
import Lib_gencode as My_Libgen
class Gen_CodeWindow(QtWidgets.QDialog):  # QWidget  QDialog

    def ClearData(self):
        self.lineEdithcode.clear()
        self.lineEditcodegen.clear()
        return None

    def Gen_Code(self):
        if ((len(self.lineEdithcode.text()) == 0) and (len(self.lineEditcodegen.text()) == 0)):
            QMessageBox.warning(self, "Warning",
                                "กรุณากรอกข้อมูลช่องใด ช่องหนึ่ง เพื่อจัดทำชุดตัวเลข หรือ ถอดรหัสชุดตัวเลข",
                                QMessageBox.StandardButton.Ok)
        else:
            if ((len(self.lineEdithcode.text()) != 0) and (len(self.lineEditcodegen.text()) != 0)):
                QMessageBox.warning(self, "Warning",
                                    "กรุณากรอกข้อมูลช่องใด ช่องหนึ่ง ต้องไม่กรอกทั้งสองชุดข้อมูล",
                                    QMessageBox.StandardButton.Ok)
            else:
                 if ((len(self.lineEdithcode.text()) != 0) and (len(self.lineEditcodegen.text()) == 0)):
                         if len(self.lineEdithcode.text()) != 5:
                             QMessageBox.warning(self, "Warning",
                                                 "กรุณากรอกข้อมูลรหัสหน่วยบริการให้ครบ 5 หลัก",
                                                 QMessageBox.StandardButton.Ok)
                         else:
                            code_den = My_Libgen.ENmix_hcodeTOstring(self.lineEdithcode.text())
                            self.lineEditcodegen.setText(code_den)
                 else:
                     if ((len(self.lineEdithcode.text()) == 0) and (len(self.lineEditcodegen.text()) != 0)):
                        ed_code =  My_Libgen.DEmix_hcodeTOstring(self.lineEditcodegen.text())
                        self.lineEdithcode.setText(ed_code)


    def __init__(self, *args, **kwargs):
        super(Gen_CodeWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/gen_codeUseApp.ui", self)
        # --------------กำหนดค่าเริ่มต้น  ---------------------------
        # self.userToLogin = "Null"

        # self.SearchUserName(username)
        # print(RegisterPerson.MessageSearch)
        #self.ReturnMessageSearch = "Defult"
        # # -----------------------------------------
        #
        self.pushButtongencode.clicked.connect(self.Gen_Code)
        self.pushButtonclear.clicked.connect(self.ClearData)

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/changPass40.png'
        self.setWindowTitle('Gen Code Windows')
        self.setWindowIcon(QIcon(image_health))
        # self.show()

# app = QApplication(sys.argv)
# windows = Gen_CodeWindow()
# windows.show()
# app.exec()

