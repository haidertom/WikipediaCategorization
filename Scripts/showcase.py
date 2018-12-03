import BloomClassify as BC
import LSIsimilarity
from baseline import Baseline
import os
import languageProcess as lp

LSIs = LSIsimilarity.LSIsimilarity()
CL = BC.BloomClassify(num = 20,baselineFolder="../RandomBaseline/plaindata")

def loadModels():
    LSIs.train(basepath="../Baseline/1000/plaindata")

def checkArticle(title):
    title ='Football'
    Base = Baseline(folder="Validation",  baseline_number = 1)

    if not os.path.exists("../Validation"):
        os.mkdir("../Validation")

    filename = "../Validation/"+"raw.txt"
    with open(filename, 'w') as the_file:
        the_file.write(Base.get_dumptext(title)[0])
    os.system("../wikiextractor/WikiExtractor.py "+"../Validation/"+"raw"+" -o"+" ../Validation"+" --json")
    category = os.listdir("../Validation")
    if '.DS_Store' in category:
        category.remove('.DS_Store')
    category = category[0]
    filepath = "../Validation/AA/wiki_00"
    testarticle = lp.languageProcess(filepath)
    return LSIs.compare(testarticle.getWords())
def main():
    loadModels()
    x=0
    while x<3:
        title = input("Ihr Name? ")
        #is title? exception
        print(title)
        checkArticle(title)

    pass

if __name__== "__main__":
  main()

