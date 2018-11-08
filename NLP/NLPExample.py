# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:47:56 2018

@author: Matt
NLP test
"""
import nltk
import random
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet

#find synsets
syns = wordnet.synsets("program")
print(syns[0].name())
#Just the word
print(syns[0].lemmas()[0].name())
#Definition
print(syns[0].definition())
#print out examples of word in use
print(syns[0].examples())

#find synonyms and antonyms
synonyms = []
antonyms = []

for syn in wordnet.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
            
print(set(synonyms))
print(set(antonyms))

#word comparisions
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print('Similarity: ', w1.wup_similarity(w2))

#Text classification
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)
print(documents[1])

all_words = []
for w in movie_reviews.words():
    all_words.append(w.lower())
    
all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))
print(all_words["stupid"])








