#!/usr/bin/env python

# merge-module: Merges the entities extracted by the other modules, avoiding duplicates. 
#Outputs the original file plus an extra column with the extracted json  (resulting of merging tempfiles for each numline)

from itertools import zip_longest

def merge(srcsentences, trgsentences, src_regex, src_addresses, src_names, trg_regex, trg_addresses, trg_names, output):
  srcsentences.seek(0)
  trgsentences.seek(0)

  for src, trg in zip_longest(srcsentences, trgsentences):
    output.write(src.strip("\n") + "\t" + trg.strip("\n") + "\n")
  return 

 


 


