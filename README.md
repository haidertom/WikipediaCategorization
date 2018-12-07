# Categorization of Wikipedia articles

## Abstract

In this project, we showcase two different approachs to automatically assign new articles to their respective main-categories in Wikipedia, based on their content.

In  a  first  prototype  we  implemented  the  automated  allocation  of  an  article  to  one  of Wikipedia’s 27 Main topic classifications, namely: Arts, Business, Concepts, Culture, Education, Entertainment, Events, Geography, Health, History, Humanities, Language, Law, Life, Mathematics, Nature, People, Philosophy, Politics, Reference, Religion, Science, Society, Sports, Technology, Universe and World.

Utilizing the Wikipedia API, we created a baseline, containing a sufficient number of articles for each category. We then processed the obtained articles, eliminated irrelevant features such as stop words and stemmed /lemmatized every word. The cleansed articles were then used to train two different models, the LSI and the Bloom Filter.

### LSI
LSI is a technique of computing relationships between documents by exploring the latent topics hidden behind the terms they contain. Term  weights  can  be  computed  using  different  techniques,  the  most popular one however is TF-IDF. By joining togehter all articles of the same category and calculating each terms TF-IDF value we create a representation matrix for every categroy in our baseline. We then calculate a vector for each matrix and thus get a vector representation of each category. Given a new article, we follow the same steps and can thus calculate the similarty to each of our baseline vectors, using the cosine similarity.  The Category of the vector for which the highest similarity is achieved, is then assigned to the new article. 

### Bloom Filter
The idea behind using a Bloom filter is, that we assume that all articles in a category are similar to each other with respect to a certain set of keywords. We therefore create a Bloomfilter for every category in our baseline and train it with a set of keywords that is characteristic for the respective category.  Given a new article, we extract the article’s keywords and check the existence of each Keyword in every Category, more specifically in every Bloomfilter.  The Category of the respective Bloomfilter, for which the highest number of matching words is achieved, is then assigned to the new article.  We  thereby achieve a similarity  determination based on the conformity of certain keywords. To extract the relevant keywords form our baseline articles, we used the TF-IDF measurement. 



## Usage 

### Requirements
Make sure you installed all packages given in the requirements.txt

### Showcase
A fast visulization of our results is given in the jupyter notebook *Showcase.ipynb*.  Run all cells and when promted, type in an article from the english Wikipedia you wish to categorize, e.g. *Football*. If the article exists, the article is downloaded in the background (you need an Internet connection for this).  For each of the Wikipida main topic classifcations, the probability that the article belongs to that category is then calculated and shown in a graph. 


### Scripts
To see how our approach works in detail, we briefly describe the function of every script.

- **basline.py:** Downloads  a basline of *baseline_number* articles for every subcategory in a parentcategory. Uses the  WikiExtractor tool to clear each text from formatting. To see how the process works, use a short number of articles in every category (e.g. 20). 
Runnable as a Script or callable via the Class *Baseline*

- **BloomClassify.py:** All Functions needed for the Bloom Filter approach, captured in the Class *BloomClassify*.
Used to train, save and load a Bloom Filter model and to calculate the Similiarity Matrix of a Basline.
Please refer to the function description for more detail.
Runnable as a Script or callable via the Class *Baseline*

- **BloomFilter.py:** Implementation of a Bloom Filter. Used to Create a BloomFilter, train it with values and classify values.
Callable via the Class *BloomFilter*.


- **languageProcess.py:** Preprocessing of obtained articles in the basline. Used to remove stop words and punctuation, lemmatize words /stigmatize words and get Frequency distributions of every word in an article.

- **LSI.py:**


- **LSIsimilarity.py:**


- **PerformanceTest.py:** All functions used for testing of our results. Similarity Calculation and  Visualization in Grpahs.
Runnable as Script.

- **tfidf.py:** Implementation of the TF-IDF measurement calcualtion. 
Callable via the Class *TfIdf*.

