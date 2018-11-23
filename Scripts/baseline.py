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
		self.datapath = "../"+ folder
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

		PARAMS = {
			'action': 'query',
			'prop':'revisions',
			'rvprop':'content',
			'titles': titles,
			'export':1,
			'exportnowrap':1,
			'format': "json"
		}
		S = requests.Session()
		R = S.get(url=self.URL, params=PARAMS)
		DATA = R.text

		return DATA

	def write_rawdata(self, titles, category):
		'''
		writes all articles titles in a category into a single xml file
		'''
		category = category.split(":")[1]

		#check if Directory exists
		if not os.path.exists(self.datapath):
			os.mkdir(self.datapath)

		if not os.path.exists(self.rawpath):
			os.mkdir(self.rawpath)

		#wirte text to the file
		filename = self.rawpath+"/"+category+"_"+str(self.baseline_number)+".xml"
		with open(filename, 'w') as the_file:
			the_file.write(self.get_dumptext(titles))

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
		for cat in main_categories:

			self.index[cat] = []

			for title in self.get_titles(cat):
				if title not in self.index.values(): # check for duplicates
					self.index[cat].append(title)

					#used of tree search
					#if len(self.index[cat]) > self.baseline_number:
					#	break

			#used for tree search
			#if len(self.index[cat]) < self.baseline_number:

			#get subcategories of a main category
			subcategories = self.get_subcategories(cat)

			# loop over subcategories of a main category
			for subcat in subcategories:

				for title in self.get_titles(subcat):
					if title not in self.index.values(): #check for duplicates
						self.index[cat].append(title)

							#used for treesearch
							#if len(self.index[cat]) > self.baseline_number:
							#	break

					# potentially loop further to get more articles

			#used for treesearch
			#self.index[cat] = self.index[cat][0:self.baseline_number] # cut to base_linenumber

			#pick random articles
			self.index[cat] = list(self.index[cat][i] for i in [random.randint(0, len(self.index[cat])-1) for i in range(self.baseline_number)])

			#write articles in file
			self.write_rawdata("|".join(self.index[cat]) , cat) # join to one string and spereate with | --> for api call

		#indexing all categories and titles for later use
		self.write_index(self.index)

	def convert_plain(self):
		'''
		Use WikiExtractor to get clear Text
		'''

		for file in os.listdir(self.rawpath):
			print("read document " + file)
			os.system("../wikiextractor/WikiExtractor.py "+self.rawpath+"/"+file+" -o "+self.plainpath+"/"+file.split(".")[0]+" --json")


def main():

	# root category your are looking for - default:"Category:Main topic classifications"
	origin_category = "Category:Main topic classifications"

	# number of articles you want from each category
	baseline_number = 20

	folder = "RandomBaseline"

	BL = Baseline(origin_category, baseline_number, folder)

	#BL.get_rawdata()
	BL.convert_plain()


if __name__== "__main__":
  main()
