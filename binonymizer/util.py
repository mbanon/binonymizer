#!/usr/bin/env python

import logging
import sys
from timeit import default_timer

try:
  from . import entity
except (ImportError, SystemError):
  import entity


# Logging config
def logging_setup(args = None):
    logger = logging.getLogger()
    logger.handlers = [] # Removing default handler to avoid duplication of log messages
    logger.setLevel(logging.ERROR)
    
    h = logging.StreamHandler(sys.stderr)
    if args != None:
       h = logging.StreamHandler(args.logfile)
      
    h.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(h)

  #logger.setLevel(logging.INFO)

    if args != None:
        if not args.quiet:
            logger.setLevel(logging.INFO)
        if args.debug:
            logger.setLevel(logging.DEBUG)

"""
Writes the performance stats at the end of the process
  time_start: Start time (beginning of measure)
  nline: Amount of lines processed
"""
def write_stats(time_start, nline):
  logging.info("Finished")
  elapsed_time = default_timer() - time_start
  logging.info("Total: {0} rows".format(nline))
  logging.info("Elapsed time {0:.2f} s".format(elapsed_time))
  logging.info("Troughput: {0} rows/s".format(int((nline*1.0)/elapsed_time)))


"""
Normalizes all posible labels given by NER taggers into those interesting for anonymizing data
"""
def normalize_label(label):
  per_labels = ["PER", "PERSON", "I-PER"]
  org_labels = ["ORG", "NORP", "I-ORG"]
  misc_labels = ["MISC", "PRODUCT"]
  unwanted_labels = ["FAC", "GPE", "LOC", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL", "I-LOC"]

  if label in unwanted_labels:
    return None  
  if label in per_labels:
    return entity.Label.PER
  elif label in org_labels:
    return entity.Label.ORG
  elif label in misc_labels:
    return entity.Label.MISC
  else:
    loging.warning("Unknown NER label found: " + str(label))
    return entity.Label.OTHER   
    
"""
Extracts uppercased words from a string, with lowercased words between them
"""
def extractUppercased(sentence):
  words = sentence.split()  #Naive tokenizing
  nonefound =True
  extracted = []
  pending = []
  
  for word in words:
    if word[0].isupper():
      nonefound = False
      extracted.extend(pending)
      pending = []
      extracted.append(word)    
    else: 
      if nonefound:
        continue
      else:
        pending.append(word)
         

  return " ".join(extracted)
  