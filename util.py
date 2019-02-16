#!/usr/bin/env python

import logging
import sys
from timeit import default_timer


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
