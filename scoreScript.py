#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 18:42:00 2019

@author: abhishek
"""
import xml.etree.ElementTree as ET
tree = ET.parse(f)            
root = tree.getroot()
postList = []
for child in root:
    if('KnowledgeData' in child.tag):
        for ch in child:
            if('Instance' in ch.tag and ch.attrib['Id']=="1"):
                for newch in ch:
                    if('Credit' in newch.tag):
                        for txt in newch:
                            if('Score' in txt.tag):                                            
                                print(txt.texts)
#                                 if(txt.text>=number):
#                                     postlist.append[f]

