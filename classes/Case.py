from classes.Pion import Pion

class Case:
    """classe Case"""

    def __init__(self,posX : str,posY : int, claire : bool):
        """initialisations :"""
        
        self.__posX = posX
        self.__posY = posY
        self.__pion = None
        self.__claire = claire
        
        self.__CaseClaireAff = "🟧"
        self.__CaseFonceeAff = "🟫"
        self.__CaseFic = "."

        
    def estVide(self) -> bool:
        if self.__pion != None:
            return False
        return True

    def estAuJoueur(self,joueur :int) -> bool:
        if self.__pion != None:
            if self.__pion.getJoueur() == joueur:
                return True
        return False

    def estClaire(self) -> bool:
        return self.__claire

    def supprPion(self) -> int:
        # on supprime le pion de la variable,
        # et on renvoie le nb de pions supprimés
        if self.__pion != None:
            self.__pion = None
            return 1
        return 0


    def recupPion(self) -> Pion:
        pion = self.__pion
        self.supprPion()
        return pion
        
    def setPion(self, pion : Pion):
        self.__pion = pion

    def getPion(self) -> Pion:
        if self.__pion == None:
            return False
        return self.__pion

    def getPosX(self) -> str:
        return self.__posX

    def getPosY(self) -> int:
        return self.__posY

    def estPlusBas(self,case2) -> bool :
        if  self.getPosX() < case2.getPosX() :
            return False
        return True

    def affiche(self,sauvegarde=False):
        if self.__pion == None:
            if sauvegarde:
                print(self.__CaseFic,end="")
            else:
                if self.__claire :
                    print(self.__CaseClaireAff,end="")
                else:
                    print(self.__CaseFonceeAff,end="")
        else:
            if sauvegarde:
                self.__pion.affiche(sauvegarde=True)
            else:
                self.__pion.affiche()