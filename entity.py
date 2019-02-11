import json

class Entity:
  def __init__(self, start, length, type, entity):
    self.start = start
    self.length = length
    self.type = type
    self.entity = entity
  
  def toDict(self):    
    d=dict()
    d["start"] = self.start
    d["length"] = self.length
    d["type"] = self.type
    d["entity"] = self.entity
    return d
  
  def serializeEntity(self):
    d=self.toDict()
    return json.JSONEncoder().encode(d)
    #return """{"start": {0}, "length": {1}, "type": "{2}", "entity": "{3}"}""".format(self.start, self.length, self.type, self.entity)
  
def deserializeEntity(json_str):
  payload = json.loads(json_str)
  return Entity(payload.start, payload.length, payload.type, payload.entity.encode("utf-8"))
  

  
def serializeArray(array):
  if len(array)==0:
    return "[]"

  serialized_entities = []
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
    
  
def serialize(entities_dict):
  d=dict()

#  d["l1"] = serializeArray(entities_dict["l1"])
#  d["l2"] = serializeArray(entities_dict["l2"])
#  return json.JSONEncoder().encode(d)
  return "{\"l1\":" +serializeArray(entities_dict["l1"]) + ", \"l2\":" +serializeArray(entities_dict["l2"]) + "}"