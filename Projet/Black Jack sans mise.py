import random
def paquet():
    couleurs =["carreau","pique","trefle","coeur"]
    valeurs =["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]
    paquet=[]
    for couleur in couleurs:
        for valeur in valeurs:
            paquet.append(valeur+" de "+couleur)
    return paquet

def valeurCarte(carte):
    valeurs =["as","2","3","4","5","6","7","8","9","10","valet","dame","roi"]
    valeurDico={}
    valeurCarte = carte.split(" ")[0]
    for e in range(0,len(valeurs)):
        valeurDico[valeurs[e]]=e+1
    if valeurCarte == "as":
        resultat = input("Quelle valeur pour l'as, 1 ou 11 ?")
        while resultat!="1" and resultat!="11":
            resultat = input("Quelle valeur pour l'as, 1 ou 11 ?")
        return int(resultat)
    return valeurDico.get(valeurCarte)

def initPioche(n):
    pioche = []
    for e in range(0,n):
        pioche.extend(paquet())
    random.shuffle(pioche)
    return pioche

def piocheCarte(pioche,x=1):
    obtenu=[]
    for e in range(0,x):
        obtenu.append(pioche.pop(0))
    return obtenu

def initJoueurs(n):
    listeJoueurs=[]
    for joueur in range(0,n):
        nom = input("Nom du joueur n° "+ str(joueur+1)+ " ?\n")
        while nom in listeJoueurs:
            nom = input("Erreur Nom déjà pris, veuillez en prendre un autre. \nNom du joueur n° "+ str(joueur+1)+ " ?\n")
        listeJoueurs.append(nom)
    print()
    return listeJoueurs

def initScores(joueurs,v=0):
    score={}
    for joueur in joueurs:
        score[joueur]=v
    return score

def initVictoires(joueurs):
    victoires={}
    for joueur in joueurs:
        victoires[joueur]=0
    return victoires

def premierTour(joueurs,pioche):
    score = initScores(joueurs)
    for joueur in joueurs:
        print("Tour n° 1")
        print("Les deux premières cartes de "+ joueur +" sont: ")
        carteTire = piocheCarte(pioche,2)
        print(carteTire)
        for carte in carteTire:
            score[joueur] = score[joueur]+valeurCarte(carte)
        input("Appuyer sur Entrée")
        print()
    return score

def gagnant(scores):
    maxi=0
    for joueur in scores.keys():
        if scores.get(joueur)>=maxi and scores.get(joueur)<=21:
            maxi=scores.get(joueur)
            gagnant=joueur
            scoreG=scores[gagnant]
    if maxi==0:
        gagnant ="personne"
        scoreG=0
    return gagnant,scoreG

def continuer():
    continuer=input("Voulez vous continuer ? (oui/non) ")
    while continuer!="oui" and continuer!="non":
        continuer=input("Voulez vous continuer ? (oui/non) ")
    return continuer=="oui"

def tourJoueur(j,joueurs,tour,scores,pioche):
    if  score[j]<21 :
        print("Tour n° " + str(tour))
        print("A "+ j +" de jouer. Score : "+str(scores.get(j)))
        if continuer(): #check score avant continuer car si score false on ne chack pas continuer et ne demande pas a un joueur qui a perdu
            carteTire = piocheCarte(pioche)
            print(carteTire)
            for carte in carteTire:
                score[j] = score[j] + valeurCarte(carte)
            if score[j] > 21:
                joueurs.remove(j)
            print()
        else:
            joueurs.remove(j)
            print()
    else:
        joueurs.remove(j)
            
def tourComplet(joueurs,tour,scores,pioche):
    joueursCop = list(joueurs)
    for joueur in joueurs:
        tourJoueur(joueur,joueursCop,tour,scores,pioche)
    return joueursCop
    
def partieFinie(joueurs):
    return len(joueurs)==0

def partieComplete(joueurs,scores,pioche,victoires):
    tour = 2;
    while not partieFinie(joueurs):
        joueurs = tourComplet(joueurs,tour,scores,pioche)
        tour+=1
    gagnantPartie, scoreGagnant = gagnant(scores)
    print("Le gagnant est "+gagnantPartie+" avec "+str(scoreGagnant)+" ! ")
    if gagnantPartie != "personne":
        victoires[gagnantPartie] = victoires[gagnantPartie] + 1

print(" ____  _            _           _            _    ")
print("|  _ \| |          | |         | |          | |   ")
print("| |_) | | __ _  ___| | __      | | __ _  ___| | __")
print("|  _ <| |/ _` |/ __| |/ /  _   | |/ _` |/ __| |/ /")
print("| |_) | | (_| | (__|   <  | |__| | (_| | (__|   < ")
print("|____/|_|\__,_|\___|_|\_\  \____/ \__,_|\___|_|\_\ ")
print()
nbJoueurs = int(input("Combien de joueurs veulent jouer ? "))
joueurs = initJoueurs(nbJoueurs)
victoires=  initVictoires(joueurs)
nouvellePartie = "oui"
while nouvellePartie == "oui":
    pioche = initPioche(nbJoueurs)
    score = premierTour(joueurs,pioche)
    partieComplete(joueurs,score,pioche,victoires)
    print(victoires)
    nouvellePartie = input("Voulez vous refaire une partie ? (oui/non) \n")
    while nouvellePartie!="oui" and nouvellePartie!="non":
        nouvellePartie=input("Voulez vous refaire une partie ? (oui/non) \n")
    print("\n")
    
                                                   
