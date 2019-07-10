#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 17:11:40 2019

@author: abhishek-31
"""
import xml.etree.ElementTree as ET
import glob
import numpy as np
from multiprocessing import Process, Lock, Manager
import shutil
def findScore(*args, **kwargs):
    
    ma=kwargs['ma']
    mate=kwargs['mate']
    print("Inside the function of findTags")
#    if(kwargs.get('list_tags')!=None):
#        list_tags = kwargs['list_tags']
#    print(list_tags)        
    if(kwargs.get('file_path')!=None):
        file_name = kwargs['file_path']            
        tree = ET.parse(file_name)            
        root = tree.getroot()
    
       

        uList = []
        for child in root:
            if('KnowledgeData' in child.tag):
                for ch in child:
                    if('Instance' in ch.tag):
                        for newch in ch:
                            if('Contributors' in newch.tag):
                                for chi in newch:
                                    if('OwnerUserId' in chi.tag):
                                        if(chi.text not in uList):
                                            uList.append(chi.text)
        return uList
        
    elif(kwargs.get('file_name')!=None):
        file_name = kwargs['file_name']
        for f in file_name:
            
            tree = ET.parse(f)            
            root = tree.getroot()
           # postList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch in child:
                        if('Instance' in ch.tag and ch.attrib['Id']=="1"):
                            for newch in ch:
                                if('Credit' in newch.tag):
                                    for txt in newch:
                                        if('Score' in txt.tag):
                                            kwargs["l"].acquire()
                                            mate["value"]+=1
                                            print(f+" : " + "score is"+ txt.text)
                                            if(int(txt.text)>=4):
                                                shutil.copy(f, '/home/abhishek/Documents/Quantum-threshold')
                                            ma[txt.text]=ma.get(txt.text,0)+1
                                            print(ma[txt.text])
                                            kwargs["l"].release()
            kwargs['ma']=ma                                

           # if(kwargs.get('tagPosts')!=None):
               # if(kwargs['tagPosts'].get(f)!=None):
                 #   kwargs['tagPosts'][f] = postList
                 #print(kwargs['revisionLength'])
                

def findAllScore(*args, **kwargs):
    #t1 = time.time()
    
    
    if(kwargs.get('file_list')!=None):
        file_list = kwargs['file_list']
        
    elif(kwargs.get('dir_path')!=None):
        dir_path = kwargs['dir_path']
        
        file_list = glob.glob(dir_path+'/*.knolml')
        
    fileNum = len(file_list)
    print(fileNum)
    if(kwargs.get('c_num')!=None):
        cnum = kwargs['c_num']
    elif(fileNum<24):
        cnum = fileNum+1           # Bydefault it is 24
    else:
        cnum = 24
    
    
    fileList = []
    if(fileNum<cnum):
        for f in file_list:
            fileList.append([f])
        
    else:           

        f = np.array_split(file_list,cnum)
        for i in f:
            fileList.append(i.tolist())        
    
    
    
    manager = Manager()
    tagPosts = manager.dict()
    ma=manager.dict()
    mate=manager.dict()
    mate["value"]=0
    l = Lock()
    processDict = {}
    if(fileNum<cnum):
        pNum = fileNum
    else:
        pNum = cnum
    for i in range(pNum):
        processDict[i+1] = Process(target=findScore, kwargs={'file_name':fileList[i],'mate':mate,'tagPosts':tagPosts,'l': l,'ma':ma})
        
        #processDict[i+1] = Process(target=self.countWords, kwargs={'file_name':fileList[i], 'lastRev':lastRev,'l': l})
    for i in range(pNum):
        processDict[i+1].start()
    
    for i in range(pNum):
        processDict[i+1].join()  
    
    '''
    t2 = time.time()
    print(t2-t1)
    '''
    #print(l)
    print(len(ma))
    x=0
    for key,val in ma.items():
        x=x+val
        print(str(key) +" : "+str(val))
    
    print(x)
    print(mate["value"])
    return tagPosts 
