import json

import nltk
#nltk.download('words')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download(...) # all the other thins we use

from pprint import pprint
from nltk.corpus import stopwords
import os
from pprint import pprint
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
import string
import sys
import io
import re
import nltk
from collections import defaultdict

class languageProcess:
    '''
    The class languageProcess shall be used to preprocess plain wikipedia articles to cleaned tokens
    '''
    def __init__(self,path):
        # Set lists with character/words to exclude
        self.stop    = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)
        self.words = set(nltk.corpus.words.words())
        # Set lematizer to increase Frequency for words with the same word stem
        self.lemma   = WordNetLemmatizer()
        self.stem = PorterStemmer()
        self.path=path
        self.data=[]
        if os.path.exists(self.path):
            for line in open(self.path, 'r'):
                self.data.append(json.loads(line))
        else:
            print('LanguageProcess.py: path does not exist',self.path)
#source: https://appliedmachinelearning.blog/2017/08/28/topic-modelling-part-1-creating-article-corpus-from-simple-wikipedia-dump/
    def clean(self,doc):
        ''' 
        This function removes stop words & punctuation, lemmatize , stematize the given words.
        Furthermore, digits and words with a lenght lower than 2 character get ignored and onyl english are considered and returned as a list of tokens
        '''
        s_free  = " ".join([i for i in doc.lower().split() if i not in self.stop])
        p_free  = "".join(ch for ch in s_free if ch not in self.exclude)
        #exclude all non
        tokens = nltk.word_tokenize(p_free)
        tagged = nltk.pos_tag(tokens)
        nouns = [item[0] for item in tagged if item[1][0] == 'N']
        lemm    = [self.lemma.lemmatize(word) for word in nouns]
        stem = [self.stem.stem(word) for word in lemm]
        noDigit = [word for word in stem if not any(ch.isdigit() for ch in word)]
        onlyEng= [word for word in noDigit if word.lower() in self.words or not word.isalpha()]
        cleaned = [word for word in onlyEng if len(word) > 2]
        return cleaned
    def getWords(self):
        '''
        Returns list of words without sorting into articles
        '''
        return_tokens=[]
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            return_tokens+=(text_clean)
        return return_tokens

    def getWordsAsDict(self):
        '''
        Returns dict of words with sorting into articles
        '''
        return_tokens={}
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            return_tokens[d['title']]=text_clean
        return return_tokens
    def getHighFreqWords(self):
        '''
        Returns list of FreqDist objects with separation into articles
        '''
        tokens=[]
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            tokens.append(nltk.FreqDist(text_clean))

        return tokens
    def getHighFreqWordsAsDict(self):
        '''
        Returns dict of FreqDist objects with separation into articles key:title,value:list(tokens)
        '''
        tokens={}
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            tokens[d['title']]=nltk.FreqDist(text_clean)
        return tokens