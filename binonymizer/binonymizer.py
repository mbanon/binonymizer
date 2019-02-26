#!/usr/bin/env python


#binonymizer.py: Entry point.
#Wraps the binonymizer-core.py, preparing the input and processing the output. 
#Takes the entry file (raw src-trg, tmx...), parallelizing if needed,
#and extracting the source and the target sentences,
#generating (in the case of tmx files) a raw parallel corpus,
#that will be input to the binonymizer-core.
#when the binonymizer-core.py finishes, builds the annotated TMXs (if the entry was a TMX file)



#We need to decide if we paralelize at lines/tus scope (in case of few files with a lot of lines)
#or at document scope (in case of a lot of files with few lines) 



import argparse
import logging
import os
import sys
import traceback

from tempfile import NamedTemporaryFile, gettempdir
from timeit import default_timer
from multiprocessing import Queue, Process,  cpu_count
from heapq import heappush, heappop


try:
  from .tmx_utils import tmx2text
  from . import binonymizer_core
  from . import util
  from . import merger_module
  from . import address_module
  from . import regex_module
  from . import entity
except (ImportError, SystemError):
  from tmx_utils import tmx2text
  import binonymizer_core
  import util
  import merger_module
  import address_module
  import regex_module
  import entity
  
  
__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 20181005 # Initial release # Marta Bañón"
__version__ = "Version 0.2 # 20180207 # Integrating SpaCy # Marta Bañón" 

def initialization():
  logging.info("Processing arguments...")
  # Getting arguments and options with argparse
  # Initialization of the argparse class
  parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

  # Mandatory parameters
  parser.add_argument('input', type=argparse.FileType('r'), default=None, help="File to be anonymized")
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
  util.logging_setup(args)
  logging.debug("Arguments processed: {}".format(str(args)))
  if args.format=="tmx" and args.input.name=="<stdin>":
    logging.error("Cannot process TMX from standard input.")
    sys.exit(1)
  logging.info("Arguments processed.")
  return args

"""
  args: Arguments given to the script
  regex_module: Module used to extract entities with regular expressions (emails, phone numbers...)
  source_names_module: Module (in the form of an object) used to extract NERs in the source 
  target_names_module: Module (in the form of an object) used to extract NERs in the target
  address_module: Module used to extract address entities
"""   
def binonymizer_process(i, args, regex_module, address_module, jobs_queue, output_queue):  
  while True:  
    job = jobs_queue.get()    
    if job:
      source_names_module = binonymizer_core.selectNamesModule(args.srclang)
      target_names_module = binonymizer_core.selectNamesModule(args.trglang)
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

          entities = binonymizer_core.extract( src, trg, args.srclang, args.trglang, regex_module, source_names_module, target_names_module, address_module)

          if args.format == "cols":
            anon_source = binonymizer_core.overwrite(src, entities["l1"])
            anon_target = binonymizer_core.overwrite(trg, entities["l2"])
            parts[2] = anon_source
            parts[3] = anon_target        
            fileout.write("\t".join(parts))
          if args.format == "tmx":
            logging.error("Unsupported feature")  
          #fileout.write(i.strip()+"\t"+entity.serialize(entities)+"\n")
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
  
"""
  args: Arguments given to the script
  input_file: Input file
  regex_module: Module used to extract entities with regular expressions (emails, phone numbers...)
  source_names_module: Module (in the form of an object) used to extract NERs in the source 
  target_names_module: Module (in the form of an object) used to extract NERs in the target
  address_module: Module used to extract address entities
"""  
  
def perform_binonymization(args, input_file, regex_module, address_module):
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
 
    job = Process(target = binonymizer_process, args = (i, args, regex_module, address_module, jobs_queue, output_queue))
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
  util.write_stats(time_start, nline)
  

def main(args):
  logging.info("Executing main program...")
  sentences = NamedTemporaryFile(mode="w+", delete=True, dir=args.tmp_dir)
  
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
      
 
      
  perform_binonymization(args, sentences, regex_module,  address_module)

  #To do: rebuild tmx files with anotations from binonymizer
  if args.format=="tmx":
   #Rebuild TMX with anon 
   logging.warning("********************* Unsupported feature!! ********************")
   pass
  logging.info("Program finished")

if __name__ == '__main__':
  try:
    util.logging_setup()
    args = initialization() # Parsing parameters
    main(args)  # Running main program
  except Exception as ex:
    tb = traceback.format_exc()
    logging.error(tb)
    sys.exit(1)
