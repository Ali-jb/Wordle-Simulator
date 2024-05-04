import pandas as pd
import nltk
from sklearn.utils import shuffle
#download text corpus
# nltk.downloader.download('gutenberg')

#reading dictionary of words
words = pd.read_csv('data/american-english', header = None, names = ['words'])
words = words.dropna()

#process and shuffle
words = words[words['words'].apply(lambda x: len(x)) == 5].reset_index().drop('index', axis = 1)
words['words'] = words['words'].apply(lambda x: x.lower())
words = words.drop_duplicates()
words['words'] = shuffle(words['words'])
words = words[~words['words'].str.contains("['àéêëñóôöü]")] 

#adding frequency scores
corpus = nltk.corpus.gutenberg.words()
corpus = pd.DataFrame(corpus, columns = ['words'])
corpus['words'] = corpus['words'].apply(lambda x: x.lower())
corpus = pd.DataFrame(corpus.value_counts()).reset_index()
corpus.columns = ['words', 'freq']
corpus = corpus[corpus['words'].apply(lambda x: len(x)) == 5]
corpus['freq'] = corpus['freq'] / corpus['freq'].max()

words = words.merge(corpus, on='words', how='left')
words['freq'] = words['freq'].fillna(0.000080)
words['freq'] = pd.qcut(words['freq'], q = 50, duplicates = 'drop', labels = list(range(1, 20)))
words['freq'] = words['freq'].cat.codes + 1

words.to_csv('data/american-english_processed.csv')
