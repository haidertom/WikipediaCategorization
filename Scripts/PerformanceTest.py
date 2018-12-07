import languageProcess as lp
import BloomFilter
#from baseline import Baseline
import os
import LSIsimilarity
import operator
import json
import csv
import BloomClassify
import pickle

BFdict = {}
LSIs = LSIsimilarity.LSIsimilarity()
CL = BloomClassify.BloomClassify(prct = 40, art = 1000, baselineFolder="../Baseline/1000/plaindata")
def save_Testarticle(name,savedict,cate):
    '''
    saves test preprocessed testfiles
    '''
    name = 'testObjects/'+ name +'_'+cate+'_1000_.pkl'
    with open(name, 'wb') as f:
        pickle.dump(savedict, f, pickle.HIGHEST_PROTOCOL)
    print("saved Traindata")
def load_Testarticle(name,category):
    '''
    load test preprocessed testfiles
    '''
    name = 'testObjects/'+ name +'_'+category+'_1000_.pkl'
    with open(name, 'rb') as f:
        print("loaded Traindata",name)
        return pickle.load(f)
def train_Baseline(basepath="../Baseline/50/plaindata"):
    '''
    This function trains both algorithms with the same baseline
    '''
    #Bloomfilter
    CL.load_BL()
    #LSI
    LSIs.train(basepath=basepath,noOfTrainArticle=50)


def check_article(validpath = "../Baseline/11000/plaindata",savename='Test_X'):
    '''
    This function is comparing testarticles with the given
    validpath = path to testfiles
    '''
    #Get all categories as list
    category = os.listdir(validpath)
    
    if '.DS_Store' in category:
        category.remove('.DS_Store')

    resultsBF={}
    resultsLSI={}
    #iterating over the different categories
    for cate in category:
        print("Testing category: "+cate)
        if os.path.exists('testObjects/TestarticleBloom_'+cate+'_1000_.pkl'):
             testarticle = load_Testarticle('TestarticleBloom',str(cate))
             testarticle2=  load_Testarticle('TestarticleLsi',str(cate))
        else:
            testarticle =   {}
            testarticle2=   {}
            path = validpath+"/"+cate
            dir_no=sum(os.path.isdir(path+"/"+i) for i in os.listdir(path))
            #only take the last 10 folders. Basline is randomized, therefore is will not effect the result 
            for no in range(dir_no)[-19:]:
                filepath = validpath+"/"+cate+"/"+cate+"_11000_"+str(no)+"/AA/wiki_00"
                #print(filepath)
                article = lp.languageProcess(filepath)
                testarticle.update(article.getHighFreqWordsAsDict())
                testarticle2.update(article.getWordsAsDict())
                #articles = lp.languageProcess(filepath).getHighFreqWordsAsDict()
            save_Testarticle('TestarticleBloom',testarticle,cate)
            save_Testarticle('TestarticleLsi',testarticle2,cate)
            #print(testarticle2)
            #print(type(testarticle2['The Haywain Triptych']))
        BFcategoryResults=[]
        LSIcategoryResults=[]
        for key,val in testarticle.items():
            #check similarity to Bloomfilter
            valid_dict = CL.check_article(testarticle[key],50)
            valid_dict['title']=key
            BFcategoryResults.append(valid_dict)
            #check similarity to LSI vectors
            lsiRes=LSIs.compare(testarticle2[key])
            lsiRes['title']=key
            LSIcategoryResults.append(lsiRes)
        resultsBF[cate]=BFcategoryResults.copy()
        resultsLSI[cate]=LSIcategoryResults.copy()
    write2csv(savename,{'bloomfilter':resultsBF,'LSI':resultsLSI})

#This function writes the testresults to a csv file
def write2csv(baseline,nestedFile):
    '''
    Writes test result into csv file
    '''

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
    train_Baseline()
    check_article()

if __name__== "__main__":
  main()
