#!/usr/bin/env python

#spacy-module:  extracts name entities 
import spacy
import logging
import sys


try:
  from . import util
  from . import entity
except (ImportError, SystemError):
  import util
  import entity


class SpacyObject:
  """
  SpacyObject constructor
  """ 
  def __init__(self):
    self.nlp = None
    
  """
  SpacyObject constructor
    lang: Language
  """
  def __init__(self, lang):
    self.nlp  = self.load_spacy_model(lang)
    
  """
  Retrieves the entity tagger from the SpacyObject
  """
  def get_tagger():
    return self.nlp        
  
  """
  Downloads language models (if needed) and loads a NER tagger for the given language
  """  
  def load_spacy_model(self,lang):
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
      

  """
  Extracts named entities from a sentence
  """
  def extract(self, sentence):  
    entities = []  
    doc = self.nlp(sentence)
    for t in doc.ents:
    #https://spacy.io/api/span#attributes
      normalized_label = util.normalize_label(t.label_)      
      if normalized_label != None:
        ent = entity.Entity(t.start_char, t.end_char - t.start_char, normalized_label, t.text)
        entities.append(ent)
    return entities

 