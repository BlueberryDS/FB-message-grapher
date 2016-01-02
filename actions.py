from utils import normalizeUserList, normalizeGroupList
from datetime import datetime, timedelta, timezone
from itertools import zip_longest
import csv
#Contains various methods for acting on the data

class Actions :
  data = None
  timeStep = timedelta(weeks=1)
  
  def __init__(self, data) :
    self.data = data
    
  def help(self, command=None) :
    helpString = ""
    if command == None or command == "help" :
      helpString += "help \"<command(optional)>\"     --   Retrieves documentation for all commands, or the specified one.\n"
    if command == None or command == "top" :
      helpString += "top <num>                      --   Retrieves first 'num' top most messaged friends \n"
    if command == None or command == "count" :
      helpString += "count [<list-of-groups>]       --   Counts the number of messages for the given friends in the order given \n"
    if command == None or command == "scale" :
      helpString += "scale \"<scale-type>\", <units>  --   Creates a x-axis to base graph operations on \n"
    if command == None or command == "simple" :
      helpString += "simple [<groups>], <scale>     --   Creates a simple frequency count graph \n"
    if command == None or command == "simplesplit" :
      helpString += "simplesplit [<groups>], <scale>--   Creates a simple frequency count graph, with individual users \n"
    if command == None or command == "csv" :
      helpString += "csv <data>, \"<file>\"           --   Writes the given data to a csv file \n"
    if not helpString :
      helpString = "Cannot find help for : " + command
    return helpString
  
  def top(self, num) :
    def keyfunction(k):
      return len(self.data[k])
    
    return sorted(self.data, key=keyfunction, reverse=True)[:num]
  
  def count(self, groups) :
    groups = normalizeGroupList(groups)
    results = []
    for group in groups:
      results.append((group, len(self.data.get(group))))
    return results
  
  def scale(self, scale, units) :
    scale = scale.lower()
    scaleList = []
    timeStep = None
    if scale == "monthly" :
      timeStep = timedelta(days=31)
    elif scale == "weekly" :
      timeStep = timedelta(weeks=1)
    else :
      raise ValueError("Scale not supported")
    
    currentTime = datetime.now(timezone.utc)
    
    for i in range(0, units) :
      scaleList.append(currentTime)
      currentTime = currentTime - timeStep  
    scaleList.append("scale (%r)" % scale)
    scaleList.reverse()
    return scaleList
  
  def simple(self, groups, scale) :
    groups = normalizeGroupList(groups)
    results = [scale]
    for group in groups:
      messages = self.data.get(group)
      if messages != None :
        messages = sorted(messages, key=lambda x: x.time)
        counts = [group]
        i = 0
        for date in scale[1:] :
          count = 0
          while i < len(messages) and messages[i].time < date :
            count += 1
            i += 1
          counts.append(count)
        results.append(counts)
      else :
        raise ValueError("Group not found!")
      
    return results
  
  def simplesplit(self, groups, scale) :
    groups = normalizeGroupList(groups)
    results = [scale]
    for group in groups:
      messages = self.data.get(group)
      if messages != None :
        messages = sorted(messages, key=lambda x: x.time)
        
        counts = {}
        i=0
        datesUsed = 0
        for date in scale[1:] :
          count = {}
          
          while i < len(messages) and messages[i].time < date :
            if messages[i].sender in count :
              count[messages[i].sender] += 1
            else :
              count[messages[i].sender] = 1
            i += 1
          
          for member in count :
            if member in counts :
              counts[member].append(count[member])
            else :
              counts[member] = [str(group) + ":" + str(member)] + [0] * datesUsed + [count[member]]
              
          datesUsed += 1
        results.extend(list(counts.values()))
      else :
        raise ValueError("Group not found!")
      
    return results
   
  def csv(self, data, name) : 
    rows = zip_longest(*data, fillvalue="--")
    with open(name + ".csv", 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerows(rows)
    return "Written to : " + name + ".csv"