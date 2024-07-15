import time
import sys
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox,QSplashScreen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class SplashWindow(QSplashScreen):
    def __init__(self):
        super(QSplashScreen,self).__init__()
        uic.loadUi("ui/splash.ui", self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)   ## เอา Fram หน้าจอออก
        self.center()

    def center(self):
        # Get the screen geometry
        screen = self.screen().availableGeometry()
        # Get the window geometry
        window = self.geometry()
        # Calculate the center position
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        # Move the window to the center
        self.move(x, y)
    def progress(self):
        for i in range(101):
            time.sleep(0.1)
            self.progressBar.setValue(i)
            if i == 100:
                self.label.setText("Loading Complete")
                self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashWindow()
    splash.show()
    splash.progress()
    sys.exit(app.exec())

