import requests
import os
import random


class Baseline:

	def __init__(self, origin_category = "Category:Main topic classifications", baseline_number = 20, folder = "Baseline"):

		#dynamic values
		self.origin_category = origin_category
		self.baseline_number = baseline_number

		#static values
		self.URL = "https://en.wikipedia.org/w/api.php"
		self.index = {}

		#Data structure
		self.basepath = "../"+ folder
		self.datapath = self.basepath +"/"+str(baseline_number)
		self.rawpath = self.datapath + "/rawdata"
		self.plainpath = self.datapath + "/plaindata"

	def get_titles(self, category):
		'''
		yields all article titles inside that category
		'''
		PARAMS = {
			'action': "query",
			'list': "categorymembers",
			'cmtitle': category,
			'cmlimit': 200, # limits results to a maximum number
			'cmnamespace':0, 	#-> plain articles belonging to that category
			'format': "json"
		}
		S = requests.Session()
		R = S.get(url=self.URL, params=PARAMS)
		DATA = R.json()

		titles = []

		for article in DATA['query']['categorymembers']:
			titles.append(article['title'])

		return titles

	def get_subcategories(self, category):
		'''
		yields all subcategories inside that category
		'''
		PARAMS = {
			'action': "query",
			'list': "categorymembers",
			'cmtitle': category,
			'cmlimit': 200,
			'cmnamespace':14, #--> subcategories
			'format': "json"
		}
		S = requests.Session()
		R = S.get(url=self.URL, params=PARAMS)
		DATA = R.json()

		subcategories = []

		for article in DATA['query']['categorymembers']:
		 	subcategories.append(article['title'])

		return subcategories

	def get_dumptext(self, titles):
		'''
		gets text from article in titles, all titles in the same category
		'''
		DATA = []
		titles = [titles[x:x+50] for x in range(0, len(titles), 50)]

		for t in titles:
			PARAMS = {
				'action': 'query',
				'prop':'revisions',
				'rvprop':'content',
				'titles': "|".join(t),
				'export':1,
				'exportnowrap':1,
				'format': "json"
				}
			S = requests.Session()
			R = S.get(url=self.URL, params=PARAMS)
			DATA.append(R.text)

		return DATA

	def write_rawdata(self, titles, category):
		'''
		writes all articles titles in a category into a single xml file
		'''
		category = category.split(":")[1]

		#check if Directory exists
		if not os.path.exists(self.basepath):
			os.mkdir(self.basepath)

		if not os.path.exists(self.datapath):
			os.mkdir(self.datapath)

		if not os.path.exists(self.rawpath):
			os.mkdir(self.rawpath)

		#wirte text to the file(s)
		print("writing files...")
		for i, data in enumerate(self.get_dumptext(titles)):

			filename = self.rawpath+"/"+category+"_"+str(self.baseline_number)+"_"+str(i)+".xml"
			with open(filename, 'w') as the_file:
				the_file.write(data)

	def write_index(self, index):
		'''
		index all articles titles in a category that were added to the baseline
		'''

		if not os.path.exists(self.datapath):
			os.mkdir(self.datapath)

		filename = self.datapath+"/zz_index.json"
		with open(filename, 'w') as the_file:
			the_file.write(str(index))

	def get_rawdata(self):
		'''
		writes n = baseline_number of random articles in all subcategories from an origincategory into a single xml file
		'''

		#get main categories
		main_categories = self.get_subcategories(self.origin_category)

		# loop over all main categories
		for cat in main_categories[1:]:
			print("looking for titles in category: {} ".format(cat))

			self.index[cat] = []

			for title in self.get_titles(cat):
				if not any(title in e for e in self.index.values()): #check for duplicates
					self.index[cat].append(title)

			#get subcategories of a main category
			subcategories = self.get_subcategories(cat)

			# loop over subcategories of a main category
			for subcat in subcategories:

				for title2 in self.get_titles(subcat):
					if not any(title2 in e for e in self.index.values()): #check for duplicates
						self.index[cat].append(title2)


				# loop further to get more articles
				subsubcategories = self.get_subcategories(subcat)

				for subsubcat in subsubcategories:

					for title3 in self.get_titles(subsubcat):
						if not any(title3 in e for e in self.index.values()): #check for duplicates
							self.index[cat].append(title3)

					if len(self.index[cat])<self.baseline_number:
						# loop further to get more articles
						subsubsubcategories = self.get_subcategories(subsubcat)

						for subsubsubcat in subsubsubcategories:

							for title4 in self.get_titles(subsubsubcat):
								if not any(title4 in e for e in self.index.values()): #check for duplicates
									self.index[cat].append(title4)


			#pick random articles
			print("found {} titles in category: {} ".format(len(self.index[cat]), cat))

			self.index[cat] = [self.index[cat][i] for i in random.sample(range(0, len(self.index[cat])-1), self.baseline_number)]

			print(len(self.index[cat]))

			print("added {} unique titles to category: {} ".format(len(set(self.index[cat])), cat))
			#write articles in file
			self.write_rawdata((self.index[cat]) , cat)

		#indexing all categories and titles for later use
		self.write_index(self.index)

	def convert_plain(self):
		'''
		Use WikiExtractor to get clear Text
		'''

		for file in os.listdir(self.rawpath):
			cat = file.split("_")[0]

			print("read document " + file)
			os.system("../wikiextractor/WikiExtractor.py "+self.rawpath+"/"+file+" -o "+self.plainpath+"/"+cat+"/"+file.split(".")[0]+" --json")

def main():

	# root category your are looking for - default:"Category:Main topic classifications"
	origin_category = "Category:Main topic classifications"

	# number of articles you want from each category
	baseline_number = 5000

	folder = "Baseline"

	BL = Baseline(origin_category, baseline_number, folder)

	BL.get_rawdata()
	BL.convert_plain()


if __name__== "__main__":
  main()
