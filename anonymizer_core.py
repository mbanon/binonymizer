#!/usr/bin/env python


#anonymizer_core.py: Processes a parallel corpus. 
#Submodules run in parallel, and loaded as needed:
#i.e.: eu-es will need one ixa and one bilst. es-en will need two instances of bilst 


import multiprocessing as mp
import sys
import logging
from tempfile import NamedTemporaryFile

import regex_module
import address_module
import ixa_module
import bilst_module
import merger_module
from itertools import zip_longest
import entity

__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"

ixa_langs=["eu"]
bilst_langs = ["en", "es"]

def extract(output, srcsentences, trgsentences, tmpdir,  srclang, trglang):
  #output_queue = mp.Queue()  
  output_queue=[]
  pool = mp.Pool()  #https://nickp60.github.io/jekyll/python/blog/2016/11/12/gripes-about-multiprocessing.html
  
  source_regex_results  = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
  target_regex_results = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
  
  source_addresses_results = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
  target_addresses_results = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
 
  source_names_results = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
  target_names_results = NamedTemporaryFile(mode="w+", delete=True, dir=tmpdir)
    
    
  #0  
  source_regex_proc = mp.Process(target=regex_module.extract, args=(srcsentences,  source_regex_results))
 #1
  target_regex_proc = mp.Process(target=regex_module.extract, args=(trgsentences, target_regex_results))
 
  #2
  source_addresses_proc = mp.Process(target=address_module.extract, args=(srcsentences, source_addresses_results))
  #3
  target_addresses_proc = mp.Process(target=address_module.extract, args=(trgsentences, target_addresses_results))
  
  source_names_module = selectNamesModule(srclang)
  #4
  source_names_proc = mp.Process(target=source_names_module.extract, args=(srcsentences, source_names_results))
  
  target_names_module = selectNamesModule(trglang)
  #5
  target_names_proc = mp.Process(target=target_names_module.extract, args=(trgsentences, target_names_results))
 
  processes = [source_regex_proc, target_regex_proc, source_addresses_proc, target_addresses_proc, source_names_proc, target_names_proc]
  
  
  for p in processes:
    p.start()
  
  for p in processes:
    p.join()
    
  source_regex_results.write("MIAU MIWU"+"\n")  
  source_regex_results.seek(0)
  for l in source_regex_results:
    print("OUT!: "  + l)
  merger_module.merge(srcsentences, trgsentences, 
    source_regex_results, source_addresses_results, source_names_results, 
    target_regex_results, target_addresses_results, target_names_results,  
    output)
    

  return

def selectNamesModule(lang):
  if lang in ixa_langs:
    return sys.modules["ixa_module"]
  if lang in bilst_langs:
    return sys.modules["bilst_module"]
  return sys.modules["bilst_module"] #default