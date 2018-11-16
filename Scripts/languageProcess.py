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
# Set lists with character/words to exclude
stop    = set(stopwords.words('english'))
exclude = set(string.punctuation)
# Set lematizer to increase Frequency for words with the same word stem
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

direc = '../../data/wiki/AA/'
path = os.path.join(direc,'wiki_00')

data=[]
for line in open(path, 'r'):
    data.append(json.loads(line))
test=data[1]['text']
test_clean=clean(test)
print(test_clean)
#^(?!\[\[Category).*$#