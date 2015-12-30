#Definitions of various execeptions

class CommandNotFound(Exception) : 
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
  
class CommandInvalid(Exception) : 
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)