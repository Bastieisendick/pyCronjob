***pyCronjob***


Easy to setup and use task automation program.<br/>


Define your own rules, checks and actions.<br/>

To start, add your own rule in modules/rules.py<br/>
You can just set the checkFunction to your own in modules/checks.py<br/>
You can just set the actionFunction to your own in modules/actions.py<br/>
You can set a checkCooldown indicating how long has to be waited until the check can be executed again. THis is useful for webscraping checks and such for example, to limit request amounts.<br/>
You can set a actionCoolDown indicating how long mas to minimally be waited until the action can be executed again. This is useful for limiting the amount of action calls.<br/>
You can set parallel to True if you want to enable that in case of actions being triggered whilst one of them is running already, to still run (or not if False).<br/>


This program has persisten check and action logs, so even in a case of shutdown or crash, the events will only be executed once in the specified timeframe if check==True is still given.<br/>
Also multithreading is used, so the order of the rules doesnt make any difference.<br/>

*Examples*:<br/>
Wait until a website has a specified text and trigger an action.<br/>

Execute a python program at a specific time.<br/>

Wait until a specific file has been created and trigger an action.<br/>

+ There are endless possibilities, so be creative!<br/>




Hereby no guarantees or responsibilities are taken.<br/>
