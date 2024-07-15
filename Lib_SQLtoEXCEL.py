import pathlib
# Database -------------------
import sqlite3
#  xeport to Excel ----------
import xlsxwriter
import os

# ---------------------------------------------------------------------------
#  การ query ข้อมูล จาก Sqlite 3
#
#
def ListDataSQLite(query):
    DataPath = str(pathlib.Path(__file__).parent.absolute()) + '/SQLite/HealthDB.db'
    sqliteConnection = sqlite3.connect(DataPath)
    cursor = sqliteConnection.cursor()
     ##  parameter   query = "SELECT * FROM user_app WHERE user_name = '" + TextSearch + "'"
    cursor.execute(query)
    Rec_user = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    sqliteConnection.commit()
    sqliteConnection.close()
    return Rec_user,columns

# ---------------------------------------------------------------------------
#  การรับค่า จาก query ข้อมูล จาก Sqlite 3
#  Export เป็น File Excel
#
#   ตัวอย่าง การ รันไฟล์   ----
# query = "SELECT idcard,prename,fname,lname,sex,address,add_mu,add_tumbon,add_amphur,add_changwat,right_health FROM person limit 100 "
# records,columns = ListDataSQLite(query)
# filename = exportTOExcel(records,columns)
#
#
def exportTOExcel(records,columns):
    wb = xlsxwriter.Workbook("file_excel/person.xlsx")
    ws = wb.add_worksheet("sheetperson")
    # column header
    # print(columns)
    # print(result)
    # write to excel    write  =  in cell    write_row  =  write muticolumn
    # write header
    ws.write_row(0, 0, columns)  ## --  writer Header (0,0)
    rownum = 1  ## --  แถว 2  เริ่ม บันทึกข้อมูล
    for record in records:
        ws.write_row(rownum, 0, record)
        rownum += 1
    # work sheet close
    ws.autofit()  # set column width automatically
    # wb = Workbook()
    # ws = wb.worksheets[0]
    ws.protect('abc123')  # set the password and protect
    wb.close()
    filename = "file_excel/person.xlsx"
    return filename





