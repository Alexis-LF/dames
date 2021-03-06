#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from asyncore import loop
from types import coroutine
from unittest import result
from commands.dames.classes.Plateau import Plateau
from commands.dames.classes.Pion import Pion
from datetime import datetime
from os import listdir,rename



class Jeu:
    """classe Jeu"""

    def __init__(self,fxAffiche,fxPrompt,msgContext = None, botContext = None):
        """initialisations :"""
        self.__msgContext = None
        self.__botContext = None
        if msgContext != None and botContext != None:
            self.__msgContext = msgContext
            self.__botContext = botContext
        self.__afficheExterne = fxAffiche
        self.__promptExterne = fxPrompt

        self.__nbTours = 0
        self.__nbToursSansMange = 0

        self.__nbToursMaxSansMange = 30

        self.__joueurCourant = 1
        self.__joueurAdverse = 2
        pion = Pion(1)
        self.__pionJoueurCourant = pion.affiche()
        pion.setJoueur(2)
        self.__pionJoueurAdverse = pion.affiche()
        self.tirageAuSort()
        self.__joueur1 = "joueur 1"
        self.__joueur2 = "joueur 2"

        self.__savesDir = "commands/dames_files/sauvegardes"
        self.__strDep1 = "Pion *à déplacer* de **joueur X**  :\n*exit pour arrêter la partie*"
        self.__strDep2 = "case(s) de *destination* de **joueur X** :\n*exit pour arrêter la partie*"

        self.__flagExitGame = "EXIT_GAME_FLAG"
        self.__motCleExitGame = "exit"

        # await self.affiche("Initialisation du plateau")
        self.__plateau = None

    async def affiche(self,msg):
        if self.__msgContext != None:
            await self.__afficheExterne(msg,self.__msgContext)
        else:
            self.__afficheExterne(msg)

    async def prompt(self,joueur : str = None):
        valueReceived = ""
        if self.__botContext != None:
            valueReceived = await self.__promptExterne(self.__botContext,joueur)
        else:
            valueReceived = self.__promptExterne(joueur)
        if valueReceived.lower().find(self.__motCleExitGame) != -1:
            return self.__flagExitGame
        return valueReceived
        

    def nouvellePartie(self,nomJ1 : str,nomJ2 : str):
        self.__joueur1 = nomJ1
        self.__joueur2 = nomJ2
        self.__plateau = Plateau()


    # on inverse le joueur courant initalement à 1 par défaut
    def tirageAuSort(self):
        if int(datetime.now().microsecond % 2) == 0 :
            self.__joueurSuivant__()


    async def chargementJeu(self) -> bool :
        line = str()
        plateauData : list[str] = list()
        parametres = dict()
        # l'utilisateur choisit la partie désirée
        fileName = await self.choixChargement()
        if fileName == self.__flagExitGame:
            return False
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
        await self.affiche("Partie restaurée")
        return True


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

    async def choixChargement(self) -> str:
        listSaves = listdir(self.__savesDir)
        aPrint = ""
        choix = 0
        while choix == 0:
            index = 0
            for saveName in listSaves:
                if saveName.find("Fini :") == 0:
                    listSaves.remove(saveName)
            aPrint += "Liste des sauvegardes:\n```"
            for saveName in listSaves:
                with open(f"{self.__savesDir}/{saveName}","r") as saveFic:
                    parametres = dict()
                    line = str()
                    while line.find("PLATEAU") == -1 :
                        line = saveFic.readline()
                        key, value = line.partition("=")[::2]
                        parametres[key.strip()] = value.strip()
                    aPrint += "{0}:\t{1} contre {2} enregistrée {3}à {4}\n".format(index+1,parametres['joueur1'],parametres['joueur2'],"automatiquement " if parametres['typeSauvegarde'] == "auto" else "", parametres['datetime'])
                    index +=1
                # self.affiche("\n")
            aPrint += f"```Total : {index} sauvegardes\n"
            aPrint += f"Choissez une sauvegarde :\n*exit pour quitter*"
            await self.affiche(aPrint)
            aPrint = ""
            choix = await self.prompt()
            if choix == self.__flagExitGame :
                return choix
            try:
                choix = int(choix)
                if (choix-1) > len(listSaves):
                    raise ValueError
            except ValueError:
                # print(f"DÉBUG :\n\tLe choix de partie vaut \"{choix}\"")
                choix = 0
            else:
                # print(f"choix n°{choix} de partie faite : chargement de {listSaves[choix-1]} ")
                pass
        return f"{listSaves[choix-1]}"

    def __joueurSuivant__(self):
        pion = Pion()
        if self.__joueurCourant == 1:
            pion.setJoueur(2)
            self.__pionJoueurCourant = pion.affiche()
            pion.setJoueur(1)
            self.__pionJoueurAdverse = pion.affiche()
            self.__joueurCourant = 2
            self.__joueurAdverse = 1
        else:
            pion.setJoueur(1)
            self.__pionJoueurCourant = pion.affiche()
            pion.setJoueur(2)
            self.__pionJoueurAdverse = pion.affiche()            
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

    async def commenceJeu(self):
        finPartie = 0
        messages = str()
        while(finPartie == 0):
            nbManges , messages = await self.__tour__(messages)
            # vérification si le jeu est coupé
            if messages.find(self.__flagExitGame) != -1 :
                # pour assurer de conserver le bon joueur à la reprise
                self.__joueurSuivant__()
                self.sauvegardeJeu(f"Auto : {self.__joueur1} VS {self.__joueur2}.txt",auto=True)
                return
            self.sauvegardeJeu(f"Auto : {self.__joueur1} VS {self.__joueur2}.txt",auto=True)

            self.__nbTours += 1
            if nbManges > 0:
                self.__nbToursSansMange = 0
                self.__plateau.decrementePions(self.__joueurAdverse,nbManges)
            else:
                self.__nbToursSansMange += 1
            
            self.__joueurSuivant__()
            finPartie = self.__finPartie__()

        # fin du jeu
        rename(f"{self.__savesDir}/Auto : {self.__joueur1} VS {self.__joueur2}.txt",f"{self.__savesDir}/Fini : {self.__joueur1} VS {self.__joueur2}.txt")
        msg = f"{self.__plateau.affiche()}"
        msg += "fin du jeu : "
        if finPartie == 3:
            msg += f"Égalité ! la partie n'a pas progressé pendant {self.__nbToursMaxSansMange} tours"
        else:
            msg += f"Victoire de **{self.__nomJoueur__(self.__joueurCourant)}** !"
        await self.affiche(msg)
    
    async def __tour__(self,msgs):
        nbManges = 0
        depart = str()
        arrivee = str()
        listDplcmt = list()
        deplacementValide = 0 # false = 0
        while deplacementValide == 0:
            listDplcmt = []

            pionValide = False
            while pionValide == False:
                msgs = f"{self.__plateau.affiche()}\n" + msgs
                msgs += f"Au tour de **{self.__nomJoueur__(self.__joueurCourant)}** le joueur `{self.__pionJoueurCourant}`\n"
                # départ de tel pion
                msgs += f'{self.__strDep1.replace("joueur X",self.__nomJoueur__(self.__joueurCourant))}\n'
                # on envoie le texte à afficher
                await self.affiche(msgs)
                msgs = ""
                depart = await self.prompt(self.__nomJoueur__(self.__joueurCourant))
                # couper le jeu
                if depart == self.__flagExitGame:
                    return 0, depart

                pionValide = self.__plateau.pionAuJoueur(depart,self.__joueurCourant)
                if not pionValide :
                    msgs += f"La case {depart.upper()} ne contient pas un pion !\n"
            # récupération, sélection du pion et affichage
            pion = self.__plateau.getCase(depart).getPion()
            self.__plateau.getCase(depart).getPion().setSelect(True)
            
            msgs += f"{self.__plateau.affiche()}\n"
            msgs += f'{self.__strDep2.replace("joueur X",self.__nomJoueur__(self.__joueurCourant))}\n'
            # on envoie le texte 
            await self.affiche(msgs)
            msgs = ""            
            arrivee =  await self.prompt(self.__nomJoueur__(self.__joueurCourant))
            # couper le jeu
            if arrivee == self.__flagExitGame:
                return 0, arrivee


            # arrivé a un ou plusieurs pions pour un enchainement de bouffage de pions
            # on met la liste des cases où sera le pion dans un tab
            listDplcmt.append(depart)
            listDplcmt += arrivee.split(",")
            # print(arrivee)
            # print(listDplcmt)


            for i in range (0,len(listDplcmt)-1):
                deplacementValide, msg = self.__plateau.deplacementValide([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant, pion)
                msgs += f"{msg}\n"
                if deplacementValide == 1 and len(listDplcmt) > 2:
                    msgs += "Rafle autorisée qu'en mangeant plusieurs pions à la chaîne.\n"
                    deplacementValide = 0
                    break
            # on le déselectionne (avant de le déplacer ou en cas de mauvaise coordonnée)
            self.__plateau.getCase(listDplcmt[0]).getPion().setSelect(False)
        for i in range (0,len(listDplcmt)-1):
            nbManges += self.__plateau.deplace_pion([listDplcmt[i],listDplcmt[i+1]],self.__joueurCourant)
       
            
        return nbManges, msgs
