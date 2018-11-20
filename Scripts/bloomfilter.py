# Bloom filter

# feed the bloom filter with top 50 words of 10 baseline articles
#
# then take top 50 words of new article -> check if exits
# -> percentage of existance of all words

import math
import mmh3

class BloomFilter:

	def __init__(self):
		'''
		Setup variables in here

		n : number of items expected to be stored in filter
		p : False Positive probability
		'''

		self.n= 200
		self.p = 0.05
		self.size = int(-(self.n * math.log(self.p))/(math.log(2)**2))
		self.hash_count = int((self.size/self.n) * math.log(2))

		self.intval = 0

	def train(self,item):
		'''
		Add an item to the BloomFilter / train the filter

		item: item that needs to be added to the filter
		'''

		for i in range(self.hash_count):
			#get the hash value for the item, maximum size is self.size
			hash_value = mmh3.hash(item,i) % self.size

			# binary with 1 at position hash_value+1
			x = 1<<(hash_value)

			# set the bit
			self.intval = self.intval | x

	def classify(self, item):
		'''
		Check the existance of an item

		returns
		- true if there is a probability that the item exists in list
		- false if it definitley doesn't exist
		'''

		for i in range(self.hash_count):
			#get hash_value as in train
			hash_value = mmh3.hash(item,i)%self.size

			# binary with 1 at position hash_value+1
			x = 1<<(hash_value)

			# check if bit is set
			if not (x & self.intval) >= 1:
				return False
		return True

anachrismBF = BloomFilter()

topwords = [('anarchism', 352), ('web', 174), ('date', 164), ('title', 157), ('anarchist', 155), ('org', 145), ('name', 144), ('publisher', 100), ('book', 95), ('cite', 92), ('isbn', 88), ('year', 82), ('anarchists', 81), ('p', 73), ('com', 70), ('movement', 69), ('access', 67), ('html', 65), ('press', 64), ('revolution', 63)]

for word in topwords:
	anachrismBF.train(word[0])

checkwords = [('anarchism', 8), ('theory', 4), ('authority', 2), ('power', 2), ('justification', 1), ('claims', 1), ('liberty', 1), ('anarchists', 1), ('consensus', 1), ('building', 1), ('efforts', 1), ('communities', 1), ('agendas', 1), ('forms', 1), ('action', 1), ('entry', 1), ('idea', 1), ('activism', 1), ('legitimation', 1), ('describe', 1)]

match_words = 0

for word in checkwords:
	if(anachrismBF.classify(word[0])):
		match_words += 1

print("Number of checkd words: " + str(len(checkwords)))
print("Number identical words: " + str(match_words))
print("Percentage of identical words: " + str(match_words/(len(checkwords))))
