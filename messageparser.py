import html
import html.parser
import html.entities
from dateutil.parser import parse
from datetime import datetime
from utils import normalizeUserList

#A simple parser for reading facebook.htm files

THREAD = "thread"
MESSAGE = "message"
UNSUPPORTED = "unsupported"
MESSAGE_HEADER = "message_header"
USER = "user"
META = "meta"
TEXT = "text"

class DomElement : 
  name = None
  data = None

  def __init__(self, name) : 
    self.name = name
    self.data = ""

class Message:
  sender = None
  content = None
  time = None

class FacebookParser(html.parser.HTMLParser):
  userToMessages = {}
  domStack = []
  currentThread = None
  currentMessage = None
  ignoringRead = None
  numMessages = 0
  
  def handle_starttag(self, tag, attrs):
    attrs = dict(attrs)
    classType = attrs.get("class")
    
    if tag == "div" and classType == THREAD :
      self.domStack.append(DomElement(THREAD))
      self.currentThread = []
    elif tag == "div" and classType == MESSAGE :
      self.currentMessage = Message()
      self.domStack.append(DomElement(MESSAGE))
    elif tag == "div" and classType == MESSAGE_HEADER :
      self.domStack.append(DomElement(MESSAGE_HEADER))
    elif tag == "span" and classType == USER :
      self.domStack.append(DomElement(USER))
    elif tag == "span" and classType == META :
      self.domStack.append(DomElement(META))
    elif tag == "p" :
      self.domStack.append(DomElement(TEXT))
    else :
      self.domStack.append(DomElement(UNSUPPORTED))
  
  def handle_endtag(self, tag) :
    domElement = None
    if self.domStack :
      domElement = self.domStack.pop()
    
    if domElement != None : 
      if domElement.name == THREAD :
        data = normalizeUserList(domElement.data)
        
        messages = self.userToMessages.get(data)
      
        if messages == None : 
          print("Recorded new thread %r (%r elements)...gathering next thread" % (str(data), len(self.currentThread)))
          self.userToMessages[data] = self.currentThread
        else : 
          print("Appended to thread %r (%r elements)....gathering next thread" % (str(data), len(self.currentThread)))
          messages.extend(self.currentThread)
          
        self.currentThread = None
      elif domElement.name == USER :
        self.currentMessage.sender = domElement.data
      elif domElement.name == META :
        self.currentMessage.time = parse(domElement.data)
      elif domElement.name == TEXT :
        self.currentMessage.content = domElement.data
        if self.currentMessage != None and self.currentMessage.content:
          self.currentThread.append(self.currentMessage)
          self.numMessages += 1

  def handle_data(self, data):
    domElement = self.domStack[-1] if self.domStack else None
    
    if domElement != None :
      domElement.data += data
      
  def handle_entityref(self, name) :
    domElement = self.domStack[-1] if self.domStack else None
    
    if domElement != None :
      domElement.data += "?"
      
  def handle_charref(self, name) :
    self.handle_entityref(name)
    
  def getData(self) : 
    return self.userToMessages
  def getNumMessages(self) :
    return self.numMessages