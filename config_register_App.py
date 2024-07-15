import sys
import pathlib
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from configparser import ConfigParser
#--------------------------------------------

class Register_AppWindow(QtWidgets.QDialog):

    def write_config(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        lineInfo = config_object["APPROVEDCODE"]

        lineInfo["approved_code"] = self.lineEditApp_Code.text()

        if (len(self.lineEditApp_Code.text()) == 0):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วน และถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            # Write changes back to file
             with open(config_file, 'w') as conf:
                config_object.write(conf)
                QMessageBox.information(self, "information", " บันทึกข้อมูลสำเร็จ.            ",
                                    QMessageBox.StandardButton.Ok)
                self.lineEditApp_Code.clear()

    def load_config(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        # HOSPITAL
        self.lineInfo = config_object["APPROVEDCODE"]
        xapproved_code = self.lineInfo["approved_code"]   # Set Values
        self.lineEditApp_Code.setText(xapproved_code)

        hospitalInfo = config_object["HOSPITAL"]
        self.xhcode_hospital = hospitalInfo["hcode"]      # Set Values

    def test_register(self):
        if (len(self.lineEditApp_Code.text()) == 0):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วน และถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            text_register = self.lineEditApp_Code.text()
            num1 = text_register[7:8]
            num2 = text_register[18:19]
            num3 = text_register[23:24]
            num4 = text_register[30:31]
            num5 = text_register[42:43]
            xcheck_hos = str(num1)+str(num2)+str(num3)+str(num4)+str(num5)
            ycheck_hos = self.xhcode_hospital
            if xcheck_hos == ycheck_hos:
                QMessageBox.information(self, "information", " ลงทะเบียนสำเร็จ สามารถใช้งานโปรแกรมได้..สามารถส่งเสนอแนะเพื่อการพัฒนา  "
                                        ,QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.critical(self, "Critical", " หัสที่ได้มา ไม่สามารถใช้ลงทะเบียนกับหน่วยงานนี้ได้ ติดต่อผู้พัฒนาระบบ             "
                                     ,QMessageBox.StandardButton.Ok)
    def __init__(self, *args, **kwargs):
        super(Register_AppWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/register_App2.ui", self)
        # -----------------------------------------

        self.pushButtonSaveRegister.clicked.connect(self.write_config)
        self.pushButtonLoadConfig.clicked.connect(self.load_config)
        self.pushButtonCheckConfig.clicked.connect(self.test_register)

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/writer-male-48.png'
        self.setWindowTitle('Register Application Windows')
        self.setWindowIcon(QIcon(image_health))
        #self.show()
        pass



# def config_linemain():
#     app = QApplication(sys.argv)
#     ex = Register_AppWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     config_linemain()