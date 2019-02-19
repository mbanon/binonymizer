#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 

import logging
import entity


"""
Solves overlapping between entities in the same sentence
  entities: List of entities sorted by starting position
"""
def mono_merge(sentence, entities):
  length = len(entities)  
  if length==0 or length==1:
    return entities
  print("********MULTIPLE ENTITIES!!***************")
  print(serialize_array(entities))
  new_entities = []  
  reprocess = False
  index = 0
  while index < length:  
    current_ent = entities[index]
    #last item
    if index == length+1:
      new_entities.append(current_ent)
      return new_entities
    else:   
      next_ent = entities[index+1]
      cur_end = current_ent.start + current_ent.length
      next_end = next_ent.start + next_ent.length
      #Overlapping:
      if (current_ent.start < next_ent.start) and (current_end > next_ent.start):
        print("******************OVERLAPPING!*******************")
        print("CURRENT: " + serialize_entity(current_ent))
        print("NEXT: " + serialize_entity(next_ent))
        new_start = current_ent.start  #because entities are sorted 
        new_end = max(cur_end, next_end)
        new_length = new_end - new_start
        if cur_ent.length >= next_ent.length:
          new_type = cur_ent.type
        else:
          new_type = next_ent.type  
        new_entity = Entity(current_ent.start, new_length, new_type, sentence[new_start:new_end])
        print("MERGED: " + serialize_entity(new_entity))
        new_entities.append(new_entity)
        
    
"""
Merges entities extracted from a parallel sentence
  src: Source
  trg: Target
  src_regex: Entites extracted by the regex_module in the source
  src_addresses: Entities extracted by the address_module in the source
  src_names: Entities extracted by the names_module in the source
  trg_regex: Entities extracted by the regex_module in the target
  trg_address: Entities extracted by the address_module in the target
  trg_names: Entities extracted by the names_module in the target
"""
def merge(src, trg, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names): 

  results = dict()
  

  src_entities = [] 
  trg_entities = [] 
  
  
  src_entities.extend(src_regex)
  src_entities.extend(src_addresses)
  src_entities.extend(l1_names)
  
  trg_entities.extend(trg_regex)
  trg_entities.extend(trg_addresses)
  trg_entities.extend(l2_names)
  
  entity.sort_by_position(src_entities)
  entity.sort_by_position(trg_entities)
  
  
  results["l1"] = src_entities
  results["l2"] = trg_entities
  
  
 
  return results



 


 


