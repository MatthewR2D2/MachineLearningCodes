# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 08:53:14 2018
Not the best need to change to split up training data and testing data
That will happen in a later version
@author: Matt
"""
#%matplotlib inline
import matplotlib.pyplot as plt
import csv
from textblob import TextBlob
import pandas
import sklearn
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split 
from sklearn.tree import DecisionTreeClassifier 
from sklearn.learning_curve import learning_curve

#File location 
file = './SpamDetection/smsspamcollection/SMSSpamCollection'

#tokenizer method
def split_into_tokens(message):
    message = str(message)  # convert bytes into proper unicode
    return TextBlob(message).words

#Normalize each word into the base form
def split_into_lemmas(message):
    message = str(message).lower()
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma 
    return [word.lemma for word in words]


#Data from UCI machine learning database
#looks at raw data to see information and basic stats
messages1 = [line.rstrip() for line in open(file)]
print (len(messages1))
for message_no, message1 in enumerate(messages1[:10]):
    print (message_no, message1)

#Use panda to set up the data
messages = pandas.read_csv(file, sep='\t', quoting=csv.QUOTE_NONE,
                           names=["label", "message"])
print (messages)
#Graph for easy anayslis and description of the messages
messages.groupby('label').describe()
messages['length'] = messages['message'].map(lambda text: len(text))
print (messages.head())

messages.length.plot(bins=20, kind='hist')
print (messages.length.describe())

#Look at message lenght difference between Spam and regular email
messages.hist(column='length', by='label', bins=50)

#Tokenize the messages
print (messages.message.head().apply(split_into_tokens))
#Base forms
print (messages.message.head().apply(split_into_lemmas))

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(messages['message'])
print (len(bow_transformer.vocabulary_))

message4 = messages['message'][3]
print (message4)

bow4 = bow_transformer.transform([message4])
print (bow4)
print (bow4.shape)

messages_bow = bow_transformer.transform(messages['message'])
print ('sparse matrix shape:', messages_bow.shape)
print ('number of non-zeros:', messages_bow.nnz)
print ('sparsity: %.2f%%' % (100.0 * messages_bow.nnz / (messages_bow.shape[0] * messages_bow.shape[1])))

#weighting and normalization
tfidf_transformer = TfidfTransformer().fit(messages_bow)
tfidf4 = tfidf_transformer.transform(bow4)
print ('TFID: ', tfidf4)

#for frequencies of words
#print (tfidf_transformer.idf_[bow_transformer.vocabulary_['u']])

# transform the entire bag-of-words corpus into TF-IDF corpus
messages_tfidf = tfidf_transformer.transform(messages_bow)

#Train the model
spam_detector = MultinomialNB().fit(messages_tfidf, messages['label'])

#Test out model with control
print ('predicted:', spam_detector.predict(tfidf4)[0])
print ('expected:', messages.label[3])

#Test on all data
all_predictions = spam_detector.predict(messages_tfidf)
print ('All Data Prediction', all_predictions)
#Examine the model
print ('accuracy', accuracy_score(messages['label'], all_predictions))
print ('confusion matrix\n', confusion_matrix(messages['label'], all_predictions))
print ('(row=expected, col=predicted)')

#Generate plots for vizulization
plt.matshow(confusion_matrix(messages['label'], all_predictions), cmap=plt.cm.binary, interpolation='nearest')
plt.title('confusion matrix')
plt.colorbar()
plt.ylabel('expected label')
plt.xlabel('predicted label')

#Make a nice report
print (classification_report(messages['label'], all_predictions))




