import time
from datetime import datetime
from threading import Lock



import telebot



class notifications:

    instance = None

    def __init__(self, notificationBotToken, notificationRateLimit):

        notifications.instance = self
        self.notificationBot = self.instantiateNotificationBot(notificationBotToken)
        self.rateLimit = notificationRateLimit
        self.lastNotifications = []
        self.notificationLock = {"lockObj": Lock(), "lastAquired": 0, "maxLockTime": 80}


    def instantiateNotificationBot(self, __botToken):

        __telegramBot = None
        if(__botToken != ""):
            __telegramBot = telebot.TeleBot(__botToken, threaded = False, parse_mode="HTML")

        return __telegramBot
    
    
    def cleanLastNotifications(self):

        currentTime = time.time()
        maximumTime = currentTime - self.rateLimit["time"]
        
        self.lastNotifications = [notificationTimestamp for notificationTimestamp in self.lastNotifications if notificationTimestamp >= maximumTime]


    def cleanNotificationLock(self):

        if(self.notificationLock["lockObj"].locked()):
            currentTime = time.time()
            lastAquiredTime = self.notificationLock["lastAquired"]
            maxLockTime = self.notificationLock["lastAquired"]

            if(currentTime >= lastAquiredTime + maxLockTime):
                self.notificationLock["lockObj"].release()
                self.notificationLock["lastAquired"] = 0


    def hasExceededRateLimit(self):

        self.cleanLastNotifications()
        self.cleanNotificationLock()

        rateLimited = False
        with self.notificationLock["lockObj"]:
            self.notificationLock["lastAquired"] = time.time()
            if(len(self.lastNotifications) >= self.rateLimit["amount"]):
                rateLimited = True

            else:
                self.addMessageToRateLimit()
                
        return rateLimited


    def addMessageToRateLimit(self):

        self.lastNotifications.append(time.time())

    
    def sendNotification(self, chatId, messageText):

        if(self.hasExceededRateLimit()):
            print(f"Error in sendNotification: RateLimit of {self.rateLimit['amount']} message/s per {self.rateLimit['time']} second/s was exceeded")

        else:
            self.notificationBot.send_message(chatId, str(messageText))
        

    def sendErrorNotification(self, ruleId, chatId, errorText):

        messageText = """
            pyCronjob Error\U000026A0:\n
            Rule with ID: """ +  str(ruleId) + """ ran into an Error.\n
            The Error:\n
            """ + str(errorText) + """\n
            \n
            """ + str(datetime.now()) + """
        """

        self.sendNotification(chatId, messageText)


    def sendSuccessNotification(self, ruleId, chatId, successText):
        
        messageText = """
            pyCronjob Success\U00002705:\n
            Rule with ID: """ +  str(ruleId) + """ ran successfully.\n
            The Action returned following data:\n
            """ + str(successText) + """\n
            \n
            """ + str(datetime.now()) + """
        """

        self.sendNotification(chatId, messageText)



    class definitions:              #DEFINE YOUR OWN MESSAGE IN YOUR OWN sendNotification() WRAPPER, DECIDE TO ONLY SEND ERRORS/SUCCESSES AND SO MUCH MORE!

        def yourNotification(notificationParameters, actionReturn, actionError, ruleId):
            
            if(actionError):
                notifications.instance.sendErrorNotification(ruleId, notificationParameters["chatId"], str(actionError))
            
            else:
                notifications.instance.sendSuccessNotification(ruleId, notificationParameters["chatId"], str(actionReturn))

            return