import languageProcess as lp
import BloomFilter

from baseline import Baseline

import os

class Classify:
	def __init__(self, mfw = 150):

		self.BFdict = {}

		self.mfw = mfw

		pass

	def train_Baseline(self):

		#iterate over given Baseline folder -> get category baseline

		self.basepath = "../Baseline/plaindata"

		categories = os.listdir(self.basepath)
		if '.DS_Store' in categories:
			categories.remove('.DS_Store')

		for cat in categories:

			filepath = "../Baseline/plaindata/"+cat+"/AA/wiki_00"

			articles = lp.languageProcess(filepath).getHighFreqWords()

			self.BFdict[cat] = BloomFilter.BloomFilter()

			for art in articles:
				for word in art.most_common(self.mfw):
					self.BFdict[cat].train(word[0])


	def check_article(self, title, category):

		Base = Baseline(folder="Validation")

		Base.write_rawdata(title, category)
		Base.convert_plain()

		self.valipath = "../Validation/plaindata"

		category = os.listdir(self.valipath)
		if '.DS_Store' in category:
			category.remove('.DS_Store')

		category = category[0]

		filepath = "../Validation/plaindata/"+category+"/AA/wiki_00"

		testarticle = lp.languageProcess(filepath).getHighFreqWords()

		vali_dict = {}

		#check all Bloomfilters
		for cat in self.BFdict.keys():

			vali_dict[cat] = 0

			for word in testarticle[0].most_common(self.mfw):
			 	if (self.BFdict[cat].classify(word[0])):
						vali_dict[cat]+=1

		return vali_dict



def main():

	CL = Classify(mfw = 150)


	CL.train_Baseline()

	title = "Space"
	category = "Category:Universe"
	vali_dict = CL.check_article(title, category)

	for key,value in vali_dict.items():
		print("%-30s%-30f"%(key, value/CL.mfw))


if __name__== "__main__":
  main()
