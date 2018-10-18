import json

class Entity:
  def __init__(self, start, length, type, entity):
    self.start = start
    self.length = length
    self.type = type
    self.entity = entity
    
  def serializeEntity(self):
    return """{"start": {0}, "length": {1}, "type": "{2}", "entity": "{3}"}""".format(self.start, self.length, self.type, self.entity)
  
def deserializeEntity(json_str):
  payload = json.loads(json_str)
  return Entity(payload.start, payload.length, payload.type, payload.entity)
  

  
def serializeArray(array):
  if len(array)==0:
    return "[]"
  serialized_entities = []
  if len(array)== 0:
    return serialized_entities
  
  for i in array:
    serialized_entities.append(i.serializeEntity())
  return """[{0}]""".format(",".join(serialized_entities))

def deserializeArray(json_str):
  if json_str==None:
    return []
  str_arr = json.loads(json_str) 
  arr = []
  for a in str_arr:
    arr.append(deserializeEntity(a))
  return arr
    
  
def serialize(source_entities, target_entities):

  return """{"l1": {0}, "l2":{1}}""".format(serializeArray(source_entities), serializeArray(target_entities))