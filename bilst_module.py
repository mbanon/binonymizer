#!/usr/bin/env python

#bilst-module: extracts name entities for ES/EN, writes tempfile with numline, entities.
import logging
import entity

def extract(sentences,  bilst_entities):
  logging.debug("Extracting Bilst...")
  sentences.seek(0)
  for sentence in sentences:
    entities = []
    bilst_entities.write(entity.serializeArray(entities))
  
  logging.debug("Exiting bilst extract...")
  return

 


