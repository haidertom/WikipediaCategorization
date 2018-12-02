import os
import numpy as np
import languageProcess as lp
from gensim import corpora,similarities
from gensim.models import LsiModel

path = '../Baseline/plaindata'
polar_wiki="Over the past several decades, Earth’s polar ice caps have gained significant attention because of the alarming decrease in land and sea ice. NASA reports"
education = "Effective education is a learning experience.Education brings about an inherent and permanent change in a person's thinking and capacity to do things.Many people have a superficial concept of education; equating it with doing a particular course or obtaining a particular qualification.Qualifications and courses however do not always equate with effective education.People can undertake courses without any significant permanent change People can achieve qualifications without changing How Good is a Qualification? There's no escaping the fact that good learning takes time.Reading a book and understanding what you read, does not mean that you have been educated or permanently changedif you don't integrate what you read into your attitudes and memory. Similarly, attending a course and hearing a lecture doesn't mean you have changed or been educated.Real education is very different to just having access to (or being exposed to) information about something. Real education embeds things into one's brain, and anyone who understands learning will understand that this comes from repeated exposure and use of information or skills.Sadly, in today's world, people want to fast track everything: but learning is something that cannot usually be fast tracked.Shorter courses simply mean that less is learnt."

categories =os.listdir(path)
#print(categories)
articles =[]
num_topics=27
for cat in categories:
    filepath = path+"/"+cat+"/AA/wiki_00"
    articles += [lp.languageProcess(filepath).getWords()]
    #print("Articles -->" , articles)

print(len(articles))
'''try:
    dictionary = corpora.Dictionary.load('dicname.dict')
    corpus = corpora.MmCorpus('corpusname.mm')
    index = similarities.MatrixSimilarity.load('indexname.index')
except FileNotFoundError:
    dictionary = corpora.Dictionary(articles)
    dictionary.save('dicname.dict')
    corpus = [dictionary.doc2bow(text) for text in articles]
    corpora.MmCorpus.serialize('corpusname.mm',corpus)
    lsimodel=LsiModel(corpus=corpus, id2word=dictionary,num_topics=num_topics)
    index = similarities.MatrixSimilarity(lsimodel[corpus]) # transform corpus to LSI space and index it
    index.save('indexname.index')'''

dictionary = corpora.Dictionary(articles)
#dictionary.save('dicname.dict')
corpus = [dictionary.doc2bow(text) for text in articles]
#corpora.MmCorpus.serialize('corpusname.mm',corpus)
lsimodel=LsiModel(corpus=corpus, id2word=dictionary,num_topics=num_topics)
index = similarities.MatrixSimilarity(lsimodel[corpus]) # transform corpus to LSI space and index it
#index.save('indexname.index')
lsimodel=LsiModel(corpus=corpus,num_topics=27, id2word=dictionary)

vec_bow = dictionary.doc2bow(education.lower().split())
vec_lsi = lsimodel[vec_bow]
#print(sorted(vec_lsi[1]))
sims = sorted(enumerate(index[vec_lsi]), key=lambda item: -item[1])
#print(categories)
print(sims)
#for i in range(0,len(sims)):
  #print("similarity of ",categories[i], " to the given article is -->", sims[i][1])
