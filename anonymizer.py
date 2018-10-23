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


import logging
import traceback
import sys 
import argparse
import os
from itertools import zip_longest

from tempfile import NamedTemporaryFile, gettempdir
#from multiprocessing import cpu_count
import anonymizer_core

try:
  from .util import logging_setup
#  from .anonymizer_core import extract
  from .tmx_utils import tmx2text
except (ImportError, SystemError):
  from util import logging_setup
#  from anonymizer_core import extract
  from tmx_utils import tmx2text
  
  
__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"


def initialization():
  logging.info("Processing arguments...")
  # Getting arguments and options with argparse
  # Initialization of the argparse class
  parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)
  # Mandatory parameters
  ## Input file (TMX). Try to open it to check if it exists
  parser.add_argument('input', type=argparse.FileType('rb'), default=None, help="TMX file to be anonymized")
  ## Output file (TMX). Try to open it to check if it exists
  parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="TMX file with anonymization annotations")
  parser.add_argument("srclang", type=str, help="Source language (SL) of the input")
  parser.add_argument("trglang", type=str, help="Target language (TL) of the input")
    
  # Options group
  groupO = parser.add_argument_group('Optional')
  groupO.add_argument('--tmp_dir', default=gettempdir(), help="Temporary directory where creating the temporary files of this program")
#  groupO.add_argument('-b', '--block_size', type=int, default=10000, help="Sentence pairs per block")
#  groupO.add_argument('-p', '--processes', type=int, default=max(1, cpu_count()-1), help="Number of processes to use")

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


def main(args):
    logging.info("Executing main program...")
    srcsentences = NamedTemporaryFile(mode="w+", delete=True, dir=args.tmp_dir)
    trgsentences = NamedTemporaryFile(mode="w+", delete=True, dir=args.tmp_dir)

    try:
      tmx2text(args.input, srcsentences, trgsentences, args.srclang, args.trglang)
      srcsentences.seek(0)
      trgsentences.seek(0)

    except Exception as ex:
      tb=traceback.format_exc()
      print("Unable to extract text from TMX")
      logging.error(tb)
      sys.exit(1)
    srcsentences.seek(0)  
    trgsentences.seek(0)
    anonymizer_core.extract(args.output, srcsentences, trgsentences, args.tmp_dir, args.srclang, args.trglang)
    #args.output.seek(0)
#    for i in args.output:
#      print(i)
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
