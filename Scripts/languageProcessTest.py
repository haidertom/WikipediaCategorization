import languageProcess as lp
import BloomFilter



path = '../TestArticle/plaindata/Arts_50/AA/wiki_00'
lang = lp.languageProcess(path)
test = lang.getWords()
test2 = [word for word in test if any(ch.isdigit() for ch in word)]
print(test2)



'''

spaceBF = BloomFilter.BloomFilter()

counter = 0

for article in test:
	for word in article.most_common(30):
		spaceBF.train(word[0])
	counter += 1
	if counter == 7:
		break


match_words = 0

checkwords = test[7].most_common(30)

match_words = 0

for word in checkwords:
	if(spaceBF.classify(word[0])):
		match_words += 1

print("Number of checkd words: " + str(len(checkwords)))
print("Number identical words: " + str(match_words))
print("Percentage of identical words: " + str(match_words/(len(checkwords))))
'''