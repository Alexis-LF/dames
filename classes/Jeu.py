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
        self.__joueur1 = "joueur 1"
        self.__joueur2 = "joueur 2"

        self.__savesDir = "sauvegardes"

        self.__strDep1 = "Pion à déplacer de joueur X >"
        self.__strDep2 = "case(s) de destination de joueur X >"


        self.affiche("Initialisation du plateau")
        self.__plateau = None

    def affiche(self,msg):
        if self.__ctx_discord != None:
            loop = asyncio.get_event_loop()
            coroutine  = self.__affiche_externe(msg,self.__ctx_discord)
            loop.run_until_complete(coroutine)
        else:
            self.__affiche_externe(msg)

        

    def nouvellePartie(self,nomJ1 : str,nomJ2 : str):
        self.__joueur1 = nomJ1
        self.__joueur2 = nomJ2
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
        while line.find("PLATEAU") == -1 :
            line = fp.readline()
            key, value = line.partition("=")[::2]
            parametres[key.strip()] = value
        # on les applique
        self.__joueur1 = parametres["joueur1"].strip() or "joueur 1"
        self.__joueur2 = parametres["joueur2"].strip() or "joueur 2"
        self.__nbTours = int(parametres["nbTours"].strip()) or 0
        self.__nbToursSansMange = int(parametres["nbToursSansMange"].strip()) or 0
        self.__joueurCourant = int(parametres["joueurCourant"].strip()) or 1
        self.__joueurSuivant__()
        # on récupère le plateau
        for _ in range(0,10):
            plateauData.append(fp.readline())

        self.__plateau = Plateau(plateauData)
        self.affiche("Partie restaurée")


    def sauvegardeJeu(self,filename : str,auto : bool = False):
        fp = open(f"{self.__savesDir}/{filename}",'w')
        if auto :
            fp.write(f"typeSauvegarde = auto\n")
        else:
            fp.write(f"typeSauvegarde = manuel\n")
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
        a_print = ""
        choix = 0
        while choix == 0:
            index = 0
            self.affiche("Liste des sauvegardes")
            for saveName in listSaves:
                with open(f"{self.__savesDir}/{saveName}","r") as saveFic:
                    parametres = dict()
                    line = str()
                    while line.find("PLATEAU") == -1 :
                        line = saveFic.readline()
                        key, value = line.partition("=")[::2]
                        parametres[key.strip()] = value.strip()
                    a_print += "{0}:\t{1} contre {2} enregistrée {3}à {4}\n".format(index+1,parametres['joueur1'],parametres['joueur2'],"automatiquement " if parametres['typeSauvegarde'] == "auto" else "", parametres['datetime'])
                    index +=1
                # self.affiche("\n")
            a_print += f"Total : {index} sauvegardes"
            self.affiche(a_print)
            choix = int(input("choisissez une sauvegarde >"))
        return f"{listSaves[choix-1]}"

    def __joueurSuivant__(self):
        if self.__joueurCourant == 1:
            self.__joueurCourant = 2
            self.__joueurAdverse = 1
        else:
            self.__joueurCourant = 1
            self.__joueurAdverse = 2
    def __nomJoueur__(self, numero : int) -> str:
        if numero == 1:
            return self.__joueur1
        elif numero == 2:
            return self.__joueur2
        else:
            print("ERREUR INTERNE : dans Jeu.py/__nomJoueur__()")


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
        finPartie = 0
        messages = str()
        while(finPartie == 0):
            nbManges , messages = self.__tour__(messages)
            self.sauvegardeJeu(f"Auto : {self.__joueur1} VS {self.__joueur2}.txt",auto=True)
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
            self.affiche(f"Victoire de {self.__nomJoueur__(self.__joueurCourant)} !")

    
    def __tour__(self,msgs):
        nbManges = 0
        depart = str()
        arrivee = str()
        listDplcmt = list()
        deplacement_valide = 0 # false = 0
        while deplacement_valide == 0:
            listDplcmt = []
            self.__plateau.affiche()
            msgs += f"au tour de {self.__nomJoueur__(self.__joueurCourant)} le joueur {self.__joueurCourant}\n"
            self.affiche(msgs)
            msgs = ""
            pion_valide = False
            while pion_valide == False:
                # départ de tel pion
                depart = input(self.__strDep1.replace("joueur X",self.__nomJoueur__(self.__joueurCourant)))
                pion_valide = self.__plateau.PionAuJoueur(depart,self.__joueurCourant)
            # récupération, sélection du pion et affichage
            pion = self.__plateau.getCase(depart).getPion()
            self.__plateau.getCase(depart).getPion().setSelect(True)
            self.__plateau.affiche()
            
            # arrivé à un ou plusieurs pions pour un enchainement de bouffage de pions
            arrivee = input(self.__strDep2.replace("joueur X",self.__nomJoueur__(self.__joueurCourant)))

            # on met la liste des cases où sera le pion dans un tab
            listDplcmt.append(depart)
            listDplcmt += arrivee.split(",")
            print(arrivee)
            print(listDplcmt)


            for i in range (0,len(listDplcmt)-1):
                self.affiche(f"dans Jeu.py/__tour()__, i de test de dplcmt valide : i = {i}. Test avec {listDplcmt[i]} et {listDplcmt[i+1]}")
                deplacement_valide, msg = self.__plateau.deplacementValide([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant, pion)
                msgs += f"{msg}\n"
                if deplacement_valide == 1 and len(listDplcmt) > 2:
                    msgs += "Rafle autorisée qu'en mangeant plusieurs pions à la chaîne.\n"
                    deplacement_valide = 0
                    break
            # on le déselectionne (avant de le déplacer ou en cas de mauvaise coordonnée)
            self.__plateau.getCase(listDplcmt[0]).getPion().setSelect(False)
        for i in range (0,len(listDplcmt)-1):
            nbManges += self.__plateau.deplace_pion([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant)
       
            
        return nbManges, msgs