import Classes as cls
from Classes import Author
import re
import pandas as pd 

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        #récupère les documents par leurs id dans la liste id2docs
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]
        print("\n".join(list(map(repr, docs))))


    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

 
# --------------- CLASSE USINE ----------------
class DocumentFactory:
    @staticmethod
    def creerDoc(source, *args):
        if source == 'HackerNews':
            # Arguments attendus : titre, auteur, date, url, texte, nbCom
            return cls.HackerNewsDocument(*args)
        elif source == 'The_Guardian':
            # Arguments attendus : titre, auteur, date, url, texte, coAuteur
            return cls.TheGuardianDocument(*args)
        else:
            raise ValueError("Source non supportée. Veuillez utiliser 'HackerNews' ou 'The_Guardian'.")
    