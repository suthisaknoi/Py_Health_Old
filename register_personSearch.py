import sys
import pathlib
import os
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot # ---  การส่งข้อมูลกลับ
from PyQt6.QtWidgets import *           #QMainWindow, QApplication,QMdiSubWindow
from PyQt6.QtWidgets import *           #QMessageBox
from PyQt6.QtGui import *               # QIcon
# Database -------------------
import sqlite3

class Register_SearchpersonWindow(QtWidgets.QDialog):  # QWidget  QDialog



    def __init__(self, *args, **kwargs):
        super(Register_SearchpersonWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/register_search.ui", self)
        # --------------เรียกใช้ค่าที่ส่งไป Windows ที่ 2  ---------------------------
        # print(RegisterPerson.MessageSearch)
        self.ReturnMessageSearch = "Defult"
        # # -----------------------------------------
        #
        # self.pushButtonREadSmartCard.clicked.connect(self.Read_SmartCard)
        # self.pushButtonSaveRegister.clicked.connect(self.Save_Register)
        ##-------- กำหนดให้มีการ double_clicked Row ในตาราง  ----------------------------
        self.tableWidgetUser.cellDoubleClicked.connect(self.cell_was_double_clicked)
        ##-------- กำหนดให้มีการ การทำงานของปุ่ม เพื่อค้นหาข้อมูล  ----------------------------
        self.pushButtonSearch.clicked.connect(self.search_person)
        ## -----  กำหนดขนาดของช่องตาราง  -----------------------------------------------
        self.tableWidgetUser.setColumnWidth(0, 150)
        self.tableWidgetUser.setColumnWidth(1, 150)
        self.tableWidgetUser.setColumnWidth(2, 150)
        self.tableWidgetUser.setColumnWidth(3, 50)
        self.tableWidgetUser.setColumnWidth(4, 200)
        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/writer-male-48.png'
        self.setWindowTitle('Search Register Person Windows')
        self.setWindowIcon(QIcon(image_health))
        # self.show()



    def search_person(self):
        if not self.lineEditSearch.text():
            QMessageBox.warning(self, "Warning", " กรอกข้อความที่ต้องการค้นหา [บางส่วนของชื่อ หรือ นามสกุล] ",
                                    QMessageBox.StandardButton.Ok)
        else:
            TextSearch =self.lineEditSearch.text()
            TextSearch = TextSearch.replace(" ", "")
            DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
            sqliteConnection = sqlite3.connect(DataPath)
            cursor = sqliteConnection.cursor()
            query = "SELECT idcard,fname,lname,sex,right_health FROM person WHERE fname like '%"+TextSearch+"%' or lname like '%"+TextSearch+"%'"
            cursor.execute(query)
            Rec_user = cursor.fetchall()
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
                    self.tableWidgetUser.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
                    self.tableWidgetUser.setItem(rowPosition, 1, QTableWidgetItem(row[1]))
                    self.tableWidgetUser.setItem(rowPosition, 2, QTableWidgetItem(row[2]))
                    self.tableWidgetUser.setItem(rowPosition, 3, QTableWidgetItem(row[3]))
                    self.tableWidgetUser.setItem(rowPosition, 4, QTableWidgetItem(row[4]))
            else:
                QMessageBox.warning(self, "Warning", f"ค้นหา[ {TextSearch} ] แล้ว..ไม่พบข้อมูลที่ต้องการค้นหา ",
                                        QMessageBox.StandardButton.Ok)

    def cell_was_double_clicked(self, row, column):
        self.ReturnMessageSearch = self.tableWidgetUser.item(row, 0).text()
        self.close()
        return self.ReturnMessageSearch






    # def register_main():
#     app = QApplication(sys.argv)
#     ex = Register_SearchpersonWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     register_main()
