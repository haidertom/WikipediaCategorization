import json
from pprint import pprint
from nltk.corpus import stopwords
import os
from pprint import pprint
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import sys

stop    = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma   = WordNetLemmatizer()
#source: https://appliedmachinelearning.blog/2017/08/28/topic-modelling-part-1-creating-article-corpus-from-simple-wikipedia-dump/  
def clean(doc):
# remove stop words & punctuation, and lemmatize words
  s_free  = " ".join([i for i in doc.lower().split() if i not in stop])
  p_free  = ''.join(ch for ch in s_free if ch not in exclude)
  lemm    = " ".join(lemma.lemmatize(word) for word in p_free.split())
  words   = lemm.split()
 
  # only take words which are greater than 2 characters
  cleaned = [word for word in words if len(word) > 2]
  return cleaned

direc = '../DataSnippets/category_space/'
path = os.path.join(direc,'0_wiki_part.json')
print(path)
with open(path, 'r') as f:
    data = json.load(f)

wikiString = data[1]['revision']['text']
wikiString2 = data[2]['revision']['text']
print(wikiString)
print(clean(wikiString))
