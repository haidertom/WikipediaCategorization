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

		self.n= 2000
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
