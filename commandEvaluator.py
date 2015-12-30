from exceptions import CommandInvalid
from exceptions import CommandNotFound
from inspect import ismethod
from ast import literal_eval

#Functions for evaluating commands

variableMap = {}

def evaluate(inputString, actions) :
  inputString = inputString.strip()
  command = inputString.split(" ", 1)
  commandInit = command[0]
  commandMethod = None
  
  
  if commandInit :
    try :
      commandMethod = getattr(actions, commandInit)
      if not ismethod(commandMethod) : 
        raise CommandNotFound("Command (" + commandInit + ") found is not method! It is : " + str(type(commandMethod)))
    except AttributeError:
      raise CommandNotFound("Command (" + commandInit + ") not found!")
  else: 
    raise CommandNotFound("Empty Command!")
  
  try :
    if len(command) > 1 :
      command = command[1]
      resultKey = None
      argumentList = None
      testSplit = command.split(" ")
      if testSplit[0] == "to" :
        if len(testSplit) == 2 :
          resultKey = testSplit[1]
        else :
          raise CommandInvalid("You must provide a variable to store result in, or you have provided too many")
      else :
        toSplit = command.split(" to ")
        if len(toSplit) == 2 :
          argumentList = parseArguments(toSplit[0])
          testSplit = toSplit[1].split(" ")
          if len(testSplit) == 1 :
            resultKey = toSplit[1]
          else :
            raise CommandInvalid("You must provide a variable to store result in, or you have provided too many")
        elif len(toSplit) == 1 :
          argumentList = parseArguments(toSplit[0])
        else :
          raise CommandInvalid("Too many ' to ' clauses")
    
      if(argumentList != None and resultKey != None) :
          variableMap[resultKey] = commandMethod(*argumentList)
      elif argumentList != None : 
          return commandMethod(*argumentList)
      elif resultKey != None :
          variableMap[resultKey] = commandMethod()
      else :
        raise CommandInvalid("Parse Error!")
    else :
      return commandMethod()
  except TypeError:
    raise CommandInvalid("Arguments Invalid")
  return "Command Success!"

def parseArguments(args) :
  try :
    return list(literal_eval("[" + args + "]"))
  except ValueError:
    raise CommandInvalid("Arguments cannot be parsed")
  
  
