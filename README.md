# projet-python
Un moteur de recherche textuel et opérationnel utilisant des corpus de documents provenant de HackerNews et The Guardian.
Une interface sous forme de notebook permet de tester ce moteur de recherche :
- Vous pouvez rechercher un ou des mots clés dans un corpus sur le thème "War" et une liste de documents vous sera affichée avec des liens cliquables pour accéder directement au site web de l'article.
- Vous pouvez choisir de "comparer" entre le thème précédent et un autre, "Computer". Dans ce cas, vous avez le choix entre une comparaison par mots-clés ou une par auteurs. 
- Vous pouvez personnaliser et filtrer vos recherches. Par exemple : rechercher seulement des articles de The Guardian, indiquer le nombre maximal de résultats que vous souhaitez ...
- Les résultats de vos recherches sont triés par ordre décroissant de taux de similitude.

# Installation
git clone https://github.com/blfmelissa/projet-python.git
cd projet-python

# Installer les dépendances nécessaires 
pip install -r requirements.txt