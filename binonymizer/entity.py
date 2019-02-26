#!/usr/bin/env python


import json
import logging
from enum import Enum, auto


class Label(Enum):
  PER=auto()
  ORG=auto()
  EMAIL=auto()
  PHONE=auto()
  ADDRESS=auto()
  ID=auto()
  MISC=auto()
  OTHER=auto()

  def __str__(self):
    return self.name
    
  def __repr__(self):
    return self.name
       
  """
  Gets a Label from a string or a Label object
  """
  def getLabel(label):

    if isinstance(label, Label):
      return label      
    else:
      try:
        return Label[label]
      except Exception:
        logging.warning("Unknown type: " + str(label))
        return Label.OTHER    

class Entity:
  """
  Constructor for class "Entity".
    start: Index of the first character of the entity in the original string
    length: Entity length (in characters)
    type: Type of the entity
    entity: Content of the entity (string)   
  """
  def __init__(self, start, length, type, entity):
    self.start = int(start)
    self.length = int(length)
    self.type = Label.getLabel(type)
    self.entity = entity

  """
  Converts an Entity object into a dictionary object
  """  
  def toDict(self):    
    d=dict()
    d["start"] = self.start
    d["length"] = self.length
    d["type"] = self.type.name
    d["entity"] = self.entity
    return d
    

  """
  Converts an Entity object into a JSON string
  """
  def serializeEntity(self):
    d=self.toDict()
    return json.dumps(d, ensure_ascii=False)

"""
Converts a JSON string into an Entity object
"""  
def deserializeEntity(json_str):
  payload = json.loads(json_str)
  return Entity(payload.start, payload.length, payload.type, payload.entity)
  

"""
Converts an array of Entity object into a JSON string
"""  
def serializeArray(array):
  if len(array)==0:
    return "[]"

  serialized_entities = []
  for i in array:
    serialized_entities.append(i.serializeEntity())
  return """[{0}]""".format(",".join(serialized_entities))

"""
Converts a JSON string into an array of Entity objects
"""
def deserializeArray(json_str):
  if json_str==None:
    return []
  str_arr = json.loads(json_str) 
  arr = []
  for a in str_arr:
    arr.append(deserializeEntity(a))
  return arr
    
"""
Converts a dictionary of Entity object for a parallel sentence (containing keys l1 y l2) into a JSON string
"""  
def serialize(entities_dict):
  return "{\"l1\":" +serializeArray(entities_dict["l1"]) + ", \"l2\":" +serializeArray(entities_dict["l2"]) + "}"

"""
Sorts an array of Entity objects by its start index
"""
def sort_by_position(entity_array):
  return sorted(entity_array, key=lambda k: k.start)