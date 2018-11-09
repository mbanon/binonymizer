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


def extract(sentence):
  print("H_OLA")
  
  entities = []

  sentences = []
  sentences.append(sentence)
  print(sentences)
  
  tags = tagger.nertag(sentences)
  print(tags)
  #process_tags(tags)
  return entities

 