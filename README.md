## SCRAPER TUTORIAL
The main file of interest to you will be ./scrapers/scraper.py which will serve as the basis (superclass) of your scrapers. To see what is expected to be done with this file, use ./scrdeal_hunters.py as a template.
The idea behind structuring our srapers like this is to make sure you can add to the database easily and access helper methods like log_block(). If the way it's layed out (object oriented) doesn't make sense to you you can use tools.py instead (see tools.py instructions section).


## Helper commands
if you are using the tools approach replace "self." with "helper."
```
self.log_block(x, y) # Creates a file "demo.html" which contains the html in x
```
Creates a file "demo.html" which contains the html in x. 
  > x can be any result of a .find() method
  > y is the number of the file (ex: log_block(x, 5) will create a file with contents x named "demo5.html")
You should be using this anytime you do a "block.find()" and are stuck with a "Nonetype does not have method ..."


## tools.py Instructions
To use helper functions, copy and paste the following at the top of your file:
```
import tools.py
```
Once imported place this code block anywhere OUTSIDE of a method (should not be indented at all)
```
helper = Tools()
```
Now you can use the variable "helper" anywhere in your code.