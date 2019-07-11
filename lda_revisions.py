#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:18:45 2019

@author: simransetia
"""

import matplotlib.pyplot as plt
import spacy
import random
import gensim
import pickle
import re
spacy.load('en')
from spacy.lang.en import English
from gensim import corpora
from gensim.corpora import Dictionary
parser = English()
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import wordnet as wn
en_stop = set(nltk.corpus.stopwords.words('english'))
spacy.load('en')
from spacy.lang.en import English
import xml.etree.cElementTree as ec
parser = English()
count=[0]*291
i=0
rev=0
p='1908 Auburn Tigers football team'
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        #print("word"+word)
        return word
    else:
        #print("lemma"+lemma)
        return lemma
    
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)
    #return stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v'))
# Function Call For Connecting To Our Database 

def prepare_text_for_lda(text):
    tokens1=[]
    tokens2=[]
    tokens = tokenize(text)
    for each in tokens:
        
        #print(each)
        if '\\n' in each:
            tokenss=str(each)
            tokenss=tokenss.replace('\\n','')
            #tokenss=list(tokenss)
            
            tokens1.append(tokenss)
        #elif each=='to' or each=='the' or each=='of' or each=='.' or each=="\\" :
            
            #tokens.remove(each)
        else:
            tokens1.append(each)
    tokens2 = [token for token in tokens1 if len(token) > 4]
    tokens3 = [token for token in tokens2 if token not in en_stop]
    tokens4 = [get_lemma(token) for token in tokens3]
    tokens5 = [get_lemma2(token) for token in tokens4]

    return tokens5




def LDA(p):
    rev=0
    f=open(p+" topics.txt","w")
    tree = ec.parse('/Users/simransetia/Documents/Dataset/C/'+p+'.xml')
    flag=0
    root = tree.getroot()
    for page in root:
        for child in page:
            if 'title' in child.tag:
                if child.text==p:
                    #print('yes')
                    flag=1
                else:
                    flag=0
        
            if 'revision' in child.tag and flag==1:
                    #print(flag)
                for each in child:
                    if 'text' in each.tag:
                        s=each.text
                            
    
                            
                        if(s!=None):
                            tokens=prepare_text_for_lda(str(s))
                            text_data=[]
                            text_data.append(tokens)
                    
                            #print(rev)
                            dictionary = corpora.Dictionary(text_data)
                            corpus = [dictionary.doc2bow(text) for text in text_data]
                            if(rev==3238):
                                print(corpus)                            
                            pickle.dump(corpus, open('corpus.pkl', 'wb'))
                            dictionary.save('dictionary.gensim')
                            NUM_TOPICS = 2
                            if(corpus!=[[]]):
                                ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
                                ldamodel.save('model5.gensim')
                                topics = ldamodel.print_topics(num_words=4)
                                for topic in topics:
                                    topic=str(topic)  
                                        #print(topic)
                                    f.write("\n"+topic+"\n")
                                    f.write("************************************")
    print(p+" done")

plist=['1908 Auburn Tigers football team'
]
for p in plist:
    LDA(p)