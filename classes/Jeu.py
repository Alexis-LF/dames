#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from asyncore import loop
from types import coroutine
from unittest import result
from classes.Plateau import Plateau
from datetime import datetime
from os import listdir
import asyncio
import nest_asyncio



class Jeu:
    """classe Jeu"""

    def __init__(self,fx_affiche,ctx_discord = None):
        """initialisations :"""
        if ctx_discord != None:
            nest_asyncio.apply()
        self.__affiche_externe = fx_affiche
        self.__ctx_discord = ctx_discord

        self.__nbTours = 0
        self.__nbToursSansMange = 0

        self.__nbToursMaxSansMange = 30

        self.__joueurCourant = 1
        self.__joueurAdverse = 2
        self.tirageAuSort()
        self.__joueur1 = "Mael"
        self.__joueur2 = "Alexis"

        self.__savesDir = "sauvegardes"

        self.__strDep1 = "Pion à déplacer du joueur X >"
        self.__strDep2 = "déplacement du PION du joueur X >"


        self.affiche("Initialisation du plateau")
        self.__plateau = None

    def affiche(self,msg):
        if self.__ctx_discord != None:
            loop = asyncio.get_event_loop()
            coroutine  = self.__affiche_externe(msg,self.__ctx_discord)
            loop.run_until_complete(coroutine)
        else:
            self.__affiche_externe(msg)

        

    def nouvellePartie(self):
        self.__plateau = Plateau()

    # on inverse le joueur courant initalement à 1 par défaut
    def tirageAuSort(self):
        if int(datetime.now().microsecond % 2) == 0 :
            self.__joueurSuivant__()

    def chargementJeu(self):
        line = str()
        plateauData : list[str] = list()
        parametres = dict()
        # l'utilisateur choisit la partie désirée
        fileName = self.choixChargement()
        # ouverture de la sauvegarde choisie
        fp = open(f"{self.__savesDir}/{fileName}",'r')
        # on récupère les infos de la partie
        while line.find("PLATEAU") != -1 :
            line = fp.readline()
            key, value = line.partition("=")[::2]
            parametres[key.strip()] = value
        # on les applique
        self.__joueur1 = parametres["joueur1"] or "joueur 1"
        self.__joueur2 = parametres["joueur2"] or "joueur 2"
        self.__nbTours = int(parametres["nbTours"]) or 0
        self.__nbToursSansMange = int(parametres["nbToursSansMange"]) or 0
        self.__joueurCourant = int(parametres["joueurCourant"]) or 1
        self.__joueurAdverse = 1 if self.__joueurCourant == 2 else 2
        # on récupère le plateau
        for _ in range(0,10):
            plateauData.append(fp.readline())

        self.__plateau = Plateau(plateauData)
        self.affiche("Partie restaurée")


    def sauvegardeJeu(self,filename):
        fp = open(f"{self.__savesDir}/{filename}",'w')
        fp.write(f"joueur1 = {self.__joueur1}\n")
        fp.write(f"joueur2 = {self.__joueur2}\n")
        fp.write(f"datetime = {datetime.now().strftime('%H:%M:%S le %A %d %B %Y')}\n")
        fp.write(f"nbTours = {self.__nbTours}\n")
        fp.write(f"nbToursSansMange = {self.__nbToursSansMange}\n")
        fp.write(f"joueurCourant = {self.__joueurCourant}\n")
        fp.write(f"PLATEAU\n")
        fp.write(self.__plateau.sauvegarde())
        fp.close()

    def choixChargement(self) -> str:
        listSaves = listdir(self.__savesDir)
        self.affiche(listSaves)
        choix = 0
        while choix == 0:
            index = 0
            self.affiche("Liste des sauvegardes")
            for saveName in listSaves:
                with open(f"{self.__savesDir}/{saveName}","r") as saveFic:
                    
                    self.affiche(f"{index+1}:\t{saveFic.readline()[:-1]} contre {saveFic.readline()[:-1]} : {saveFic.readline()[:-1]}")
                    index +=1
                # self.affiche("\n")
            self.affiche(f"Total : {index} sauvegardes")
            choix = int(input("choisissez une sauvegarde >"))
        return f"{listSaves[choix-1]}"

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

    def commenceJeu(self):
        datePartie = datetime.now().strftime('%H:%M:%S le %A %d %B %Y')
        finPartie = 0
        while(finPartie == 0):
            nbManges = self.__tour__()
            self.sauvegardeJeu(f"Auto : {datePartie}")
            self.__nbTours += 1
            if nbManges > 0:
                self.__nbToursSansMange = 0
                self.__plateau.decrementePions(self.__joueurAdverse,nbManges)
            else:
                self.__nbToursSansMange += 1
            
            self.__joueurSuivant__()
            finPartie = self.__finPartie__()
        
        self.affiche("fin du jeu !")
        if finPartie == 3:
            self.affiche(f"Égalité ! la partie n'a pas progressé pendant {self.__nbToursMaxSansMange} tours")
        else:
            self.affiche(f"Victoire du joueur {finPartie} !")

    
    def __tour__(self) -> int:
        nbManges = 0
        depart = str()
        arrivee = str()
        listDplcmt = list()
        self.__plateau.affiche()
        self.affiche(f"au tour du joueur {self.__joueurCourant}")
        deplacement_valide = False
        while deplacement_valide == False:
            pion_valide = False
            while pion_valide == False:
                # départ de tel pion
                depart = input(self.__strDep1.replace("joueur X",f"joueur {self.__joueurCourant}"))
                pion_valide = self.__plateau.PionAuJoueur(depart,self.__joueurCourant)
            # récupération, sélection du pion et affichage
            pion = self.__plateau.getCase(depart).getPion()
            self.__plateau.getCase(depart).getPion().setSelect(True)
            self.__plateau.affiche()
            
            # arrivé à un ou plusieurs pions pour un enchainement de bouffage de pions
            arrivee = input(self.__strDep2.replace("joueur X",f"joueur {self.__joueurCourant}"))

            # on met la liste des cases où sera le pion dans un tab
            listDplcmt.append(depart)
            listDplcmt += arrivee.split(",")


            for i in range (0,len(listDplcmt)-1):
                deplacement_valide = self.__plateau.deplacementValide([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant, pion)
        
            for i in range (0,len(listDplcmt)-1):
                nbManges += self.__plateau.deplace_pion([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant)
            # on le déselectionne
            self.__plateau.getCase(listDplcmt[i+1]).getPion().setSelect(False)
            
        return nbManges