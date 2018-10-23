#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 
#Outputs the original file plus an extra column with the extracted json  (resulting of merging tempfiles for each numline)
import logging
import entity

from itertools import zip_longest


def merge(srcsentences, trgsentences, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names, output):
  srcsentences.seek(0)
  trgsentences.seek(0)
  src_regex.seek(0)
  trg_regex.seek(0)
  
  logging.debug("Starting merging...")
  for src, trg, raw_src_r, src_a, src_n, raw_trg_r, trg_a, trg_n in zip_longest(srcsentences, trgsentences, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names):
    src_ent = []
    trg_ent = []
    print(src)
    print(trg)
    print(raw_src_r)
    print(raw_trg_r)
    src_r = entity.deserializeArray(raw_src_r)
    trg_r = entity.deserializeArray(raw_trg_r)
    
    if len(src_r) > 0:
      src_ent.append(src_r)
#    src_ent.append(src_a)
#    src_ent.append(src_n)
    if len(trg_r) > 0:
      trg_ent.append(trg_r)
#    trg_ent.append(trg_a)
#    trg_ent.append(trg_n)

    output.write(src.strip("\n") + "\t" + trg.strip("\n") + "\t" + entity.serialize(src_ent, trg_ent)+"\n")
  logging.debug("Exiting merging...")
  return 



 


 


