#!/usr/bin/env python

import xml.parsers.expat
import re
#import pycld2 as cld2

  
__author__ = "Marta Bañón"
__version__ = "Version 0.1 # 05/10/2018 # Initial release # Marta Bañón"


curlang  = ""
curtuv = []
intuv = False
p = re.compile(r'<.*?>')
p1 = re.compile(r'\n')
p2 = re.compile(r'  *')
tu       = {}
exclude  = []

def tmx2text(tmxfile, sentences, srclang, trglang):
  #    tmx2txt(input, output, lang_list)
  langlist = [srclang, trglang]
  def se(name, attrs):
    global intuv, curtuv, tu, curlang
    if intuv:
      curtuv.append(u"")
    elif name == u"tu":
      tu = {i:u'' for i in langlist}
    elif name == u"tuv":
      if u"xml:lang" in attrs:
        curlang = attrs[u"xml:lang"]
      elif u"lang" in attrs:
        curlang = attrs[u"lang"]
    elif name == u"seg":
      curtuv = []
      intuv = True
    
  def ee(name):
    global intuv, curtuv, p, p1, p2, tu, curlang, exclude
    if name == u"tu":
#      for i in range(len(langlist)):
#        lang = langlist[i]
#        if cld2.detect(tu[lang].encode("utf-8"))[2][0][1] in exclude:
#          print("DISCARDED",tu[lang])
#          return
        
#        print(tu[srclang])
#        print(tu[trglang])
        sentences.write(tu[srclang]+"\t")
        sentences.write(tu[trglang]+"\n")
#        srcsentences.write("\n")
#        trgsentences.write("\n")
      
    elif name == u"seg":
      intuv = False
      mystr = p2.sub(u' ', p1.sub(u' ', p.sub(u' ', u"".join(curtuv)))).strip()
      tu[curlang] = mystr
      curlang = u""
    elif intuv:
      curtuv.append(u"")

  def cd(data):
    if intuv:
      curtuv.append(data)

  p = xml.parsers.expat.ParserCreate()
  p.StartElementHandler  = se
  p.EndElementHandler    = ee
  p.CharacterDataHandler = cd
  p.ParseFile(tmxfile) 
  
