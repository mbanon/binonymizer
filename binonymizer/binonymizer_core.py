#!/usr/bin/env python


#binonymizer_core.py: Processes a parallel corpus. 
#Submodules run in parallel, and loaded as needed:
#i.e.: eu-es will need one ixa and one bilst. es-en will need two instances of bilst 



import logging
import sys
import os


try:
  from . import merger_module
  from . import entity
except (ImportError, SystemError):
  import merger_module
  import entity

__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"


#Constants  
ixa_langs = ["eu"]
bilst_langs = []
spacy_langs=["bg", "da", "el", "sk", "sl", "sv", "ga", "hr", "mt", "lt", "hu", "et", "de", "fr", "es", "it", "pt", "nl", "pl", "cs", "ro", "fi", "lv"]



"""
Retrieves a names module  (NER tagger) object, configured and ready to use with the given language
"""
def selectNamesModule(lang):

  if lang in ixa_langs:

    sys.path.append(os.path.dirname(sys.argv[0])+"/prompsit-python-bindings/")
    print(os.path.dirname(sys.argv[0])+"/prompsit-python-bindings/")
    
    try:
      from . import ixa_module
    except (ImportError, SystemError):
      import ixa_module
    ixa_object = ixa_module.IxaObject(lang)
    return ixa_object

  if lang in bilst_langs:
    logging.warning("****************UNSUPPORTED MODULE!!!****************")
    return sys.modules["bilst_module"]

  if lang in spacy_langs:
    try:
      from . import spacy_module
    except (ImportError, SystemError):   
      import spacy_module
      
    return spacy_module.SpacyObject(lang)
  #default
  else:  
    try:
      from . import spacy_module
    except (ImportError, SystemError):  
      import spacy_module
    return spacy_module.SpacyObject(lang)


"""
Extracts all entities from a pair of parallel sentences:
  src: Source sentence
  trg: Target sentence
  srclang: Source language
  trglang: Target language
  regex_module: Regex module
  src_names_module: NER tagger module (object) for the source
  trg_names_module: NER tagger module (object) for the target
  address_module: Address extraction module

"""
def extract(src, trg, srclang, trglang, regex_module, src_names_module, trg_names_module, address_module): 
  
  src_regex_results = regex_module.extract(src)
  trg_regex_results = regex_module.extract(trg)
  
  src_addresses_results = address_module.extract(src)
  trg_addresses_results = address_module.extract(trg)
  src_names_results = src_names_module.extract(src)
  trg_names_results = trg_names_module.extract(trg)

  merger_results = merger_module.merge(src, trg, src_regex_results, src_addresses_results, src_names_results, trg_regex_results, trg_addresses_results,  trg_names_results)
    
  return merger_results
  
"""
Returns the XML-like string to replace a entity in a text
  e: Entity object
"""
def get_replacement(e):
  return  '''<entity class="{0}">{1}</entity>'''.format(e.type, e.entity)
  

"""
Overwrites a piece of text with the XML-like annotations of its entities
  text: Text to anonymize
  entities: Array of entities
"""
def overwrite(text, entities):
  if len(entities) == 0:
    return text
    
  sorted_entities = entity.sort_by_position(entities)
  slices = []
  prev_pos = 0
  
  for e in sorted_entities:
    #print("Prev pos: " + str(prev_pos))
    #print("e.start: " + str(e.start))
    #print("Index: " + str(prev_pos)
    sub = text[prev_pos:e.start]+get_replacement(e)
    prev_pos = e.start + e.length
    slices.append(sub)
  else:
  #last slice
    slices.append(text[prev_pos:])
#  logging.debug("Final text: " + "".join(slices))    
  return "".join(slices)