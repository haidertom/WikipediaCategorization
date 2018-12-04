import languageProcess as lp
import BloomFilter
#from baseline import Baseline
import os
import LSIsimilarity
import operator
import json
import csv
import BloomClassify as BC
import pickle

BFdict = {}
LSIs = LSIsimilarity.LSIsimilarity()
#CL = BC.BloomClassify(num = 50,baselineFolder="../Baseline/10/plaindata")
def save_Testarticle(name,savedict,cate):
    name = 'trainedObjects/'+ name +'_'+cate+'_1000_.pkl'
    with open(name, 'wb') as f:
        pickle.dump(savedict, f, pickle.HIGHEST_PROTOCOL)
    print("saved Traindata")
def load_Testarticle(name,category):
    name = 'trainedObjects/'+ name +'_'+category+'_1000_.pkl'
    with open(name, 'rb') as f:
        print("loaded Traindata",name)
        return pickle.load(f)
#This function trains both algorithms with the same baseline
def train_Baseline(basepath="../TestArticle/plaindata"):
    #Bloomfilter
    #CL.get_mfw()
    #CL.get_tfidf_1000()
    #CL.train_BL(mfw = 0, tfidf = 1)
    #CL.load_BL()
    #LSI
    LSIs.train(basepath="../Baseline/11000/plaindata",noOfTrainArticle=5000)
    #Create LSI object
    
    #iterate over given Baseline folder -> get category baseline

#This function is comparing testarticles with the given
#validpath = path to testfiles
def check_article(validpath = "../Baseline/11000/plaindata"):
    #print("checking articles for test")
    #get article which should be excluded from testarticles
    #with open('../BigBaseline/zz_index.json') as f:
        #data = json.load(f)

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
        #filepath = validpath+"/"+cate+"/AA/wiki_00"
        #article = lp.languageProcess(filepath)
        if os.path.exists('trainedObjects/TestarticleBloom_'+cate+'_1000_.pkl'):
             testarticle = load_Testarticle('TestarticleBloom',str(cate))
             testarticle2=  load_Testarticle('TestarticleLsi',str(cate))
        else:
            testarticle =   {}#article.getHighFreqWordsAsDict()
            testarticle2=   {}#article.getWordsAsDict()
            path = validpath+"/"+cate
            dir_no=sum(os.path.isdir(path+"/"+i) for i in os.listdir(path))
            #only take the last 10 folders. Basline is randomized, therefore is will not effect the result 
            for no in range(dir_no)[-19:]:
                filepath = validpath+"/"+cate+"/"+cate+"_11000_"+str(no)+"/AA/wiki_00"
                print(filepath)
                article = lp.languageProcess(filepath)
                testarticle.update(article.getHighFreqWordsAsDict())
                testarticle2.update(article.getWordsAsDict())
                #articles = lp.languageProcess(filepath).getHighFreqWordsAsDict()
            save_Testarticle('TestarticleBloom',testarticle,cate)
            save_Testarticle('TestarticleLsi',testarticle2,cate)
            #print(testarticle2)
            #print(type(testarticle2['The Haywain Triptych']))
        testedarticle=0
        BFcategoryResults=[]
        LSIcategoryResults=[]
        for key,val in testarticle.items():
            #get exclude file per category
            #if key not in data['Category:'+cate.split('_')[0]]:
            #    testedarticle+=1
                #Create result dictionary for all categories
            #check all Bloomfilters ( different Bloomfilter are stored in BFdict)
                #valid_dict = CL.check_article(testarticle[key],50)
                #valid_dict['title']=key
                #BFcategoryResults.append(valid_dict)
            test=testarticle2[key]
            print(type(test))
            lsiRes=LSIs.compare(test)
            lsiRes['title']=key
            LSIcategoryResults.append(lsiRes)
        resultsBF[cate]=BFcategoryResults.copy()
        resultsLSI[cate]=LSIcategoryResults.copy()
        #print([key for key,value in resultsBF.items()])
    write2csv('Test_Baseline_10000_1000',{'bloomfilter':resultsBF,'LSI':resultsLSI})
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
