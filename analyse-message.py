from zipfile import ZipFile
from sys import argv
from sys import getsizeof
import traceback
import parser
from exceptions import CommandInvalid
from exceptions import CommandNotFound
from commandEvaluator import evaluate
from actions import Actions

execName, filename = argv

content = None

if filename and filename[-3:] == "zip":
  print("extracting file(%r/html/messages.htm)..." % filename)
  file = ZipFile(filename)
  content = str(file.open("html/messages.htm").read())
  file.close()
else :
  print("Loading file(%r/html/messages.htm)..." % filename)
  content = open(filename).read()

print("Done...(%r mb)" % (getsizeof(content) / 1000000.0))

print("Parsing contents...(warning this may take a long time)")

parser = parser.FacebookParser()
#parser.feed(content)
result = parser.getData()
total = parser.getNumMessages()
del content

print("Done...Parsed size (%r messages) in (%r) threads" % (total, len(result)))
print("Ready!")

actions = Actions(result)

def startCommandInterpreter() : 
  while True : 
    try:
      inputString = input(">>>> ")
      print(evaluate(inputString, actions))
    except EOFError:
      return
    except KeyboardInterrupt:
      return
    except CommandInvalid as e:
      print("The command entered is invalid : " + e.value)
    except CommandNotFound as e:
      print("The command you are looking for does not exist : " + e.value)
    except:
      print("Exception : " + traceback.format_exc())
      
startCommandInterpreter()

print("STOPPED!")
