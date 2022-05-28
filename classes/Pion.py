class Pion:
    """classe Pion"""

    def __init__(self,joueur : int):
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

    def setJoueur(self,joueur : int):
        self.__joueur = joueur

    def setDame(self,dame :bool):
        self.__dame = dame
    
    def affiche(self,sauvegarde=False):
        if self.__joueur == 2:
            if self.__dame:
                if sauvegarde:
                    print(self.__j2DameFic,end="")
                else:
                    print(self.__j2DameAff,end="")
            else:
                if sauvegarde:
                    print(self.__j2PionFic,end="")
                else:
                    print(self.__j2PionAff,end="")
        else:
            if self.__dame:
                if sauvegarde:
                    print(self.__j1DameFic,end="")
                else:
                    print(self.__j1DameFic,end="")
            else:
                if sauvegarde:
                    print(self.__j1PionFic,end="")
                else:                    
                    print(self.__j1PionFic,end="")