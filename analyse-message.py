from zipfile import ZipFile
from sys import argv
from sys import getsizeof
import parser
  


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
parser.feed(content)
result = parser.getData()
del content
  

print("Done...Parsed size (%r messages) in (%r) threads" % (parser.getNumMessages(), len(result)))

