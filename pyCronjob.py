import time
from threading import Thread
import os
import datetime



from modules import actions
from modules import rules
from modules import checks
from modules import notifications



RULECHECKINTERVAL = 0.1
LOGSFOLDER = "logs"
ACTIONLOG_EXTENSION = ".action_log"
CHECKLOG_EXTENSION = ".check_log"
NOTIFICATIONLOG_EXTENSION = ".notification_log"
NOTIFICATION_BOT_TOKEN = """YOUR NOTIFICATION (TELEGRAM) BOT TOKEN"""
NOTIFICATION_TOTAL_RATELIMIT = {
    "amount": 5,
    "time": 30
}



os.chdir(os.path.dirname(os.path.realpath(__file__)))



formatted_time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

print("*************************************")
print("*                                   *")
print("*    pyCronjob is running...        *")
print("*                                   *")
print("*************************************")

print(f"Start Time: {formatted_time}")




def watchMainloop():

    try:
        global mainloopWatcher
        while True:
            if(mainloopWatcher.is_alive() == False):
                mainloopWatcher = Thread(target=mainloop, args=())
                mainloopWatcher.start()
                print("Restarted mainloop")

            time.sleep(5)
    except:
        watchMainloop()
        

def mainloop():
    while True:

        rulesObj.checkRules()
        time.sleep(RULECHECKINTERVAL)
        
actionsObj = actions.actions()
checksObj =  checks.checks()
notificationsObj =  notifications.notifications(NOTIFICATION_BOT_TOKEN, NOTIFICATION_TOTAL_RATELIMIT)
rulesObj = rules.rules(actionsObj, checksObj, notificationsObj, LOGSFOLDER, CHECKLOG_EXTENSION, ACTIONLOG_EXTENSION, NOTIFICATIONLOG_EXTENSION)


mainloopWatcher = Thread(target=mainloop, args=())
mainloopWatcher.start()
watchMainloop()