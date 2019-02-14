#!/usr/bin/env python


#anonymizer_core.py: Processes a parallel corpus. 
#Submodules run in parallel, and loaded as needed:
#i.e.: eu-es will need one ixa and one bilst. es-en will need two instances of bilst 



import logging


import merger_module
import entity

__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"



#def extract(src, trg, srclang, trglang, regex_module, src_names_module, trg_names_module, address_module, tagger, mode):
"""
Extracts all entities from a pair of parallel sentences:
  src: Source sentence
  trg: Target sentence
  srclang: Source language
  trglang: Target language
  regex_module:
  src_names_module:
  trg_names_module:
  address_module:
  source_tagger:
  target_tagger:    
"""
def extract(src, trg, srclang, trglang, regex_module, src_names_module, trg_names_module, address_module, source_tagger, target_tagger): 
  
  src_regex_results = regex_module.extract(src)
  trg_regex_results = regex_module.extract(trg)
  
  src_addresses_results = address_module.extract(src)
  trg_addresses_results = address_module.extract(trg)
  #src_names_results = src_names_module.extract(src, tagger, mode)
  #trg_names_results = trg_names_module.extract(trg, tagger, mode)
  src_names_results = src_names_module.extract(src, source_tagger)
  trg_names_results = trg_names_module.extract(trg, target_tagger)

  merger_results = merger_module.merge(src, trg, src_regex_results, src_addresses_results, src_names_results, trg_regex_results, trg_addresses_results,  trg_names_results)
    
  return merger_results

def get_replacement(e):
  return  '''<entity class="{0}">{1}</entity>'''.format(e.type, e.entity)
  

def overwrite(text, entities):
  if len(entities) == 0:
    return text
    
  sorted_entities = entity.sort_by_position(entities)
  slices = []
  prev_pos = 0
  
  for e in sorted_entities:
    sub = text[prev_pos:e.start]+get_replacement(e)
    prev_pos = e.start + e.length 
    slices.append(sub)
  else:
  #last slice
    slices.append(text[prev_pos:])
#  logging.debug("Final text: " + "".join(slices))    
  return "".join(slices)