#!/usr/bin/env python

#ixa-module:  extracts name entities for EU, writes tempfile with numline, entities.
import logging
import entity

#
#import sys
#
##TO DO
#sys.path.append("/home/mbanon/project/anonymizer/anonymizer/prompsit-python-bindings/")
#import prompsit_python_bindings.ixa
#
#tagger=prompsit_python_bindings.ixa.IXANERPipeline('eu')  


def extract(sentence, tagger):
  
  entities = []
#  sentences = []
#  sentences.append(sentence)
#  print(sentences)
  
  tags = tagger.nertag([sentence], "ED")
  #tags is an array
#  print(tags)
#  tag_array = entity.deserializeArray((tags))
  for t in tags:
    ent = entity.Entity( t.get("start"), t.get("length"), t.get("type"), t.get("entity") )
    entities.append(ent)
  return entities

 