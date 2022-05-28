class Pion:
    """classe Pion"""

    def __init__(self,joueur : int = 0):
        """initialisations :"""        
        self.__dame = False
        self.__joueur = joueur

        self.__j2PionAff = "⚫"
        self.__j2PionFic = "y"
        self.__j2DameAff = "🖤"
        self.__j2DameFic = "Y"
        self.__j1PionAff = "⚪"
        self.__j1PionFic = "x"
        self.__j1DameAff = "🤍"
        self.__j1DameFic = "X"

    def estDame(self) -> bool:
        return self.__dame

    def getJoueur(self) -> int:
        return self.__joueur

    def getValSave(self,joueur : int, dame : bool = False):
        if joueur == 2:
            if dame:
                return self.__j2DameFic
            else:
                return self.__j2PionFic
        else:
            if dame:
                return self.__j1DameFic
            else:
                return self.__j1PionFic

    def setJoueur(self,joueur : int):
        self.__joueur = joueur

    def setDame(self,dame :bool):
        self.__dame = dame
    
    def affiche(self,sauvegarde=False) -> str:
        if self.__joueur == 2:
            if self.__dame:
                if sauvegarde:
                    return self.__j2DameFic 
                else:
                    return self.__j2DameAff 
            else:
                if sauvegarde:
                    return self.__j2PionFic 
                else:
                    return self.__j2PionAff 
        else:
            if self.__dame:
                if sauvegarde:
                    return self.__j1DameFic 
                else:
                    return self.__j1DameAff 
            else:
                if sauvegarde:
                    return self.__j1PionFic
                else:                    
                    return self.__j1PionAff 