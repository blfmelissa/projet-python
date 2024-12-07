
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def get_text(self) : 
        return f"{self.texte}"
    
    def getType(self) :
        pass

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"


class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
    #===== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)

    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    

class HackerNewsDocument(Document) : 
    def __init__(self, titre, auteur, date, url, texte, score) : 
        Document.__init__(self, titre, auteur, date, url, texte)
        self.setScore(score)

    def getScore(self):
        return self.score
    
    def setScore(self,score) : 
        self.score = score

    def __str__(self) : 
        return f"L'article '{self.titre}' a été écrit par {self.auteur}"
    
    def getType(self) :
        return "HackerNews"


class TheGuardianDocument(Document) : 
    def __init__(self, titre, auteur, date, url, texte, firstPublicationDate) : 
        Document.__init__(self, titre, auteur, date, url, texte)
        self.setFirstPublicationDate(firstPublicationDate)

    def getFirstPublicationDate(self):
        return self.firstPublicationDate
    
    def setFirstPublicationDate(self,firstPublicationDate) : 
        self.firstPublicationDate = firstPublicationDate

    def __str__(self) : 
        return f"L'article '{self.titre}' a été écrit par {self.auteur}"
    
    def getType(self) :
        return "The_Guardian"
