#!/usr/bin/env python

#ixa-module:  extracts name entities for EU, writes tempfile with numline, entities.
import logging
import entity

def extract(sentences,  ixa_entities):
  logging.debug("Extracting IXA...")
  sentences.seek(0)
  for sentence in sentences:
    entities = []
    ixa_entities.write(entity.serializeArray(entities))
  
#  output.put(ixa_entities)  
  logging.debug("Exiting ixa extract...")
  return 

 