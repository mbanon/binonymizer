#!/usr/bin/env python


#anonymizer_core.py: Processes a parallel corpus. 
#Submodules run in parallel, and loaded as needed:
#i.e.: eu-es will need one ixa and one bilst. es-en will need two instances of bilst 

import multiprocessing as mp

def extract(output, srcsentences, trgsentences, srclang, trglang):
  output_queue = mp.Queue()  
      
  #0  
  source_regex_proc = mp.Process(target=regex_module.extract, args=(srcsentences, output_queue))
  #1
  target_regex_proc = mp.Process(target=regex_module.extract, args=(trgsentences, output_queue))
  
  #2
  source_addresses_proc = mp.Process(target=address_module.extract, args=(srcsentences, output_queue))
  #3
  target_addresses_proc = mp.Process(target=address_module.extract, args=(trgsentences, output_queue))
  
  source_names_module = selectNamesModule(srclang)
  #4
  source_names_proc = mp.Process(target=source_names_module.extract, args=(srcsentences, output_queue))
  
  target_names_module = selectNamesModule(trglang)
  #5
  target_names_proc = mp.Process(target=target_names_module.extract, args=(trgsentences, output_queue))
  
  processes = [source_regex_proc, target_regex_proc, source_addresses_proc, target_addresses_proc, source_names_proc, target_names_proc]
  
  for p in processes:
    p.start()
    
  for p in processes:
    p.join()
    
  results = [output_queue.get() for p in processes]
  
  source_regex_results = results[0]  
  target_regex_results = results[1]
  source_addresses_results = results[2]
  target_addresses_results = results[3]
  source_names_results = results[4]
  target_names_results = results[5]
  
  processes.clear()
  output_queue.clear()
  
  merge_proc = mp.Process(target=merger_module.merge, args=(source_regex_results, source_addresses_results, source_names_results, target_regex_results, target_addresses_results, target_names_results, target_output, merge_output))
    
  merge_proc.start()    
  merge_proc.join()
    
  return