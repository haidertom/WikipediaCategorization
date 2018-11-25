import nltk
import json
import pyLDAvis
import pyLDAvis.gensim
from pprint import pprint
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from gensim.models import LsiModel
import os
from pprint import pprint

class Similarity:
    '''def __init__(self,filename,index):
        with open(filename, 'r') as fil:
            data=json.load(fil)
            wikiString = data[index]['revision']['text']'''




    def parser(self, filename, index):
        data=[]
        for line in open('wiki_00.json','r'):
            data.append(json.loads(line))
            #wikiString = data[1]['text']

        '''with open(filename, 'r') as fil:
            data=json.load(fil)
            wikiString = data[index]['text']
            #wikiString2 = data[2]['revision']['text']'''
        return data[2]['text']


    def cleanString(self,wikitext):
        stop_words = set(stopwords.words('english'))
        is_noun = lambda pos: pos[:2] == 'NN'
        htmlTags = ['ref','www','http','https']
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        wikiTokens=tokenizer.tokenize(wikitext)
        #exclude Stopwords
        tokens = [w for w in wikiTokens if w.lower() not in (stop_words or htmlTags) or not w.isdigit()]
        #exclude numbers
        #tokens = [w for w in tokens if not w.isdigit()]
        #extract nouns
        tokens = [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]
        #filter for html tags

        #set everything to lower case
        tokens = [w.lower() for w in tokens]
        return tokens

    def SaveDictionary(self, alltockens, dicname):
        dictionary = corpora.Dictionary(alltockens)
        dictionary.save(dicname)
        #dictionary = corpora.Dictionary.load(dicname)
        return dictionary

    def loadDictionary(self, dicname):
        dictionary = corpora.Dictionary.load(dicname)
        return dictionary

    def saveCorpus(self, altokens, corpusname,dicname):
        dictionary = corpora.Dictionary.load(dicname)
        corpus = [dictionary.doc2bow(text) for text in altokens]
        corpora.MmCorpus.serialize(corpusname,corpus)
        return corpus

    def loadCorpus(self, corpusname):
        corpus = corpora.MmCorpus(corpusname)
        return corpus



    def lsi(self,corpus,dictionary, num_topics):
        lsimodel=LsiModel(corpus=corpus, id2word=dictionary,num_topics=num_topics)
        return lsimodel

    #Assumed a Single LSI model
    def saveIndex(self, corpus,dictionary, num_topics, indexname):
        lsimodel=LsiModel(corpus=corpus, id2word=dictionary,num_topics=num_topics)
        index = similarities.MatrixSimilarity(lsimodel[corpus]) # transform corpus to LSI space and index it
        index.save(indexname)
        return index

    def Similarity(self,corpus, dictionary, num_topics, indexname, quaryDoc):
        #corpus=self.loadCorpus(corpus)
        corpus=corpus
        dictionary=dictionary
        index=indexname
        #dictionary=self.loadDictionary(dictionary)
        lsimodel=self.lsi(corpus,dictionary,num_topics)
        #LsiModel(corpus=corpus, id2word=dictionary,num_topics=num_topics)
        index = similarities.MatrixSimilarity.load(indexname)
        vec_bow = dictionary.doc2bow(quaryDoc.lower().split())
        vec_lsi = lsimodel[vec_bow] # convert the query to LSI space
        #sims = index[vec_lsi] # perform a similarity query against the corpus
        sims = sorted(enumerate(index[vec_lsi]), key=lambda item: -item[1])
        return sims

#Here needs a sort of loop to extract all the files
quary_doc = "Anarchism is a political theory, which is skeptical of the justification of authority and power, especially political power. Anarchism is usually grounded in moral claims about the importance of individual liberty. Anarchists also offer a positive theory of human flourishing, based upon an ideal of non-coercive consensus building."
num_topics=2
corpus_name='draft.mm'
dict_name='draft.dict'
index_name='indexdraft.index'
obj = Similarity()
Alltockens=[obj.cleanString(obj.parser('wiki_00.json',1)),obj.cleanString(obj.parser('0_wiki_part.json',2))]
#print(Alltockens)
'''LSI =obj.lsi(obj.loadCorpus(corpus_name),obj.loadDictionary(dict_name),num_topics).show_topics()
Dic= obj.loadDictionary(dict_name)
Cor = obj.loadCorpus(corpus_name)'''

print(obj.SaveDictionary(Alltockens,corpus_name))
print(obj.saveCorpus(Alltockens, corpus_name,dict_name))
print(obj.lsi(obj.loadCorpus(corpus_name),obj.loadDictionary(dict_name),num_topics).show_topics())
print(obj.saveIndex(obj.loadCorpus(corpus_name),obj.loadDictionary(dict_name),num_topics,index_name))
print(obj.Similarity(obj.loadCorpus(corpus_name),obj.loadDictionary(dict_name),num_topics,index_name,quary_doc))

#print(obj.cleanString(obj.parser('0_wiki_part.json',2)))

