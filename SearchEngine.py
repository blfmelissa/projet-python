from Corpus import Corpus, DocumentFactory
import scipy as sp
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from collections import defaultdict
import string

class SearchEngine : 
    def __init__(self, corpus) : 
        self.corpus = corpus
        self.mat_TFIDF = None   # On la définira avec la fonction matrice_TF_IDF
        self.SetVocab()         # Crée le vocabulaire et le met dans self.vocab
        self.SetMatrice_TFIDF() 

    def SetVocab(self) : 
        voc = self.corpus.stats()
        # tri par ordre alphabétique
        voc = voc.sort_values(by="Mot").reset_index(drop=True)
        self.vocab = {}
        for id, row in voc.iterrows(): # parcourir un dataframe (par ligne)
            mot = row["Mot"]
            self.vocab[mot] = {
                "id": id
            }

    def SetMatrice_TFIDF(self) :
        rows, cols, data = [], [], []
        n_docs, n_words = self.corpus.ndoc, len(self.vocab)

        for i,doc in enumerate(self.corpus.id2doc.values()):
            words = doc.get_text().lower().split()
            for word in words : 
                word = word.translate(str.maketrans("", "", string.punctuation))
                if word in self.vocab : 
                    rows.append(i) # indices des documents
                    cols.append(self.vocab[word]['id']) # id du mot
                    data.append(1) # le mot apparait (au moins) une fois

        #matrice creuse
        mat_TF = csr_matrix((data,(rows,cols)), shape =(n_docs,n_words))
        #rows = indice du document dans lequel le mot apparait
        #cols = indice du mot dans le vocabulaire
        #data = la frequence du mot dans ce document (tjr 1 pour l'instant)

        term_freq = np.array(mat_TF.sum(axis=0)).flatten() # term frequency
        doc_freq = np.array((mat_TF > 0).sum(axis=0)).flatten() # document frequency

        for i, word in enumerate(self.vocab):
            # pour ajouter des attributs dans vocab
            self.vocab[word]['tf'] = int(term_freq[i]) 
            self.vocab[word]['df'] = int(doc_freq[i])

        idf = np.log(n_docs / (term_freq+1)) + 1

        #Multiplier la matrice TF avec le vecteur IDF pour la matrice TF-IDF
        self.mat_TFIDF = mat_TF.multiply(idf) 


    def search(self,query) : 
        # prétraitement de query
        listeMotsUser = query.lower().split()
        
        #On vectorise la requete
        query_vec = np.zeros(len(self.vocab)) # vecteur initialisé avec des 0
        for word in listeMotsUser:
            if word in self.vocab : 
                query_vec[self.vocab[word]['id']] += 1

        # calcule la norme (longueur) du vecteur
        query_norm = np.linalg.norm(query_vec) 
        if query_norm == 0 : 
            print ("Aucun mot n'existe dans le vocabulaire du corpus")
            return pd.DataFrame(columns=["Document", "Similitude"])
        
        # calcul de la norme de chaque document dans la matrice tf-idf
        doc_norms = np.linalg.norm(self.mat_TFIDF.toarray(), axis=1)
        doc_norms[doc_norms == 0] = 1 # remplace les 0 par 1 pour éviter division by 0
        # calcul de la similarité cosinus entre la requête et chaque document
        cos_sim = self.mat_TFIDF.dot(query_vec) / (doc_norms * query_norm)

        # Tri décroissant des résultats 
        most_similar_doc = np.argsort(cos_sim)[::-1]
        
        results = [
            {"Document": self.corpus.id2doc[i+1], "Similitude": cos_sim[i]} 
            for i in most_similar_doc if cos_sim[i] > 0
        ]

        if len(results) == 0:
            print("Aucun document ne correspond à la requête")
            return pd.DataFrame(columns=["Document", "Similitude"])

        return pd.DataFrame(results)
