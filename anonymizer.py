#!/usr/bin/env python


#anonymizer.py: Entry point.
#Wraps the anonymizer-core.py, preparing the input and processing the output. 
#Takes the entry file (raw src-trg, tmx...), parallelizing if needed,
#and extracting the source and the target sentences,
#generating (in the case of tmx files) a raw parallel corpus,
#that will be input to the anonymizer-core.
#hen the anonymizer-core.py finishes, builds the annotated TMXs (if the entry was a TMX file)



#We need to decide if we paralelize at lines/tus scope (in case of few files with a lot of lines)
#or at document scope (in case of a lot of files with few lines) 


import anonymizer_core
import argparse
import logging
import os
import sys
import traceback
#import jpype

from tempfile import NamedTemporaryFile, gettempdir
from timeit import default_timer
from multiprocessing import Queue, Process,  cpu_count
from heapq import heappush, heappop



import merger_module
import address_module
import regex_module
#import ixa_module
#import bilst_module
import entity
import spacy_module
import sys

#TO DO
#sys.path.append("/home/mbanon/project/anonymizer/anonymizer/prompsit-python-bindings/")


try:
  from .util import logging_setup
#  from .anonymizer_core import extract
  from .tmx_utils import tmx2text
except (ImportError, SystemError):
  from util import logging_setup
#  from anonymizer_core import extract
  from tmx_utils import tmx2text
  
  
__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 20181005 # Initial release # Marta Bañón"
__version__ = "Version 0.2 # 20180207 # Integrating SpaCy # Marta Bañón" 

def initialization():
  logging.info("Processing arguments...")
  # Getting arguments and options with argparse
  # Initialization of the argparse class
  parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  # Mandatory parameters
  ## Input file (TMX). Try to open it to check if it exists
  parser.add_argument('input', type=argparse.FileType('r'), default=None, help="File to be anonymized")
  ## Output file (TMX). Try to open it to check if it exists
  parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="File with anonymization annotations")
  parser.add_argument("srclang", type=str, help="Source language (SL) of the input")
  parser.add_argument("trglang", type=str, help="Target language (TL) of the input")
  
  ## Parameters required
  groupM = parser.add_argument_group('Mandatory')
  groupM.add_argument("--format", choices=["tmx", "cols"], required=True, type=str, help="Input file format. Values: cols, tmx")
  
  
  # Options group
  groupO = parser.add_argument_group('Optional')
  groupO.add_argument('--tmp_dir', default=gettempdir(), help="Temporary directory where creating the temporary files of this program")
  groupO.add_argument('-b', '--block_size', type=int, default=10000, help="Sentence pairs per block")
  groupO.add_argument('-p', '--processes', type=int, default=max(1, cpu_count()-1), help="Number of processes to use")

  # Logging group
  groupL = parser.add_argument_group('Logging')
  groupL.add_argument('-q', '--quiet', action='store_true', help='Silent logging mode')
  groupL.add_argument('--debug', action='store_true', help='Debug logging mode')
  groupL.add_argument('--logfile', type=argparse.FileType('a'), default=sys.stderr, help="Store log to a file")
  groupL.add_argument('-v', '--version', action='version', version="%(prog)s " + __version__, help="show version of this script and exit")

  # Validating & parsing
  args = parser.parse_args()
  logging_setup(args)
  logging.debug("Arguments processed: {}".format(str(args)))
  #print(args.input.name)
  if args.format=="tmx" and args.input.name=="<stdin>":
    logging.error("Cannot process TMX from standard input.")
    sys.exit(1)
  logging.info("Arguments processed.")
  return args

  
  
#ixa_langs = ["eu"]
#bilst_langs = ["en", "es"]

spacy_langs=["bg", "da", "el", "sk", "sl", "sv", "ga", "hr", "mt", "lt", "hu", "et", "de", "fr", "es", "it", "pt", "nl", "pl", "cs", "ro", "fi", "lv"]


def selectNamesModule(lang):
'''
  if lang in ixa_langs:
    return sys.modules["ixa_module"]
  if lang in bilst_langs:
    return sys.modules["bilst_module"]
  return sys.modules["bilst_module"] #default
'''
  if lang in spacy_langs:
    load_spacy_model(lang)
    return sys.modules["spacy_module"]  
  #default
  else:  
  return sys.modules["spacy_module"]  

def load_spacy_model(lang):
  if lang in ["de"]:
  
  if lang in ["fr"]:
  if lang in ["es"]:
  if lang in ["it"]:
  if lang in ["pt"]:
  if lang in ["nl"]  
  if lang in ["bg", "da", "el", "sk", "sl", "sv", "ga", "hr", "mt", "lt", "hu", "et", "pl", "cs", "ro", "fi", "lv"]:
  else
    //load xx
def anonymizer_process(i, args, regex_module, source_names_module, target_names_module, address_module, jobs_queue, output_queue):
  #import prompsit_python_bindings.ixa 
  #tagger=prompsit_python_bindings.ixa.IXANERPipeline('eu')  

  while True:
    job = jobs_queue.get()    
    if job:
      logging.debug("Job {0}".format(job.__repr__()))
      nblock, filein_name = job
      ojob = None
      with open(filein_name, "r") as filein, NamedTemporaryFile(mode="w", delete=False, dir=args.tmp_dir) as fileout:
        logging.debug("Creating temporary filename {0}".format(fileout.name))
        for i in filein:
          parts = i.split("\t")
          if args.format == "tmx":
            src = parts[0].strip()
            trg = parts[1].strip()
          if args.format == "cols":
            src = parts[2].strip()
            trg = parts[3].strip()

          #if not jpype.isThreadAttachedToJVM():
          #  jpype.attachThreadToJVM()
          #mode = prompsit_python_bindings.ixa.Mode.ENTITY_DETECTION  
          #entities = anonymizer_core.extract( src, trg, args.srclang, args.trglang, regex_module, source_names_module, target_names_module, address_module, tagger, mode)
          entities = anonymizer_core.extract( src, trg, args.srclang, args.trglang, regex_module, source_names_module, target_names_module, address_module)
          fileout.write(i.strip()+"\t"+entity.serialize(entities)+"\n")
        ojob = (nblock, fileout.name)
        filein.close()
        fileout.close()
      if ojob :
        output_queue.put(ojob)
      os.unlink(filein_name)  
    else:
      logging.debug("Exiting worker")
      break
   
def mapping_process(args, input_file, jobs_queue):        
  logging.info("Start mapping")
  nblock = 0
  nline = 0
  mytemp = None
  for line in input_file:
    if (nline % args.block_size) == 0:
      logging.debug("Creating block {}".format(nblock))
      if mytemp:
        job = (nblock, mytemp.name)
        mytemp.close()
        jobs_queue.put(job)
        nblock += 1
      mytemp = NamedTemporaryFile(mode="w", delete=False, dir=args.tmp_dir)  
      logging.debug("Mapping: creating temporary filename {0}".format(mytemp.name))  
    mytemp.write(line)  
    nline += 1
    
  if nline > 0  :
    job = (nblock, mytemp.name)
    mytemp.close()
    jobs_queue.put(job)
  
  return nline
      
def reduce_process(output_queue, args):
  h = []
  last_block = 0
  while True:
    logging.debug("Reduce: heap status {0}".format(h.__str__()))
    while len(h) > 0 and h[0][0] == last_block:
      nblock, filein_name = heappop(h)
      last_block += 1
      
      with open(filein_name, "r") as filein:
        for i in filein:
          args.output.write(i)
        filein.close()
      os.unlink(filein_name)  
    job = output_queue.get()
    if job:
      nblock, filein_name = job
      heappush(h, (nblock, filein_name))
    else:
      logging.debug("Exiting reduce loop")
      break
  if  len(h)>0:
    logging.debug("Still elements in heap")
  
  while len(h) > 0 and h[0][0] == last_block:
    nblock, filein_name = heapq.heappop(h)
    last_block += 1
    os.unlink(filein_name)
  
  if len(h) != 0:
    logging.error("The queue is not empty and it should!")
  
  logging.info("Anonymization finished. Output available in  {}".format(args.output.name))
  
  args.output.close()
  
  
def perform_anonymization(args, input_file, regex_module, source_names_module, target_names_module, address_module):
  time_start = default_timer()
  logging.info("Starting process")
  logging.info("Running {0} workers at {1} rows per block".format(args.processes, args.block_size))
  
  process_count = max(1, args.processes)
  maxsize = 1000 * process_count
  
  output_queue = Queue(maxsize = maxsize)
  worker_count = process_count
  
  #Start reducer
  reduce = Process(target=reduce_process, args = (output_queue, args))
  reduce.start()
  
  #Start workers
  jobs_queue = Queue(maxsize = maxsize)
  workers = []
  for i in range(worker_count):
    job = Process(target = anonymizer_process, args = (i, args, regex_module, source_names_module, target_names_module, address_module, jobs_queue, output_queue))
    job.daemon = True
    job.start()
    workers.append(job)
  
  #Mappers process
  nline = mapping_process(args, input_file, jobs_queue)
  input_file.close()
  
  #Worker termination
  for _ in workers:
    jobs_queue.put(None)
   
  logging.info("End mapping")  
  
  for w in workers:
    w.join()
    
  #Reducer termination
  output_queue.put(None)
  reduce.join()
  
  #Stats
  logging.info("Finished")
  elapsed_time = default_timer() - time_start
  logging.info("Total: {0} rows".format(nline))
  logging.info("Elapsed time {0:.2f} s".format(elapsed_time))
  logging.info("Troughput: {0} rows/s".format(int((nline*1.0)/elapsed_time)))

def main(args):
  logging.info("Executing main program...")
  sentences = NamedTemporaryFile(mode="w+", delete=True, dir=args.tmp_dir)
  
  #To do: allow raw files 
  #To do: keep format in raw input file, just add column
  if args.format=="tmx":
    try:
      args.input.close()
      with open(args.input.name, "rb") as filein:
        tmx2text(filein, sentences, args.srclang, args.trglang)
      sentences.seek(0) 
      
    except Exception as ex:
      tb = traceback.format_exc()
      print("Unable to extract text from TMX")
      logging.error(tb)
      sys.exit(1)
  else:
    sentences = args.input
      
 
#  trgsentences.seek(0)
    
  source_names_module = selectNamesModule(args.srclang)
  target_names_module = selectNamesModule(args.trglang)
  
  perform_anonymization(args, sentences, regex_module, source_names_module, target_names_module, address_module)
  
#  for src, trg in zip(srcsentences, trgsentences):
#    entities = anonymizer_core.extract( src, trg, args.srclang, args.trglang, regex_module, source_names_module, target_names_module, address_module)
#    args.output.write(src.strip("\n")+"\t"+trg.strip("\n")+"\t"+entity.serialize(entities)+"\n")

  #To do: rebuild tmx files with anotations from anonymizer
  if args.format=="tmx":
   #Rebuild TMX with anon 
   pass
  logging.info("Program finished")

if __name__ == '__main__':
  try:
    logging_setup()
    args = initialization() # Parsing parameters
    main(args)  # Running main program
  except Exception as ex:
    tb = traceback.format_exc()
    logging.error(tb)
    sys.exit(1)
