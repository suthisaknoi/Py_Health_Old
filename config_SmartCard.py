import sys
import pathlib
from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication,QMessageBox,QLabel
from PyQt6.QtGui import QIcon, QAction ,QPixmap
# Load Lib การอ่านบัตร Smartcard ชื่อไฟล์ Lib_ReadSmartCard.py  --------------
from Lib_ReadSmartCard import textCard, photoCard, resizeImg
# Load Lib การอ่านบัตร Smartcard เพื่อตรวจสอบว่ามีเครือ่งอ่าน หรือมีบัตร หรือเปล่า
from smartcard.System import readers
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest

class ReadSmartcard(QtWidgets.QDialog):

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
        self.check_SmartCard()
        if self.code_error == 'YE':    # ตรวจสอบค่า การตรวจว่า มีบัตร และ เครื่องอ่าน หรือไม่..............
            #print("หยุดการทำงา")
            self.lineEdit1.setText("")
            self.lineEdit2.setText("")
            self.lineEdit3.setText("")
            self.lineEdit4.setText("")
            self.lineEdit5.setText("")
            path = "temp/" + "user.png"
            pixmap = QPixmap(path)
            self.label_6.resize(148, 165)
            self.label_6.setPixmap(pixmap)
            self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
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

                self.label_6.resize(148, 165)
                self.label_6.setPixmap(pixmap)
                self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                # a[0]  = cid
                # a[1]  = ชื่อไทย
                # a[2]  = ชื่อ ENg
                # a[3]  = วันเกิด Eng
                # a[4]  = วันเกิด ไทย
                # a[5]  = เพศ
                # a[6]  = สถานที่ออกบัตร
                # a[7]  = cid
                # a[8]  = วันออกบัตร
                # a[9]  = cid
                # a[10]  = วันหมดอายุบัตร
                # a[11]  = ที่อยู่
                # a[12]  = เวลาอ่านบัตร
                # a[13]  = วันเกิด
                # a[14]  = อายุ
                # print(str(fileName[0]))
                # cid = str(a[0])
                # name = a[1]
                nameText = a[11]
                nameText = nameText.replace("#", " ")

                self.lineEdit1.setText(a[0])
                self.lineEdit2.setText(a[1])
                self.lineEdit3.setText(a[3])
                self.lineEdit4.setText(a[5])
                self.lineEdit5.setText(a[7])
                self.lineEditAddress.setText(nameText)

            except:
                try:  # แสดงสถานะเตือนกณีไม่มีข้อมูล

                    self.lineEdit1.setText(a["ไม่มีข้อมูล"])
                    self.lineEdit2.setText(a["ไม่มีข้อมูล"])
                    self.lineEdit3.setText(a["ไม่มีข้อมูล"])
                    self.lineEdit4.setText(a["ไม่มีข้อมูล"])
                    self.lineEdit5.setText(a["ไม่มีข้อมูล"])
                    self.lineEditAddress.setText("ไม่มีข้อมูล")
                except:
                    pass


    def Read_SmartCardTest(self):
        self.check_SmartCard()
        try:
            fileName = a = textCard()
            photoCard(fileName)  # รับอากิวเมน fileName ที่เป็น array โดย photoCard()ทำหน้าที่ดึงรูปและบันทึก
            resizeImg(fileName)  # resizeImg()ทำหน้าที่ปรับขนาดรูปและบันทึก


            # a[0]  = cid
            # a[1]  = ชื่อไทย
            # a[2]  = ชื่อ ENg
            # a[3]  = วันเกิด Eng
            # a[4]  = วันเกิด ไทย
            # a[5]  = เพศ
            # a[6]  = สถานที่ออกบัตร
            # a[7]  = cid
            # a[8]  = วันออกบัตร
            # a[9]  = cid
            # a[10]  = วันหมดอายุบัตร
            # a[11]  = ที่อยู่
            # a[12]  = เวลาอ่านบัตร
            # a[13]  = วันเกิด
            # a[14]  = อายุ
            # print(str(fileName[0]))
            # cid = str(a[0])
            # name = a[1]
            # ename = a[3]

            self.lineEdit1.setText(a[0])
            self.lineEdit2.setText(a[1])
            self.lineEdit3.setText(a[3])
            self.lineEdit4.setText(a[5])
            self.lineEdit5.setText(a[7])


        except:
            try:  # แสดงสถานะเตือนกณีไม่มีข้อมูล
                self.lineEdit1.setText(a["ไม่มีข้อมูล"])
                self.lineEdit2.setText(a["ไม่มีข้อมูล"])
                self.lineEdit3.setText(a["ไม่มีข้อมูล"])
                self.lineEdit4.setText(a["ไม่มีข้อมูล"])
                self.lineEdit5.setText(a["ไม่มีข้อมูล"])
            except:
                pass


    def __init__(self, *args, **kwargs):
        super(ReadSmartcard,self).__init__(*args, **kwargs)
        uic.loadUi("ui/config_Smartcard2.ui", self)
        #-------Load คำสั่งการทำงานครั้งแรกตอนเปิดโปรแกรม   -------------
        # self.initUI()
        # -------Load คำสั่งการทำงานครั้งแรกตอนเปิดโปรแกรม   -------------
        self.pushButton2.clicked.connect(self.Read_SmartCard)  ## กดปุ่ม เพื่ออ่านบัตรประชาชน

        # Display Windows -----
        image_health = str(pathlib.Path(__file__).parent.absolute())+'/images/card-53.png'
        self.setWindowTitle('Test SmartCard Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()
        pass
#
def Main_ReadSmartcard():
    app = QApplication(sys.argv)
    windows = ReadSmartcard()
    app.exit(app.exec())

if __name__ == '__main__':
    Main_ReadSmartcard()