#!/usr/bin/env python


#binonymizer_lite.py: Monothread entry point.
#Wraps the binonymizer-core.py, preparing the input and processing the output. 
#Takes the entry file (raw src-trg, tmx...), 
#and extracting the source and the target sentences,
#generating (in the case of tmx files) a raw parallel corpus,
#that will be input to the binonymizer-core.
#when the binonymizer-core.py finishes, builds the annotated TMXs (if the entry was a TMX file)


import argparse
import logging
import os
import sys
import traceback

from tempfile import NamedTemporaryFile, gettempdir
from timeit import default_timer


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
Reads a file (tmx or columns),
extracts  entities from each pair of parallel sentences,
writes an anonymized file.
  args: Arguments given to the script
  filein: Input file
  regex_module: Module used to extract entities with regular expressions (emails, phone numbers...)
  source_names_module: Module (in the form of an object) used to extract NERs in the source 
  target_names_module: Module (in the form of an object) used to extract NERs in the target
  address_module: Module used to extract address entities
"""  
def binonymizer_process(args, filein, regex_module, source_names_module, target_names_module, address_module):
  nline = 0
  time_start = default_timer()
  with  open(args.output.name, "w") as fileout:
    for i in filein:
      nline = nline + +1
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
    #filein.close()
    #fileout.close()

  logging.info("Anonymization finished. Output available in  {}".format(args.output.name))
  #Stats
  util.write_stats(time_start, nline)
 
  args.output.close()
  
  
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
      
 
  source_names_module = binonymizer_core.selectNamesModule(args.srclang)
  target_names_module = binonymizer_core.selectNamesModule(args.trglang)
  

  binonymizer_process(args, sentences, regex_module, source_names_module, target_names_module, address_module)

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
