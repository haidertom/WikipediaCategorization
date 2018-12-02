import math

class TfIdf():
	def __init__(self):
		pass

	# function tf takes document length and number of word occurences in the file and returns calculated term frequency
	def tf(self, occurence, length):
		return (occurence/length)

	# function idf takes number of all proccessed documents ( in our case N = 2 ) and number of documents this word appeard at least once (in our case it can be 1 or 2)
	def idf(self, total_num_of_doc, no_of_doc_it_appeard_in):
		return math.log(total_num_of_doc / no_of_doc_it_appeard_in )

	# function tfidf takes document length and number of word occurences and calculate tf-idf factor
	def tfidf(self, no_of_occurences,total_length, total_num_of_doc, no_of_doc_it_appeard_in ):
		return tf(no_of_occurences,total_length) * idf(total_num_of_doc,no_of_doc_it_appeard_in)
