#!/usr/bin/env python

#regex-module: extracts email addresses, phone numbers, DNIs, passports, IP addresses, GPS coordinates. 
#writes tempfile with numline, entities.

import re
import entity
import logging

__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"



#https://www.regextester.com/19
#to check
email_regex = re.compile(r"([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)")


#https://www.regextester.com/1978
#to check
phone_regex = re.compile(r"((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))")



##Spain##
DNI_regex = re.compile(r"\b([0-9]{7,8}[-\ ]{0,1}[A-Za-z])\b")
#http://www.nie.com.es/ejemplo.html
NIE_regex = re.compile(r"\b([xXyYzZ][-\ ]{0,1}[0-9]{7}[-\ ]{0,1}[A-Za-z])\b")


#https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
IPv4_regex = re.compile(r"((?:[0-9]{1,3}\.){3}[0-9]{1,3})")
#https://www.regextester.com/25
IPv6_regex = re.compile(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")


GPS_regex = re.compile(r"")

def extract(sentences,  regex_entities):
  logging.debug("Extracting regex...")
  
  sentences.seek(0)
  for sentence in sentences:
    entities = []
    entities.extend(extract_emails(sentence))
    entities.extend(extract_phones(sentence))
    entities.extend(extract_IDs(sentence))
    entities.extend(extract_IPs(sentence))
    entities.extend(extract_GPSs(sentence))
    regex_entities.write(entity.serializeArray(entities))
#  print(regex_entities)  
#  output_queue = regex_entities
  logging.debug("Exiting regex extract...")
  return

def extract_emails(sentence):
  emails = []
  return emails

def extract_phones(sentence):
  phones = []
  return phones

def extract_IDs(sentence):
  IDs = []
  return IDs

def extract_IPs(sentence):
  IPs = []
  return IPs

def extract_GPSs(sentence):
  GPSs = []
  return GPSs