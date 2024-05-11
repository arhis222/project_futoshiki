from random import *

def initialisation_grille(taille_grille):  # Initialise une grille de (taille_grille x taille_grille) avec des zéros
    grille = [[0] * taille_grille for _ in range(taille_grille)]
    return grille

def count_signes(signes):  # Compte le nombre de signe dans une table des signes
    count = 0
    for ligne in range (len(signes)):
        for colonne in range (len(signes)):
            if signes[ligne][colonne] is not None and (signes[ligne][colonne].get('comparaison_ligne', '')  != '' or
                                                       signes[ligne][colonne].get('comparaison_colonne', '') != ''):
                count += 1
    return count

def creer_hint_grille(grille,mode):
    hint_grille = initialisation_grille(len(grille))
    choix = choice([1, 2, 3, 4, 5])  # Faire un choix aléatoire (on donne la table de hint avec une pourcentage de 60%)
    liste_choix = list(range(len(grille)))  # Liste des nombres de 0 à len(grille)-1
    if choix < 4:  # ça veut dire on donne une hint (des numéros déjà placés)
        if mode == 'facile':
            for nombre_hint in range(len(grille)-1):
                i = choice(liste_choix)  # Faire un choix aléatoire pour i et k
                k = choice(liste_choix)
                hint_grille[i][k] = grille[i][k] #prend une valeur aléatoire de la table qui existe, pour donner une hint
        elif mode == 'moyen':
            for nombre_hint in range(len(grille)-2):
                i = choice(liste_choix)  # Faire un choix aléatoire pour i et k
                k = choice(liste_choix)
                hint_grille[i][k] = grille[i][k] #prend une valeur aléatoire de la table qui existe, pour donner une hint
        elif mode == 'difficile':
            for nombre_hint in range(len(grille)-3):
                i = choice(liste_choix)  # Faire un choix aléatoire pour i et k
                k = choice(liste_choix)
                hint_grille[i][k] = grille[i][k] #prend une valeur aléatoire de la table qui existe, pour donner une hint
    return hint_grille

def initialisation_signes(taille_grille, mode):
    """Initialise une liste des signes avec des signes ('<', '>', '^', 'v', ou '') en fonction du mode de jeu.
    Étant donné que nous devons comparer deux valeurs par nature des relations d’inégalité, nous avons ajusté
    notre fonction de façon à ne pas mettre ces signes aux extrémités."""
    signes = []
    if mode == 'entrainement':
        proportion_vide = 1 #1   # Aucun signe '<' ou '>'
    elif mode == 'facile':
        proportion_vide = 0.785  # Taux de fréquence des cases vides
    elif mode == 'moyen':
        proportion_vide = 0.69  # Taux de fréquence des cases vides
    elif mode == 'difficile':
        proportion_vide = 0.65  # Taux de fréquence des cases vides
    else:
        raise ValueError("Mode de jeu invalide")

    for ligne in range(taille_grille):
        lignes = []
        for colonne in range(taille_grille):
            if ligne == taille_grille - 1 and colonne == taille_grille - 1:  # Dernière cellule
                signes_dict = {}
            else:
                signes_dict = {'comparaison_ligne': '', 'comparaison_colonne': ''}

                if random() < proportion_vide:
                    signes_dict['comparaison_ligne'] = ''
                    signes_dict['comparaison_colonne'] = ''
                else:
                    choix = choice([1, 2])  # Faire un choix aléatoire
                    if choix == 1 and colonne != taille_grille - 1:  # Ne pas placer de signe'>' sur la dernière colonne
                        signes_dict['comparaison_ligne'] = '<'  # Symbole inférieur
                    elif choix == 2 and colonne != taille_grille - 1:  # Ne pas placer de signe'<' sur la dernière colonne
                        signes_dict['comparaison_ligne'] = '>'  # Symbole supérieur

                    choix = choice([3, 4])  # Faire un choix aléatoire
                    if choix == 3 and ligne != taille_grille - 1:  # Ne pas placer de signe '^' sur la dernière ligne
                        signes_dict['comparaison_colonne'] = '^' # Symbole vers le haut : le chiffre est plus grand que le chiffre ci-dessus
                    elif choix == 4 and ligne != taille_grille - 1:  # Ne pas placer de signe 'v' sur la dernière ligne
                        signes_dict['comparaison_colonne'] = 'v' # Symbole vers le bas : le chiffre est plus grand que le chiffre ci-dessous
            lignes.append(signes_dict)
        signes.append(lignes)
    if count_signes(signes) < len(signes) - 2 and mode == 'facile':
        return initialisation_signes(taille_grille, mode)
    elif count_signes(signes) < len(signes) - 1 and mode == 'moyen':
        return initialisation_signes(taille_grille, mode)
    elif count_signes(signes) < len(signes) and mode == 'difficile':
        return initialisation_signes(taille_grille, mode)
    else :
        return signes

def afficher_grille(grille):
    for ligne in grille:
        print(ligne)
    print()

def afficher_signes(signes):  # Affiche les signes de chaque cellule dans le tableau des signes.
    taille = len(signes)
    for i in range(taille):
        for j in range(taille):
            comparaison_ligne = signes[i][j].get('comparaison_ligne', '')
            if comparaison_ligne == '<':
                print(f"|_|<", end=" ")
            elif comparaison_ligne == '>':
                print(f"|_|>", end=" ")
            else:
                print("|_| ", end=" ")
        print()
        for j in range(taille):
            comparaison_colonne = signes[i][j].get('comparaison_colonne', '')
            if comparaison_colonne == '^':
                print(f" ^  ", end=" ")
            elif comparaison_colonne == 'v':
                print(f" v  ", end=" ")
            else:
                print("    ", end=" ")
        print()

def melanger_grille(grille): # Mélanger les lignes et les colonnes de la grille
    for ligne in grille:
        shuffle(ligne)
    shuffle(grille)

def est_numeros_valides(grille, ligne, colonne, nombre): # Verifie si chaque chiffre dans chaque cellule est différent
    taille_grille = len(grille)
    for i in range(taille_grille):
        if grille[ligne][i] == nombre and i != colonne:
            return False
        if grille[i][colonne] == nombre and i != ligne:
            return False
    return True

def est_signes_valides(grille, signes, ligne, colonne, nombre): # Verifie si le chiffre donné respecte les signes dans la grille
    taille_grille = len(grille)
    if colonne < len(grille) - 1:
        if signes[ligne][colonne].get('comparaison_ligne', '') == '>' and grille[ligne][colonne + 1] >= nombre:
            return False
        elif signes[ligne][colonne].get('comparaison_ligne', '') == '<' and grille[ligne][colonne + 1] <= nombre:
            return False
    if ligne < len(grille) - 1:
        if signes[ligne][colonne].get('comparaison_colonne', '') == '^' and grille[ligne + 1][colonne] <= nombre:
            return False
        elif signes[ligne][colonne].get('comparaison_colonne', '') == 'v' and grille[ligne + 1][colonne] >= nombre:
            return False
    return True # sinon automatiquement vrai

def generer_solution(taille_grille, signes):  # Pour créer une solution pour le tableau du jeu
    # Initialiser une grille de solution avec des zéros
    grille = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]
    def backtrack(ligne, colonne):
        if ligne == taille_grille: # Récursion pour placer les numéros dans chaque cellule
            return True
        # Déterminer la ligne et la colonne suivantes
        ligne_suivante = ligne if colonne < taille_grille - 1 else ligne + 1
        colonne_suivante = (colonne + 1) % taille_grille
        if grille[ligne][colonne] != 0: # Vérifier si la cellule est déjà remplie
            return backtrack(ligne_suivante, colonne_suivante)
        # Générer les candidats pour la cellule actuelle
        candidates = list(range(1, taille_grille + 1))
        candidates.sort(key=lambda x: sum(1 for c in candidates if est_numeros_valides(grille, ligne, colonne, c)))
        for num in candidates: # Parcourir les candidats pour remplir la cellule
            if est_numeros_valides(grille, ligne, colonne, num):
                grille[ligne][colonne] = num
                # Appeler récursivement backtrack pour la cellule suivante
                if backtrack(ligne_suivante, colonne_suivante):
                    return True
                grille[ligne][colonne] = 0
        return False
    if backtrack(0, 0):  # Appeler la fonction backtrack pour générer une solution
        return grille  # Renvoie la grille de la solution
    return None  # Si aucune solution n'est trouvée, retourner None

def valider_solution(grille, signes):
    # Valider si la grille de solution réspecte les contraintes des signes
    taille_grille = len(grille)
    for ligne in range(taille_grille):
        for colonne in range(taille_grille):
            nombre = grille[ligne][colonne]
            if not est_signes_valides(grille, signes, ligne, colonne, nombre):
                return False
    return True

def generer_jeu(taille_grille, mode):
    # Génère un jeu de futoshiki (jusqu'on obtien un jeu valide) avec le mode donné
    while True:
        signes = initialisation_signes(taille_grille, mode)
        # Essai de trouver une solution selon une table de signe fixe
        solution_grille = generer_solution(taille_grille, signes)

        if solution_grille is not None and valider_solution(solution_grille, signes):  # Controlle la solution
            return solution_grille, signes

def generer_jeu_valide(taille_grille, mode):
    # Génère et affiche un jeu de futoshiki valide avec le mode donné ('entrainement','facile','moyen','difficile')
    jeu_grille, signes = generer_jeu(taille_grille, mode)
    hint_grille = creer_hint_grille(jeu_grille, mode)
    return jeu_grille, signes, hint_grille

generer_jeu_valide(5, 'moyen')
generer_jeu_valide(6, 'difficile')
