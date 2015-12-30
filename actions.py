#Contains various methods for acting on the data

class Actions :
  data = None
  
  def __init__(self, data) :
    self.data = data
    
  def help(self, command=None) :
    helpString = ""
    if command == None or command == "help" :
      helpString += "help \"<command(optional)>\"   --   Retrieves documentation for all commands, or the specified one.\n"
    if command == None or command == "top" :
      helpString += "top <num>                      --   Retrieves first 'num' top most messaged friends \n"
    if not helpString :
      helpString = "Cannot find help for : " + command
    return helpString
  
  def top(self, num) :
    def keyfunction(k):
      return len(self.data[k])
    
    return sorted(self.data, key=keyfunction, reverse=True)[:num]