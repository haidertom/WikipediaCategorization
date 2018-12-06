import os
import numpy as np
import languageProcess as lp
from gensim import corpora,similarities,models
from gensim.models import LsiModel



class LSIsimilarity:
    def __init__(self):
        self.articles=[]
        self.num_topics=0
    #This function trains the model
    def train(self,basepath='../Baseline/50/plaindata',noOfTrainArticle=5000):
        self.categories=os.listdir(basepath)
        if '.DS_Store' in self.categories:
            self.categories.remove('.DS_Store')
        self.num_topics = sum([1 for cat in self.categories])
                #Check if the dictionary/corpus/index is already created if so load it donot create a new one
        if (os.path.exists("dict"+str(noOfTrainArticle)+".dict")):
            self.dictionary = corpora.Dictionary.load("dict"+str(noOfTrainArticle)+".dict")
            self.corpus = corpora.MmCorpus("corpus"+str(noOfTrainArticle)+".mm1")
            self.index = similarities.MatrixSimilarity.load("index"+str(noOfTrainArticle)+".index")
         #If the dictionary/corpus/index is not already created create a new one and save it.
        else:
            for cat in self.categories:
                print("Train category: ",cat)
                cat_articles=[]
                path = basepath+"/"+cat
                dir_no=sum(os.path.isdir(path+"/"+i) for i in os.listdir(path))
                
                for no in range(dir_no)[0:1]:
                    #print(cat,'article folder',no)
                    filepath = basepath+"/"+cat+"/"+cat+"_50_"+str(no)+"/AA/wiki_00"
                    cat_articles += lp.languageProcess(filepath).getWords()

            #if os.path.exists(filepath):               #Save all base articles in an array of arrays
                self.articles.append(cat_articles)
            print(self.articles)
            self.dictionary = corpora.Dictionary(self.articles)
            self.dictionary.save("dict"+str(noOfTrainArticle)+".dict")
            self.corpus = [self.dictionary.doc2bow(text) for text in self.articles]
            corpora.MmCorpus.serialize("corpus"+str(noOfTrainArticle)+".mm1", self.corpus)
            self.tfidf = models.TfidfModel(self.corpus)
            corpus_tfidf = self.tfidf[self.corpus]
            self.lsi = models.LsiModel(corpus_tfidf, id2word=self.dictionary, num_topics=self.num_topics)
            self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])
            self.index.save("index"+str(noOfTrainArticle)+".index")
        #Compute the tf*idf/lsi/and index
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]
        self.lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=self.num_topics)
    def optimize(self, sim):
        if(sim<0):
            sim*=-1
        return sim
#This function compare a single document with the trained model
    def compare(self, query):
        #Vectorize your query doc with ur dictionary
        self.query_path=self.dictionary.doc2bow(query)
        vec_lsi = self.lsi[self.query_path]

        #Compute similarity of the query document to base articles(model)
        sims = self.index[vec_lsi]
        sims=list(enumerate(sims))
        print(sims)
        return  { self.categories[i]:self.optimize(sims[i][1]) for i in range(self.num_topics)}