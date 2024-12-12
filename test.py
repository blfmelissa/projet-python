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
corpus.add(Document("14/11/2024","doc1","me","url1","someday yes wednesday program i am programming"))
corpus.add(Document("14/11/2024","doc2","confident me","url2","hello everybody actually israel is killing palestinians."))
corpus.add(Document("14/11/2024","doc3","my girl","url3","palestinians need help. would you like to see my program?"))
corpus.add(Document("14/11/2024","doc4","my mother","url4","i am very very very thankful for what you did last wednesday you really are the best"))



search_engine = SearchEngine(corpus)
results = search_engine.search("help")
res = corpus.stats()
lign = res[res["Mot"] == "program"]
tst = search_engine.vocab
print(tst)