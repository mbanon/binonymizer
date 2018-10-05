#!/usr/bin/env python

import logging
import traceback
import sys 
import argparse
import os

from tempfile import gettempdir
from multiprocessing import cpu_count

try:
  from .util import logging_setup
except (ImportError, SystemError):
  from util import logging_setup
  
  
  
__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"



def initialization():
  logging.info("Processing arguments...")
  # Getting arguments and options with argparse
  # Initialization of the argparse class
  parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  # Mandatory parameters
  ## Input file (TMX). Try to open it to check if it exists
  parser.add_argument('input', type=argparse.FileType('rt'), default=None, help="TMX file to be anonymized")
  ## Output file (TMX). Try to open it to check if it exists
  parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="TMX file with anonymization annotations")
  
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
  logging.info("Arguments processed.")
  return args

def anonymizer_process(output_queue, source_lang, target_lang, tmpdir):
  #blah blah blah
  with MosesTokenizer(source_lang) as source_tokenizer, MosesTokenizer(target_lang) as target_tokenizer:
    while True:
      job = jobs_queue.get()
      if job:
        logging.debug("Job {0}".format(job.__repr__()))
        nblock, filein_name = job
        ojob = None
        with open(filein_name, 'r') as filein, NamedTemporaryFile(mode="w", delete=False, dir=tmpdir) as fileout:
          logging.debug("Anonymization: creating temporary filename {0}".format(fileout.name))          

          for tu in yieldTUsFromTMX(filein):  
            srcsen,trgsen = getSrcAndTrgFromTU(tu)
            if srcsen and trgsen:  #both exist
              entities = entities_extract(srcsen, trgsen, source_tokenizer, target_tokenizer, source_lang, target_lang)
              annotated_tu = buildAnnotatedTU(tu, entities)
              fileout.write(annotated_tu)
              fileout.write("\n")
              
          ojob = (nblock, fileout.name)
          filein.close()
          fileout.close()
          
        if ojob:
          output_queue.put(ojob)
        os.unlink(filein_name)  
      else:
        logging.debug("Exiting worker")
        break
        
def mapping_process(input, block_size, tmp_dir, jobs_queue):
    logging.info("Start mapping")
    nblock = 0
    nline = 0
    mytemp = None
    for nline, tu in yieldTUsFromTMX(input):
        if (nline % block_size) == 0:
            logging.debug("Creating block {}".format(nblock))
            if mytemp:
                job = (nblock, mytemp.name)
                mytemp.close()
                jobs_queue.put(job)
                nblock += 1
            mytemp = NamedTemporaryFile(mode="w", delete=False, dir=tmp_dir)
            logging.debug("Mapping: creating temporary filename {0}".format(mytemp.name))
        mytemp.write(tu)
        nline += 1

    if nline > 0:
        job = (nblock, mytemp.name)
        mytemp.close()        
        jobs_queue.put(job)

    return nline

def reduce_process(output, output_queue):
  h = []
  last_block = 0
  while True:
      logging.debug("Reduce: heap status {0}".format(h.__str__()))
      while len(h) > 0 and h[0][0] == last_block:
          nblock, filein_name = heappop(h)
          last_block += 1

          #?????  Mistery codeblock!
          with open(filein_name, 'r') as filein:
              for i in filein:
                  output.write(i)
              filein.close()
          os.unlink(filein_name)

      job = output_queue.get()
      if job:
          nblock, filein_name = job
          heappush(h, (nblock, filein_name))
      else:
          logging.debug("Exiting reduce loop")
          break

  if len(h) > 0:
      logging.debug("Still elements in heap")

  while len(h) > 0 and h[0][0] == last_block:
      nblock, filein_name = heapq.heappop(h)
      last_block += 1

      os.unlink(filein_name)
  if len(h) != 0:
      logging.error("The queue is not empty and it should!")

  logging.info("Anonymization finished. Output available in {}".format(output.name))
  output.close()
#    if args.discarded_tus:
#        logging.info("Discarded TUs are available in {}".format(args.discarded_tus.name))
#        args.discarded_tus.close()

def perform_anonymization(processes, block_size, input, output):
    time_start = default_timer()
    logging.info("Starting process")
    logging.info("Running {0} workers at {1} rows per block".format(processes, block_size))

    process_count = max(1, processes)
    maxsize = 1000 * process_count

    output_queue = Queue(maxsize = maxsize)
    worker_count = process_count

    # Start reducer
    reduce = Process(target = reduce_process,
                     args   = (output_queue, output))
    reduce.start()

    # Start workers
    jobs_queue = Queue(maxsize = maxsize)
    workers = []
    for i in range(worker_count):
        filter = Process(target = anonymizer_process, #profile_classifier_process
                         args   = (output_queue, source_lang, target_lang, tmpdir)) 
                         
        filter.daemon = True # dies with the parent process

        filter.start()
        workers.append(filter)

    # Mapper process (foreground - parent)
    nline = mapping_process(input, block_size, tmp_dir, jobs_queue)
    input.close()

    # Worker termination
    for _ in workers:
        jobs_queue.put(None)

    logging.info("End mapping")

    for w in workers:
        w.join()

    # Reducer termination
    output_queue.put(None)
    reduce.join()

    # Stats
    logging.info("Finished")
    elapsed_time = default_timer() - time_start
    logging.info("Total: {0} rows".format(nline))
    logging.info("Elapsed time {0:.2f} s".format(elapsed_time))
    logging.info("Troughput: {0} tus/s".format(int((nline*1.0)/elapsed_time)))
    ### END PARALLELIZATION METHODS ###


def main(args):
    logging.info("Executing main program...")
    perform_anonymization(args.processes, args.block_size, args.input, args.output)
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
