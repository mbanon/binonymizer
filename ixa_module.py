#!/usr/bin/env python

#ixa-module:  extracts name entities for EU, writes tempfile with numline, entities.
import logging
import entity
import sys

#TO DO
#sys.path.append("/home/mbanon/project/anonymizer/anonymizer/prompsit-python-bindings/")

#import prompsit_python_bindings.ixa as ixa

#
#import sys
#
##TO DO
#sys.path.append("/home/mbanon/project/anonymizer/anonymizer/prompsit-python-bindings/")
#import prompsit_python_bindings.ixa
#
#tagger=prompsit_python_bindings.ixa.IXANERPipeline('eu')  



class IxaObject():

  def __init__(self):
    self.tagger = None
    self.mode = None

  def __init__(self, lang):
    self.tagger  = prompsit_python_bindings.ixa.IXANERPipeline(lang)
    self.mode = prompsit_python_bindings.ixa.Mode.ENTITY_DETECTION

  def get_tagger(self):
    return self.tagger

  def attachThreadToJVM(self):
    if not jpype.isThreadAttachedToJVM():
      jpype.attachThreadToJVM()  

  def extract(self, sentence):
  
    entities = []
     #  sentences = []
     #  sentences.append(sentence)
     #  print(sentences)
  
    tags = self.tagger.nertag([sentence], self.mode)
     #tags is an array
     #  print(tags)
     #  tag_array = entity.deserializeArray((tags))
    for t in tags:
      ent = entity.Entity( t.get("start"), t.get("length"), t.get("type"), t.get("entity") )
      entities.append(ent)
    return entities

 