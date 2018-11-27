import languageProcess as lp
import BloomFilter
from baseline import Baseline
import os
import LSIsimilarity
import operator
import json
import csv

BFdict = {}
LSIs = LSIsimilarity.LSIsimilarity()

#This function trains both algorithms with the same baseline
def train_Baseline(mfw,basepath="../Baseline/plaindata"):
#Bloomfilter
    #iterate over given Baseline folder -> get category baseline
    categories = os.listdir(basepath)
    
    if '.DS_Store' in categories:
        categories.remove('.DS_Store')

    for cat in categories:
        #Create Bloomfilter object for every category
        BFdict[cat] = BloomFilter.BloomFilter()
        #Create path for specific category
        filepath = basepath+cat+"/AA/wiki_00"
        #get high frequent word of articles
        articles = lp.languageProcess(filepath).getHighFreqWords()
        #train Bloom filter of specific category
        for art in articles:
            for word in art.most_common(mfw):
                BFdict[cat].train(word[0])
#LSI
    #Create LSI object
    LSIs.train(basepath="../Baseline/plaindata")
def check_article(mfw,validpath = "../TestArticle/plaindata"):
    #get article which should be excluded from testarticles
    with open('../Baseline/zz_index.json') as f:
        data = json.load(f)

    #Get all categories as list
    category = os.listdir(validpath)
    #What is that for?
    if '.DS_Store' in category:
        category.remove('.DS_Store')

    #results {key=category,value=list of dicts (results of the two differnt tests)}
    resultsBF={}
    resultsLSI={}
    #iterating over the different categories
    for cate in category:
        filepath = validpath+"/"+cate+"/AA/wiki_00"
        article = lp.languageProcess(filepath)
        testarticle =   article.getHighFreqWordsAsDict()
        testarticle2=   article.getWordsAsDict()
        testedarticle=0
        BFcategoryResults=[]
        LSIcategoryResults=[]
        for key,val in testarticle.items():
            #get exclude file per category
            if key not in data['Category:'+cate.split('_')[0]]:
                testedarticle+=1
                #Create result dictionary for all categories
                valid_dict = {}
            #check all Bloomfilters ( different Bloomfilter are stored in BFdict)
                for cat in BFdict.keys():
                    valid_dict[cat] = 0
                    for word in val.most_common(mfw):
                        if (BFdict[cat].classify(word[0])):
                            valid_dict[cat]+=1
                    valid_dict[cat]=valid_dict[cat]/mfw
                valid_dict['title']=key
                BFcategoryResults.append(valid_dict)

                lsiRes=LSIs.compare(testarticle2[key])
                lsiRes['title']=key
                LSIcategoryResults.append(lsiRes)
                #print(LSIcategoryResults)
        resultsBF[cate]=BFcategoryResults.copy()
        resultsLSI[cate]=LSIcategoryResults.copy()
        #print([key for key,value in resultsBF.items()])
    write2csv('Baseline01',{'bloomfilter':resultsBF,'LSI':resultsLSI})
    #return {'bloomfilter':resultsBF,'LSI':resultsLSI}


def write2csv(baseline,nestedFile):
    
    print(type(nestedFile))
    print(type(nestedFile['bloomfilter']))
    print(type(nestedFile['LSI']))

    with open('../TestResults/'+baseline+'.csv','w',newline="") as f:
        writer = csv.writer(f,delimiter = ',')
        # Write CSV Header, If you dont need that, remove this line
        header=["Algorithm",
                "Baseline",
                "originalTitle",
                "originalCategory"]
        header.extend([key for key,value in nestedFile['LSI'].items()])
        writer.writerow(header)
        #decide between bloomfilter or LSI
        for key, value in nestedFile.items():
            #iterating over all tested categories
            for key2,value2 in value.items():
                for res in value2:
                    line=[str(key),
                        str(baseline),
                        str(res['title']),
                        str(key2),
                    ]
                    line.extend([val3 for key3, val3 in res.items() if key3 != 'title'])
                    print(line)
                    writer.writerow(line)

def main():
    mfw=50
    train_Baseline(mfw,"../Baseline/plaindata/")
    check_article(mfw)
    #write2csv('RandomBaseline04',vali_dict)
    #print(vali_dict['bloomfilter'])
    #print(vali_dict['LSI'])

if __name__== "__main__":
  main()
