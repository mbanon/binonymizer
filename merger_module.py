#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 

import logging
import entity

"""
Merges the result of NER extraction
  src: Source
  trg: Target
  src_names: Entities found in the source
  trg_names: Entities found in the target
"""
def merge_names(src, trg, src_names, trg_names):
  l1_names=src_names
  l2_names=trg_names
  return l1_names, l2_names  

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
  
  
  l1 = [] #src results
  l2 = [] #trg results
  
  l1_names, l2_names = merge_names(src, trg, src_names, trg_names)
  
  l1.extend(src_regex)
  l1.extend(src_addresses)
  l1.extend(l1_names)
  
  l2.extend(trg_regex)
  l2.extend(trg_addresses)
  l2.extend(l2_names)
  
  results["l1"] = l1
  results["l2"] = l2
  
  
 
  return results



 


 


