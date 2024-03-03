import time
import os
from threading import Thread
import uuid


class rules:

    def __init__(self, actionsObj, checksObj, notificationsObj, logsFolder, checkLogExtension, actionLogExtension, notificationLogExtension):

        self.actionsObj = actionsObj
        self.checksObj = checksObj
        self.notificationsObj = notificationsObj
        self.checkThreads = {}
        self.logsFolder = logsFolder
        self.checkLogExtension = checkLogExtension
        self.actionLogExtension = actionLogExtension
        self.notificationLogExtension = notificationLogExtension

        self.definedRules = self.generateRules()



    def generateRules(self):

        __definedRules = {
            "yourRule": {
                "checkFunction" : self.checksObj.definitions.yourCheck,
                "actionFunction": self.actionsObj.definitions.yourAction,
                "notificationFunction": self.notificationsObj.definitions.yourNotification,
                "checkCoolDown": 4,
                "actionCoolDown": 30,
                "notificationCoolDown": 30,
                "parallel": True,
                "notificationActive": True,
                "notificationParameters": {
                    "chatId": "YOUR NOTIFICATION (TELEGRAM) BOT CHAT ID HERE"
                }
            }
        }

        return __definedRules



    def checkRules(self):

        self.clean_checkThreads()

        for ruleId in self.definedRules:

            checkCoolDown = self.definedRules[ruleId]["checkCoolDown"]

            if(self.hasCooledDown(ruleId, checkCoolDown, self.checkLogExtension)):
                checkFunction = self.definedRules[ruleId]["checkFunction"]
                actionCoolDown = self.definedRules[ruleId]["actionCoolDown"]

                check = self.performCheck(checkFunction, ruleId)

                if(check and self.hasCooledDown(ruleId, actionCoolDown, self.actionLogExtension)):
                    parallelExecution = self.definedRules[ruleId]["parallel"]

                    if(parallelExecution or ruleId not in self.checkThreads):
                        actionFunction = self.definedRules[ruleId]["actionFunction"]

                        self.performAction(actionFunction, ruleId)             




    def performCheck(self, checkFunction, ruleId):

        returnBool = checkFunction()
        self.writeLog(ruleId, self.checkLogExtension)

        return returnBool


    def performAction(self, actionFunction, ruleId):

        def __actionProcedure():
            
            actionError = None
            actionReturn = None
            try:
                actionReturn = actionFunction()
            except Exception as e:
                print(f"Error during actionProcedure: {e}")
                actionError = e

            del self.checkThreads[ruleId][uniqueThreadId]               #removing the thread already, because the action has stopped and only notification related code will be executed from now on

            isNotificationActivated = self.definedRules[ruleId]["notificationActive"]
            notificationCoolDown = self.definedRules[ruleId]["notificationCoolDown"]
            notificationHasCooledDown = self.hasCooledDown(ruleId, notificationCoolDown, self.notificationLogExtension)

            if(isNotificationActivated and notificationHasCooledDown):
                notificationFunction  = self.definedRules[ruleId]["notificationFunction"]
                notificationParameters  = self.definedRules[ruleId]["notificationParameters"]

                self.performNotification(notificationFunction, notificationParameters, ruleId, actionReturn, actionError)


        uniqueThreadId = str(uuid.uuid4())

        actionThread = Thread(target=__actionProcedure, args=())
        actionThread.setDaemon(True)

        if(ruleId in self.checkThreads):
            self.checkThreads[ruleId][uniqueThreadId] = {
                "threadObj": actionThread
            }

        else:
            self.checkThreads[ruleId]= {
                uniqueThreadId: {
                    "threadObj": actionThread
                }
            }

        actionThread.start()

        self.writeLog(ruleId, self.actionLogExtension)
        

    def performNotification(self, notificationFunction, notificationParameters, ruleId, actionReturn, actionError):
        
        def __notificationProcedure():
            try:
                notificationFunction(notificationParameters, actionReturn, actionError, ruleId)
            except Exception as e:
                print(f"Error during notificationProcedure: {e}")

        notificationThread = Thread(target=__notificationProcedure, args=())
        notificationThread.setDaemon(True)
        notificationThread.start()

        self.writeLog(ruleId, self.notificationLogExtension)


    def clean_checkThreads(self):

        for ruleId in list(self.checkThreads.keys()):
            for uniqueThreadId in self.checkThreads[ruleId]:
                threadObj = self.checkThreads[ruleId][uniqueThreadId]["threadObj"]
                if(threadObj.is_alive() == False):
                    del self.checkThreads[ruleId][uniqueThreadId]

            if(len(self.checkThreads[ruleId]) == 0):
                del self.checkThreads[ruleId]


    def hasCooledDown(self, ruleId, coolDown, fileExtension):

        filePath = self.logsFolder + "/" + ruleId + fileExtension
        fileExists = os.path.isfile(filePath)
        if(fileExists):

            lastTime = self.getLastLogTime(filePath)
            if(lastTime == None):
                return True

            currentTime = time.time()
            coolDownEndTime = lastTime + coolDown
            if(currentTime < coolDownEndTime):
                return False

        return True


    def getLastLogTime(self, filePath):

        with open(filePath, "r") as file:
            content = file.read()

        lastTime = None
        try:
            lastTime = float(content)
        except Exception as e:
            print(f"Couldnt convert logFile content to float: {e}")

        return lastTime


    def writeLog(self, ruleId, fileExtension):

        filePath = self.logsFolder + "/" + ruleId + fileExtension
        with open(filePath, "w") as file:
            file.write(str(time.time()))