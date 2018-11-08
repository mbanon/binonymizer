#!/usr/bin/env python

#ixa-module:  extracts name entities for EU, writes tempfile with numline, entities.
import logging
import entity
import sys

#TO DO
sys.path.append("/home/motagirl2/projects/anonymizer/ixa-pipe-ner-python/ixa_pipes_python")

import ixa_pipes_python.pipeline
tagger=ixa_pipes_python.pipeline.IXANERPipeline('eu')

def extract(sentence):
  
  entities = []
  
  tags = tagger.nertag(sentences)
  process_tags(tags)
  return entities

 