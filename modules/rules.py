import time
import os
from threading import Thread
import uuid


class rules:

    def __init__(self, actionsObj, checksObj, logsFolder, checkLogExtension, actionLogExtension):

        self.actionsObj = actionsObj
        self.checksObj = checksObj
        self.checkThreads = {}
        self.logsFolder = logsFolder
        self.checkLogExtension = checkLogExtension
        self.actionLogExtension = actionLogExtension

        self.definedRules = self.generateRules()



    def generateRules(self):

        __definedRules = {
            "yourRule": {
                "checkFunction" : self.checksObj.definitions.yourCheck,
                "actionFunction": self.actionsObj.definitions.yourAction,
                "checkCoolDown": 4,
                "actionCoolDown": 30,
                "parallel": False
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

        uniqueThreadId = str(uuid.uuid4())

        def __actionProcedure():
            try:
                actionFunction()
            except Exception as e:
                print(f"Error during actionProcedure: {e}")

            del self.checkThreads[ruleId][uniqueThreadId]


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







        

