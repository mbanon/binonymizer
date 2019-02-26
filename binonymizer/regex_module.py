#!/usr/bin/env python

#regex-module: extracts email addresses, phone numbers, DNIs, passports, IP addresses, GPS coordinates. 


import re
import logging


try:
  from . import entity
except (ImportError, SystemError):
  import entity


from itertools import chain


__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"



#Regular expression for emails
#https://www.regextester.com/19
email_regex = re.compile(r"(\b|^)([a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)(\b|$)")


#Regular expression for phone numbers
#https://www.regextester.com/1978
#phone_regex = re.compile(r"(\b|^)((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))(\b|$)")
#Marta's custom
phone_regex = re.compile(r"\(?(\+)?[\+\-\–\d]+[\(\)' '\+\-\–\d]{6,}\d\b")


#Regular expression for Spanish DNIs
##Spain##
DNI_regex = re.compile(r"(\b|^)([0-9]{7,8}[-\ ]{0,1}[A-Za-z])(\b|$)")
#Regular expression for Spanish NIEs
#http://www.nie.com.es/ejemplo.html
NIE_regex = re.compile(r"(\b|^)([xXyYzZ][-\ ]{0,1}[0-9]{7,8}[-\ ]{0,1}[A-Za-z])(\b|$)")

#Regular expression for v4 IP addresses
#https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
IPv4_regex = re.compile(r"((?:[0-9]{1,3}\.){3}[0-9]{1,3})")
#Regular expression for v6 IP addresses
#https://www.regextester.com/25
IPv6_regex = re.compile(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")


#GPS_regex = re.compile(r"")

"""
Applies regular expressiones to a sentence, to extract matching entities
"""
def extract(sentence):

  entities = []
  entities.extend(extract_emails(sentence))
  entities.extend(extract_phones(sentence))
  entities.extend(extract_IDs(sentence))
  entities.extend(extract_IPs(sentence))
  entities.extend(extract_GPSs(sentence))

  return entities

"""
Applies all email regular expressions to a sentence and extracts matching entities
"""
def extract_emails(sentence):
  emails = []
  
#  matches = email_regex.finditer(sentence)
#  if matches != None:
#    for i, m in enumerate(matches):
  for m in re.finditer(email_regex, sentence):
      e = entity.Entity(m.start(), m.end()-m.start(), "EMAIL", m.group(0))  # matches.end(i)-matches.start(i)
      emails.append(e)
  return emails

"""
Applies all phone number regular expressions to a sentence and extracts matching entities
"""
def extract_phones(sentence):
  phones = []    
#  matches = phone_regex.finditer(sentence)
#  if matches != None:
##    print(sentence)
#    for i, m in enumerate(matches):
#      e = entity.Entity(m.span(i)[0], m.span(i)[1]-m.span(i)[0], "PHONE", m.group(i))  # matches.end(i)-matches.start(i)
#      phones.append(e)
  for m in re.finditer(phone_regex, sentence):
      e = entity.Entity(m.start(), m.end()-m.start(), "PHONE", m.group(0))  # matches.end(i)-matches.start(i)
      phones.append(e)
  return phones

"""
Applies all IDs regular expressions to a sentence and extracts matching entities
"""
def extract_IDs(sentence):
  IDs = []
#  DNI_matches = DNI_regex.finditer(sentence)
#  NIE_matches = NIE_regex.finditer(sentence)
#  matches = chain(DNI_matches, NIE_matches)
#  if matches != None:
#    for i, m in enumerate(matches):
#      e = entity.Entity(m.span(i)[0], m.span(i)[1]-m.span(i)[0], "ID", m.group(i))  # matches.end(i)-matches.start(i)
#      IDs.append(e)

  for m in chain(re.finditer(DNI_regex, sentence), re.finditer(NIE_regex, sentence) ):
    e = entity.Entity(m.start(), m.end()-m.start(), "ID", m.group(0))  # matches.end(i)-matches.start(i)
    IDs.append(e)
      
  return IDs

"""
Applies all IP addresses regular expressions to a sentence, and extracts matching entities
"""
def extract_IPs(sentence):
  IPs = []
  return IPs

"""
Applies all GPS regular expressions to a sentence, and extracts matching entities
"""
def extract_GPSs(sentence):
  GPSs = []
  return GPSs