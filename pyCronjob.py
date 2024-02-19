import time
from threading import Thread
import os
import datetime



from modules import actions
from modules import rules
from modules import checks



RULECHECKINTERVAL = 0.1
LOGSFOLDER = "logs"
CHECKLOG_EXTENSION = ".check_log"
ACTIONLOG_EXTENSION = ".action_log"



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
rulesObj = rules.rules(actionsObj, checksObj, LOGSFOLDER, CHECKLOG_EXTENSION, ACTIONLOG_EXTENSION)


mainloopWatcher = Thread(target=mainloop, args=())
mainloopWatcher.start()
watchMainloop()