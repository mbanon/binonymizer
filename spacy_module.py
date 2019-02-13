#!/usr/bin/env python

#spacy-module:  extracts name entities for EU, writes tempfile with numline, entities.
import spacy
import logging
import entity
import sys

def load_spacy_model(lang):
  logging.debug("Import lang package for " + lang)
  
  if lang in ["en"]:  
    spacy.cli.download("en_core_web_sm")    
    return spacy.load("en_core_web_sm")
  elif lang in ["de"]:
    spacy.cli.download("de_core_news_sm")
    return spacy.load("de_core_news_sm")
  elif lang in ["fr"]:
    spacy.cli.download("fr_core_news_sm")
    return spacy.load("fr_core_news_sm")
  elif lang in ["es"]:
    spacy.cli.download("es_core_news_sm")
    return spacy.load("es_core_news_sm")
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

def normalize_label(label):
  per_labels = ["PER", "PERSON"]
  org_labels = ["ORG", "NORP"]
  misc_labels = ["MISC", "PRODUCT"]
  unwanted_labels = ["FAC", "GPE", "LOC", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]

  if label in unwanted_labels:
    return None  
  if label in per_labels:
    return "PER"
  elif label in org_labels:
    return "ORG"
  elif label in misc_labels:
    return "MISC"
  else:
    loging.warning("Unknown NER label found: " + label)
    return "OTHER"   


def extract(sentence, nlp):  
  entities = []  
  doc = nlp(sentence)
  for t in doc.ents:
  #https://spacy.io/api/span#attributes
    normalized_label = normalize_label(t.label_)      
    if normalized_label != None:
      ent = entity.Entity(t.start_char, t.end_char - t.start_char, normalized_label, t.text)
      entities.append(ent)
  return entities

 