#!/usr/bin/env python

#Extracts addresses
import logging
from tempfile import NamedTemporaryFile

import entity

def extract(sentences, address_entities):
  logging.debug("Extracting addresses...")
  sentences.seek(0)
  for sentence in sentences:
    entities = []
    address_entities.write(entity.serializeArray(entities))
  
  logging.debug("Exiting address extract...")
  return

 


 


