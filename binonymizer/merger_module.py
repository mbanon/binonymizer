#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 

import logging


try:
  from . import util
  from . import entity
except (ImportError, SystemError):
  import util
  import entity


"""
Solves overlapping between entities in the same sentence
  sentence: Sentence containing the entities
  entities: List of entities 
The list of entities is sorted by position and checked from the beginning.
If two consecutive entities overlap (fully or partially), it is, 
the beginning of the second one is between the beginning and the end of the first one,
both entities are merged into a single entity, containing the union of both entities.
 
"""
def mono_merge(sentence, entities):  
  length = len(entities)  
  if length==0 or length==1:
    return entities
  index = 0
  entities = entity.sort_by_position(entities)
  while index < len(entities):  
    
    #last item
    if index == len(entities)-1:
      return entities
    else:   
      current_ent = entities[index]
      next_ent = entities[index+1]
      cur_end = current_ent.start + current_ent.length
      next_end = next_ent.start + next_ent.length
      #Overlapping:
      if (current_ent.start <= next_ent.start) and (cur_end >= next_ent.start):
        new_start = current_ent.start  #because entities are sorted 
        new_end = max(cur_end, next_end)
        new_length = new_end - new_start
        if current_ent.length >= next_ent.length:
          new_type = current_ent.type
        else:
          new_type = next_ent.type  
        new_entity = entity.Entity(current_ent.start, new_length, new_type, sentence[new_start:new_end])
        del entities[index+1]
        del entities[index]        
        entities.append(new_entity)
        entities = entity.sort_by_position(entities)
        index = 0
      else:
        index += 1  

"""
Solves tagging  of named entities when only in one side of the parallel sentence.
  src_sentence: Source sentence
  src_entities: List of entities found in the source sentence
  trg_sentence: Target sentence
  trg_entities: List of entities found in the target sentence
"""
def para_merge(src_sentence, src_entities, trg_sentence, trg_entities):
  """
  * CASE A: Entity text is in A and B:
    * Keep the label as in A
  * CASE B: Entity text is in A and not in B:
    * CASE B1: Entity has no uppercased words (excluding string beginning): Ignore in both
      * example: "My cousin's friend is ugly" {} - "El amigo de mi primo es feo" {El amigo de mi primo: PER}
      * becomes: "My cousin's friend is ugly" {} - "El amigo de mi primo es feo" {}
    * CASE B2: Entity text has an uppercased part, the part in uppercase is not in any entity in B, and the uppercased part can be found also in B : Tag the entity in both
      * example: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Model S de Tesla es caro" {Tesla: ORG}
      * becomes: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Model S de Tesla es caro" {Model S: MISC, Tesla: ORG}
    * CASE B3: Entity text is not present in B: Keep the entity in A, it's unsafe to remove 
       * example: "Tesla's Model S is expensive" {Tesla's Model S: MISC} - "El Modelo S de Tesla es caro" {Tesla: ORG}
       * remains the same.
  """
  if len(src_entities)==0 and len(trg_entities)==0:
    #nothing to do here 
    return src_entities, trg_entities

  src_index = 0
  trg_index = 0  
  matched = [] #Keeps all entities in target that matched entities in source
  
  while src_index < len(src_entities):
    current_src_entity = src_entities[src_index]

    found = False
    
    if current_src_entity.start == 0:
      str_to_check = current_src_entity.entity[1:]  #Remove first char if it's beginning of sentence
    else:
      str_to_check = current_src_entity.entity  
    if (any(x.isupper() for x in str_to_check)):
      #Has uppercased parts
      uppercased_part = util.extractUppercased(str_to_check)
    else:	
      uppercased_part = None

    while trg_index < len(trg_entities):
      current_trg_entity = trg_entities[trg_index]
      #CASE A
      if current_src_entity.entity == current_trg_entity.entity:
        current_trg_entity.type = current_src_entity.type
        found = True
        matched.append(current_trg_entity)
      trg_index += 1


    #CASE B2
    if uppercased_part != None and  uppercased_part in trg_sentence: #it's ok even if it is in another entity because after para_merge comes mono_merge to solve overlappings
      new_entity_start = trg_sentence.index(uppercased_part)
      new_entity_length = len(uppercased_part)
      new_entity_type = current_src_entity.type
      new_entity_text = uppercased_part
      new_entity = entity.Entity(new_entity_start, new_entity_length, new_entity_type, new_entity_text)
      trg_entities.append(new_entity)
      matched.append(new_entity)
      found = True
            
    if found==False and  uppercased_part==None:
      #No uppercases: CASE B1
      del src_entities[src_index]
      src_index = 0 #Start from the beginning again
      trg_index = 0
    else:  
      #Case base (found entity) or CASE B3 (unsafe to remove, ignore and keep going)
      src_index += 1  
      trg_index = 0


  #Now, do a lighter version of the same but with those entities in target that didn't match anything in the source  
  not_matched = list(set(trg_entities) - set(matched))

  if len(not_matched) > 0:
    src_index = 0
    not_matched_index = 0
    
    while not_matched_index < len(not_matched):
      current_trg_entity = not_matched[not_matched_index]
      found = False
      if current_trg_entity.start == 0:
        str_to_check = current_trg_entity.entity[1:]
      else:
        str_to_check = current_trg_entity.entity
      if (any(x.isupper() for x in str_to_check)):
        uppercased_part = util.extractUppercased(str_to_check)
      else:
        uppercased_part = None
      while src_index < len(src_entities):
        current_src_entity = src_entities[src_index]
        if current_trg_entity.entity == current_src_entity.entity:
          found = True
        src_index += 1
      if uppercased_part != None and uppercased_part in src_sentence:
        new_entity_start = src_sentence.index(uppercased_part)
        new_entity_length = len(uppercased_part)
        new_entity_type = current_trg_entity.type
        new_entity_text = uppercased_part
        new_entity = entity.Entity(new_entity_start, new_entity_length, new_entity_type, new_entity_text)
        src_entities.append(new_entity)
        found = True
      if found == False and uppercased_part == None:
        trg_index = trg_entities.index(current_trg_entity)
        del trg_entities[trg_index]
        del not_matched[not_matched_index]    
        src_index = 0
        not_matched_index = 0
      else:
        src_index += 1
        not_matched_index += 1         
      
      
  return src_entities, trg_entities                      
        

    
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
  src_entities.extend(src_names)
  
    
  trg_entities.extend(trg_regex)
  trg_entities.extend(trg_addresses)
  trg_entities.extend(trg_names)
  
 
  src_merged, trg_merged = para_merge(src, src_entities, trg, trg_entities)
      
  l1 = mono_merge(src, src_merged)
  l2 = mono_merge(trg, trg_merged)
  

  results["l1"] = l1
  results["l2"] = l2
  
  
 
  return results



 


 


