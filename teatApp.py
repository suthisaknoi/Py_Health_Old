import sys
import pathlib
import requests                            ## Sent Line
#-------------------
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon
#-------------------
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QDir, Qt, QUrl, QSize
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, QStyleFactory,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar)

class AtestWindow(QtWidgets.QWidget): # QWidget  QDialog


    def __init__(self, *args, **kwargs):
        super(AtestWindow,self).__init__(*args, **kwargs)
        uic.loadUi("ui/camera2.ui", self)

        #------ Notifi ----------------
        #self.notifi()
        # ------ Notifi ----------------
        # self.pushButtonSent.clicked.connect(self.sent_message)    ## กดปุ่ม เพื่อส่งข้อมูลทางไลน์
        # self.pushButtonSentMail.clicked.connect(self.sent_mail)  ## กดปุ่ม เพื่อส่งข้อมูลทางเมส์
        # Display Windows -----
        image_health = str(pathlib.Path(__file__).parent.absolute())+'/images/health24.png'
        self.setWindowTitle('About Dev Windows')
        self.setWindowIcon(QIcon(image_health))
        self.show()
        pass


app = QApplication(sys.argv)
windows = AtestWindow()
windows.show()
app.exec()

# def about_devmain():
#     app = QApplication(sys.argv)
#     ex = About_DevWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     about_devmain()


