#!/usr/bin/env python

#spacy-module:  extracts name entities for EU, writes tempfile with numline, entities.
import spacy
#import sputnik
import logging
import entity
import sys

def load_spacy_model(lang):
  logging.debug("Import lang package for " + lang)
  
  if lang in ["en"]:  
    spacy.cli.download("en_core_web_md")    
    return spacy.load("en_core_web_md")
  elif lang in ["de"]:
    spacy.cli.download("de_core_news_sm")
    return spacy.load("de_core_news_sm")
  elif lang in ["fr"]:
    spacy.cli.download("fr_core_news_md")
    return spacy.load("fr_core_news_md")
  elif lang in ["es"]:
    spacy.cli.download("es_core_news_md")
    return spacy.load("es_core_news_md")
  elif lang in ["it"]:
    spacy.cli.download("it_core_news_sm")
    return spacy.load("it_core_news_sm")
  elif lang in ["pt"]:
    spacy.cli.download("pt_core_news_sm")
    return spacy.load("pt_core_news_sm")  
  elif lang in ["nl"]:
    spacy.cli.download("nl_core_news_sm")
    return spacy.load("nl_core_news_sm")
  elif lang in ["bg", "da", "el", "sk", "sl", "sv", "ga", "hr", "mt", "lt", "hu", "et", "pl", "cs", "ro", "fi", "lv"]:
    spacy.cli.download("xx_ent_wiki_sm")
    return spacy.load("xx_ent_wiki_sm") 
  else:  #default
    spacy.cli.download("xx_ent_wiki_sm")
    return spacy.load("xx_ent_wiki_sm")

def extract(sentence, nlp):
  
  entities = []
  
  doc = nlp(sentence)
  for t in doc.ents:
  #https://spacy.io/api/span#attributes
    ent = entity.Entity(t.start_char, t.end_char - t.start_char, t.label_, t.text)
    entities.append(ent)
  return entities

 