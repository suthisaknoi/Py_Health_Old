import sys
import pathlib
from PyQt6 import QtWidgets,uic
from PyQt6.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt6.QtGui import QIcon
from datetime import datetime
## -----------------
import socket
import platform
import locale
#-------------------
from winotify import Notification  # แสดง Notification ใน Task ด้านล่าง ---
#------------------
import gspread
from google.oauth2.service_account import Credentials  # Excel Google sheets

class About_ApplicationWindow(QtWidgets.QDialog):
    def write_computer(self):
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        xFolderFile = str(pathlib.Path(__file__).parent.resolve()) + "/configs/credentials.json"
        creds = Credentials.from_service_account_file(xFolderFile, scopes=scopes)
        client = gspread.authorize(creds)

        sheet_id = "1gvJbL_ezAqpKK1WZv65h005H4OPkUFkSu-XbwrbvysY"
        workbook = client.open_by_key(sheet_id)
        sheet = workbook.worksheet("Sheet1")
        #-----------
        computerName = str(socket.gethostname())
        IpAddress = self.get_ip()
        Windows = platform.system()
        VerWindows = platform.release()
        today = datetime.today()
        todayDate = today.strftime("%d-%m-%Y")
        todayTime = today.strftime("%H:%M:%S")
        #-----------
        values_col_list = workbook.sheet1.col_values(3)
        x = len(values_col_list)  # หาตำแหน่งสุดท้าย  Rec ที่จะทำต่อ ต้อง + 1
        sheet.update_cell(x + 1, 1, str(todayDate))
        sheet.update_cell(x + 1, 2, str(todayTime))
        sheet.update_cell(x + 1, 3, computerName)
        sheet.update_cell(x + 1, 4, IpAddress)
        sheet.update_cell(x + 1, 5, Windows)
        sheet.update_cell(x + 1, 6, VerWindows)

    def notifi(self):
        xFolderFile = str(pathlib.Path(__file__).parent.resolve())+"/ui/images/developer60.png"
        xapp_id = "ระบบสารสนเทศเพื่อสุขภาพ"
        xtitle = "ระบบสารสนเทศเพื่อสุขภาพ"
        xmsg = "สร้างเพื่อให้เจ้าหน้าที่สาธารณสุขนำข้อมูลสารสนเทศ จัดการสุขภาพคนในชุมชน!"
        show_notifi = Notification(app_id=xapp_id,
                                   title=xtitle,
                                   msg=xmsg,
                                   icon=xFolderFile
                                   )
        show_notifi.add_actions(label="เยี่ยมชมเวปไซค์ได้ที่นี่..!",
                          launch="https://phitsanulok.nhso.go.th/FrontEnd/Default.aspx")
        show_notifi.show()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def __init__(self):
        super(About_ApplicationWindow,self).__init__()
        uic.loadUi("ui/about_application2.ui", self)
        # Display List Name computer and ALl
        computerName = str(socket.gethostname())
        IpAddress = self.get_ip()
        VerWindows = platform.system()+'-'+platform.release()
        defaultlocale = str(locale.setlocale(locale.LC_ALL, ''))
        FolderFile = str(pathlib.Path(__file__).parent.resolve())

        self.label_ComName.setText(computerName)
        self.label_IPAddress.setText(IpAddress)
        self.label_Windows.setText(VerWindows)
        self.label_InterNet.setText(defaultlocale)
        self.label_Directory.setText(FolderFile)

        # Show Notifi-----------------------------
        self.notifi()
        # Display Windows ------------------------
        # Write Name Computer to Google Sheets ---
        #self.write_computer()                    ###   การเขียนข้อมูล บน Excel ในการเข้าใช้งานของระบบ
        #-----------------------------------------
        image_health = str(pathlib.Path(__file__).parent.absolute())+'/images/infopopup24.png'
        self.setWindowTitle('About Application Windows')
        self.setWindowIcon(QIcon(image_health))
        #self.show()
        pass

# def about_applicationmain():
#     app = QApplication(sys.argv)
#     ex = About_ApplicationWindow()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     about_applicationmain()