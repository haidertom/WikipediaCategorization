import languageProcess as lp
import BloomFilter
from tfidf import TfIdf
import csv
import pickle

from baseline import Baseline

import os

class BloomClassify:
	def __init__(self, prct = 50, art = 50, baselineFolder="../Baseline/1000/plaindata"):

		#Inital values
		self.num = 50 	#number of most frequent words
		self.art = art #number of articles
		self.prct = prct #percentage of highest tfidf values used for training
		self.min = 2**64

		#Folder structure
		self.basepath = baselineFolder

		#dictionaries
		self.BFdict = {}
		self.MFWdict = {}
		self.AWdict = {}
		self.TFIDFdict = {}


	def get_mfw(self):
		'''
		iterate over given Baseline folder and get most frequent words for every article in every category, saved to TFIDFdict
		'''

		categories = os.listdir(self.basepath)
		if '.DS_Store' in categories:
			categories.remove('.DS_Store')

		for cat in categories:
			self.MFWdict[cat] = []

			for subfolder in os.listdir(self.basepath+"/"+cat):

				filepath = self.basepath+"/"+cat+"/"+subfolder+"/AA/wiki_00"

				print(filepath)

				articles = lp.languageProcess(filepath).getHighFreqWords()

				for art in articles:
					for word in art.most_common():
						self.MFWdict[cat].append(word[0])

			print("fetched {} most common words for {}".format(len(self.MFWdict[cat]), cat))

		return

	def get_tfidf(self):
		'''
		Iterate over given Baseline folder, Calculates the tfidf for all words and sorts them in the dictionary 'TFIDFdict'
		'''
		categories = os.listdir(self.basepath)
		if '.DS_Store' in categories:
			categories.remove('.DS_Store')

		for cat in categories:
			self.AWdict[cat] = []

			for subfolder in os.listdir(self.basepath+"/"+cat):

				filepath = self.basepath+"/"+cat+"/"+subfolder+"/AA/wiki_00"

				#get frquency distribution of words in articles
				articles = lp.languageProcess(filepath).getHighFreqWords()

				for art in articles:
					for word in art.most_common(self.num):
						self.AWdict[cat].append(word[0])

				print("fetched {} most common words for {}".format(len(self.AWdict[cat]), cat))

			# get the lenth of the smallest bag of words
			self.min = min(self.min, len(set(self.AWdict[cat])))
			print(len(self.AWdict[cat]))
			print(self.min)

		# truncate list to most important tfidf values
		trunc = int(self.min*(self.prct/100))

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

				#Calculations
				tf = TFIDF.tf(no_of_occurences,total_length)
				idf = TFIDF.idf(total_num_of_doc,no_of_doc_it_appeard_in)
				tfidf = tf * idf

				self.TFIDFdict[cat][word] = tfidf

			# transfer to sorted list
			self.TFIDFdict[cat] = sorted(self.TFIDFdict[cat], key=self.TFIDFdict[cat].__getitem__, reverse=True)[:trunc]
			print("added {} words to {}".format(len(self.TFIDFdict[cat]), cat))
		pass

	def train_BL(self, mfw = 0, tfidf = 1):
		'''
		Takes a dictionary, creates a Bloomfilter for every key and trains this BF for all values for this key
		'''
		# train with MFW
		if mfw:
			TrainDict = self.MFWdict

		# train with tfidf
		if tfidf:
			TrainDict = self.TFIDFdict

		for cat in TrainDict.keys():
			print("Training Category: {} with {} words".format(cat, len(TrainDict[cat])))
			self.BFdict[cat] = BloomFilter.BloomFilter(len(TrainDict[cat]))

			for word in TrainDict[cat]:
				self.BFdict[cat].train(word)
		pass

	def save_BL(self):
		'''
		Saves a trained BloomFilter as binary file
		'''
		name = 'trainedObjects/'+ 'BFdict' +'_'+ str(self.art)+'_'+str(self.prct)+'p'+'.pkl'
		with open(name, 'wb') as f:
			pickle.dump(self.BFdict, f, pickle.HIGHEST_PROTOCOL)
		print("saved Traindata")

	def load_BL(self):
		'''
		Loads a trained BloomFilter as binary file
		'''
		name = 'trainedObjects/'+ 'BFdict' +'_'+ str(self.art)+'_'+str(self.prct)+'p'+'.pkl'
		with open(name, 'rb') as f:
			self.BFdict = pickle.load(f)
		print("loaded Traindata")

	def check_article(self, article,numOfCheckWords):
		'''
		Check the Category of a given article
		'''
		vali_dict = {}

		#check all Bloomfilters
		for cat in self.BFdict.keys():

			vali_dict[cat] = 0

			for word in article.most_common(numOfCheckWords):
			 	if (self.BFdict[cat].classify(word[0])):
						vali_dict[cat]+=1
			vali_dict[cat]=vali_dict[cat]/numOfCheckWords
		return vali_dict

	def check_single_article(self, title, baseline_number = 20, category="Category:Unkown", numOfCheckWords = 20):
		'''
		Check the Category of a single article, the article is downladed via the wikipedia api on demand
		'''
		# check if Validationfolder exists
		if not os.path.exists("../Validation"): os.mkdir("../Validation")

		# get article from wikipedia API
		Base = Baseline(folder="Validation",  baseline_number = baseline_number)
		filename = "../Validation/"+title.replace(' ','')+"_raw.txt"
		with open(filename, 'w') as the_file:
			the_file.write(Base.get_dumptext([title]))

		#convert to plain text
		os.system("../wikiextractor/WikiExtractor.py "+"../Validation/"+title.replace(' ','')+"_raw.txt"+" -o"+" ../Validation/"+title.replace(' ','')+"/ --json")

		#housekeeping
		category = os.listdir("../Validation")
		if '.DS_Store' in category: category.remove('.DS_Store')

		#languageProcess
		filepath = "../Validation/"+title.replace(' ','')+"/AA/wiki_00"
		testarticle = lp.languageProcess(filepath).getHighFreqWords()

		#Check if article with that name exists
		assert (len(bfarticle)>= 1),"No article with that name"

		vali_dict = {}

		#check all Bloomfilters
		for cat in self.BFdict.keys():
			vali_dict[cat] = sum([1 for word in testarticle[0].most_common(numOfCheckWords) if self.BFdict[cat].classify(word[0])])/numOfCheckWords

		return vali_dict

	def similarity_matrix(self, mfw = 0, tfidf = 1):
		'''
		Creates a similarity matrix for a trained model
		'''
		# trained with MFW
		if mfw:
			TrainDict = self.MFWdict

		# trained with tfidf
		if tfidf:
			TrainDict = self.TFIDFdict

		file = "../TestResults"+"/BF_similarity_matrix"+str(self.art)+"_"+str(self.prct)+".csv"

		with open(file, 'w') as the_file:

			writer = csv.writer(the_file,delimiter = ',')

			description = ["percentage of tfidf values:", self.prct, "number of articles per category:", self.art]
			writer.writerow(description)

			header = [" "]
			header.extend(TrainDict.keys())
			writer.writerow(header)

			for c in TrainDict.keys():

				counter =  []
				for cat in TrainDict.keys():
					counter.append(len([1 for word in TrainDict[cat] if self.BFdict[c].classify(word)])/len(TrainDict[cat]))

				row = [c]
				row.extend(counter)
				writer.writerow(row)
		pass

def main():

	CL = BloomClassify(prct = 40, art = 1000)

	#CL.get_tfidf()
	#CL.train_BL(mfw = 0, tfidf = 1)
	#CL.save_BL()

	CL.load_BL()
	#CL.similarity_matrix(mfw = 0, tfidf = 1)

	title = "Football"
	print(title)

	vali_dict = CL.check_single_article(title=title, numOfCheckWords = 50)

	for key,value in vali_dict.items():
	 	print("%-30s%-30f"%(key, value))

if __name__== "__main__":
	main()
