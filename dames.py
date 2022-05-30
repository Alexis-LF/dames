#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from classes.Jeu import Jeu
from datetime import datetime
# main file
"""
PLATEAU :
  1 2 3 4  5 6 7 8 9 10 
A 🟧🟫🟧🟫🟧🟫🟧🟫🟧🟫
B 🟫🟧🟫🟧🟫🟧🟫🟧🟫🟧
C 🟧🟫🟧🟫🟧🟫🟧🟫🟧🟫
D 🟫🟧🟫🟧🟫🟧🟫🟧🟫🟧
E 🟧🟫🟧🟫🟧🟫🟧🟫🟧🟫
F 🟫🟧🟫🟧🟫🟧🟫🟧🟫🟧
G 🟧🟫🟧🟫🟧🟫🟧🟫🟧🟫
H 🟫🟧🟫🟧🟫🟧🟫🟧🟫🟧
I 🟧🟫🟧🟫🟧🟫🟧🟫🟧🟫
J 🟫🟧🟫🟧🟫🟧🟫🟧🟫🟧

Je veux la case A1 = ligne A (0*10) col 1 (0) = id 0
Je veux la case A10 = ligne A (0*10) col 10 (9) = id 9
Je veux la case B1 = ligne B (1*10) col 1 (0) = id 10

Je veux la case xy = ligne x (x*10) col y (y-1) = id x*10 + (y-1)

TODO:
     - faire les miams multiples
     - mettre en surbrillance le pion choisi
     - faire en sorte de sauvegarder / charger une partie => plus qu'à proposer un système de mots-clés

"""

if __name__ == "__main__":
    print("hello")
    jeu = Jeu()
    print("commencement du jeu de dames !")
    jeu.chargementJeu()
    jeu.commenceJeu()

    print("fin du programme")
