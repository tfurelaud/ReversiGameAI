# -*- coding: utf-8 -*-

import time
import Reversi
import math
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        global etat
        global nb_coups
        nb_coups = 0
        etat = "debut_partie"

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        global etat
        global nb_coups


        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        maxi = -math.inf
        moves = [m for m in self._board.legal_moves()]
        move = moves[0]
        #On parcourt les coups possibles
        for k in moves:
            #3 différents cas pour les 3 différents moments de la partie
            if(etat == "debut_partie"):
                #Recherche de la plus grande valeur de PVS.
                self._board.push(k)
                curr = -self.pvs(3,-math.inf,math.inf,True,False)
                self._board.pop()
                if (curr > maxi):
                    maxi = curr
                    move = k
                if(self._board._nbBLACK + self._board._nbWHITE >18):
                    etat = "milieu_partie"

            if(etat == "milieu_partie"):
                self._board.push(k)
                curr = -self.pvs(3,-math.inf,math.inf,False,False)
                self._board.pop()
                if (curr > maxi):
                    maxi = curr
                    move = k
                if(self._board._nbBLACK + self._board._nbWHITE >=89):
                    etat = "fin_partie"

            if(etat == "fin_partie"):
                self._board.push(k)
                curr = -self.pvs(11,-math.inf,math.inf,False,True)
                mobility = self.mobility()
                self._board.pop()
                if (curr > maxi):
                    maxi = curr
                    move = k
            print("MAXI :",maxi)

        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        nb_coups = nb_coups +1
        return (x,y)

    #Heuristique de début de partie
    def firstHeuristique(self):
        res = 0
        nb_pieces = 0
        nb_voisins = 0
        #Si on peut gagner directement alors on renvoie une énorme valeur pour faire le coup en question
        if(self._board.is_game_over()):
            if ((self._mycolor is self._board._WHITE) and ((self._board._nbWHITE - self._board._nbBLACK)>0)):
                return 100000
            elif((self._board._nbBLACK - self._board._nbWHITE) > 0):
                return 100000
        #Cette boucle sert à valoriser les cases au centre du plateau et à compter les pièces qu'on a,
        #ainsi que le nombre de voisin total qu'on a(on veut que nos jetons soient groupés)
        for i in range(self._board._boardsize) :
            for j in range(self._board._boardsize) :
                if self._board._board[i][j] == self._mycolor :
                    nb_pieces = nb_pieces + 1
                    middle = int(self._board._boardsize / 2)
                    if (i == 0 or i == self._board._boardsize - 1) and (j == 0 or j == self._board._boardsize - 1):
                        res = res + 30
                    if ( (i>=1 and i<self._board._boardsize - 2) and (j == 1 or j == self._board._boardsize - 2)) or ((j>=1 and j<self._board._boardsize - 2) and (i == 1 or i == self._board._boardsize - 2)):
                        res = res - 500
                    if ( (i>=3 and i<self._board._boardsize - 4) and (j == 3 or j == self._board._boardsize - 4)) or ((j>=3 and j<self._board._boardsize - 4) and (i == 3 or i == self._board._boardsize - 4)):
                        res = res + 30
                    if ((i == middle - 1 or i == middle) and (j == middle - 1 or j == middle)):
                        res = res + 100
                    if(((i==0 or i==self._board._boardsize-1) and (j>1 or j<self._board._boardsize-2)) or ((j==0 or j==self._board._boardsize-1) and (i>1 or i<self._board._boardsize-2))):
                        res = res - 50
                    if ( (i>=1 and i<self._board._boardsize - 2) and (j == 0 or j == self._board._boardsize - 1)) or ((j>=1 and j<self._board._boardsize - 2) and (i == 0 or i == self._board._boardsize - 1)):
                        res = res +5
                    if(i >= 1 and j >= 1):
                        if(self._board._board[i-1][j-1] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(j >= 1):
                        if(self._board._board[i-1][j] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(i>=1 and j<self._board._boardsize - 1):
                        if(self._board._board[i-1][j+1] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(j < self._board._boardsize-1):
                        if(self._board._board[i][j+1] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(i<self._board._boardsize-1 and j<self._board._boardsize-1):
                        if(self._board._board[i+1][j+1] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(i < self._board._boardsize-1):
                        if(self._board._board[i+1][j] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(i<self._board._boardsize-1 and j>=1):
                        if(self._board._board[i+1][j-1] == self._mycolor):
                            nb_voisins = nb_voisins + 1
                    if(j>=1):
                        if(self._board._board[i][j-1] == self._mycolor):
                            nb_voisins = nb_voisins + 1

        mobility = self.mobility()
        if(mobility == 0):
            mobility = 10000
        #On renvoie la somme (On veut une grande valeur, le moins de pièces possibles
        #la plus grande mobilité et le plus de voisins possibles)
        return (res/(nb_pieces+1))+3*mobility+3*nb_voisins

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost !!")


    #Regarde si la ligne "ligne" est complètement remplie de nos jetons
    def checkHorizontal(self,ligne):
        for j in range(self._board._boardsize):
            if(self._board._board[ligne][j] != self._mycolor):
                return False
        return True

    #Regarde si la colonne "colonne" est complètement remplie de nos jetons
    def checkVertical(self,colonne):
        for i in range(self._board._boardsize-1):
            if(self._board._board[i][colonne] != self._mycolor):
                return False
        return True

    #Regarde si la diagonale en haut à gauche à "space" espace de 0 est complètement remplie de nos jetons
    def checkDiagonalTopLeft(self,space):
        for i in range(space+1):
            j = space - i
            if(self._board._board[i][j] != self._mycolor):
                return False
        return True

    #Regarde si la diagonale en bas à droite à "space" espace de 0 est complètement remplie de nos jetons
    def checkDiagonalBotRight(self,space):
        for i in range(self._board._boardsize-1-space, self._board._boardsize):
            j = self._board._boardsize - 1 - i
            if(self._board._board[space - i][j] != self._mycolor):
                return False
        return True

    #Regarde si la diagonale en bas à gauche à "space" espace de 0 est complètement remplie de nos jetons
    def checkDiagonalBotLeft(self,space):
        j = 0
        for i in range(self._board._boardsize-1-space, self._board._boardsize):
            if(self._board._board[i][j] != self._mycolor):
                return False
            j = j + 1
        return True

    #Regarde si la diagonale en haut à droite à "space" espace de 0 est complètement remplie de nos jetons
    def checkDiagonalTopRight(self,space):
        j = self._board._boardsize-1
        for i in range(space + 1):
            if(self._board._board[i][j] != self._mycolor):
                return False
            j = j - 1
        return True

    #Regarde si il existe un bloc de 4x4 colé au coin "where"
    def check44(self,where):
        if(where == "topleft"):
            for i in range(4):
                for j in range(4):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where == "topright"):
            for i in range(4):
                for j in range(self._board._boardsize-4,self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where == "botleft"):
            for i in range(self._board._boardsize-4,self._board._boardsize):
                for j in range(4):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where == "botright"):
            for i in range(self._board._boardsize-4,self._board._boardsize):
                for j in range(self._board._boardsize-4,self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True

    #Regarde si il existe un bloc de 6x3 collé au coin "where"
    def check63(self,where):
        if(where=="topleft"):
            for i in range(3):
                for j in range(6):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="topright"):
            for i in range(3):
                for j in range(self._board._boardsize - 6, self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="botleft"):
            for i in range(self._board._boardsize - 3, self._board._boardsize):
                for j in range(7):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="botright"):
            for i in range(self._board._boardsize - 3,self._board._boardsize):
                for j in range(self._board._boardsize - 6, self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True

    #Regarde si il existe un bloc de 3x6 collé au coin "where"
    def check36(self,where):
        if(where=="topleft"):
            for i in range(6):
                for j in range(3):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="topright"):
            for i in range(self._board._boardsize - 6, self._board._boardsize):
                for j in range(3):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="botleft"):
            for i in range(7):
                for j in range(self._board._boardsize - 3, self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True
        if(where=="botright"):
            for i in range(self._board._boardsize - 6, self._board._boardsize):
                for j in range(self._board._boardsize - 3,self._board._boardsize):
                    if(self._board._board[i][j] != self._mycolor):
                        return False
            return True


    #Regarde si il existe une ligne ou une colonne avec deux points adjacents et diagonaux aux coins de
    # la ligne ou la colonne en question :
    #[..........]
    #[..........]
    #[..........]
    #[..........]
    #[..........]
    #[..........]
    #[..........]
    #[..........]
    #[.x......x.]
    #[xxxxxxxxxx]
    def checkBoard(self,where):
        if(where == "top"):
            if(self.checkHorizontal(0)):
                if(self._board._board[1][1] != self._mycolor or self._board._board[1][self._board._boardsize - 2] != self._mycolor):
                    return False
                return True
        if(where=="left"):
            if(self.checkVertical(0)):
                if(self._board._board[1][1] != self._mycolor or self._board._board[self._board._boardsize-1][1] != self._mycolor):
                    return False
                return True
        if(where == "right"):
            if(self.checkVertical(self._board._boardsize-1)):
                if(self._board._board[1][self._board._boardsize - 2] != self._mycolor or self._board._board[self._board._boardsize - 2][self._board._boardsize - 2] != self._mycolor):
                    return False
                return True
        if(where == "bot"):
            if(self.checkHorizontal(self._board._boardsize-1)):
                if(self._board._board[self._board._boardsize - 2][1] != self._mycolor or self._board._board[self._board._boardsize - 2][self._board._boardsize - 2] != self._mycolor):
                    return False
                return True

    #Heuristique utilisée en milieu de partie
    def heuristique(self):
        res = 0
        #Si on peut gagner directement alors on renvoie une énorme valeur pour faire le coup en question
        if(self._board.is_game_over()):
            if ((self._mycolor == self._board._WHITE)and ((self._board._nbWHITE - self._board._nbBLACK)>0)):
                return 1000000
            elif((self._board._nbBLACK - self._board._nbWHITE) > 0):
                return 1000000

        #On calcule la valeur de la grille actuelle.
        #Le coin vaut 4000
        #Les cases à cotés des coins valent 200 si l'adversaire ne peut pas prendre le coin le coup d'après, -10000 sinon
        #Les cases adjacentes et diagonales aux coins valent -10000
        for i in range(self._board._boardsize) :
            for j in range(self._board._boardsize) :
                if self._board._board[i][j] == self._mycolor :
                    middle = int(self._board._boardsize / 2)
                    if (i == 0 or i == self._board._boardsize - 1) and (j == 0 or j == self._board._boardsize - 1):
                        res = res + 4000
                    if(i==0 and j==1):
                        if(self._board.is_valid_move(self._opponent,0,0)):
                            res = res - 10000
                        elif (self._board._board[0][0] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i==0 and j == self._board._boardsize-2):
                        if(self._board.is_valid_move(self._opponent,0,9)):
                            res = res - 10000
                        elif (self._board._board[0][9] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i==self._board._boardsize-1 and j == 1):
                        if(self._board.is_valid_move(self._opponent,9,0)):
                            res = res - 10000
                        elif (self._board._board[9][0] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i == self._board._boardsize-1 and j == self._board._boardsize-2):
                        if(self._board.is_valid_move(self._opponent,9,9)):
                            res = res - 10000
                        elif (self._board._board[9][9] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i == self._board._boardsize-2 and j == 0):
                        if(self._board.is_valid_move(self._opponent,9,0)):
                            res = res - 10000
                        elif (self._board._board[9][0] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i == 1 and j == self._board._boardsize-1):
                        if(self._board.is_valid_move(self._opponent,0,9)):
                            res = res - 10000
                        elif (self._board._board[0][9] == self._mycolor):
                            res = res + 200
                        else:
                            res = res +150
                    if(i == 1 and j == 0):
                        if(self._board.is_valid_move(self._opponent,0,0)):
                            res = res - 10000
                        elif (self._board._board[0][0] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if(i == self._board._boardsize-2 and j == self._board._boardsize-1):
                        if(self._board.is_valid_move(self._opponent,9,9)):
                            print("res :",res)
                            res = res - 10000
                        elif (self._board._board[9][9] == self._mycolor):
                            res = res + 200
                        else:
                            res = res + 150
                    if (i == 1 and j == 1) :
                        if(self._board.is_valid_move(self._opponent,0,0)):
                            res = res -10000
                        elif (self._board._board[0][0] == self._mycolor):
                            res = res + 200
                    if (i == 1 and j == self._board._boardsize - 2):
                        if(self._board.is_valid_move(self._opponent,0,9)):
                            res = res - 10000
                        elif (self._board._board[0][9] == self._mycolor):
                            res = res + 200
                    if (i == self._board._boardsize - 2 and j == 1) :
                        if(self._board.is_valid_move(self._opponent,9,0)):
                            res = res - 10000
                        elif (self._board._board[9][0] == self._mycolor):
                            res = res + 200
                    if (i == self._board._boardsize - 2 and j == self._board._boardsize - 2):
                        if(self._board.is_valid_move(self._opponent,9,9)):
                            res = res - 10000
                        elif (self._board._board[9][9] == self._mycolor):
                            res = res + 200
                    #Les cases sur les bords autres que les coins et que les cases à 1 de distance des coins valent 250
                    if((i == 0 or i == self._board._boardsize-1) and (j==2 or j == self._board._boardsize-3)) or ((i == 2 or i == self._board._boardsize-3) and (j == 0 or j == self._board._boardsize-1)):
                        res = res + 250
                    if((i == 0 or i == self._board._boardsize-1) and (j==3 or j == self._board._boardsize-4)) or ((i == 3 or i == self._board._boardsize-4) and (j == 0 or j == self._board._boardsize-1)):
                        res = res + 250
                    if((i == 0 or i == self._board._boardsize-1) and (j==4 or j == self._board._boardsize-5)) or ((i == 4 or i == self._board._boardsize-5) and (j == 0 or j == self._board._boardsize-1)):
                        res = res + 250
                    #Les cases centrals valent 75
                    if ((i == middle - 1 or i == middle) and (j == middle - 1 or j == middle)):
                        res = res + 75
                    #Les cases au tour du centre valent 50 ou 15
                    if (((i == 3 or i == 6) and (j == 4 or j == 5)) or ((i == 4 or i == 5) and (j == 3 or j == 6))):
                        res = res + 50
                    if ((i == 3 or i == 6) and (j == 3 or j == 6)):
                        res = res + 15

        #Ici nous comptabilisons tout les patterns que nous avons. Les grandes diagonales valent chères car
        #elles englobent 2 coins
        #Les lignes et colonnes englobant 2 coins valent aussi chère
        for i in range(0,self._board._boardsize):
            if(self.checkHorizontal(i)):
                if(i == 0 or i == self._board._boardsize - 1):
                    res = res + 1000
                if(i == 2 or i == self._board._boardsize - 3):
                    res = res + 400
                if(i == 3 or i == self._board._boardsize - 4):
                    res = res + 400
                if(i == 4 or i == self._board._boardsize - 5):
                    res = res + 400
            if(self.checkVertical(i)):
                if(i == 0 or i == self._board._boardsize - 1):
                    res = res + 1000
                if(i == 2 or i == self._board._boardsize - 3):
                    res = res + 400
                if(i == 3 or i == self._board._boardsize - 4):
                    res = res + 400
                if(i == 4 or i == self._board._boardsize - 5):
                    res = res + 400

        for i in range(3,self._board._boardsize):
            if(self.checkDiagonalBotLeft(i)):
                if(i == self._board._boardsize-1):
                    res = res + 1000
                if(i == self._board._boardsize-3):
                    res = res + 400
                if(i == self._board._boardsize-4):
                    res = res + 400
                if(i == self._board._boardsize-5):
                    res = res + 400
                if(i == self._board._boardsize-6):
                    res = res + 400
            if(self.checkDiagonalTopLeft(i)):
                if(i == self._board._boardsize-3):
                    res = res + 400
                if(i == self._board._boardsize-4):
                    res = res + 400
                if(i == self._board._boardsize-5):
                    res = res + 400
                if(i == self._board._boardsize-6):
                    res = res + 400
            if(self.checkDiagonalBotRight(i)):
                if(i == self._board._boardsize-1):
                    res = res + 1000
                if(i == self._board._boardsize-3):
                    res = res + 400
                if(i == self._board._boardsize-4):
                    res = res + 400
                if(i == self._board._boardsize-5):
                    res = res + 400
                if(i == self._board._boardsize-6):
                    res = res + 400
            if(self.checkDiagonalTopRight(i)):
                if(i == self._board._boardsize-3):
                    res = res + 400
                if(i == self._board._boardsize-4):
                    res = res + 400
                if(i == self._board._boardsize-5):
                    res = res + 400
                if(i == self._board._boardsize-6):
                    res = res + 400

        if(self.checkBoard("top")):
            res = res + 2000
        if(self.checkBoard("right")):
            res = res + 2000
        if(self.checkBoard("left")):
            res = res + 2000
        if(self.checkBoard("bot")):
            res = res + 2000

        if(self.check44("topright")):
            res = res + 2000
        if(self.check44("topleft")):
            res = res + 2000
        if(self.check44("botright")):
            res = res + 2000
        if(self.check44("botleft")):
            res = res + 2000

        if(self.check63("topleft")):
            res = res + 1000
        if(self.check63("topright")):
            res = res + 1000
        if(self.check63("botleft")):
            res = res + 1000
        if(self.check63("botright")):
            res = res + 1000

        if(self.check36("topleft")):
            res = res + 1000
        if(self.check36("topright")):
            res = res + 1000
        if(self.check36("botleft")):
            res = res + 1000
        if(self.check36("botright")):
            res = res + 1000

        #On calcule la mobilité que notre adversaire aura après ce coups
        mobility = self.mobility()
        if mobility == 0 :
            mobility = 10000

        if(self._mycolor == self._board._BLACK):
            return res + 3*mobility
        else:
            return res + 2*mobility

    #Heuristique de fin de partie
    def lastHeuristique(self):
        #On renvoie le nombre de pièces que l'on a à la fin de la partie pour choisir le plus gros nombre.
        if(self._mycolor == self._board._BLACK):
            return self._board._nbBLACK
        return self._board._nbWHITE

    #Calcule la mobilité grâce au tableau ci-dessous
    def mobility(self):
        mob = [[2000,-250,75,50,50,50,50,75,-250,2000],
               [-250,-250,1,1,1,1,1,1,-250,-250],
               [75,1,1,1,1,1,1,1,1,75],
               [50,1,1,10,15,15,10,1,1,50],
               [50,1,1,15,55,55,15,1,1,50],
               [50,1,1,15,55,55,15,1,1,50],
               [50,1,1,10,15,15,10,1,1,50],
               [75,1,1,1,1,1,1,1,1,75],
               [-250,-250,1,1,1,1,1,1,-250,-250],
               [2000,-250,75,50,50,50,50,75,-250,2000]]
        mobility = 0
        if(self._mycolor == self._board._WHITE):
            self._board._nextPlayer=self._board._BLACK
        else :
            self._board._nextPlayer=self._board._WHITE
        for i in range(self._board._boardsize) :
            for j in range(self._board._boardsize) :
                if self._board.is_valid_move(self._opponent,i,j):
                    mobility = mobility - mob[j][i]
        #On veut la plus petite mobilité pour le forcer à faire des coups faibles.
        return mobility

    #Algorithme PVS/NegaScout
    def pvs(self,depth,alpha,beta,first,last):
        start = time.time()
        if (depth<=0) or not(self._board.at_least_one_legal_move(self._mycolor)):
            #On applique la bonne heuristique suivant le moment de la partie
            if(first==True):
                return self.firstHeuristique()
            if(last == True):
                return self.lastHeuristique()
            return self.heuristique()
        first_child = True
        for m in self._board.legal_moves():
            if first_child:
                first_child = False
                self._board.push(m)
                score = -self.pvs(depth-1,-beta,-alpha,first,last)
                self._board.pop()
            else :
                self._board.push(m)
                score = -self.pvs(depth-1,-alpha-1, -beta,first,last)
                self._board.pop()
                if alpha < score and score < beta :
                    self._board.push(m)
                    score = -self.pvs(depth-1,-beta,-score,first,last)
                    self._board.pop()
            alpha = max(alpha,score)
            if(alpha >= beta):
                break
            stop = time.time()
            #Dans une partie on a 96 coups maximum, donc 48 par joueur,
            #or on a 300 secondes pour jouer tout nos coups (300/48 = 6.2)
            #Si un coup dépasse 6 secondes on stop.
            if(stop-start>=6.2):
                return alpha
        return alpha
