#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 
#Outputs the original file plus an extra column with the extracted json  (resulting of merging tempfiles for each numline)
import logging
import entity

def merge(src, trg, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names):
 
 
  results = dict()
  
  l1 = [] #src results
  l2 = [] #trg results
  
  l1.extend(src_regex)
  l1.extend(src_addresses)
  l1.extend(src_names)
  
  l2.extend(trg_regex)
  l2.extend(trg_addresses)
  l2.extend(trg_names)
  
  results["l1"] = l1
  results["l2"] = l2
  
 
  return results



 


 


