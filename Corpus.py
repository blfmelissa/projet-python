import Classes as cls
from Classes import Author
import re
import pandas as pd
from collections import defaultdict
from nltk.corpus import stopwords  #permet de ne pas prendre en compte les "stopwords" dans le vocabulaire
import random

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
    
    def search(self, mot_cle) :
        if not mot_cle or not isinstance(mot_cle, str):
            raise ValueError("Le mot-clé est invalide")
        try :
            texte = self.textes_all
        except : 
            self.textes_all = " ".join([doc.texte for doc in [*self.id2doc.values()]])
            texte = self.textes_all
        pattern = re.compile(re.escape(mot_cle), re.IGNORECASE)
        # re.escape garantit que les caractères spéciaux sont
        # correctement interprétés comme du texte brut

        res = pattern.finditer(texte)
        if not res : 
            print("Aucune occurrence trouvée.")
            return []
        
        start_pattern = [m.start() for m in res]
        print(f'{len(start_pattern)} occurrences trouvées')
        return list(texte[i-20:i+20] for i in start_pattern)
    
    def concorde(self, mot_cle, taille) : 
        try :
            texte = self.textes_all
        except : 
            self.textes_all = " ".join([doc.texte for doc in [*self.id2doc.values()]])
            texte = self.textes_all
        pattern = re.compile(mot_cle, re.IGNORECASE)
        res = pattern.finditer(texte)
        pos_pattern = [m.span() for m in res]
        context_left = pd.DataFrame("..."+texte[i-taille:i-1] for (i,j) in pos_pattern)
        center = pd.DataFrame(texte[i:j] for (i,j) in pos_pattern)
        context_right = pd.DataFrame(texte[j+1:j+taille]+"..." for (i,j) in pos_pattern)
        result = pd.concat([context_left, center, context_right], axis = 1)
        result.columns=["contexte gauche", "centre", "contexte droit"]
        return result
    
    def nettoyer_texte(self, texte) : 
        texte = texte.lower()
        texte = texte.replace("\n"," ")
        # Suppression des chiffres 
        texte = re.sub(r'\d+', '', texte)
        # Suppression de la ponctuation
        texte = re.sub(r'[^\w\s]', '', texte)
        # Suppression des espaces multiples
        texte = re.sub(r'\s+', ' ', texte).strip()
        return texte

    def stats(self, nreturn=10) :
        tf = defaultdict(int)  # occurrences des mots
        df = defaultdict(int)    # nombre de documents contenant chaque mot
        vocab = set()            
        
        stop_words = set(stopwords.words('english')) #stopwords anglais

        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.get_text())
            mots_doc = set(texte_nettoye.split())
            vocab.update(mots_doc)
            
            for mot in mots_doc:
                if mot not in stop_words :
                    tf[mot] += texte_nettoye.split().count(mot)  
                    df[mot] += 1  
    
        tf_df = pd.DataFrame(list(tf.items()), columns=["Mot", "TF"])
        df_df = pd.DataFrame(list(df.items()), columns=["Mot", "DF"])
        # term frequency et document frequency
        
        # fusionner des deux dataframes sur la colonne "Mot"
        freq = pd.merge(tf_df, df_df, on="Mot")
        
        print(f"{len(vocab)} mots différents dans le vocabulaire")
        print(f"Les {nreturn} mots les plus fréquents :")
        print(freq.nlargest(nreturn, 'TF')[['Mot', 'TF', 'DF']]) # tri par TF

        return freq # renvoie un dataframe
    
    #On récupérera aléatoirement un extrait de texte
    #Ici, il n'y a pas de recherche parmots clés, on prend juste un extrait aléatoire
    def get_random_excerpt(self, texte, length=20):
        words = texte.split()
        if len(words) <= length:
            return texte
        start = random.randint(0, len(words) - length)
        excerpt = ' '.join(words[start:start + length])
        return f"... {excerpt} ..."

    #On récupère la liste des auteurs en fonction du type de document
    #On utilisera cette fonction pour la visualisation des auteurs par type de document
    def get_name_authors_by_type(self,typeDoc="all"):
        #Par défaut "all" pour avoir la liste de tous les auteurs
        if typeDoc == 'all':
            return sorted([author.name for author in self.authors.values()]) 
        else:
            #Si le type est précisé à l'appel de la fonction
            authors_by_type = set()
            for doc in self.id2doc.values():
                if doc.getType() == typeDoc:
                    authors_by_type.add(doc.auteur)
            return sorted(authors_by_type)

    #On récupère les documents avec une liste de noms d'auteur
    #On renvoie un dataframe avec les colonnes Titre, Auteur, Extrait, URL et Type        
    def get_doc_by_authors(self,authors) : 
        results = []
        for doc in self.id2doc.values():
            extrait = self.get_random_excerpt(doc.texte)
            if doc.auteur in authors : 
                results.append({
                    "Titre": doc.titre,
                    "Auteur": doc.auteur,
                    "Extrait": extrait,
                    "URL": getattr(doc, 'url', 'Non disponible'),
                    "Type": doc.getType()
                })
        return pd.DataFrame(results)

 
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
    