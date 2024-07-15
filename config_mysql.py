import sys
import pathlib
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt6.QtGui import QIcon
from configparser import ConfigParser
#-------------------
import mysql.connector          ## Mydel-connect-python
import Lib_Encoding as My_Lib
class Config_MysqlWindow(QtWidgets.QDialog):

    def save_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        hospitalInfo = config_object["SERVERCONFIG"]
        hospitalInfo["host_ip"] = My_Lib.Encoding(self.lineEditServer.text())
        hospitalInfo["user_host"] = My_Lib.Encoding(self.lineEditUserName.text())
        hospitalInfo["pass_host"] = My_Lib.Encoding(self.lineEditPassword.text())
        hospitalInfo["port_host"] = My_Lib.Encoding(self.lineEditPort.text())
        hospitalInfo["database_name"] = My_Lib.Encoding(self.lineEditDataBaseName.text())

        if ((len(self.lineEditServer.text()) == 0) or (len(self.lineEditUserName.text()) == 0)
                or (len(self.lineEditPassword.text()) == 0) or (len(self.lineEditPort.text()) == 0)
                or (len(self.lineEditDataBaseName.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง และ ถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            # Write changes back to file
             with open(config_file, 'w') as conf:
                config_object.write(conf)
                QMessageBox.information(self, "information", " บันทึกข้อมูลความสำเร็จ             "
                                        ,QMessageBox.StandardButton.Ok)
                self.lineEditServer.clear()
                self.lineEditUserName.clear()
                self.lineEditPassword.clear()
                self.lineEditPort.clear()
                self.lineEditDataBaseName.clear()
                self.lineEditServerStatus.clear()
                # self.labelResultTest.setText('รอแสดงผลทดสอบ....')

    def load_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        # HOSPITAL
        self.hospitalInfo = config_object["SERVERCONFIG"]
        # Set Values
        xhost_ip = My_Lib.Decoding(self.hospitalInfo["host_ip"])
        xuser_host = My_Lib.Decoding(self.hospitalInfo["user_host"])
        xpass_host = My_Lib.Decoding(self.hospitalInfo["pass_host"])
        xport_host = My_Lib.Decoding(self.hospitalInfo["port_host"])
        xdatabase_name = My_Lib.Decoding(self.hospitalInfo["database_name"])

        self.lineEditServer.setText(xhost_ip)
        self.lineEditUserName.setText(xuser_host)
        self.lineEditPassword.setText(xpass_host)
        self.lineEditPort.setText(xport_host)
        self.lineEditDataBaseName.setText(xdatabase_name)


    def test_message(self):
        if ((len(self.lineEditServer.text()) == 0) or (len(self.lineEditUserName.text()) == 0)
                or (len(self.lineEditPassword.text()) == 0) or (len(self.lineEditPort.text()) == 0)
                or (len(self.lineEditDataBaseName.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง และ ถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            xhost_ip = self.lineEditServer.text()
            xuser_host = self.lineEditUserName.text()
            xpass_host = self.lineEditPassword.text()
            xport_host = int(self.lineEditPort.text())
            xdatabase_name = self.lineEditDataBaseName.text()
            if ((len(self.lineEditServer.text()) == 0) or (len(self.lineEditUserName.text()) == 0)
                    or (len(self.lineEditPassword.text()) == 0) or (len(self.lineEditPort.text()) == 0)
                    or (len(self.lineEditDataBaseName.text()) == 0)):
                QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง และ ถูกต้อง              ",
                                    QMessageBox.StandardButton.Ok)
            else:
                checkIP,resultmessage = My_Lib.ping_ip(self.lineEditServer.text())
                if checkIP == False:
                    QMessageBox.critical(self, "Critical", f" ไม่สามารถเชื่อมต่อIPAddress กรุณาตรวจสอบ \n Error: {resultmessage}",
                                        QMessageBox.StandardButton.Ok)
                else:
                    result, sentmessage = My_Lib.testconnect_to_mysql(xhost_ip, xuser_host, xpass_host, xdatabase_name, xport_host)
                    if result == True:
                        self.lineEditServerStatus.setText("สถานะการเชื่อมต่อ MySQL : " + sentmessage)
                    else:
                        self.lineEditServerStatus.setText("สถานะการเชื่อมต่อ MySQL : " + sentmessage)

                    # cnx = mysql.connector.connect(user=xuser_host,
                    #                               password=xpass_host,
                    #                               host=xhost_ip,
                    #                               database=xdatabase_name,
                    #                               port = xport_host)
                    # try:
                    #     cursor = cnx.cursor()
                    #     cursor.execute(""" SELECT VERSION() """)
                    #     result = cursor.fetchall()
                    #     if result:
                    #         xresult = result
                    #     else:
                    #         xresult = "Not Connect"
                    # finally:
                    #     cnx.close()
                    # self.labelResultTest.setText("เชื่อมต่อ MySQL Version: "+str(xresult))



    def __init__(self, *args, **kwargs):
        super(Config_MysqlWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/config_mysql2.ui", self)
        # -----------------------------------------

        self.pushButtonSaveConfig.clicked.connect(self.save_message)
        self.pushButtonLoadConfig.clicked.connect(self.load_message)
        self.pushButtonTestDatabase.clicked.connect(self.test_message)

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/mysql25.png'
        self.setWindowTitle('Config MySQL Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()
        #pass



def config_mysqlmain():
    app = QApplication(sys.argv)
    ex = Config_MysqlWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    config_mysqlmain()