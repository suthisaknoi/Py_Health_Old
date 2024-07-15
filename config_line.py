import sys
import pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from configparser import ConfigParser
#--------------------------------------------
import requests     ##---- การส่งไลน์ ----------
import Lib_Encoding as My_Lib

class Config_LineWindow(QtWidgets.QDialog):

    def save_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        lineInfo = config_object["LINENOTIFYTOKEN"]
        XcheckBoxsentline = self.checkBoxsentline.isChecked()
        if XcheckBoxsentline == True:
            lineInfo["sent_line"] = "True"
        else:
            lineInfo["sent_line"] = "False"
        lineInfo["line_notify_token"] = My_Lib.Encoding(self.lineEditTokenLine.text())

        if ((len(self.lineEditTokenLine.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง และ ถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            # Write changes back to file
             with open(config_file, 'w') as conf:
                config_object.write(conf)
                QMessageBox.information(self, "information", " บันทึกข้อมูลความสำเร็จ             "
                                        , QMessageBox.StandardButton.Ok)
                self.lineEditTokenLine.clear()
                self.checkBoxsentline.setChecked(False)
                #self.labelResultTest.setText('รอแสดงผลทดสอบ....')

    def load_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        # HOSPITAL
        self.lineInfo = config_object["LINENOTIFYTOKEN"]
        # Set Values
        xsentline = self.lineInfo["sent_line"]  #x = self.folderactive.isChecked()
        xtokenline = My_Lib.Decoding(self.lineInfo["line_notify_token"])
        if xsentline == "True":
            self.checkBoxsentline.setChecked(True)
        else:
             self.checkBoxsentline.setChecked(False)
        self.lineEditTokenLine.setText(xtokenline)

    def test_linemessage(self):
        if (len(self.lineEditTestLine.text()) == 0) or (len(self.lineEditTokenLine.text()) == 0):
            QMessageBox.warning(self, "warning", " กรุณากรอกที่ต้องการส่งทดสอบไลน์             ",
                                QMessageBox.StandardButton.Ok)
        else:
            url = 'https://notify-api.line.me/api/notify'
            # token = 'pmxi681pV4aaUhKTbpOpuTKBbmf2EzywZTNZcmzDIjq'  # Line Notify Token
            # token = 'dGH3mEvzkl66osToa3XXeeKF4e0rhlkj892CfeLqoy4'
            token = self.lineEditTokenLine.text()
            headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
            session = requests.Session()
            msg = self.lineEditTestLine.text() + 'จาก :ระบบทดสอบของโปรแกรม '
            print(msg)
            r = requests.post(url, headers=headers, data={'message': msg})
            QMessageBox.information(self, "information", " ส่งข้อความสำเร็จ             "
                                    , QMessageBox.StandardButton.Ok)
            self.lineEditTestLine.clear()

    def __init__(self, *args, **kwargs):
        super(Config_LineWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/config_line2.ui", self)
        # -----------------------------------------

        self.pushButtonSaveConfig.clicked.connect(self.save_message)
        self.pushButtonLoadConfig.clicked.connect(self.load_message)
        self.pushButtonTestDatabase.clicked.connect(self.test_linemessage)

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/line-24.png'
        self.setWindowTitle('Config Line notify Windows')
        self.setWindowIcon(QIcon(image_health))
        #QtWidgets.QWidget.setWindowModality(self, Qt.WindowModality.WindowModal)  # show windows Modal..
        # self.show()
        pass



# def config_linemain():
#     app = QApplication(sys.argv)
#     ex = Config_LineWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     config_linemain()