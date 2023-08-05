docs = """
<br><!doctype HTML>
<br><html>
<br><p>
<br>XGame Documentation\n
<br>
<br>please note that features are still in development\n
<br>
<br>\n
<br>-----------------------------------------------\n
<br>welcome to xgame! time to get you started!\n
<br>lets make a simple hello world program in xgame!
<br>
<br>first we will create a game script to do this make a new python file and put:
<br>import XGame
<br>game = XGame.game(name="Hello World")
<br>
<br>-------
<br>that is a xgame project! now lets give our project some code!
<br>first we are going to use the @XGame.game.code decorator like this to write code:
<br>
<br>write the following:
<br>@game.code
<br>def code()#this function can be any name
<br>    return XGame.FreeStyle(
<br>
<br>    )
<br>
<br>now we can add code more efficiently using XGame.FreeStyle! this function lets us write
<br>blocks of code fast and simple! inside of the `XGame.FreeStyle() function put:
<br>XGame.Main(f'''
<br>{XGame.Log("hello","world","nice!")}
<br>system("pause");
<br>''') #defines our xgame main point! 
<br>
<br>
<br>note: in xgame ALLL APPS/PROJECTS MUST HAVE XGame.Main! otherwise they wont be ran!
<br>goood job! once you do that do:
<br>
<br>
<br>game.debug() #runs the script
<br>
<br>to run your game!
<br>
<br>
<br>
<br>the code now should look like this:
<br>import XGame
<br>game = XGame.game(name="Hello World")
<br>@game.code
<br>def code()#this function can be any name
<br>    return XGame.FreeStyle(
<br>    XGame.Main("system("pause");
<br>)
<br>
<br>    )
<br>
<br>after you run this you should see a console window pop up displaying
<br>"press enter to close" this means that your program works!
<br>
<br>if your program doesnt run that means you miscoded the code! so check and make sure everythings correct!
<br>
<br>make sure you run the code in the console! this makes error catching easier!
<br></p>
<br></html>
<br>"""
