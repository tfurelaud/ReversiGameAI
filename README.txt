Pour notre joueur nous avons décidé d'utiliser un algorithme NegaMax et l'algorithme PVS pour l'élagage. L'algorithme NegaMax nous permet de faire des recherches
 plus rapide dans notre arbre. Et le PVS/NegaScout nous permet d'élager plus de branches de notre arbre. Ainsi PVS est bien plus avancé qu'un simple alpha-beta sur un
  MiniMax. Pour implémenter cet algorithme, nous nous sommes inspiré du pseudo code présent sur : https://en.wikipedia.org/wiki/Principal_variation_search.
  
L'arbre utilise 3 heuristiques suivant l'avancée de la partie.

L'heuristique du début de partie peut être représentée sous la forme d'un tableau (grille de jeu) avec les valeurs les plus importantes au centre. Cette heuristique
prend aussi en compte le nombre de pièces alliées que nous avons sur le plateau ainsi que le nombre de voisins que l'on a. En effet, en début de partie on voudra
avoir le moins de pièces possible sur le plateau, que celles ci soient disposées le plus au centre possible et qu'elles soient le plus groupées possible.

La deuxième heuristique est celle de milieu de partie. Nous pouvons elle aussi la représenter sous forme de tableau. Les valeurs les plus grandes sont les 4 coins
(une fois qu'un coin est pris par un joueur, il le restera toute la partie, ces cases sont donc importantes). Les 2 cases adjacentes à chaque coin se trouvant sur
les bords du tableau sont quant à elles, négatives si l'adversaire peut prendre le coin si on joue notre coup ici, ou alors assez grandes sinon. Ces cases sont
en effet assez importantes si elles ne conduisent pas l'adversaire à prendre un coin. La dernière case adjacente à chaque coin est quant à elle négative car elle
représente un vrai danger. Ensuite nous avons donné une valeur positive aux autres cases se trouvant sur les bords du tableau car celles-ci sont avantageuses.
Enfin nous donnons aussi une valeur positive aux cases se trouvant au centre car à tout moment de la partie celles-ci sont importantes (pour éviter que
l'adversaire ne prenne toute une ligne, colonne, ou diagonale). Pour des précisions sur les valeurs retournaient par cette heuristique nous avons fait des
pattarns (diagonales, lignes, colonnes, bloc 4x4 dans un coin, bloc 6x3 dans un coin ...) qui valent plus ou moins de points. Par exemple, la diagonale de
longueur 10 vaut beaucoup de points car elle regroupe deux coins. Pour finir, on calcule la mobilité du joueur adverse après notre coup, pour que celle ci soit
la plus faible possible (qu'il ne puisse jouer que des mauvais coups, voir ne pas jouer si possible).

La dernière heuristique est celle de fin de partie. Pour celle la nous regardons juste si on gagne ou pas.

Les deux premières heuristiques sont utilisées sur un PVS de profondeur 3 et la dernière sur un PVS de profondeur 11 à 11 coups de la fin
(si une victoire est possible à 11 coups de la fin alors on gagnera surement).
