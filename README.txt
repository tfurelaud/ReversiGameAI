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

///////// ENGLISH

For our player we decided to use a NegaMax algorithm and the PVS algorithm for pruning. The NegaMax algorithm allows us to do research
 faster in our tree. And the PVS / NegaScout allows us to prune more branches from our tree. Thus PVS is much more advanced than a simple alpha-beta on a
  MiniMax. To implement this algorithm, we were inspired by the pseudo code present on: https://en.wikipedia.org/wiki/Principal_variation_search.


The tree uses 3 heuristics depending on the progress of the game.

The start-of-game heuristic can be represented in the form of a table (game grid) with the most important values ​​in the center. This heuristic
also takes into account the number of allied pieces that we have on the board as well as the number of neighbors that we have. Indeed, at the start of the game we will want
have as few pieces as possible on the board, that they are placed as centrally as possible and that they are as grouped as possible.

The second heuristic is the mid-game heuristic. We can also represent it in the form of a table. The largest values ​​are the 4 corners
(once a corner is taken by a player, it will remain so the whole game, so these boxes are important). The 2 squares adjacent to each corner located on
the edges of the table are negative if the opponent can take the corner if we play our shot here, or quite large if not. These boxes are
indeed quite important if they do not lead the opponent to take a corner. The last square adjacent to each corner is negative because it
represents a real danger. Then we gave a positive value to the other boxes located on the edges of the table because they are advantageous.
Finally we also give a positive value to the boxes located in the center because at any time of the game they are important (to prevent
the opponent does not take a whole row, column, or diagonal). For details on the values ​​returned by this heuristic we have made
pattarns (diagonals, lines, columns, 4x4 block in a corner, 6x3 block in a corner ...) which are worth more or less points. For example, the diagonal of
length 10 is worth a lot of points because it has two corners. Finally, we calculate the mobility of the opposing player after our move, so that it is
as weak as possible (that he can only play bad moves, or even not play if possible).

The last heuristic is the end-of-game heuristic. For this we are just looking at whether we win or not.

The first two heuristics are used on a PVS of depth 3 and the last on a PVS of depth 11 to 11 strokes from the end
(if a victory is possible with 11 moves from the end then we will surely win).

SORRY IF THE TRANSLATION IS NOT CORRECT AT ALL, ITS SIMPLY A GOOGLE TRAD TRADUCTION.
