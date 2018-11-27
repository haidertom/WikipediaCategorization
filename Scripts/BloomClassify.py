import languageProcess as lp
import BloomFilter
from tfidf import TfIdf

from baseline import Baseline

import os

class BloomClassify:
	def __init__(self, num = 50):

		self.num = num 	#number of most frequent words

		self.art = 20 # number of articles

		self.total = self.num * self.art

		self.basepath = "../Baseline/plaindata"

		self.BFdict = {}

		self.MFWdict = {}

		self.AWdict = {}

		self.TFIDFdict = {}


	def get_mfw(self):
		'''
		iterate over given Baseline folder and get most frequent words for every article in every category
		'''

		categories = os.listdir(self.basepath)
		if '.DS_Store' in categories:
			categories.remove('.DS_Store')

		for cat in categories:

			filepath = self.basepath+"/"+cat+"/AA/wiki_00"

			articles = lp.languageProcess(filepath).getHighFreqWords()

			self.MFWdict[cat] = []

			for art in articles:
				for word in art.most_common(self.num):
					self.MFWdict[cat].append(word[0])

		return

	def get_tfidf(self):
		'''
		Calculates the tfidf for all words and sorts them in a list
		'''

		categories = os.listdir(self.basepath)
		if '.DS_Store' in categories:
			categories.remove('.DS_Store')

		for cat in categories:

			filepath = self.basepath+"/"+cat+"/AA/wiki_00"

			articles = lp.languageProcess(filepath).getHighFreqWords()

			self.AWdict[cat] = []

			for art in articles:
				for word in art.most_common(self.num*4):
					self.AWdict[cat].append(word[0])


		TFIDF = TfIdf()

		# number of categories - should be 27
		total_num_of_doc = len(self.AWdict.keys())

		for cat in self.AWdict.keys():

			self.TFIDFdict[cat] = {}

			#length of the document
			total_length =  len(self.AWdict[cat])

			for word in self.AWdict[cat]:

				# number of times the word occured in the document
				no_of_occurences = self.AWdict[cat].count(word)

				# number of documents the word occured in
				no_of_doc_it_appeard_in = sum(1 for c in self.AWdict.keys() if word in self.AWdict[c])

				tf = TFIDF.tf(no_of_occurences,total_length)
				idf = TFIDF.idf(total_num_of_doc,no_of_doc_it_appeard_in)
				tfidf = tf * idf

				self.TFIDFdict[cat][word] = tfidf

			# transfer to sorted list
			self.TFIDFdict[cat] = sorted(self.TFIDFdict[cat], key=self.TFIDFdict[cat].__getitem__, reverse=True)[:self.total]

		pass

	def train_BL(self, mfw = 1, tfidf = 0):
		'''
		Takes a dictionary, creates a Bloomfilter for every key and trains this BL for all values in this key
		'''

		# train with MFW
		if mfw:
			TrainDict = self.MFWdict

		# train with tfidf
		if tfidf:
			TrainDict = self.TFIDFdict

		for cat in TrainDict.keys():

			self.BFdict[cat] = BloomFilter.BloomFilter()

			for word in TrainDict[cat]:
				self.BFdict[cat].train(word)
		pass

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

			for word in testarticle[0].most_common(self.num):
			 	if (self.BFdict[cat].classify(word[0])):
						vali_dict[cat]+=1

		return vali_dict



def main():

	CL = BloomClassify(num = 50)

	CL.get_mfw()
	CL.get_tfidf()

	title = "Amateur sports"
	category = "Category:Universe"


	CL.train_BL(mfw = 1, tfidf = 0)
	vali_dict = CL.check_article(title, category)

	for key,value in vali_dict.items():
		print("%-30s%-30f"%(key, value/CL.num))

	CL.train_BL(mfw = 0, tfidf = 1)

	vali_dict = CL.check_article(title, category)

	for key,value in vali_dict.items():
		print("%-30s%-30f"%(key, value/CL.num))





if __name__== "__main__":
  main()
