#Contains various methods for acting on the data

class Actions :
  def __init__(self, data) :
    self.data = data
    
  def help(self, command=None) :
    helpString = ""
    if command == None or command == "help" :
      helpString += "help \"<command(optional)>\"   --   Retrieves documentation for all commands, or the specified one.\n"
    if not helpString :
      helpString = "Cannot find help for : " + command
    return helpString