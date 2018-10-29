#!/usr/bin/env python


#anonymizer_core.py: Processes a parallel corpus. 
#Submodules run in parallel, and loaded as needed:
#i.e.: eu-es will need one ixa and one bilst. es-en will need two instances of bilst 



import logging

#import regex_module
#import address_module
#import ixa_module
#import bilst_module
import merger_module
#from itertools import zip_longest
import entity

__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"


def extract(src, trg, srclang, trglang, regex_module, src_names_module, trg_names_module, address_module):
 
  
  src_regex_results = regex_module.extract(src)
  trg_regex_results = regex_module.extract(trg)
  
  src_addresses_results = address_module.extract(src)
  trg_addresses_results = address_module.extract(trg)
  
  src_names_results = src_names_module.extract(src)
  trg_names_results = trg_names_module.extract(trg)


  merger_results = merger_module.merge(src, trg, src_regex_results, src_addresses_results, src_names_results, trg_regex_results, trg_addresses_results,  trg_names_results)
    
  return merger_results
