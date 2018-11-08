# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:42:18 2018

Convert Words to Feaatures example
Then classify it with Naive Bayes classifier
@author: Matthew 
"""

import nltk
import random
import pickle 
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


#Methods
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features




documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]

#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

# split the reatureset into training and testing data
trainingSet = featuresets[:1900]
testingSet = featuresets[1900:]

#Create a Naive Bayes classifier based on training sets
classifier = nltk.NaiveBayesClassifier.train(trainingSet)

print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testingSet))*100)


#show most valueable words
classifier.show_most_informative_features(15)

#Save the classifier
save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

#read in classifier from file
classifier_f = open("naivebayes.pickle", "rb")
classifier = pickle.load(classifier_f)
classifier_f.close()

#Scikit methods
MNBClassifier = SklearnClassifier(MultinomialNB())
MNBClassifier.train(trainingSet)
print("MultinomialNB accuracy percent:",nltk.classify.accuracy(MNBClassifier, testingSet))

BNBClassifier = SklearnClassifier(BernoulliNB())
BNBClassifier.train(trainingSet)
print("BernoulliNB accuracy percent:",nltk.classify.accuracy(BNBClassifier, testingSet))

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(trainingSet)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testingSet))*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(trainingSet)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testingSet))*100)

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(trainingSet)
print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testingSet))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(trainingSet)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testingSet))*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(trainingSet)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testingSet))*100)






