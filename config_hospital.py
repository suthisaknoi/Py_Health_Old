import sys
import pathlib
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt6.QtGui import QIcon
from configparser import ConfigParser
##------- Changwat  ---------------------
import Lib_MyLib as MyLib
class Config_HospitalWindow(QtWidgets.QDialog):   # QWidget  QDialog

    def save_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        hospitalInfo = config_object["HOSPITAL"]
        hospitalInfo["hcode"] = self.lineEditHcode.text()
        hospitalInfo["hcode_name"] = self.lineEditHname.text()
        hospitalInfo["province_id"] = self.lineEditProvince_id.text()
        hospitalInfo["province_name"] = self.comboBoxPtChangwat.currentText() #self.lineEditProvince_name.text()
        hospitalInfo["latitude"] = self.lineEditLatitude.text()
        hospitalInfo["longitude"] = self.lineEditLongitude.text()

        if ((len(self.lineEditHcode.text()) == 0) or (len(self.lineEditHname.text()) == 0) or (len(self.lineEditProvince_id.text()) == 0)):
            QMessageBox.warning(self, "warning", " กรุณากรอกข้อมูลให้ครบถ้วนทุกช่อง และ ถูกต้อง             ",
                                QMessageBox.StandardButton.Ok)
        else:
            # Write changes back to file
             with open(config_file, 'w') as conf:
                config_object.write(conf)
                QMessageBox.information(self, "information", " บันทึกข้อมูลความสำเร็จ             "
                                        , QMessageBox.StandardButton.Ok)
                self.lineEditHcode.clear()
                self.lineEditHname.clear()
                self.lineEditProvince_id.clear()
                # self.lineEditProvince_name.clear()
                # self.comboBoxPtChangwat.setCurrentIndex(0)
                self.lineEditLatitude.clear()
                self.lineEditLongitude.clear()

    def load_message(self):
        config_object = ConfigParser()
        config_file = str(pathlib.Path(__file__).parent.absolute()) + '/configs/config.ini'
        config_object.read(config_file)
        # HOSPITAL
        self.hospitalInfo = config_object["HOSPITAL"]
        # Set Values
        xhcode = self.hospitalInfo["hcode"]
        xhname = self.hospitalInfo["hcode_name"]
        xhprovince_Id = self.hospitalInfo["province_id"]
        xxhprovince_Name = self.hospitalInfo["province_name"]
        xhlatitude = self.hospitalInfo["latitude"]
        xlongitude = self.hospitalInfo["longitude"]
        # --- Changwat ------------------------------------------------
        index_changwat = self.comboBoxPtChangwat.findText(xxhprovince_Name)  # รับค่าจังหวัด ด้านบน
        if index_changwat != -1:
            self.comboBoxPtChangwat.setCurrentIndex(index_changwat)
            codeChangwat = MyLib.Search_CodeChangwat(xxhprovince_Name)
            self.lineEditProvince_id.setText(codeChangwat)
        else:
            self.comboBoxPtChangwat.setCurrentIndex(0)

        self.lineEditHcode.setText(xhcode)
        self.lineEditHname.setText(xhname)
        #self.lineEditProvince_id.setText(xhprovince_Id)
        # self.lineEditProvince_name.setText(xxhprovince_Name)
        self.lineEditLatitude.setText(xhlatitude)
        self.lineEditLongitude.setText(xlongitude)

    def __init__(self, *args, **kwargs):
        super(Config_HospitalWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/config_hospital2.ui", self)
        # -----------------------------------------
        ##-- Build Data to Select changwat Amphur Tumbon-----
        lookChangwat = MyLib.list_ProvinceName()
        self.comboBoxPtChangwat.addItems(lookChangwat)

        self.pushButtonSaveConfig.clicked.connect(self.save_message)
        self.pushButtonLoadConfig.clicked.connect(self.load_message)
        # ------- Combobox จังหวัด อำเภอ ที่อยู่ของผู้ป่วย  -----------
        self.comboBoxPtChangwat.currentTextChanged.connect(self.Combo_SearchCodeChangwat)  ##--- ตรวจสอบค่าเมื่อ มีการกดปุ่ม

        image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/hospital24.png'
        self.setWindowTitle('Config Hospital Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()
        pass

    def Combo_SearchCodeChangwat(self):
        codeChangwat = MyLib.Search_CodeChangwat(self.comboBoxPtChangwat.currentText())
        self.lineEditProvince_id.setText(codeChangwat)





# app = QApplication(sys.argv)
# windows = Config_HospitalWindow()
# windows.show()
# app.exec()


