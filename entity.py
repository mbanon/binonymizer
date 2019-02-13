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
    return json.dumps(d, ensure_ascii=False)

  
def deserializeEntity(json_str):
  payload = json.loads(json_str)
  return Entity(payload.start, payload.length, payload.type, payload.entity)
  

  
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
  return "{\"l1\":" +serializeArray(entities_dict["l1"]) + ", \"l2\":" +serializeArray(entities_dict["l2"]) + "}"

def sort_by_position(entity_array):
  return sorted(entity_array, key=lambda k: k.start)