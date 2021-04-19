import random
import matplotlib.pyplot as plt
import tkinter
import os

def paquet():
    couleurs =["carreau","pique","trefle","coeur"]
    valeurs =["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
    paquet=[]
    for couleur in couleurs:
        for valeur in valeurs:
            paquet.append(valeur+" de "+couleur)
    return paquet

def valeurCarte(carte):
    valeurCarte = carte.split(" ")[0]
    if valeurCarte == "As":
        resultat = "1/11"
        return resultat
    if valeurCarte == "Valet" or valeurCarte == "Dame" or valeurCarte == "Roi":
        resultat = 10
    else:
        resultat = int(valeurCarte)
    return resultat

#fonction qui calcul le nouveau score est permet l'affichage des différentes possibilités quand un as est tiré pour choisir seul à la fin la meilleure possibilité
def calculScoreAuto(scores,carte):
    nouveauScores=[]
    for score in list(str(scores).split("/")):
        for valeur in str(valeurCarte(carte)).split("/"):
            if not (str(int(score)+int(valeur)) in nouveauScores) and int(score)+int(valeur) <= 21:
                nouveauScores.append(str(int(score)+int(valeur)))
    if len(nouveauScores)==0:
        return "22" #le joueur a perdu
    return "/".join(nouveauScores) #la valeur de retour est un string

#fonction qui choisit la meilleure possibilité et la retourne sous la forme d'un entier
def meilleurScore(scores,j):
    if "/" in list(str(scores[j])):
        return int(scores[j].split("/")[1])
    if scores[j]=="Black Jack":
        return 21
    else:
        return int(scores[j])

#on utilise une pioche commune de n paquet sinon il faudrait un dictionnaire dont la clé "nom du joueur" renvoie son paquet
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

def initCroupier(nom,listeCroupiers):
    probabilite = 0
    pourcentage = 0
    print("\n1 : aléatoire \n2 : Probabilité \n3 : Avantage et probabilté modulé selon le score \n4 : Joue tant qu'un joueur a mieux \n5 : Moyenne restante par carte du paquet \n6 : Tricheur")
    strat = int(input("Stratégie n° : "))
    if strat == 3 or strat == 2:
        probabilite = float(input("Quelle est la probabilité de piocher ?"))
    while not (int(strat) in list(range(1,7))):
        strat = int(input("Stratégie inexistante, veuillez changer : "))
        if strat == 3 or strat == 2:
            probabilite = float(input("Quelle est la probabilité de piocher ?"))
    print("\n1 : Pourcentage \n2 : Risque \n3 : Probabilité d'arriver à 21 \n4 : Avantage\n5 : Avantage Pourcentage \n6 : Avantage + Probabilité d'arriver à 21 \n7 : Combiné de tous les facteurs \n8 : Carte des autres")
    stratMise = int(input("Stratégie n° : "))
    if stratMise == 1 or stratMise ==5 or stratMise == 7 or stratMise == 8:
        pourcentage = float(input("Quelle est le pourcentage de la cagnotte à miser ?"))
    while not (int(stratMise) in list(range(1,9))):
        stratMise = int(input("Stratégie inexistante, veuillez changer : "))
        if stratMise == 1 or stratMise ==5:
            pourcentage = float(input("Quelle est le pourcentage de la cagnotte à miser ?"))
    listeCroupiers[nom]=[strat,stratMise,probabilite,pourcentage]
    return listeCroupiers

def initTable(n):
    listeJoueurs=[]
    listeCroupiers={}
    print("\n Initialisation du Croupier")
    initCroupiers = initCroupier("Croupier",listeCroupiers)
    for personne in range(0,n):
        nom = input("Nom du joueur n° "+ str(personne+1)+ " ?\n")
        isIA = continuer("Voulez vous que ce joueur soit une IA ?")
        if isIA:
            while nom in listeCroupiers or " " in list(nom):
                nom = input("Erreur Nom déjà pris ou il y a un espace dans le nom, veuillez en prendre un autre. \nNom du joueur n° "+ str(personne+1)+ " ?\n")
            listeCroupiers = initCroupier(nom,listeCroupiers)
        else:
            while nom in listeJoueurs or " " in list(nom):
                nom = input("Erreur Nom déjà pris ou il y a un espace dans le nom, veuillez en prendre un autre. \nNom du joueur n° "+ str(joueur+1)+ " ?\n")
            listeJoueurs.append(nom)
    return listeJoueurs,listeCroupiers

def initScores(joueurs,v="0"):
    score={}
    for joueur in joueurs:
        score[joueur]=v
    return score

def initCagnotte(joueurs):
    cagnotte={}
    for joueur in joueurs:
        cagnotte[joueur]=100
    return cagnotte

def continuer(question):
    rep = input(question + "(oui/non)")
    while rep != "non" and rep!= "oui":
        rep = input(question + "(oui/non)")
    return rep == "oui"

#Les différentes case où on distribue les cartes on leurs coordonnées stockés dans une liste
#où chaque élément est une liste avec comme premier élément coordonnée en x et une seconde valeur pour y
def afficherCarte(carte,numCarte,numJoueur,numJeu=0):
    coordonnees=[[630,80],[225,100],[315,250],[460,350],[640,385],[830,350],[970,250],[1060,100]]
    coordonnee=coordonnees[numJoueur]
    if carte=="vide":
        cartePNG = tkinter.PhotoImage(file="vide.png")
        setattr(canvas,"carte"+str(numJoueur)+str(numCarte)+str(numJeu),cartePNG) # équivalent à canvas."carte"+str(numJoueur)+str(numCarte)+str(numJeu) = cartePNG
        #mais permet de mettre un string variable après le canvas.
    else:
        valeur=carte[0]
        if valeur=="1":
            valeur="10"
        couleur = carte.split()[2]
        cartePNG = tkinter.PhotoImage(file=valeur+"_"+couleur+".png")
        canvas.create_image(coordonnee[0]+(numJeu*25), coordonnee[1]+(numCarte*30), image=cartePNG)
    setattr(canvas,"carte"+str(numJoueur)+str(numCarte)+str(numJeu),cartePNG)
    #garde en référence la carte pour ne pas la détruire comme une variable locale

def premierTour(joueurs,croupiers,pioche,cagnotte,mise,affichage,miseMessage):
    personnes = []
    personnes.extend(croupiers)
    personnes.extend(joueurs)
    scores = initScores(personnes)
    cagnotte["pot"]=0
    boutonClique = tkinter.BooleanVar()
    mise = {}
    for croupier in croupiers:
        print("Tour n° 1 " + croupier)
        if croupier == "Croupier":
            carteTire = piocheCarte(pioche,1)
            print(carteTire)
            afficherCarte(carteTire[0],1,list(scores.keys()).index(croupier))
            scores[croupier] = calculScoreAuto(scores[croupier],carteTire[0])
        else:
            carteTire = piocheCarte(pioche,2)
            print(carteTire)
            numCarte=1
            for carte in carteTire:
                afficherCarte(carteTire[numCarte-1],numCarte,list(scores.keys()).index(croupier))
                scores[croupier] = calculScoreAuto(scores[croupier],carteTire[numCarte-1])
                numCarte+=1
        mise[croupier]=miseCroupier(cagnotte,croupier,scores,croupiers,joueurs,miseMessage)
    for joueur in list(joueurs):
        print("Tour n° 1 " + joueur)
        miseBouton = tkinter.Button(fenetre,text="Miser",command = lambda: boutonClique.set(True))
        miseBouton.pack(side = tkinter.LEFT, padx=5, pady=5)
        numCarte=1
        carteTire = piocheCarte(pioche,2)
        print(carteTire)
        for carte in carteTire:
            afficherCarte(carte,numCarte,list(scores.keys()).index(joueur))
            scores[joueur] = calculScoreAuto(scores[joueur],carte)
            numCarte+=1
        affichage.set("Combien "+joueur+" veut-il joueur ?")
        print("wait..")
        miseBouton.wait_variable(boutonClique)
        print("Continue")
        miseBouton.destroy()
        boutonClique.set(False)
        miseJoueur(cagnotte,joueur,scores,croupiers,mise,affichage,entree,miseMessage)
        if carteTire[0].split()[0] == carteTire[1].split()[0]:
            reponse = tkinter.BooleanVar(None)
            affichage.set(joueur+" veut-il diviser ?")
            ouiBouton = tkinter.Button(fenetre,text="Oui",command = lambda: reponse.set(True))
            ouiBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
            nonBouton = tkinter.Button(fenetre,text="Non",command = lambda: reponse.set(False))
            nonBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
            print("wait..")
            ouiBouton.wait_variable(reponse)
            print("Continue")
            if cagnotte[joueur]>=mise[joueur] and reponse.get()==True:
                diviser(scores,carteTire[1],joueur,joueurs,cagnotte,mise,2,1)
            ouiBouton.destroy()
            nonBouton.destroy()
    for joueur in list(joueurs):
        if "/" in list(str(scores[joueur])) and int(scores[joueur].split("/")[1])==21:
            scores[joueur]="Black Jack"
            joueurs.remove(joueur)
        print()
    return scores,mise

def diviser(scores,carteTire,joueur,joueurs,cagnotte,mise,numJeu,tour):
    if "jeux" in joueur.split():
        numeroJeu=int(joueur.split()[3]) # on récupère le pseudo original du joueur sans le numéro de jeu qu'on a concaténer C'est pour cela qu'on veut pas d'espace dans le nom
        joueur=joueur.split()[0]
    else:
        numeroJeu=1
    afficherCarte("vide",tour+1,list(scores.keys()).index(joueur),numeroJeu-1)
    afficherCarte(carteTire,1,list(scores.keys()).index(joueur),numJeu-1)
    scores[joueur] = valeurCarte(carteTire)
    joueurs.append(joueur+" jeux n° "+str(numJeu))
    scores[joueur+" jeux n° "+str(numJeu)]=valeurCarte(carteTire)
    cagnotte[joueur] -= mise[joueur]
    cagnotte[joueur+" jeux n° "+str(numJeu)]= cagnotte[joueur]
    mise[joueur+" jeux n° "+str(numJeu)] = mise[joueur]
    print("Reste : " + str(cagnotte[joueur]))
    cagnotte["pot"] = cagnotte["pot"] + mise[joueur]

#Calcul le numéro du prochain jeu si le joueur j divise
def numJeu(joueurP,j):
    maxi=0
    for joueur in joueurP:
        if joueur.split()[0]==j and len(joueur.split())==3 and int(list(joueur)[len(list(joueur))-1])>maxi:
            maxi=int(list(joueur)[len(list(joueur))-1])
    return int(list(joueur)[len(list(joueur))-1])+1

def miseJoueur(cagnotte,j,scores,croupiers,mise,affichage,entree,miseMessage):
    mise[j]=int(entree.get())
    assurancePossible = False
    reponse = tkinter.BooleanVar(None)
    if scores["Croupier"]=="1/11": #si le croupier a un as cf. calculScoreAuto
        assurancePossible=True
    print("Mise de "+ j + str(mise))
    if mise[j]>cagnotte[j]:
        mise[j] = cagnotte[j]
    if cagnotte[j] >=0.5*mise[j] and assurancePossible:
        mise[j]=int(entree.get())
        affichage.set(j+" veut-il prendre une assurance ?")
        ouiBouton = tkinter.Button(fenetre,text="Oui",command = lambda: reponse.set(True))
        ouiBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
        nonBouton = tkinter.Button(fenetre,text="Non",command = lambda: reponse.set(False))
        nonBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
        print("wait..")
        ouiBouton.wait_variable(reponse)
        print("Continue")
        ouiBouton.destroy()
        nonBouton.destroy()
    if reponse.get():
            assurance = {}
            cagnotte["assurance"]=assurance
            cagnotte[j]=cagnotte[j]- int(0.5*mise[j])
            cagnotte["assurance"][j]= int(0.5*mise[j])
    cagnotte[j] = cagnotte[j]- mise[j]
    miseMessage.set(miseMessage.get()+"Mise de "+j+" : "+str(mise[j])+" / ")
    print("Reste : " + str(cagnotte[j]))
    cagnotte["pot"] = cagnotte["pot"] + mise[j]

#Donne la probabilité d'arriver à 21 ou moins
def probaXsur21(c,scores):
    if ( 21 - int(scores[c].split("/")[0]) <10): # le score le plus nul pour que la proba soit la plus haute
        # 21 - int(scores[c].split("/")[0]) => valeur à tiré pour 21
        probaXsur21 = 21 - int(scores[c].split("/")[0])
    else :
        probaXsur21 = 13
    return probaXsur21/13
    
def miseCroupierPourcentage(cagnotte,c,scores,croupiers,joueurs,pourcentage):
    mise = int(pourcentage * cagnotte[c])
    return mise

def miseCroupierRisque(cagnotte,c,scores,croupiers,joueurs):
    if meilleurScore(scores,c)<11:
        risque=0.2
    elif meilleurScore(scores,c)>15:
        risque=0.8
    else:
        risque=0.1
    mise = int((1-risque)*cagnotte[c]) # Si le risque est bas on mise beaucoup
    return mise

def miseCroupierProba(cagnotte,c,scores,croupiers,joueurs):
    mise = int(cagnotte[c] * probaXsur21(c,scores)*0.5)# Si la proba d'arriver à un 21 ou moins est de 1 on mise que la moitié de même pour les autres proba
    return mise

def miseCroupierAvant(cagnotte,c,scores,croupiers,joueurs):
    avantage = int(maximum(scores)<meilleurScore(scores,c)) #True => 1 // False => 0
    mise = 10 + avantage*10
    return mise

def miseCroupierAvPourcent(cagnotte,c,scores,croupiers,joueurs,pourcentage):
    avantage = int(maximum(scores)<meilleurScore(scores,c)) #True => 1 // False => 0
    mise = int(avantage * pourcentage * cagnotte[c])
    return mise

def miseCroupierAvProba(cagnotte,c,scores,croupiers,joueurs):
    avantage = int(maximum(scores)<meilleurScore(scores,c)) #True => 1 // False => 0
    mise = int(avantage * (1-probaXsur21(c,scores)) * cagnotte[c])
    return mise

#Pour cette variante il faut un pourcentage haut ce qu'on veut miser si on a l'avantage et un risque bas car par exemple 0.1*0.1*6/13 donne 0.0049 ce qui est très failble
#Conseillé entre 0.2 et 1
def miseCroupierCombiné(cagnotte,c,scores,croupiers,joueurs,pourcentage):
    avantage = int(maximum(scores)<meilleurScore(scores,c)) #True => 1 // False => 0
    if meilleurScore(scores,c)<11:
        mise=int(0.8*avantage * pourcentage * (1-probaXsur21(c,scores)) * cagnotte[c]) #risque=0.2 et on mise avec un facteur de 0.8 car plus le risque est bas plus on peut ce permettre de miser haut
    elif meilleurScore(scores,c)>15 :
        mise=int(0.2 * avantage * pourcentage * (1-probaXsur21(c,scores)) * cagnotte[c]) #risque=0.8 et on mise bas
    else:
        mise=int(0.1 * avantage * pourcentage * (1-probaXsur21(c,scores)) * cagnotte[c]) #risque = 1 et on mise encore plus petit
    return mise

def miseCarteRestante(cagnotte,c,scores,croupiers,joueurs,pourcentage):
    valeurRestante = 340*(len(croupiers)+len(joueurs)) #340 score de tous le paquet
    nbCarteRest= 52*(len(croupiers)+len(joueurs)) #n*taille Paquet
    avantage = int(maximum(scores)<meilleurScore(scores,c))
    for personne in scores.keys():
        valeurRestante-meilleurScore(scores,personne)
        if scores[personne] != 0: # si le joueur à pioché au premier tour
            nbCarteRest -= 2
    moyennePioche = valeurRestante/nbCarteRest
    if (21-meilleurScore(scores,c))< moyennePioche: # si la valeur qu'il faut est plus petite que la valeur moyenne du paquet et on pioche
        mise = int(avantage * pourcentage * (1-probaXsur21(c,scores)) * cagnotte[c])
    else:
        mise = 10
    return mise

def miseCroupier(cagnotte,c,scores,croupiers,joueurs,miseMessage):
    #Calcul mise
    stratMise = croupiers[c][1]
    pourcent = croupiers[c][3]
    print("Stratégie de Mise : " + str(stratMise) +"Pourcent : " + str(pourcent))
    if stratMise == 1:
        mise = miseCroupierPourcentage(cagnotte,c,scores,croupiers,joueurs,pourcent)
    elif stratMise == 2:
        mise = miseCroupierRisque(cagnotte,c,scores,croupiers,joueurs)
    elif stratMise == 3:
        mise = miseCroupierProba(cagnotte,c,scores,croupiers,joueurs)
    elif stratMise == 4:
        mise = miseCroupierAvant(cagnotte,c,scores,croupiers,joueurs)
    elif stratMise == 5:
        mise = miseCroupierAvPourcent(cagnotte,c,scores,croupiers,joueurs,pourcent)
    elif stratMise == 6:
        mise = miseCroupierAvProba(cagnotte,c,scores,croupiers,joueurs)
    elif stratMise == 7:
        mise = miseCroupierCombiné(cagnotte,c,scores,croupiers,joueurs,pourcent)
    elif stratMise == 8:
        mise = miseCarteRestante(cagnotte,c,scores,croupiers,joueurs,pourcent)
    else : #implémenter pour que les croupiers misent tous la même somme pour les graphes
        mise=10
    if cagnotte[c]>=10 and mise <=10:
        mise = 10
    elif cagnotte[c]>=10 and mise > 10:
        mise = mise
    else:
        mise = cagnotte[c]
    cagnotte["pot"] = cagnotte["pot"] + mise 
    print("mise :" + str(mise) +"\n")
    miseMessage.set(miseMessage.get()+"Mise de "+c+" : "+str(mise)+" / ")
    cagnotte[c]=cagnotte[c]- mise
    print("Reste : " + str(cagnotte[c]))
    return mise
        
def gagnantP(scores):
    maxi=0
    gagnant=[]
    for joueur in scores.keys():
        if "/" in list(str(scores.get(joueur))):
            scoresAs = scores.get(joueur).split("/")
            if int(scoresAs[1])>21:
                scores[joueur]=scoresAs[0]
            else:
                scores[joueur]=scoresAs[1]
        if scores[joueur] == "Black Jack":
            gagnant.append(joueur)
            maxi=21
        elif int(scores.get(joueur))>maxi and int(scores.get(joueur))<=21:
            maxi=int(scores.get(joueur))
    for joueur in scores.keys():
        if scores[joueur] != "Black Jack" and int(scores.get(joueur))==maxi:
            gagnant.append(joueur)
    if len(gagnant)==0:
        gagnant.append("personne")
    print(gagnant)
    if gagnant[0]!= "personne":
        scoreVainqueur=meilleurScore(scores,gagnant[0])
    else:
        scoreVainqueur="21 dépassé"
    return gagnant,scoreVainqueur

#donne les meilleur score de la partie à l'instant t pour se comparer aux autres joueurs
def maximum(scores):
    maxScore=0
    for personne in scores:
        if meilleurScore(scores,personne) > maxScore and meilleurScore(scores,personne)<=21:
            maxScore = meilleurScore(scores,personne)
    print("Max score : " + str(maxScore))
    return maxScore

def tourJoueur(j,joueursP,tour,scores,pioche,mise,cagnotte,affichage):
    print("Tour n° " + str(tour))
    print("A "+ j +" de jouer. Score : "+str(scores.get(j)))
    action = tkinter.StringVar()
    piocheBouton = tkinter.Button(fenetre,text="Piocher",command = lambda: action.set("piocher"))
    stopBouton = tkinter.Button(fenetre,text="Stop",command = lambda: action.set("stop"))
    piocheBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
    stopBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
    if "jeux" in j.split():
        nomJoueur=j.split()[0]
        numeroJeu=int(j.split()[3])
    else:
        nomJoueur=j
        numeroJeu=1
    if cagnotte[j]<mise[j]:
        affichage.set( "A "+ j +" de jouer. Score : "+str(scores.get(j)) +"\nVoulez-vous piocher ?")
        piocheBouton.wait_variable(action)
        piocheBouton.destroy()
        stopBouton.destroy()
    else:
        affichage.set("A "+ j +" de jouer. Voulez-vous piocher, doubler, non ?")
        doublerBouton = tkinter.Button(fenetre,text="Doubler",command = lambda: action.set("doubler"))
        doublerBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
        piocheBouton.wait_variable(action)
        piocheBouton.destroy()
        stopBouton.destroy()
        doublerBouton.destroy()
    if action.get()=="piocher": 
        carteTire = piocheCarte(pioche)
        print(carteTire)
        afficherCarte(carteTire[0],tour+1,list(scores.keys()).index(nomJoueur),numeroJeu-1)
        if valeurCarte(carteTire[0]) == scores[j] and cagnotte[j]>=mise[j]:
            reponse = tkinter.BooleanVar(None)
            affichage.set(j+" veut-il diviser ?")
            ouiBouton = tkinter.Button(fenetre,text="Oui",command = lambda: reponse.set(True))
            ouiBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
            nonBouton = tkinter.Button(fenetre,text="Non",command = lambda: reponse.set(False))
            nonBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
            print("wait..")
            ouiBouton.wait_variable(reponse)
            print("Continue")
            ouiBouton.destroy()
            nonBouton.destroy()
            if reponse.get() :
                diviser(scores,carteTire[0],j,joueursP,cagnotte,mise,numJeu(joueursP,j),tour) # le numéro du jeu est le numTour+1 car on divise seulement si on a 2 carte et si on a 2 carte
            else:                                                                            # dans un jeu au tour n on a déjà diviser n-1 fois on a donc n jeu si on divise 1 fois par tour
                scores[j] = calculScoreAuto(scores[j],carteTire[0])
        else:
            scores[j] = calculScoreAuto(scores[j],carteTire[0])
            if not ("/" in list(str(scores[j]))) and int(scores[j])>=21: 
                joueursP.remove(j)
            if "/" in list(str(scores[j])) and int(scores[j].split("/")[1])>=21:
                joueursP.remove(j)
    elif action.get()=="doubler" : 
        carteTire = piocheCarte(pioche)
        print(carteTire)
        afficherCarte(carteTire[0],tour+1,list(scores.keys()).index(nomJoueur),numeroJeu-1)
        cagnotte["pot"] = cagnotte["pot"] + mise[j]
        mise[j]=mise[j]*2
        cagnotte[j] = cagnotte[j] - mise [j]
        for carte in carteTire:
            scores[j] = calculScoreAuto(scores[j],carte)
        joueursP.remove(j)
    else:
        joueursP.remove(j)
    action.set(None)
    print()
    
def tourCroupierAleatoire(scores,c):
    if random.randint(1,2)==1 and meilleurScore(scores,c)<21:
        veutPiocher = True
    else:
        veutPiocher=False
    return veutPiocher
        
def tourCroupierProba(c,scores,proba):
    if proba<0:
        veutPiocher=False
    elif proba>=1 and meilleurScore(scores,c)<21:
        veutPiocher=True
    elif random.randint(1,100)/100<=proba and meilleurScore(scores,c)<21:
        veutPiocher = True
    else:
        veutPiocher=False
    return veutPiocher

def tourCroupierScore(c,scores):
    aleatoire = random.randint(12,21)
    if len(scores[c].split("/"))>1 and int(scores[c].split("/")[0]) < 12 and int(scores[c].split("/")[1]) < 21:
        veutPiocher=True
    elif aleatoire>int(scores[c].split("/")[0]) and int(scores[c].split("/")[0])<21: #pour 12 =>  9/10 // pour 16 =>  5/10 // pour 18 =>  3/10 // pour 19 =>  2/10 // pour 20 =>1/10 // pour 21 =>0/10
        veutPiocher=True
    else:
        veutPiocher=False
    return veutPiocher

def tourCroupierScoreAutre(c,croupiers,joueurs,scores):
    maxScore = maximum(scores)
    for j in scores:
        if meilleurScore(scores,j)>0:
            autreJoue = True
            break # On veut juste savoir si UN joueur à déjà jouer
    if meilleurScore(scores,c)<maxScore or (not autreJoue and meilleurScore(scores,c)<15): #Si les autres n'ont pas joué le croupier tire si il est inférieure à 15
        veutPiocher=True                                                                     # and à la priorité sur or donc les parenthèse sont inutiles
    else:
        veutPiocher=False
    return veutPiocher

def tourCarteRestante(c,croupiers,joueurs,tour,scores):
    valeurRestante = 340*(len(croupiers)+len(joueurs)) #340 valeur de tous le paquet
    nbCarteRest= 52*(len(croupiers)+len(joueurs))-len(joueurs)-len(croupiers)+1 #taille Paquet*nbJoueurs et on considère que chaque joueur/IA (sauf le croupier) à piocher une carte car au tour 1 tous le monde pioche 2 cartes
    for personne in scores.keys():
        valeurRestante-meilleurScore(scores,personne)
        if scores[personne]!=0:
            nbCarteRest-= tour # On ne retire pas la Deuxième carte du premier Tour des joueurs/IA
    moyennePioche = valeurRestante/nbCarteRest
    print(moyennePioche)
    if (21-meilleurScore(scores,c))> moyennePioche or meilleurScore(scores,c)<maximum(scores):
        veutPiocher=True
    else:
        veutPiocher=False
    return veutPiocher

def tourCarteTricheur(pioche,scores,c):
    #Si c'est un As la valeur de la carte est un str sinnon un int par la fonction valeurCarte
    if type(valeurCarte(pioche[0])) == str and 1 <= (21-meilleurScore(scores,c)) or valeurCarte(pioche[0]) <= (21-meilleurScore(scores,c)):
        return True
    else:
        return False

def tourCroupier(joueurs,c,croupiers,tour,scores,pioche):
    print("Tour n° " + str(tour))
    print("A "+ c +" de jouer. Score : "+str(scores.get(c)))
    strat = croupiers[c][0]
    proba = croupiers[c][2]
    print("Strat " + str(strat)+"Proba : "+str(proba))
    if strat==1:
        veutPiocher = tourCroupierAleatoire(scores,c)
    elif strat==2:
        veutPiocher = tourCroupierProba(c,scores,proba)
    elif strat==3:
        veutPiocher = tourCroupierScore(c,scores)
    elif strat==4:
        veutPiocher = tourCroupierScoreAutre(c,croupiers,joueurs,scores)
    elif strat == 5 :
        veutPiocher = tourCarteRestante(c,croupiers,joueurs,tour,scores)
    elif strat == 6:
        veutPiocher = tourCarteTricheur(pioche,scores,c)
    if veutPiocher :
        carteTire = piocheCarte(pioche)[0]
        print("Le Croupier tire " + carteTire)
        afficherCarte(carteTire,tour+1,list(scores.keys()).index(c))
        scores[c] = calculScoreAuto(scores[c],carteTire)
    else:
        print("Le croupier se retire")
        del croupiers[c]
    if "/" in list(str(scores[c])) and scores[c].split("/")[1]=="21" and tour==2 and c in croupiers:
        scores[c]="Black Jack"
        del croupiers[c]
    
def tourComplet(joueursP,croupiersP,tour,scores,pioche,mise,cagnotte,affichage):
    for joueur in list(joueursP):
        tourJoueur(joueur,joueursP,tour,scores,pioche,mise,cagnotte,affichage)
    for croupier in list(croupiersP):
        tourCroupier(joueursP,croupier,croupiersP,tour,scores,pioche)
    
def partieFinie(joueurs):
    return len(joueurs)==0

def partieComplete(joueursPart,croupiersPart,scores,pioche,cagnotte,mise,affichage):
    tour = 2;
    paieAssurance=False
    while not partieFinie(joueursPart) or not partieFinie(croupiersPart):
        tourComplet(joueursPart,croupiersPart,tour,scores,pioche,mise,cagnotte,affichage)
        tour+=1
    gagnantPartie,scoreGagnant = gagnantP(scores)
    continuer=tkinter.BooleanVar(False)
    continuerBouton = tkinter.Button(fenetre,text="Continuer",command = lambda: continuer.set(True))
    continuerBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
    affichage.set("Le gagnant est/sont "+ str(gagnantPartie)+" avec  "+str(scoreGagnant)+" !")
    print("Attente d'une entrée..")
    continuerBouton.wait_variable(continuer)
    print("Réponse recue")
    continuerBouton.destroy()
    print("Le gagnant est/sont "+ str(gagnantPartie)+" !\n")
    if scores["Croupier"]=="Black Jack":
        paieAssurance=True
    if paieAssurance and len(gagnantPartie)<=1:
        for assurer in cagnotte["assurance"]:
            cagnotte[assurer] = cagnotte[assurer] + cagnotte["assurance"][assurer]*3 #Rend la mise et paie le double
    if not gagnantPartie[0] == "personne":
        cagnotte["pot"] = int(cagnotte["pot"]/len(gagnantPartie))
        for gagnant in gagnantPartie:
            if "jeux" in gagnant.split():
                gagnant = gagnant.split()[0]
            cagnotte[gagnant] = cagnotte[gagnant] + cagnotte["pot"]
    else:
        for j in joueursTable:
            cagnotte[j] = cagnotte[j] + mise[j]            
        for c in croupiersTable:
            cagnotte[c] = cagnotte[c] + mise[c]

#Fonctions qui crée le dictionnaire des listes pour tracer les graphique
def scoreDesParties(scores,scoresParties):
    for j in scores:
        if j not in scoresParties:
            scoresParties[j]=[]
        scoresParties[j].append(meilleurScore(scores,j))
    return scoresParties

def cagnotteDesParties(cagnotte,cagnotteParties):
    for j in scores:
        if j not in cagnotteParties:
            cagnotteParties[j]=[]
        cagnotteParties[j].append(cagnotte[j])
    return cagnotteParties

def close():
    fenetre.destroy()
    os._exit(1)

#    for joueur in scoresPart:
#        scores=scoresPart[joueur]
#        n, bins, patches = plt.hist(scores,range=(0,22), bins = 22,color = 'blue', edgecolor='black', density=True)
#        plt.ylabel("Fréquence")
#        plt.xlabel("Scores")
#        plt.title("Fréquence des scores obtenus par " + str(joueur))
#        print(scores)
#        plt.show()
#    for joueur in cagnottePart:
#        mises=cagnottePart[joueur]
#        print(mises)
#        plt.plot(list(range(1,len(mises)+1)),mises,"b-.", linewidth = 0.8, marker="+",label="Mise d'un joueur")
#        plt.ylabel("Cagnotte")
#        plt.xlabel("Numéro de parties")
#        plt.title("Evolution de la cagnotte de " + str(joueur))
#        plt.show()


print(" ____  _            _           _            _    ")
print("|  _ \| |          | |         | |          | |   ")
print("| |_) | | __ _  ___| | __      | | __ _  ___| | __")
print("|  _ <| |/ _` |/ __| |/ /  _   | |/ _` |/ __| |/ /")
print("| |_) | | (_| | (__|   <  | |__| | (_| | (__|   < ")
print("|____/|_|\__,_|\___|_|\_\  \____/ \__,_|\___|_|\_\ ")
print()
nbJoueurs = int(input("Combien de joueurs veulent jouer ? MAX : 7 : "))
while nbJoueurs not in list(range(1,8)):
    nbJoueurs = int(input("Combien de joueurs veulent jouer ? MAX : 7 :"))

joueursTable,croupiersTable = initTable(nbJoueurs)
personneTable= joueursTable+list(croupiersTable.keys())
nouvellePartie = "oui"
cagnotte = initCagnotte(personneTable)

nouvellePartie == "oui"

#INTERFACE GRAPHIQUE
print("\n Ouverture de l'interface graphique \n")

fenetre = tkinter.Tk()

fenetre.protocol("WM_DELETE_WINDOW", close)
canvas = tkinter.Canvas(fenetre, width=1280, height=700, background='white')

entree = tkinter.Entry(fenetre, width=50)
entree.insert(0, "Entrez mise")

miseMessage = tkinter.StringVar()
miseAffichage = tkinter.Label(fenetre, textvariable=miseMessage, bg="white")
affichage = tkinter.StringVar()
affichage.set("Bienvenue à la table")
message = tkinter.Label(fenetre, textvariable=affichage, bg="white")

miseAffichage.pack()
canvas.pack()
message.pack(padx=5, pady=5)
entree.pack(side = tkinter.LEFT, padx=5, pady=5)

while len(personneTable)>1 and nouvellePartie:

        miseMessage.set("")

        table = tkinter.PhotoImage(file="table.png")

        canvas.create_image(640, 350, image=table)

        cagnotte["assurance"] = {}
        miseJoueurs={}
        pioche = initPioche(nbJoueurs)
        joueursPart = list(joueursTable)
        croupiersPart = croupiersTable.copy()
        
        scores,miseJoueurs = premierTour(joueursPart,croupiersPart,pioche,cagnotte,miseJoueurs,affichage,miseMessage)
        joueursParti = partieComplete(joueursPart,croupiersPart,scores,pioche,cagnotte,miseJoueurs,affichage)
        
        print(str(cagnotte)+ str(miseJoueurs)+"\n")
        print(str(scores))
        reponse = tkinter.BooleanVar(None)
        ouiBouton = tkinter.Button(fenetre,text="Oui",command = lambda: reponse.set(True))
        ouiBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
        nonBouton = tkinter.Button(fenetre,text="Non",command = lambda: reponse.set(False))
        nonBouton.pack(side = tkinter.RIGHT, padx=5, pady=5)
        for j in list(joueursTable):
            affichage.set(j+" veut-il continuer de jouer ?")
            reponse = tkinter.BooleanVar(None)
            print("wait..")
            ouiBouton.wait_variable(reponse)
            print("Continue")
            if not reponse.get():
                print(j +" quitte la table !\n")
                joueursTable.remove(j)
                nbJoueurs-=1
            if cagnotte[j]==0:
                print(j +" a fait faillite !\n")
                joueursTable.remove(j)
                nbJoueurs-=1
        for c in list(croupiersTable):
            if cagnotte[c]==0:
                print(c +" a fait faillite !\n")
                nbJoueurs-=1
                del croupiersTable[c]
        reponse = tkinter.BooleanVar(None)
        affichage.set("Voulez vous refaire une partie ?")
        print("wait..")
        ouiBouton.wait_variable(reponse)
        print("Continue")
        nouvellePartie=reponse.get()
        ouiBouton.destroy()
        nonBouton.destroy()
        

        personneTable= joueursTable+list(croupiersTable.keys())
        
if len(personneTable)==1:
    affichage.set("Il reste que " + personneTable[0] + " à la table ! \n THE END ")
print("THE END")
affichage.set("THE END")
fenetre.mainloop()
