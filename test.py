from SearchEngine import SearchEngine
import SearchEngine
import requests
from datetime import datetime, timezone 
from Classes import Document, Author, HackerNewsDocument, TheGuardianDocument
from bs4 import BeautifulSoup
from Corpus import Corpus, DocumentFactory
from scipy.sparse import csr_matrix
from SearchEngine import SearchEngine

'''
actually, ID: 0
best, ID: 1
everybody, ID: 2
hello, ID: 3
help, ID: 4
israel, ID: 5
killing, ID: 6
last, ID: 7
like, ID: 8
need, ID: 9
palestinians, ID: 10
program, ID: 11
programming, ID: 12
really, ID: 13
see, ID: 14
someday, ID: 15
thankful, ID: 16
wednesday, ID: 17
would, ID: 18
yes, ID: 19
pus test'''
corpus = Corpus("mon corpus")
corpus.add(Document("14/11/2024","doc1","me","url1","last sunday i was programming a game"))
corpus.add(Document("05/09/2024", "doc10", "my neighbor", "url10", "thank you for watering my plants while I was away, you saved them"))
corpus.add(Document("14/11/2024","doc3","my girl","url3","your support during the last few weeks has meant the world to me, thank you"))
corpus.add(Document("14/11/2024","doc4","my mother","url4","i am very very very thankful for what you did last wednesday, you really are the best"))


search_engine = SearchEngine(corpus)


print(search_engine.search("hands"))

'''
SearchEngine
SetVocab()
SetMatrice_TFIDF()
search() '''