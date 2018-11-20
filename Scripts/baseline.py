import requests
import os

URL = "https://en.wikipedia.org/w/api.php"

origin_category = "Category:Main topic classifications"

basline_number = 20


def get_titles(category):
	'''
	yields all article titles inside that category
	'''
	PARAMS = {
		'action': "query",
		'list': "categorymembers",
		'cmtitle': category,
		'cmlimit': 200,
		'cmnamespace':0, 	#-> plain articles belonging to that category
		'format': "json"
	}
	S = requests.Session()
	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()

	titles = []

	for article in DATA['query']['categorymembers']:
		titles.append(article['title'])

	return titles

def get_subcategories(category):
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
	R = S.get(url=URL, params=PARAMS)
	DATA = R.json()

	subcategories = []

	for article in DATA['query']['categorymembers']:
	 	subcategories.append(article['title'])

	return subcategories

def get_dumptext(title):
	'''
	gets text from a specific article, formated the same as the wiki dump file
	'''

	PARAMS = {
		'action': 'query',
		'prop':'revisions',
		'rvprop':'content',
		'titles': title,
		'export':1,
		'exportnowrap':1,
		'format': "json"
	}
	S = requests.Session()
	R = S.get(url=URL, params=PARAMS)
	DATA = R.text

	return DATA

def write_file(title, category):

	category = category.split(":")[1]

	#check if Directory exists
	if not os.path.exists("rawdata"):
		os.mkdir("rawdata")

	if not os.path.exists("rawdata/"+category):
		os.mkdir("rawdata/"+category)

	#wirte text to the file
	filename = "rawdata/"+category+"/"+title +".xml"
	with open(filename, 'w') as the_file:
		the_file.write(get_dumptext(title))

def main():

	#get main categories
	main_categories = get_subcategories(origin_category)


	# loop over all main categories
	for cat in main_categories:

		titles = []

		titles = titles + get_titles(cat)

		if len(titles) < basline_number:

			#get subcategories of a main category
			subcategories = get_subcategories(cat)

			# loop over subcategories of a main category
			for subcat in subcategories:
				titles = titles+ get_titles(subcat)
				if len(titles) > basline_number:
					break

			#if len(titles) < basline_number:
				# potentially loop further to get more articles

		titles = titles[0:basline_number]

		for title in titles:
			write_file(title, cat)



if __name__== "__main__":
  main()
