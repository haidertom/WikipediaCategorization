import nltk
import json
from pprint import pprint
from nltk.corpus import stopwords
import os
from pprint import pprint
from gensim import corpora,similarities
from gensim.models import LsiModel
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
# This article about polar Ice is added as addition document so that we will be able to compare whether the rest 4 articles(from Space) are more similar to the base article or to this article. 
polar_wiki="Over the past several decades, Earth’s polar ice caps have gained significant attention because of the alarming decrease in land and sea ice. NASA reports that since the late 1970s, the Arctic has lost an average of 20,800 square miles (53,900 square kilometers) of ice per year while the Antarctic has gained an average of 7,300 square miles (18,900 km2) of ice per year. On September 19, 2014, for the first time since 1979, Antarctic sea ice extent exceeded 7.72 million square miles (20 million square kilometers), according to the National Snow and Ice Data Center. The ice extent stayed above this benchmark extent for several days. The average maximum extent between 1981 and 2010 was 7.23 million square miles (18.72 million square kilometers). The single-day maximum extent in 2014 was reached on Sept. 20, according to NSIDC data, when the sea ice covered 7.78 million square miles (20.14 million square kilometers). The 2014 five-day average maximum was reached on Sept. 22, when sea ice covered 7.76 million square miles (20.11 million square kilometers), according to NSIDC.[5]"
print(polar_wiki)

direc = '/home/kdane/Desktop/Computationaltools/WikipediaCategorization.git/DataSnippets/Baseline/Space/wiki/AA'
data=[]
articles7=[]
path = os.path.join(direc,'wiki_00')
#print(path)
sep =','
for line in open(path,'r'):
  data.append(json.loads(line))
for i in range(0,len(data)-4):
  articles7.append(data[i]['text'])
#This will be joining as a single article.
Baseart=sep.join(articles7)
stop_words = set(stopwords.words('english'))
is_noun = lambda pos: pos[:2] == 'NN'
htmlTags = ['ref','www','http','https']
def CleanString(wikiText):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')  
    wikiTokens=tokenizer.tokenize(wikiText)
    #exclude Stopwords
    tokens = [w for w in wikiTokens if w.lower() not in stop_words]
    #exclude numbers
    tokens = [w for w in tokens if not w.isdigit()]
    #extract nouns
    tokens = [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)] 
    #filter for html tags
    tokens = [w for w in tokens if w.lower() not in htmlTags] 
    #set everything to lower case
    tokens = [w.lower() for w in tokens]
    return tokens

#The base article tockens made from (8 articles from Space and the polar ice)
Basearttokens=[CleanString(Baseart),CleanString(polar_wiki)]
#The 8th article of Space cathegory
article8=data[7]['text']
#The 10th article of Space cathegory 
article10=data[9]['text']
#Adictionary from Basearttokens(Plar ice and Space base cathegory) 
dictionary = corpora.Dictionary(Basearttokens)
#corpus from Basearttokens
corpus = [dictionary.doc2bow(text) for text in Basearttokens]
#LSI model from the Dictionary and the corpus
lsimodel=LsiModel(corpus=corpus,num_topics=10, id2word=dictionary)
#Index from the model
index = similarities.MatrixSimilarity(lsimodel[corpus]) # transform corpus to LSI space and index it
#use the dictionary to create a vector of article10 (which is from space)
vec_bow = dictionary.doc2bow(article10.lower().split())
#Feed the vector to the model
vec_lsi = lsimodel[vec_bow]

#This is an array used to provide labels, just for a better readability. 
labels = ["Basearticle", "Polararticle"]
#Compute the similarity and out put a sorted reasult according to the similarity
sim = sorted(enumerate(index[vec_lsi]), key=lambda item: -item[1])
for i in range(0,len(sim)):
  print("similarity of Article10(Space BaseCathegory) to ",labels[i], " is -->", sim[i][1])
