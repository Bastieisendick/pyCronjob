***pyCronjob***


Easy to setup and use task automation program.<br/>
Supports Telegram notifications via [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) about your executed tasks.<br/>


Define your own rules, checks, actions and notifications.<br/>

To *start*, add your own rule in modules/rules.py<br/>
You can just set the checkFunction to your own in modules/checks.py<br/>
You can just set the actionFunction to your own in modules/actions.py<br/>
You can just set the notificationFunction to your own in modules/notifications.py<br/>
You can set a checkCooldown indicating how long has to be waited until the check can be executed again. This is useful for webscraping checks and such for example, to limit request amounts.<br/>
You can set an actionCoolDown indicating how long has to minimally be waited until the action can be executed again. This is useful for limiting the amount of action calls.<br/>
You can set a notificationCoolDown indicating how long has to minimally be waited until another notification can be sent again by this rule. This is useful for limiting the amount of notifications received.<br/>
You can set parallel to True if you want to enable that in case of actions being triggered whilst one of them is running already, to still run (or not if False).<br/>
You can set notificationActive to True, if you want to receive a notification of your own definition when a task has for example run successfully or on error (or both)(or whenever you like it).<br/>
You can set notificationParameters to your own parameters that will be passed to your notification handler. Defining chatId is mandatory when using notifications, if not otherwise specified.<br/>
When using notifications, NOTIFICATION_BOT_TOKEN in pyCronjob.py will have to be set. If no notifications are needed, just keep the notification values at default or None or "".<br/>


This program has persistent check, action and notification logs, so even in a case of shutdown or crash, the events will only be executed once in the specified timeframe if check==True is still given.<br/>
Also multithreading is used, so the order of the rules doesnt make any difference.<br/>
Notifications can be sent via Telegram and some rateLimits have been added to prevent notification spamming in case of an emergency (When all actions would be called at the same time for example). This will not interrupt any action defined.<br/>


Its best to use this program coupled with my other project [script-restarter](https://github.com/Bastieisendick/script-restarter).

*Examples*:<br/>
Wait until a website has a specified text and trigger an action (and a notification).<br/>

Execute a python program at a specific time.<br/>

Wait until a specific file has been created and trigger an action.<br/>

Get informed when your server is offline.<br/>

+ There are endless possibilities, so be creative!<br/>


Hereby no guarantees or responsibilities are taken.<br/>
