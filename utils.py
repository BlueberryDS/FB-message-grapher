#Utilities

def normalizeUserList(users) :
  return tuple(sorted(users.split(", ")))

def normalizeGroupList(groups) :
  results = []
  for group in groups:
    if isinstance(group, tuple) :
      results.append(group)
    elif isinstance(group, str) :
      results.append(normalizeUserList(group))
  return results
  