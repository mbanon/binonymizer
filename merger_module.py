#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 
#Outputs the original file plus an extra column with the extracted json  (resulting of merging tempfiles for each numline)
import logging
import entity

def merge_names(src, trg, src_names, trg_names):
  l1_names=src_names
  l2_names=trg_names
  return l1_names, l2_names  


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



 


 


