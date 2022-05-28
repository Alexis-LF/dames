from fileinput import filename
from time import sleep
from typing import Tuple
from classes.Pion import Pion
from classes.Case import Case

class Plateau:
    """classe Plateau"""


    def __init__(self,fileName = False) :
        self.__lignes = "ABCDEFGHIJ"
        self.__nbPionsJ1 = 20
        self.__nbPionsJ2 = 20

        self.__cases = self.__initCases__()
        if fileName :
            self.__initPionsSauvegarde__(fileName)
        else:
            self.__initPions__()
    

    def __initCases__(self) -> list[Case]:
        cases = []
        case_claire = True 
        for ligne in self.__lignes:
            for col in range(1,11):
                cases.append(Case(ligne,col,case_claire))
                case_claire = not case_claire
            case_claire = not case_claire
        return cases

    def __initPions__(self):
        # on retire tous les pions s'il y en avait
        for case in self.__cases:
            case.supprPion()
        
        # placement des pions foncés du joueur 2
        i = 0
        nbPions = 0
        while(nbPions<self.__nbPionsJ2):
            if not self.__cases[i].estClaire():
                self.__cases[i].setPion(Pion(2))
                nbPions+=1
            i+=1
        # placement des pions foncés du joueur 1
        i = 0
        nbPions = 0
        length = len(self.__cases) -1
        while(nbPions<self.__nbPionsJ1):
            if not self.__cases[length-i].estClaire():
                self.__cases[length-i].setPion(Pion(1))
                nbPions+=1
            i+=1
    
    def __initPionsSauvegarde__(self,fileName):
        saveFic = open(filename,"r")
        # on s'en fiche des 3 première lignes
        for i in range(0,3):
            _ = saveFic.readline()
        # on initialise le nb de pion
        self.__nbPionsJ1 = 0
        self.__nbPionsJ2 = 0
        # on lit les 10 lignes du plateau
        for i in range(0,10):
            line = saveFic.readline()
            # on lit les 10 cases de la ligne
            for j in range(0,10):
                if line[i] not in ".\n":
                    # cette case contient un pion
                    if self.__cases[(i*10)+j].setPionSave(line[j]) == 1:
                        self.__nbPionsJ1 += 1
                    else:
                        self.__nbPionsJ1 += 2
        saveFic.close()

    
    def getNbPions(self,joueur : int) -> int:
        if joueur == 1 :
            return self.__nbPionsJ1 
        elif joueur == 2 :
            return self.__nbPionsJ2
        else:
            print("ERREUR INTERNE dans getNbPions")

    def decrementePions(self,joueur : int, nbPions : int):
        if joueur == 1:
            self.__nbPionsJ1 -= nbPions
        elif joueur == 2:
            self.__nbPionsJ2 -= nbPions
        else:
            print("ERREUR INTERNE dans decrementePions")

    def affiche(self):
        nb_cases = 0
        print("   1 2 3 4 5 6 7 8 9 10")
        for case in self.__cases:
            nb_cases+=1
            if ((nb_cases-1)%10) == 0:
                print(self.__lignes[(int)(nb_cases/10)],end=" ")            
            print(case.affiche(),end="")
            if (nb_cases%10) == 0:
                print("",end="\n")
        self.affichePionsRestants()
    
    def sauvegarde(self) -> str:
        lignes = ""
        nb_cases = 0
        for case in self.__cases:
            nb_cases+=1
            lignes += case.affiche(sauvegarde=True)
            if (nb_cases%10) == 0:
                lignes += "\n"
        return lignes

        
    def affichePionsRestants(self):
        pionAffiche = Pion(1)    
        print("\t",end="")
        print(pionAffiche.affiche(),end="")
        print(f" = {self.__nbPionsJ1}")
        print("\t",end="")
        pionAffiche.setJoueur(2)
        print(pionAffiche.affiche(),end="")
        print(f" = {self.__nbPionsJ2}")

    def afficheLigne(self,ligne : str):
        for case in self.__cases:
            if case.getPosX() == ligne:
                case.affiche()
        print("",end="\n")

    def afficheCol(self, col : int):
        for case in self.__cases:
            if case.getPosY() == col:
                case.affiche()

    def getCaseId(self,coords : str) -> int:
        if len(coords) < 2:
            return False
        # récupération de la ligne
        ligne = coords[0].upper()
        # récupération de la colonne
        col = coords[1:]
        if col[:-1] == "\n" :
            col.remove[:-1]
        col = int(col)  
        # vérification que c'est bien dans le tableau
        if ligne not in self.__lignes:
            print(f"ligne {ligne} hors tableau")
            return False
        if col not in range(1,11):
            print(f"colonne {col} hors tableau")
            return False        
        # on détermine l'id par le n° de col/ligne
        numLigne = self.__lignes.find(ligne)
        return ((numLigne*10) + (col-1))

        

    def getCase(self,coords : str) -> Case:
        return self.__cases[self.getCaseId(coords)]


    def PionAuJoueur(self,coords : str, joueur : int) -> bool:
        case = self.getCase(coords)
        if case != False :
            return case.estAuJoueur(joueur)
        return False

    def getCoordsCasesTraversees(self,case1 : Case, case2 : Case) -> list[str]:
        # on récupère la distance entre les 2 cases : et si elle est bien en diagonale
        indexV1 = case1.getPosY()
        indexV2 = case2.getPosY()
        indexH1 = self.__lignes.find(case1.getPosX())
        indexH2 = self.__lignes.find(case2.getPosX())
        nb_cases = abs(indexV1 - indexV2)
        if abs(indexH1-indexH2) != nb_cases:
            print("Le déplacement n'est pas en diagonale")
            return []
        # on génère les coordonnées des cases à récup
        sensH = indexH2 > indexH1
        sensV = case2.getPosY() > case1.getPosY()
        coords = []
        for i in range(0,nb_cases+1):
            coord = ""
            if sensH:
                coord = f"{self.__lignes[indexH1+i]}"
            else:
                coord = f"{self.__lignes[indexH1-i]}"
            if sensV:
                coord += f"{indexV1+i}"
            else:
                coord += f"{indexV1-i}"
            coords.append(coord)
        return coords

    def getIdCasesTraversees(self,case1 : Case, case2 : Case) -> list[int]:
        ids = []
        coords = self.getCoordsCasesTraversees(case1, case2)
        for coord in coords:
            ids.append(self.getCaseId(coord))
        return ids


    def getCasesTraversees(self,case1 : Case, case2 : Case) -> list[Case]:
        cases = []
        coords = self.getCoordsCasesTraversees(case1, case2)
        for coord in coords:
            cases.append(self.getCase(coord))
        return cases


    def deplacementValide(self,coords : list[str], joueur : int) -> bool:
        """
        TODO : vérifier le déplacement en arrière pour un simple pion
        """
        # vérification si la case existe et est vide
        cases = []
        for i in range(0,2):
            cases.append(self.getCase(coords[i]))
            if cases[i] == False :
                print("case marquée non valide")
                return False
        if cases[1].estVide() == False:
            print("case marquée non vide")
            return False            
        # vérification de la distance
        cases = self.getCasesTraversees(cases[0],cases[1])

        if len(cases) <= 1:
            return False

        # on vérifie s'il y a un pion à soi-même sur le chemin (sans compter la 1re et dernière case)
        for i in range(1,len(cases)-1):
            if not(cases[i].estVide()):
                # print(f"case {cases[i].getPosX()}{cases[i].getPosY()} pas vide")
                if cases[i].getPion().getJoueur() == joueur:
                    print("Un pion à soi-même est sur le chemin")
                    return False

        # dame ou simple pion ?
        if cases[0].getPion().estDame()  :
            print("c'est une dame")
            return True
        else:
            if len(cases) > 3:
                print("un pion ne peut pas se déplacer aussi loin")
            elif (len(cases)) == 3:
                if not cases[1].estVide():
                    print(f"il y a un pion du joueur {cases[1].getPion().getJoueur()} qui va se faire manger")
                    return True
                else:
                    print(f"un pion peut se déplacer de 2 cases que s'il y a un pion adversaire entre les 2")
                    return False
            elif len(cases) == 2:
                versLeHaut = cases[0].estPlusBas(cases[len(cases)-1])
                if (joueur == 1 and not versLeHaut) or ( joueur == 2 and versLeHaut):
                    print("déplacement dans le sens contraire de la marche")
                    return False
                else:
                    print("déplacement d'une case")
                    return True
        print("ERREUR INTERNE : deplacementValide() n'a pas déterminé la possibilité de se déplacer")
        return False

    def boutDuPlateau(self,joueur: int, case_id: int) -> bool:
        if joueur == 1:
            if self.__cases[case_id].getPosX == 'A':
                return True
        if joueur == 2:
            if self.__cases[case_id].getPosX == 'J':
                return True
        return False

    def deplace_pion(self,coords : list[str], joueur : int) -> int:
        # on récupère les identifiants des cases, pour pouvoir les modifier ensuite
        case1 = self.getCase(coords[0])
        case2 = self.getCase(coords[1])
        ids = self.getIdCasesTraversees(case1,case2)
        # on supprime tous les pions sur le chemin (sans compter la case initiale et finale)
        pionsManges = 0
        for i in range(1,len(ids)-1):
            pionsManges += self.__cases[ids[i]].supprPion()
        # on déplace le pion à la zone d'arrivée
        pionCourant = self.__cases[ids[0]].recupPion()
        self.__cases[ids[-1]].setPion(pionCourant)

        # on le transforme en dame si nécessaire
        if not self.__cases[ids[-1]].getPion().estDame():
            if self.boutDuPlateau(joueur,ids[-1]):
                self.__cases[ids[-1]].getPion().setDame(True)

        return pionsManges