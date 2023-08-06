
def capitalize(txt):
  return txt[0].upper() + txt[1:]

def objPathToTypeParam(fieldPath):
  '''
  from: "brightBeer.name"
  to: "brightBeerName"
  '''
  fieldTags = fieldPath.split('.')
  if len(fieldTags) == 1:
    typeParam = fieldTags[0]
  else:
    typeParam = f'{fieldTags[0]}{capitalize(fieldTags[1])}'
  return typeParam
