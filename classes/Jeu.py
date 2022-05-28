#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from classes.Plateau import Plateau
from datetime import datetime
from os import listdir

class Jeu:
    """classe Jeu"""

    def __init__(self):
        """initialisations :"""
        self.__nbTours = 0
        self.__nbToursSansMange = 0

        self.__nbToursMaxSansMange = 30

        self.__joueurCourant = 1
        self.__joueurAdverse = 2
        self.__joueur1 = "Mael"
        self.__joueur2 = "Alexis"

        self.__savesDir = "sauvegardes"

        self.__strDep1 = "Pion à déplacer du joueur X >"
        self.__strDep2 = "déplacement du PION du joueur X >"


        print("Initialisation du plateau")
        self.__plateau = None

    def nouvellePartie(self):
        self.__plateau = Plateau()

    def chargementJeu(self):
        fileName = self.choixChargement()
        self.__plateau = Plateau(fileName)
        print("ok")

    def __joueurSuivant__(self):
        if self.__joueurCourant == 1:
            self.__joueurCourant = 2
            self.__joueurAdverse = 1
        else:
            self.__joueurCourant = 1
            self.__joueurAdverse = 2


    def __finPartie__(self) -> int:
        """
            0 : partie pas finie
            1 : victoire du joueur 1
            2 : victoire du joueur 2
            3 : ex-æquo
        """
        if self.__plateau.getNbPions(1) == 0:
            return 2
        elif self.__plateau.getNbPions(2) == 0:
            return 1
        elif self.__nbToursSansMange >= self.__nbToursMaxSansMange :
            return 3
        else:
            return 0

    def sauvegardeJeu(self,filename):
        fp = open(f"{self.__savesDir}/{filename}",'w')
        fp.write(f"{self.__joueur1}\n")
        fp.write(f"{self.__joueur2}\n")
        fp.write(f"{datetime.now().strftime('%H:%M:%S le %A %d %B %Y')}\n")
        fp.write(self.__plateau.sauvegarde())

    def choixChargement(self) -> str:
        listSaves = listdir(self.__savesDir)
        print(listSaves)
        choix = 0
        while choix == 0:
            index = 0
            print("Liste des sauvegardes")
            for saveName in listSaves:
                with open(f"{self.__savesDir}/{saveName}","r") as saveFic:
                    
                    print(f"{index+1}:\t{saveFic.readline()[:-1]} contre {saveFic.readline()[:-1]} : {saveFic.readline()[:-1]}")
                    index +=1
                # print("\n")
            print(f"Total : {index} sauvegardes")
            choix = int(input("choisissez une sauvegarde >"))
        return f"{self.__savesDir}/{listSaves[choix-1]}"

    def commenceJeu(self):
        finPartie = 0
        while(finPartie == 0):
            nbManges = self.__tour__()
            self.__nbTours += 1
            if nbManges > 0:
                self.__nbToursSansMange = 0
                self.__plateau.decrementePions(self.__joueurAdverse,nbManges)
            else:
                self.__nbToursSansMange += 1
            
            self.__joueurSuivant__()
            finPartie = self.__finPartie__()
        
        print("fin du jeu !")
        if finPartie == 3:
            print(f"Égalité ! la partie n'a pas progressé pendant {self.__nbToursMaxSansMange} tours")
        else:
            print(f"Victoire du joueur {finPartie} !")

    
    def __tour__(self) -> int:
        nbManges = 0
        coords1 = str()
        coords2 = str()
        self.__plateau.affiche()
        print(f"au tour du joueur {self.__joueurCourant}")
        deplacement_valide = False
        while deplacement_valide == False:
            pion_valide = False
            while pion_valide == False:
                coords1 = input(self.__strDep1.replace("joueur X",f"joueur {self.__joueurCourant}"))
                pion_valide = self.__plateau.PionAuJoueur(coords1,self.__joueurCourant)

            coords2 = input(self.__strDep2.replace("joueur X",f"joueur {self.__joueurCourant}"))
            deplacement_valide = self.__plateau.deplacementValide([coords1,coords2],self.__joueurCourant)
        nbManges = self.__plateau.deplace_pion([coords1,coords2],self.__joueurCourant)
        return nbManges