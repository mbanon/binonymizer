#!/usr/bin/env python

#spacy-module:  extracts name entities for EU, writes tempfile with numline, entities.
import spacy
import logging
import entity
import sys


def extract(sentence, nlp):
  
  entities = []
  
  
  doc = nlp(sentence)
  for t in doc.ents:
  #https://spacy.io/api/span#attributes
    ent = entity.Entity(t.start_char, t.end_char - t.start_char, t.label_, t.text )
    entities.append(ent)
  return entities

 