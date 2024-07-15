import sys
import pathlib
import os
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import *  #QMainWindow, QApplication,QMdiSubWindow
from PyQt6.QtWidgets import *  #QMessageBox
from PyQt6.QtGui import *      # QIcon
# Database -------------------
import sqlite3
#----------------------------
import Lib_Encoding as My_Lib
class User_assignWindow(QtWidgets.QDialog):  # QWidget  QDialog

    def LoadData(self):
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app"
        cursor.execute(query)
        result = cursor.fetchall()
        sqliteConnection.close()
        return result

    def SearchCID(self):
        TextSearch = self.lineEditCid.text()
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app WHERE cid = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        return Rec_user
    def SearchEMAIL(self):
        TextSearch = self.lineEditEmail.text()
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app WHERE email = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        return Rec_user

    def SearchUserName(self):
        TextSearch = self.lineEditUser.text()
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM user_app WHERE user_name = '" + TextSearch + "'"
        cursor.execute(query)
        Rec_user = cursor.fetchone()
        sqliteConnection.commit()
        sqliteConnection.close()
        return Rec_user



    def Search_User(self):
        if not self.lineEditSearchName.text():
            QMessageBox.information(self, "Warning", " ช่องค้นหา Email/ต้องเป็นว่าง กรอกข้อความที่ต้องการค้นหา ",
                                    QMessageBox.StandardButton.Ok)
        else:
            TextSearch =self.lineEditSearchName.text()
            TextSearch = TextSearch.replace(" ", "")
            DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
            sqliteConnection = sqlite3.connect(DataPath)
            cursor = sqliteConnection.cursor()
            query = "SELECT * FROM user_app WHERE email = '"+TextSearch+"'"
            cursor.execute(query)
            #Rec_user = cursor.fetchall()
            Rec_user = cursor.fetchone()
            #print(Rec_user)
            if not Rec_user:
                QMessageBox.information(self, "Warning", " ไม่พบข้อมูลที่ค้นหา.. กรุณาลองใหม่ ",
                                            QMessageBox.StandardButton.Ok)
            else:
                self.lineEditCid.setText(Rec_user[0])
                self.CID_PERSON = Rec_user[0]          # = ประกาศค่าตัวแปร เลข 13 หลักไว้ก่อน
                self.lineEditName.setText(Rec_user[1])
                self.lineEditUser.setText(Rec_user[3])
                self.lineEditPass.setText(My_Lib.Decoding(Rec_user[4]))
                self.lineEditEmail.setText(Rec_user[2])
                self.comboBoxType.setCurrentText(Rec_user[5])
                self.comboBoxStatus.setCurrentText(Rec_user[6])
    def Delete_User(self):
        if not self.lineEditCid.text():
            QMessageBox.information(self, "Warning", " ไม่พบข้อมูลที่ต้องการลบ กรุณาค้นหาข้อมูลก่อน ",
                                    QMessageBox.StandardButton.Ok)
        else:
            DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
            sqliteConnection = sqlite3.connect(DataPath)
            cursor = sqliteConnection.cursor()
            query = "DELETE FROM user_app WHERE cid = '"+self.lineEditCid.text()+"'"
            selected_option = QMessageBox.warning(self, "Warning", "ต้องการลบข้อมูลที่อยู่หน้าจอนี้หรือไม่ กรุณา Yes เพื่อยืนยัน?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if selected_option == QMessageBox.StandardButton.Yes:
                cursor.execute(query)
                sqliteConnection.commit()
                sqliteConnection.close()
                QMessageBox.information(self, "Warning", "ข้อมูลถูกลบเรียบร้อยแล้ว....",
                                        QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.information(self, "Warning", "ข้อมูลถูกยกเลิกเรียบร้อยแล้ว....(ไม่มีการลบข้อมูล)",
                                        QMessageBox.StandardButton.Ok)
        self.Clear_date()  # --- ล้างข้อมูล  --------------
        self.load_Data()   # --- ดึงข้อมูลในตารางใหม่อีกครั้ง ---

    def Update_data(self):
        DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        sqliteConnection = sqlite3.connect(DataPath)
        cursor = sqliteConnection.cursor()
        if self.lineEditSearchName.text():
            cid =self.CID_PERSON
            ##---- ตรวจสอบ อีเมส และ User ใหม่------------

            name = self.lineEditName.text()
            #email = self.lineEditEmail.text()
            #xuser = self.lineEditUser.text()
            #xpass = self.lineEditPass.text()
            xtype = self.comboBoxType.currentText()
            xstatus = self.comboBoxStatus.currentText()
            query = "UPDATE user_app SET name=?,type_user=?,status_user=? WHERE cid = ?"
            cursor.execute(query, (name, xtype, xstatus,cid))
            sqliteConnection.commit()
            sqliteConnection.close()
            QMessageBox.information(self, "Warning", " บันทึกการปรับปรุงข้อมูลชุดนี้ เรียบร้อยแล้ว ",
                                    QMessageBox.StandardButton.Ok)
            self.Clear_date()
        else:   ##-------------- ทำการบันทึกข้อมูลใหม่ เงือนไข เพราะ lineEditSearchName เป็นช่องว่าง..-------------
            if ((len(self.lineEditCid.text()) == 0) or (len(self.lineEditName.text()) == 0)
                    or (len(self.lineEditEmail.text()) == 0) or (len(self.lineEditUser.text()) == 0)
                    or (len(self.lineEditPass.text()) == 0) or (str(self.comboBoxType.currentIndex())=="0")
                    or (str(self.comboBoxStatus.currentIndex())=="0")):
                QMessageBox.information(self, "Warning", "กรุณากรอกข้อมูลให้ครบทุกช่อง และเลือก สิทธิเข้าถึง และสถานะการใช้งาน",
                                        QMessageBox.StandardButton.Ok)
            else:
                CheakCID = self.SearchCID()          ## ตรวจสอบเลข 13 หลักซ้ำซ้อน
                CheakEMAIL = self.SearchEMAIL()      ## ตรวจสอบ อีเมส ซ้ำซ้อน
                CheckUserName = self.SearchUserName()  ## ตรวจสอบ UserName ซ้ำซ้อน
                if CheakCID:
                    QMessageBox.information(self, "Warning",
                                            "มีการบันทึกเลขบัตรประชาชนซ้ำซ้อน.. ไม่สามารถบันทึกข้อมูลได้ กรุณาตรวจสอบแก้ไข",
                                            QMessageBox.StandardButton.Ok)
                else:
                    if CheakEMAIL:
                        QMessageBox.information(self, "Warning",
                                                "มีการบันทึกอีเมส์ซ้ำซ้อน.. ไม่สามารถบันทึกข้อมูลได้ กรุณาตรวจสอบแก้ไข",
                                                QMessageBox.StandardButton.Ok)
                    else:
                        if CheckUserName:
                            QMessageBox.information(self, "Warning",
                                                    "มีการบันทึก User Name ซ้ำซ้อน.. ไม่สามารถบันทึกข้อมูลได้ กรุณาตรวจสอบแก้ไข",
                                                    QMessageBox.StandardButton.Ok)
                        else:
                            cid=self.lineEditCid.text()
                            name=self.lineEditName.text()
                            email=self.lineEditEmail.text()
                            xuser=self.lineEditUser.text()
                            xpass= My_Lib.Encoding(self.lineEditPass.text())
                            xtype=self.comboBoxType.currentText()
                            xstatus=self.comboBoxStatus.currentText()
                            query = "INSERT INTO user_app (cid, name, email ,user_name ,pass_user,type_user,status_user) VALUES (?,?,?,?,?,?,?)"
                            cursor.execute(query,(cid, name, email,xuser,xpass,xtype,xstatus))
                            sqliteConnection.commit()
                            sqliteConnection.close()
                            QMessageBox.information(self, "Warning", " บันทึกข้อมูลชุดใหม่ เรียบร้อยแล้ว ",
                                                    QMessageBox.StandardButton.Ok)
                            self.Clear_date()
        #----  Update ข้อมูลในตารางให้ เป็นข้อมูลใหม่ เสมอ
        self.load_Data()

    def Clear_date(self):
        self.lineEditCid.clear()
        self.lineEditName.clear()
        self.lineEditUser.clear()
        self.lineEditPass.clear()
        self.lineEditEmail.clear()
        self.lineEditSearchName.clear()
        #print(str(self.comboBoxType.currentIndex()))
        self.comboBoxType.setCurrentIndex(0)
        self.comboBoxStatus.setCurrentIndex(0)

    def remove_item(self):
        filaSeleccionada = self.tableWidgetUser.selectedItems()
        if filaSeleccionada:
            fila = filaSeleccionada[0].row()
            self.tableWidgetUser.removeRow(fila)
            self.tabla.clearSelection()
    def load_Data(self):
        ##---------- Remove ------------
        for i in reversed(range(self.tableWidgetUser.rowCount())):
            self.tableWidgetUser.removeRow(i)
        ##---------- Remove ------------
        User = self.LoadData()
        rowPosition = self.tableWidgetUser.rowCount()
        #print(rowPosition)
        for row in User:
            #print(row)
            #print(rowPosition)
            self.tableWidgetUser.insertRow(rowPosition)
            self.tableWidgetUser.setItem(rowPosition, 0, QTableWidgetItem(row[1]))
            self.tableWidgetUser.setItem(rowPosition, 1, QTableWidgetItem(row[2]))
            self.tableWidgetUser.setItem(rowPosition, 2, QTableWidgetItem(row[3]))
            self.tableWidgetUser.setItem(rowPosition, 3, QTableWidgetItem(row[5]))
            self.tableWidgetUser.setItem(rowPosition, 4, QTableWidgetItem(row[6]))



    def cell_was_double_clicked(self, row, column):
        item_id = self.tableWidgetUser.item(row, 1).text()
        print(item_id)
        # ##----------
        self.lineEditSearchName.setText(item_id)        # ส่งค่าไป เพื่อให้ ตรวจสอบเรื่อง การ Update หรือ เพิ่มใหม่...
        self.Search_User()
        # ##---------
        # DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
        # sqliteConnection = sqlite3.connect(DataPath)
        # cursor = sqliteConnection.cursor()
        # query = "SELECT * FROM user_app WHERE email = '" + item_id + "'"
        # cursor.execute(query)
        # Rec_user = cursor.fetchone()
        # self.lineEditCid.setText(Rec_user[0])
        # self.CID_PERSON = Rec_user[0]  # = ประกาศค่าตัวแปร เลข 13 หลักไว้ก่อน
        # self.lineEditName.setText(Rec_user[1])
        # self.lineEditUser.setText(Rec_user[3])
        # self.lineEditPass.setText(My_Lib.Decoding(Rec_user[4]))
        # self.lineEditEmail.setText(Rec_user[2])
        # self.comboBoxType.setCurrentText(Rec_user[5])
        # self.comboBoxStatus.setCurrentText(Rec_user[6])


    # def closeEvent(self, event):
    #     self.sqliteConnection.close()

    def __init__(self, *args, **kwargs):
        super(User_assignWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/user_assign.ui", self)

        # Path DataBase Sqlite #-------------------
        self.DataPath = str(pathlib.Path(__file__).parent.absolute())+'/SQLite/HealthDB.db'
        isFile = os.path.isfile(self.DataPath)
        if not isFile:
            QMessageBox.information(self, "Warning", "ไม่พบไฟล์ฐานข้อมูล ในการเก็บข้อมูล HealthDB.db ",
                                    QMessageBox.StandardButton.Ok)
        else:
            sqliteConnection = sqlite3.connect(self.DataPath)        # เชื่อมต่อ Database
            try:
                cursor = sqliteConnection.cursor()
                # display version
                query = 'select sqlite_version();'
                cursor.execute(query)
                # get data
                record = cursor.fetchall()
                self.labelVersionSqlite.setText(f'SQLite Version - {record}')
                cursor.close()
                sqliteConnection.commit()
                sqliteConnection.close()

            except sqlite3.Error as error:
                print('Error occurred - ', error)
            finally:
                # If the connection was established then close it
                if sqliteConnection:
                    sqliteConnection.close()
                    #print('SQLite Connection closed')
        # Path DataBase Sqlite #-------------------
        ##-------- กำหนดขนาดของตารางแสดงผล List ----------------------------
        self.tableWidgetUser.setColumnWidth(0,180)
        self.tableWidgetUser.setColumnWidth(1,180)
        self.tableWidgetUser.setColumnWidth(2,150)
        self.tableWidgetUser.setColumnWidth(3,150)
        self.tableWidgetUser.setColumnWidth(4,150)
        # self.tableWidgetUser.setAlternatingRowColors(True)
        ##-------- กำหนดให้มีการ double_clicked Row ในตาราง  ----------------------------
        self.tableWidgetUser.cellDoubleClicked.connect(self.cell_was_double_clicked)

        self.pushButtonLoadConfig.clicked.connect(self.Search_User)    ## กดปุ่ม
        self.pushButtonDelete.clicked.connect(self.Delete_User)  ## กดปุ่ม
        self.pushButtonClearData.clicked.connect(self.Clear_date)  ## กดปุ่ม
        self.pushButtonSaveData.clicked.connect(self.Update_data)  ## กดปุ่ม
        self.pushButtonListData.clicked.connect(self.load_Data)  ## กดปุ่ม

        # Display Windows -----
        image_health = str(pathlib.Path(__file__).parent.absolute())+'/images/health24.png'
        # self.setGeometry(QtCore.QRect(545, 310, 830, 460))
        self.setWindowTitle('การกำหนดสิทธิการใช้งาน Windows')
        self.setWindowIcon(QIcon(image_health))

        self.show()
        pass


# app = QApplication(sys.argv)
# windows = User_assignWindow()
# windows.show()
# app.exec()

def about_devmain():
    app = QApplication(sys.argv)
    ex = User_assignWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    about_devmain()


