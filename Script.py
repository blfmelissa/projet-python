
import requests
from datetime import datetime, timezone 
from Classes import Document, Author, HackerNewsDocument, TheGuardianDocument
from bs4 import BeautifulSoup
from Corpus import Corpus, DocumentFactory

#--------------Définition des variables
#variable pour stocker les documents à l'état 'brut'
collection = []
#Nombre d'articles à récupérer
nbDoc = 10
#query = ["Day","Country","Travel","Tokyo"] 
query ="War"
api_key_guardian = "265a16e3-294c-4c62-ae88-a274906a6333"


def search_query(texte,mots_cles) : 
    #Vérifie si un des mots clés est présent dans le texte ou le titre
    return any(mot.lower() in texte.lower() for mot in mots_cles)

def extraire_text_url(url) : 
    try:
        #On récupère la page html puis on vérifie si la requête a réussi
        response = requests.get(url)
        response.raise_for_status()
        #On extrait uniquement les balises <p> présentes dans le body
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.body
        if body is None:
            return "Texte non disponible" #Car pas de body
           
        paragraphes = body.find_all("p")    #Texte à partir du body
        texte = "\n".join(p.get_text(strip=True) for p in paragraphes)
        if(texte.strip) : 
            return texte
        else : 
            return "Texte non disponible"
    except Exception :
        return "Texte non disponible"

#-----------------------WebScrapping avec Hacker News API
def add_doc_HackerNews(collection,query,nbDoc) :
    #Nombre de storys récupérées
    nbCount =0
    url = "https://hacker-news.firebaseio.com/v0/beststories.json"
    response = requests.get(url)
    #Renvoie une exception si aucun article n'a été trouvé 
    if response.status_code !=200 : 
        raise Exception(f"Aucun texte provenant de HackerNews ne correspond à la recherche {query}")
    
    top_stories = response.json()
    for id in top_stories[:1000]:  #C'est pour être sûr d'avoir un jeu de données conséquent
        #Si on a atteint le nombre de doc, on arrête de chercher
        if nbCount >= nbDoc:
            break

        url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
        
        data = requests.get(url)
        data = data.json()
        #Récupération des données pour chaque url
        titre = data.get("title", "No title")
        auteur = data.get("by", "Unknown")
        timestamp = data.get("time", 0)
        #Formatage de la date 
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        article_url = data.get("url")
        texte = extraire_text_url(article_url)  
        score = data.get("score", 0)

        #On créé un document à partir des informations récoltées
        if texte != "Texte non disponible" :
            #On applique la recherche de mots clés sur le titre et le texte
            if search_query(titre, query) or search_query(texte, query):
                doc = DocumentFactory.creerDoc('HackerNews', titre, auteur, date, article_url, texte, score)
                collection.append(doc)
                nbCount +=1
    return collection

#-----------------------WebScrapping avec The Guardian API
def add_doc_Guardian(collection, query, nbDoc, api_key):
    nbCount = 0
    url = f"https://content.guardianapis.com/search?q={query}&page-size={nbDoc}&api-key={api_key}"
    response = requests.get(url)
    #Renvoie une exception si aucun article n'a été trouvé 
    if response.status_code !=200 : 
        raise Exception(f"Aucun article provenant de The Guardian ne correspond à la recherche {query}")
    
    data = response.json()
    for article in data["response"]["results"]:
        #Si on a atteint le nombre de doc, on arrête de chercher
        if nbCount >= nbDoc:
            break
        #Récupération des données pour chaque url
        titre = article["webTitle"]
        article_url = article["webUrl"]
        texte = extraire_text_url(article_url)
        try :   #Il n'y a pas tout le temps des auteurs
            auteur = article.get("author", "Auteur inconnu")
        except : 
            auteur = "The Guardian"
        # Première date de publication (on récupère sous forme de string avant de la convertir en date)
        release_date_str = article.get("firstPublicationDate", "")
        release_date = None     #Il faut instancier
        if release_date_str:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")  
        
        # Dernière date de mise à jour (on récupère sous forme de string avant de la convertir en date)
        last_maj_str = article.get("lastModified", "")
        last_maj = None         #Il faut instancier
        if last_maj_str:
            last_maj = datetime.strptime(last_maj_str, "%Y-%m-%dT%H:%M:%S.%fZ") 

        if texte != "Texte non disponible":
            doc = DocumentFactory.creerDoc('The_Guardian', titre, auteur, last_maj, article_url, texte, release_date)
            collection.append(doc)
            nbCount += 1

    return collection

#-------------------RECUPERATION DES DONNEES
add_doc_HackerNews(collection,query,nbDoc) 
add_doc_Guardian(collection,query, nbDoc, api_key_guardian)
'''
for doc in collection : 
    print(doc.texte)
    print('------------------------------')
'''
print(f"nbCount : {len(collection)}")    


# Création de l'index de documents à partir de la collection
#Clé : un Id 
#Valeur : le titre du document
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de l'index des Auteurs à partir de la collection
#Clé : un Id (en fonction de la valeur de la variable num_auteurs_vus)
#Valeur : un objet de type Author
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus
    authors[aut2id[doc.auteur]].add(doc.texte)


# Construction du corpus à partir des documents présents dans la collection
corpus = Corpus("Mon corpus")
for doc in collection:
    corpus.add(doc)
