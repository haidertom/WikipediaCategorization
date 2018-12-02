import languageProcess as lp
import BloomFilter
from baseline import Baseline
import os
import LSIsimilarity
import operator
import json
import csv
import BloomClassify as BC
import pickle
BFdict = {}
LSIs = LSIsimilarity.LSIsimilarity()
CL = BC.BloomClassify(num = 50,baselineFolder="../Baseline/10/plaindata")
def save_Testarticle(name,savedict,cate):
    name = 'trainedObjects/'+ name +'_'+cate+'_500_.pkl'
    with open(name, 'wb') as f:
        pickle.dump(savedict, f, pickle.HIGHEST_PROTOCOL)
    print("saved Traindata")
def load_Testarticle(name,category):
    name = 'trainedObjects/'+ name +'_'+category+'_500_.pkl'
    with open(name, 'rb') as f:
        print("loaded Traindata",name)
        return pickle.load(f)
#This function trains both algorithms with the same baseline
def train_Baseline(basepath="../Baseline/1000/plaindata"):
    #Bloomfilter
    #CL.get_mfw()
    #CL.get_tfidf_1000()
    #CL.train_BL(mfw = 0, tfidf = 1)
    CL.load_BL()
    #LSI
    LSIs.train(basepath="../Baseline/1000/plaindata")
    #Create LSI object
    pass
    #iterate over given Baseline folder -> get category baseline

#This function is comparing testarticles with the given
#validpath = path to testfiles
def check_article(validpath = "../TestArticle500/plaindata"):
    print("checking articles for test")
    #get article which should be excluded from testarticles
    with open('../BigBaseline/zz_index.json') as f:
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
        print("Testing category: "+cate)
        filepath = validpath+"/"+cate+"/AA/wiki_00"
        if os.path.exists('trainedObjects/TestarticleBloom_'+cate+'_500_.pkl'):
            testarticle = load_Testarticle('TestarticleBloom',str(cate))
            testarticle2=  load_Testarticle('TestarticleLsi',str(cate))
        else:
            testarticle =   {}#article.getHighFreqWordsAsDict()
            testarticle2=   {}#article.getWordsAsDict()
            path = validpath+"/"+cate
            dir_no=sum(os.path.isdir(path+"/"+i) for i in os.listdir(path))

            for no in range(dir_no):
                filepath = validpath+"/"+cate+"/"+cate+"_500_"+str(no)+"/AA/wiki_00"
                print(filepath)
                article = lp.languageProcess(filepath)
                testarticle.update(article.getHighFreqWordsAsDict())
                testarticle2.update(article.getWordsAsDict())
                #articles = lp.languageProcess(filepath).getHighFreqWordsAsDict()
            save_Testarticle('TestarticleBloom',testarticle,cate)
            save_Testarticle('TestarticleLsi',testarticle2,cate)

        testedarticle=0
        BFcategoryResults=[]
        LSIcategoryResults=[]
        checkedarticles=0
        for key,val in testarticle.items():
            #get exclude file per category
            if key not in data['Category:'+cate.split('_')[0]]:
                testedarticle+=1
                #Create result dictionary for all categories
                #valid_dict = {}
            #check all Bloomfilters ( different Bloomfilter are stored in BFdict)

                #for cat in BFdict.keys():
                #    valid_dict[cat] = 0
                #    for word in val.most_common(mfw):
                #        if (BFdict[cat].classify(word[0])):
                #            valid_dict[cat]+=1
                #    valid_dict[cat]=valid_dict[cat]/mfw
                valid_dict = CL.check_article(testarticle[key],50)
                valid_dict['title']=key
                BFcategoryResults.append(valid_dict)

                lsiRes=LSIs.compare(testarticle2[key])
                lsiRes['title']=key
                LSIcategoryResults.append(lsiRes)
        resultsBF[cate]=BFcategoryResults.copy()
        resultsLSI[cate]=LSIcategoryResults.copy()
        #print([key for key,value in resultsBF.items()])
    write2csv('BigBaseline02',{'bloomfilter':resultsBF,'LSI':resultsLSI})
    #return {'bloomfilter':resultsBF,'LSI':resultsLSI}

#This function writes the testresults to a csv file
def write2csv(baseline,nestedFile):


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
                    #print(line)
                    writer.writerow(line)
#main function to compute the tests for a specific Baseline
def main():
    train_Baseline(basepath="../BigBaseline/plaindata/")
    check_article()
    #write2csv('RandomBaseline04',vali_dict)
    #print(vali_dict['bloomfilter'])
    #print(vali_dict['LSI'])

if __name__== "__main__":
  main()
