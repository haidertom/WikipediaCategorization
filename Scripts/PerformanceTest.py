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
def train_Baseline(mfw,basepath="../RandomBaseline/plaindata"):
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
    LSIs.train(basepath="../RandomBaseline/plaindata")
def check_article(mfw,title, category,validpath = "../TestArticle/plaindata"):
    #get article which should be excluded from testarticles
    with open('../RandomBaseline/zz_index.json') as f:
        data = json.load(f)

    #Get all categories as list
    category = os.listdir(validpath)
    #What is that for?
    if '.DS_Store' in category:
        category.remove('.DS_Store')

    #category = category[0]
    resultsBF={}
    resultsLSI={}
    for cate in category:
        #get exclude file per category
        filepath = validpath+"/"+cate+"/AA/wiki_00"
        article = lp.languageProcess(filepath)
        testarticle =   article.getHighFreqWordsAsDict()
        testarticle2=   article.getWordsAsDict()
        #testarticle2=   article.getWords()
        #Iterate over all testarticle
        testedarticle=0
        for key,val in testarticle.items():
            if key not in data['Category:'+cate.split('_')[0]]:
                testedarticle+=1
                valid_dict = {}
            #check all Bloomfilters
                for cat in BFdict.keys():
                    valid_dict[cat] = 0
                    for word in val.most_common(mfw):
                        if (BFdict[cat].classify(word[0])):
                            valid_dict[cat]+=1
                    valid_dict[cat]=valid_dict[cat]/mfw
                bestFit = max(valid_dict.items(), key=operator.itemgetter(1))[0]
                if bestFit.split('_')[0]==cate.split('_')[0]:
                    #print('bestFit: ',bestFit.split('_')[0],'original',cate.split('_')[0])
                    if cate in resultsBF:
                        resultsBF[cate]+=1
                    else:
                        resultsBF[cate]=1

                lsiRes=LSIs.compare(testarticle2[key])
                bestFit = min(lsiRes.items(), key=operator.itemgetter(1))[0]
                if bestFit.split('_')[0]==cate.split('_')[0]:
                    #print('bestFit: ',bestFit.split('_')[0],'original',cate.split('_')[0])
                    if cate in resultsLSI:
                        resultsLSI[cate]+=1
                    else:
                        resultsLSI[cate]=1
        if cate in resultsBF:
            resultsBF[cate]={'testedarticle':testedarticle,'value':resultsBF[cate]/testedarticle}
        else: resultsBF[cate]={'testedarticle':testedarticle,'value':0}
        if cate in resultsLSI:
            resultsLSI[cate]={'testedarticle':testedarticle,'value':resultsLSI[cate]/testedarticle}
        else: resultsLSI[cate]={'testedarticle':testedarticle,'value':0}
    return {'bloomfilter':resultsBF,'LSI':resultsLSI}
def write2csv(baseline,nestedFile,):
    with open('../TestResults/'+baseline+'.csv','w',newline="") as f:
        writer = csv.writer(f,delimiter = ',')
        # Write CSV Header, If you dont need that, remove this line
        writer.writerow(["Algorithmus",
                "Baseline",
                "Category",
                "testedFiles",
                "correctFiles"])

        for key, value in nestedFile.items():
            for key2,value2 in value.items():
                writer.writerow([str(key),
                    str(baseline),
                    str(key2),
                    str(value2['testedarticle']),
                    str(value2['value']),
                ])

def main():
    mfw=150
    train_Baseline(mfw,"../RandomBaseline/plaindata/")
    title = "Space"
    category = "Category:Universe"
    vali_dict = check_article(mfw,title, category)
    write2csv('RandomBaseline01',vali_dict)


if __name__== "__main__":
  main()
