import json
from pprint import pprint
from nltk.corpus import stopwords
import os
from pprint import pprint
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import sys
import io
import re
import nltk
class languageProcess:
    def __init__(self,path):
        # Set lists with character/words to exclude
        self.stop    = set(stopwords.words('english'))
        self.exclude = set(string.punctuation)
        # Set lematizer to increase Frequency for words with the same word stem
        self.lemma   = WordNetLemmatizer()
        self.path=path
        self.data=[]
        if os.path.exists(self.path):
            for line in open(self.path, 'r'):
                self.data.append(json.loads(line))
        else:
            print('LanguageProcess.py: path does not exist')
#source: https://appliedmachinelearning.blog/2017/08/28/topic-modelling-part-1-creating-article-corpus-from-simple-wikipedia-dump/
    def clean(self,doc):
    # remove stop words & punctuation, and lemmatize words
        s_free  = " ".join([i for i in doc.lower().split() if i not in self.stop])
        p_free  = ''.join(ch for ch in s_free if ch not in self.exclude)
        lemm    = " ".join(self.lemma.lemmatize(word) for word in p_free.split())
        words   = lemm.split()

        # only take words which are greater than 2 characters
        cleaned = [word for word in words if len(word) > 2]
        return cleaned
    def getWords(self):
        return_tokens=[]
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            return_tokens+=(text_clean)
        return return_tokens
    def getWordsAsDict(self):
        return_tokens={}
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            return_tokens[d['title']]=text_clean
        return return_tokens
    def getHighFreqWords(self):
        tokens=[]
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            tokens.append(nltk.FreqDist(text_clean))

        return tokens
    def getHighFreqWordsAsDict(self):
        tokens={}
        for d in self.data:
            text=d['text']
            text_clean=self.clean(text)
            tokens[d['title']]=nltk.FreqDist(text_clean)
        return tokens

