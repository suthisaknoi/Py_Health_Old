
import datetime

def pass_superadmin():
    userSuper = "superadmin"
    now = datetime.datetime.now()
    datetime.time(now.hour, now.minute, now.second)
    if int(now.day)<10:
        pass_day =  "0"+str(int(now.day))
    else:
        pass_day = str(int(now.day))
    ##------------------------
    if int(now.hour)<10:
        pass_hour = "0"+str(int(now.hour))
    else:
        pass_hour = str(int(now.hour))
    ##------------------------
    if int(now.minute)<10:
        pass_minute = "0"+str(int(now.minute))
    else:
        pass_minute = str(int(now.minute))
    passSuper = pass_day+pass_hour+pass_minute
    return userSuper,passSuper


# userSuper,passSuper = pass_superadmin()
# print(userSuper)
# print(passSuper)







# p=strftime("%H", gmtime())
# print(p)
# today = date.today()
# print("Today's date:", today)
# isday = date.today().strftime('%d')
# print(isday)