import sys
import pathlib
import requests                            ## Sent Line
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
#-------------------
import smtplib, ssl
from email.message import EmailMessage  ## Mail..
#-------------------
from winotify import Notification  # แสดง Notification ใน Task ด้านล่าง ---

class About_DevWindow(QtWidgets.QDialog):    # QWidget  QDialog
    def notifi(self):
        xFolderFile = str(pathlib.Path(__file__).parent.resolve())+"/ui/images/developer60.png"
        xapp_id = "ระบบสารสนเทศเพื่อสุขภาพ"
        xtitle = "ส่งไลน์ หรือ อีเมส์ เพื่อพัฒนา"
        xmsg = "ถ้าต้องการเสนอแนะ หรือติดต่อเพื่อให้ข้อมูลในการพัฒนาระบบต่าง ๆให้ดีขึ้น เพื่อเป็นประโยชน์ต่อการพัฒนาโปรแกรมฯ ต่อไป"
        show_notifi = Notification(app_id=xapp_id,
                                   title=xtitle,
                                   msg=xmsg,
                                   icon=xFolderFile
                                   )
        show_notifi.add_actions(label="เยี่ยมชมเวปไซค์ได้ที่นี่..!",
                          launch="https://phitsanulok.nhso.go.th/FrontEnd/Default.aspx")
        show_notifi.show()

    def sent_message(self):
        url = 'https://notify-api.line.me/api/notify'
        # token = 'pmxi681pV4aaUhKTbpOpuTKBbmf2EzywZTNZcmzDIjq'  # Line Notify Token
        token = 'dGH3mEvzkl66osToa3XXeeKF4e0rhlkj892CfeLqoy4'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        session = requests.Session()
        msg = self.lineEditmassage.text() + '  จาก :' + self.lineEditmassage2.text()

        if ((len(self.lineEditmassage.text()) == 0) and (len(self.lineEditmassage2.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรอกข้อมูลข้อความที่ต้องการส่ง และ กรุณากรอกข้อมูลเบอร์โทร/line ID             ",
                                    QMessageBox.StandardButton.Ok)
            # self.show_popup_message3()
        elif ((len(self.lineEditmassage.text()) == 0) and (len(self.lineEditmassage2.text()) != 0)):
            QMessageBox.warning(self, "warning"," กรุณากรอกข้อมูลข้อความที่ต้องการส่ง             ",
                                    QMessageBox.StandardButton.Ok)
            #self.show_popup_message1()
        elif ((len(self.lineEditmassage.text()) != 0) and (len(self.lineEditmassage2.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลเบอร์โทร/line ID             ",
                                    QMessageBox.StandardButton.Ok)
        elif  ((len(self.lineEditmassage.text()) != 0) and (len(self.lineEditmassage2.text()) != 0)):
            r = requests.post(url, headers=headers, data={'message': msg})
            # self.show_popup()
            QMessageBox.information(self, "information", " ส่งข้อความสำเร็จ             ",QMessageBox.StandardButton.Ok)
            self.lineEditmassage.clear()
            self.lineEditmassage2.clear()

    def sent_mail(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "testnhso2@gmail.com"  # Enter your address
        receiver_email = "suthisak.noi@gmail.com"  # Enter receiver address
        password = "ioqzuvntmbsehrup"

        msg = EmailMessage()

        mytext = str(self.textEditMail.toPlainText())            ## การแปลง Text ให้แสดงเป็นข้อความต่าง ๆ
        msg.set_content(mytext)

        #msg.set_content(mytext)
        msg['Subject'] = "ส่งข้อความเสนอแนะ/ให้คำแนะนำ จาก App Python!"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        if  len(mytext) == 0:
            QMessageBox.warning(self, "Warning", " กกรอกข้อมูลข้อความเมส์ที่ต้องการส่ง (สามารถพิมพ์ได้หลายบรรทัด) ",
                                    QMessageBox.StandardButton.Ok)
            #self.show_popup_mail()
        else:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
            #self.show_popup()
            QMessageBox.information(self, "information", " ส่งข้อความสำเร็จ             ",QMessageBox.StandardButton.Ok)
            self.textEditMail.clear()
        
    def __init__(self, *args, **kwargs):
        super(About_DevWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/about_dev2.ui", self)
        self.textEditMail.setPlaceholderText("กรุณากรอกข้อความเพื่อส่งเมส์")  # ทำตัวอักษรจางๆ ให้เป็นแนวทางการพิมพ์
        self.lineEditmassage.setPlaceholderText("กรุณากรอกข้อความส่งไลน์")  # ทำตัวอักษรจางๆ ให้เป็นแนวทางการพิมพ์
        self.lineEditmassage2.setPlaceholderText("เบอร์โทร/Line ID")  # ทำตัวอักษรจางๆ ให้เป็นแนวทางการพิมพ์

        #------ Notifi ----------------
        self.notifi()
        # ------ Notifi ----------------
        self.pushButtonSent.clicked.connect(self.sent_message)    ## กดปุ่ม เพื่อส่งข้อมูลทางไลน์
        self.pushButtonSentMail.clicked.connect(self.sent_mail)  ## กดปุ่ม เพื่อส่งข้อมูลทางเมส์
        # Display Windows -----
        image_health = str(pathlib.Path(__file__).parent.absolute())+'/images/health24.png'
        self.setWindowTitle('About Dev Windows')
        self.setWindowIcon(QIcon(image_health))
        #self.show()
        pass


# app = QApplication(sys.argv)
# windows = About_DevWindow()
# windows.show()
# app.exec()

# def about_devmain():
#     app = QApplication(sys.argv)
#     ex = About_DevWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     about_devmain()


