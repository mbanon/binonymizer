#!/usr/bin/env python

#ixa-module:  extracts name entities for EU, writes tempfile with numline, entities.
import logging
import sys
import jpype
import prompsit_python_bindings.ixa


try:
  from . import util
  from . import entity  
  #from .prompsit_python_bindings import ixa
except (ImportError, SystemError):
  import util
  import entity
  #import prompsit_python_bindings.ixa



class IxaObject():

  def __init__(self):
    self.tagger = None
    self.mode = None

  def __init__(self, lang):
    self.attachThreadToJVM()
    self.tagger  = prompsit_python_bindings.ixa.IXANERPipeline(lang)
    self.mode = prompsit_python_bindings.ixa.Mode.ENTITY_DETECTION

  def get_tagger(self):
    return self.tagger

  def attachThreadToJVM(self):
    if not jpype.isThreadAttachedToJVM():
      jpype.attachThreadToJVM()  
      
 
  def extract(self, sentence):
    entities = []
    tags = self.tagger.nertag([sentence], self.mode)
    for t in tags:
      label = util.normalize_label(t.get("type"))
      if label!=None:
        ent = entity.Entity( t.get("start"), t.get("length"), label, t.get("entity") )
        entities.append(ent)
    return entities

 