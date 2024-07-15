import sys
import pathlib

from PIL.ImageQt import ImageQt
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt6.QtGui import QIcon
from configparser import ConfigParser
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import cv2
import time
from PyQt6.QtCore import Qt
#--------------------------
import Lib_MyLib as F_MyLib
#--------------------------

class Camera_Window(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(Camera_Window, self).__init__(*args, **kwargs)
        if not F_MyLib.CheckFile_FolderUi("cam.ui"):
            QMessageBox.critical(self, "Error ขั้นรุนแรง", " ไม่พบ File แสดงผลหน้าจอ [cam.ui] กรุณาติดต่อผู้พัฒนาระบบ  ",
                                 QMessageBox.StandardButton.Ok)
            #------------
            self.close()

        else:
            uic.loadUi("ui/cam.ui", self)
            # -----------------------------------------
            self.pushButtonStart.clicked.connect(self.start_video)
            self.pushButtonStop.clicked.connect(self.cancel)
            image_health = str(pathlib.Path(__file__).parent.absolute()) + '/images/camera-48.png'
            self.setWindowTitle('Camera Windows')
            self.setWindowIcon(QIcon(image_health))
            self.show()

    def exit(self):
        QApplication.instance().quit()

    def start_video(self):
        print("start")
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.savePhoto()
        self.label.clear()
        self.Work.stop()


    def salir(self):
        sys.exit()

    def savePhoto(self):
        """ This function will save the image"""
        pixmap = self.label.pixmap()        # 160, 120
        if pixmap:
             pixmap_resized = pixmap.scaled(213, 160, Qt.AspectRatioMode.KeepAspectRatio)  ## ย่อรูป อีก ครึ่งหนึ่ง
             pixmap_resized.save("temp/camera_image.png")
             #print("Image saved successfully!")


class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(0)
        #print("WORK")
        while self.hilo_corriendo:
            ret, frame = cap.read()
            #print("WORK2")
            if ret:
                #print("WORK3")
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # --- Old
                #print("WORK4")
                # h, w, ch = Image.shape
                # bytesPerLine = ch * w
                flip = cv2.flip(Image, 1)   #-- Old
                #print("WORK5")
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format.Format_RGB888)  # --Old  QImage.Format.Format_RGB888

                #print("WORK6")
                pic = convertir_QT.scaled(320, 240, Qt.AspectRatioMode.KeepAspectRatio)
                #print("WORK7")
                self.Imageupd.emit(pic) #-- Old
                #self.changePixmap.emit(pic)
                #print("WORK8")
    def stop(self):
        self.hilo_corriendo = False
        self.quit()

def config_cammain():
    app = QApplication(sys.argv)
    ex = Camera_Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    config_cammain()