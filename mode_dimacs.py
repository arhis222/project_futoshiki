# On montre les FNC avec des ',' au lieu de et('n')
# et des ' ' au lieu de ou('v')

import pysat.solvers
from random import *


################################ Fonctions de contrainte donnant le format souhaité ################################
################################ CONTRAINTES PAR DEFAUT ################################

def controle_grille_signes(inegalites): # On contrôle si les signes placés dans la grille se trouvent dans des cellules adjacentes
    pairs_corriges = []
    for inegalite in inegalites:
        i, j, k, l, signe = inegalite
        if signe not in [' ','<','>']:
            print("Erreur: signe invalide (les signes sont '>' ou '<')\n")
            return False
        if (i != k and j != l) or (i==k and j ==l):
            print("Erreur: Les signes de inégalités doivent être placées entre les cellules adjacentes\n")
            return False
        if [i,j,k,l] in pairs_corriges or [k,l,i,j] in pairs_corriges:
            print("Erreur: Les mêmes cellules sont comparées plus d'une fois\n")
            return False
        pairs_corriges.append([i,j,k,l])
    return True

def contrainte_cellule_unique_bis(taille_grille, grille=None): # Contrainte 1
    cnf = []
    for i in range(1, taille_grille + 1):
        for j in range(1, taille_grille + 1):
            variables = []
            for k in range(1, taille_grille + 1):
                variable = int(f"{i}{j}{k}")
                variables.append(variable)
                cnf.append(variables)  # Encadrer la valeur par des crochets
                for l in range(k + 1, taille_grille + 1):
                    cnf.append([-variable, -int(f"{i}{j}{l}")])
            if grille:
                chiffre = grille[i - 1][j - 1]
                if chiffre:
                    cnf.append([int(f"{i}{j}{chiffre}")])
    return cnf

def contrainte_ligne_colonne_unique_bis(taille_grille): # Contrainte 2
    cnf = []
    for k in range(1, taille_grille + 1):
        for i in range(1, taille_grille + 1):
            variables_ligne = [int(f"{i}{j}{k}") for j in range(1, taille_grille + 1)]
            cnf.append(variables_ligne)
            for j in range(1, taille_grille):
                for l in range(j + 1, taille_grille + 1):
                    cnf.append([-int(f"{i}{j}{k}"), -int(f"{i}{l}{k}")])

        for j in range(1, taille_grille + 1):
            variables_colonne = [int(f"{i}{j}{k}") for i in range(1, taille_grille + 1)]
            cnf.append(variables_colonne)
            for i in range(1, taille_grille):
                for l in range(i + 1, taille_grille + 1):
                    cnf.append([-int(f"{i}{j}{k}"), -int(f"{l}{j}{k}")])


    return cnf

################################ CONTRAINTES SUPPLEMENTAIRE  ################################
def contrainte_inegalites_bis(taille_grille, inegalites): # Contrainte 3
    if controle_grille_signes(inegalites):
        cnf = []
        for inegalite in inegalites:
            i, j, k, l, signe = inegalite
            if signe == '>':
                for x in range(1, taille_grille + 1):
                    for y in range(x, taille_grille + 1):
                        if not x > y:
                            cnf.append([-int(f"{i}{j}{x}"), -int(f"{k}{l}{y}")])
            elif signe == '<':
                for x in range(1, taille_grille + 1):
                    for y in range(1, taille_grille + 1):
                        if not x < y:
                            cnf.append([-int(f"{i}{j}{x}"), -int(f"{k}{l}{y}")])
        return cnf
    return []

################################ GENERATION DE LA FNC ################################
def generer_fnc(taille_grille, inegalites=None, grille=None): # Combiner les trois contraintes sous formule conjonctive
    # Génère la forme normale conjonctive en combinant toutes les contraintes
    cnf = []
    #Contraintes defaut
    cnf.extend(contrainte_cellule_unique_bis(taille_grille, grille)) # Contrainte 1
    cnf.extend(contrainte_ligne_colonne_unique_bis(taille_grille)) # Contrainte 2
    if (inegalites):
        # Contrainte si il y a une instance
        cnf.extend(contrainte_inegalites_bis(taille_grille, inegalites)) # Contrainte 3
    return cnf


################################ DE FNC AU FORMAT DIMACS ################################
def fnc_a_dimacs(fnc, output_file): # Convertir la formule conjonctive au format DIMACS
    nb_variables = len(set(abs(literal) for clause in fnc for literal in clause)) #Nombre des variables
    nb_clauses = len(fnc) # Nombre des clauses
    dimacs_str = f"p cnf {nb_variables} {nb_clauses}\n" # Ligne de problem
    for clause in fnc:
        dimacs_str += " ".join(str(literal) for literal in clause) + " 0\n" # Ajoute des clauses apres le ligne de problem

    with open(output_file, "w") as file:
        file.write("c Example CNF format file\n") # Ajout des commentaires
        file.write("c\n")
        file.write(dimacs_str)


################################ DE DIMACS À SAT ################################
def dimacs_a_sat(input_file, output_file): # Convertir le fichier dimacs au format SAT
    with open(input_file, "r") as file: # Ouvrir le fichier dimacs en lire
        lignes = file.readlines()
    cnf = [] # Liste pour prendre les fnc
    for ligne in lignes:
        # Ignorer les lignes de commentaire et la ligne de déclaration du problème
        if ligne.startswith("c") or ligne.startswith("p"):
            continue
        clause = [int(x) for x in ligne.split() if x != "0"]
        cnf.append(clause)

    with open(output_file, "w") as file:
        # Ajouter des lignes de titre et de commentaire au fichier de sortie
        file.write("c Sample SAT format\n")
        file.write("c\n")
        # Ajouter la ligne de déclaration du problème avec le nombre de variables et de clauses
        nb_variables = max(abs(literal) for clause in cnf for literal in clause)
        nb_clauses = len(cnf)
        file.write(f"p sat {nb_variables}\n")
        for i, clause in enumerate(cnf):
            literals = " ".join(str(literal) for literal in clause)
            # Si c'est la première ligne de formule, ajouter la parenthèse ouvrante
            if i == 0:
                file.write(f"(*(+({literals})\n")
            # Si c'est la dernière ligne de formule(pas de \n), ajouter la parenthèse fermante
            elif i == nb_clauses - 1:
                file.write(f"  +({literals})")
            # Sinon, ajouter la ligne de formule entre les parenthèses avec des espaces
            else:
                file.write(f"   +({literals})\n")
        # Ajouter la parenthèse fermante si c'est la dernière ligne de formule
        for i in range(nb_clauses-1):
            file.write(")")

################################ DE DIMACS À 3-SAT ################################

def de_dimacs_a_3sat(dimacs_file, output_file):
    with open(dimacs_file, 'r') as file:
        lines = file.readlines()

    # Remove comments and problem line
    lines = [line for line in lines if line[0] not in ['c', 'p']]

    # Convert each line to a list of integers
    clauses = [[int(x) for x in line.split() if int(x) != 0] for line in lines]

    # Convert to 3-SAT
    new_clauses = []
    for clause in clauses:
        while len(clause) > 3:
            new_var = max(max(abs(literal) for literal in clause), max(abs(literal) for new_clause in new_clauses for literal in new_clause)) + 1
            new_clauses.append([clause[0], clause[1], new_var])
            clause = [-new_var] + clause[2:]
        new_clauses.append(clause)

    # Write to output file
    with open(output_file, 'w') as file:
        file.write(f"p cnf {new_var} {len(new_clauses)}\\n")
        for clause in new_clauses:
            file.write(" ".join(str(literal) for literal in clause) + " 0\\n")

#########################Creation une jeu valide ############################
def initialisation_grille_sat(taille_grille):  # Initialise une grille de (taille_grille x taille_grille) avec des zéros
    grille = [[0] * taille_grille for _ in range(taille_grille)]
    return grille

def count_signes_sat(signes):  # Compte le nombre de signe dans une table des signes
    count = 0
    for ligne in range (len(signes)):
        for colonne in range (len(signes)):
            if signes[ligne][colonne] is not None and (signes[ligne][colonne].get('comparaison_ligne', '')  != '' or
                                                       signes[ligne][colonne].get('comparaison_colonne', '') != ''):
                count += 1
    return count

def creer_hint_grille_sat(grille,mode):
    hint_grille = initialisation_grille_sat(len(grille))
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

def initialisation_signes_sat(taille_grille, mode):
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
    if count_signes_sat(signes) < len(signes) - 2 and mode == 'facile':
        return initialisation_signes_sat(taille_grille, mode)
    elif count_signes_sat(signes) < len(signes) - 1 and mode == 'moyen':
        return initialisation_signes_sat(taille_grille, mode)
    elif count_signes_sat(signes) < len(signes) and mode == 'difficile':
        return initialisation_signes_sat(taille_grille, mode)
    else :
        return signes

def transformer_signes_bis(grille_signes): # Pour transformer la grille de signes à une liste pour nos contraintes
    liste_signes = []  # Initialise une liste vide pour stocker les signes transformés

    for ligne in range(len(grille_signes)):  # Parcourt chaque ligne dans la grille de signes
        for colonne in range(len(grille_signes[0])):  # Parcourt chaque colonne dans la grille de signes

            # Récupère le signe de comparaison sur la ligne et la colonne de la cellule actuelle
            signe_ligne = grille_signes[ligne][colonne].get('comparaison_ligne', '')
            signe_colonne = grille_signes[ligne][colonne].get('comparaison_colonne', '')

            # Si un signe de comparaison sur la ligne est trouvé, l'ajoute à la liste des signes transformés
            if signe_ligne:
                liste_signes.append((ligne + 1, colonne + 1, ligne + 1, colonne + 2, signe_ligne))

            # Si un signe de comparaison sur la colonne est trouvé, l'ajoute à la liste des signes transformés
            if signe_colonne:
                # Transforme les symboles 'v' en '>' et '^' en '<' pour le bon fonctionnement des contraintes
                if signe_colonne == "v": signe_colonne = ">"
                elif signe_colonne == "^": signe_colonne = "<"
                liste_signes.append((ligne + 1, colonne + 1, ligne + 2, colonne + 1, signe_colonne))

    return liste_signes  # Retourne la liste des signes transformés

def afficher_grille_sat(grille):
    for ligne in grille:
        print(ligne)
    print()

def afficher_signes_sat(signes):  # Affiche les signes de chaque cellule dans le tableau des signes.
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

def melanger_grille_sat(grille): # Mélanger les lignes et les colonnes de la grille
    for ligne in grille:
        shuffle(ligne)
    shuffle(grille)

def generer_solution_sat(taille_grille, signes):  # Pour créer une solution pour le tableau du jeu
    global model_finale
    # Initialiser une grille de solution avec des zéros
    reponse_grille = [[0 for _ in range(taille_grille)] for _ in range(taille_grille)]
    while not valider_solution_sat(reponse_grille, signes) :
        return None  # Si aucune solution n'est trouvée, retourner None
    solution_grille = transformer_modelf_solution_grille(model_finale)
    return solution_grille

def decode_model(model): #Pour decoder le model donnée par le SAT solveur
    model_finale = []
    for var in model:
        if var > 0:
            model_finale.append(var)
    return model_finale

def transformer_modelf_solution_grille(model_finale):  # Pour transformer le modèle décodé en forme de grille
    taille_grille = int(len(model_finale) ** 0.5)  # Calculer la taille de la grille
    grille_solution = []  # Initialiser une liste pour stocker la grille solution
    for i in range(0, len(model_finale), taille_grille):
        ligne = [num % 10 for num in model_finale[i:i + taille_grille]]
        grille_solution.append(ligne) # On ajoute seulement le dernier numéro qui correspond au valuer du cellule
    return grille_solution


def valider_solution_sat(reponse_grille, signes_grille): # Valider si la grille de solution réspecte les contraintes des signes
    global model_finale
    taille = len(reponse_grille)
    liste_signes = transformer_signes_bis(signes_grille)
    fnc = generer_fnc(taille, liste_signes, reponse_grille)

    # Créez une instance du solveur
    solver = pysat.solvers.Minisat22()

    # Ajoutez des clauses
    for clause in fnc:
        solver.add_clause(clause)

    # Vérifiez la satisfaisabilité
    if solver.solve():
        print("Satisfiable")
        model = solver.get_model()
        model_finale = decode_model(model)
        print("Model:", model_finale)
        return True

    else:
        print("Unsatisfiable")
        return False


def afficher_solution_sat(grille_decodée):
# Affichage de resoultion
    print("Grille décodée :")
    grille= []
    taille_grille = int(len(grille_decodée) ** 0.5) # Calculer la taille de la grille
    for ligne in grille_decodée:
        grille.append(ligne % 10)
    for x in range(taille_grille):
        for y in range(taille_grille):
            print(grille[x*taille_grille+y], "|", end="")
        print("\n" + "-" * taille_grille * taille_grille)

def generer_jeu_sat(taille_grille, mode):
    # Génère un jeu de futoshiki (jusqu'on obtien un jeu valide) avec le mode donné
    while True:
        signes = initialisation_signes_sat(taille_grille, mode)
        # Essai de trouver une solution selon une table de signe fixe
        solution_grille = generer_solution_sat(taille_grille, signes)

        if solution_grille is not None:  # Controlle la solution
            return solution_grille, signes

def generer_jeu_valide_sat(taille_grille, mode):
    # Génère et affiche un jeu de futoshiki valide avec le mode donné ('entrainement','facile','moyen','difficile')
    jeu_grille, signes = generer_jeu_sat(taille_grille, mode)
    hint_grille = creer_hint_grille_sat(jeu_grille, mode)
    return jeu_grille, signes, hint_grille


####################Test pour creation du fichier dimacs#########################
#Test 1
"""
cnf = [[1, 3, -4], [4], [2, -3]]
output1_file = "output_dimacs.cnf"
output2_file = "output_sat.sat"

fnc_a_dimacs(cnf, output1_file)
print(f"Résultat écrit dans '{output1_file}'")

dimacs_a_sat(output1_file,output2_file)
print(f"Résultat écrit dans '{output2_file}'")
"""
#Test 2
"""
taille_grille = 3
inegalites = [(1, 1, 1, 2, '>')]  # Exemple d'une seule inégalité pour la démonstration
grille_jeu = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Exemple d'une grille de jeu
fnc = generer_fnc(taille_grille, inegalites)
print("exemple_fnc : ",fnc)

dimacs_file = "output_dimacs_for_minisat.dimacs"
sat_file = "output_sat.sat"

fnc_a_dimacs(fnc, dimacs_file)
print(f"Résultat écrit dans '{dimacs_file}'")

dimacs_a_sat(dimacs_file, sat_file)
print(f"Résultat écrit dans '{sat_file}'")

"""

"""
#Test 3

taille_grille = 20
jeu_grille,signes,hint_grille = generer_jeu_valide_sat(taille_grille, "facile")#inegalites = [(1, 1, 1, 2, '>')]  # Exemple d'une seule inégalité pour la démonstration
"""
###############################Pas Besoin (nos tests)###############################
#############Test pour le transformation des signes #############################
"""
signes = initialisation_signes_sat(3,"facile")
afficher_signes_sat(signes)
liste_signes = transformer_signes_bis(signes)
print(liste_signes)
"""
"""
######################################## EXEMPLES POUR LES FONCTIONS BIS ####################################

# Exemple d'utilisation
cnf = contrainte_cellule_unique_bis(3)
print("contrainte1_3x3_bis",cnf)


cnf = contrainte_ligne_colonne_unique_bis(3)
print("contrainte2_3x3_bis",cnf)

inegalites_bis = [
    (1, 1, 1, 2, '>')   # la cellule (1,1) doit être supérieure à la cellule (1,2)
]
cnf = contrainte_inegalites_bis(3,inegalites_bis)
print("contrainte3_3x3_bis",cnf)


inegalitex_bis = [
    (1, 1, 2, 1, '>')   # la cellule (1,1) doit être supérieure à la cellule (2,1)
]
cnf = contrainte_inegalites_bis(3, inegalitex_bis)
print("contrainte3_3x3_dernier_test_bis", cnf)




print()
print()
print()


#############################################################################################################

# Exemple d'utilisation
cnf = contrainte_cellule_unique(3)
print("contrainte1_3x3",cnf)

cnf = contrainte_ligne_colonne_unique(3)
print("contrainte2_3x3",cnf)


inegalites = [
    (1, 1, 1, 2, '>')   # la cellule (1,1) doit être supérieure à la cellule (1,2)
]
cnf = contrainte_inegalites(3,inegalites)
print("contrainte3_3x3",cnf)

#################################################

inegalitex = [
    (1, 1, 2, 1, '>')   # la cellule (1,1) doit être supérieure à la cellule (2,1)
]
cnf = contrainte_inegalites(3, inegalitex)
print("contrainte3_3x3_dernier_test", cnf)

#~~~~~~~~~~~~~~~~~~~~~~~~

inegalites = [
    (1, 1, 2, 1, '>'),   # la cellule (1,1) doit être supérieure à la cellule (2,1)
    (2, 2, 3, 2, '<'),   # la cellule (2,2) doit être inférieure à la cellule (3,2)
    (3, 3, 4, 3, '>'),   # la cellule (3,3) doit être supérieure à la cellule (4,3)
    (4, 4, 1, 4, '<'),   # la cellule (4,4) doit être inférieure à la cellule (1,4)
    (1, 2, 2, 2, '>'),   # la cellule (1,2) doit être supérieure à la cellule (2,2)
    (2, 3, 3, 3, '<'),   # la cellule (2,3) doit être inférieure à la cellule (3,3)
    (3, 4, 4, 4, '>'),   # la cellule (3,4) doit être supérieure à la cellule (4,4)
    (4, 1, 1, 1, '<'),   # la cellule (4,1) doit être inférieure à la cellule (1,1)
]
cnf = contrainte_inegalites(4, inegalites)
print("contrainte3_4x4", cnf)

################################################



"""
#### EXEMPLE DE SATISFAISABILITE #########
"""
taille_grille = 3
inegalites = [(1, 2, 1, 3, '>'), (3, 2, 3, 3, '<'), (1, 3, 2, 3, '>'), (1, 1, 2, 1, '<')]
print("liste_avant = ", inegalites )

fnc = generer_fnc(taille_grille, inegalites)
print("exemple_fnc : ",fnc)

signes = initialisation_signes_sat(taille_grille,"facile")
print(signes)
afficher_signes_sat(signes)


liste = [[{'comparaison_ligne': '', 'comparaison_colonne': '^'}, {'comparaison_ligne': '>', 'comparaison_colonne': ''}, {'comparaison_ligne': '', 'comparaison_colonne': '>'}], [{'comparaison_ligne': '', 'comparaison_colonne': ''}, {'comparaison_ligne': '', 'comparaison_colonne': ''}, {'comparaison_ligne': '', 'comparaison_colonne': ''}], [{'comparaison_ligne': '', 'comparaison_colonne': ''}, {'comparaison_ligne': '<', 'comparaison_colonne': ''}, {}]]
print ("liste_originale: ", transformer_signes_bis(liste))


# Créez une instance du solveur
"""
"""
taille_grille = 3
grille = [[0,0,0],[0,0,0], [0,0,0]]

inegalites= initialisation_signes_sat(taille_grille,"facile")
print("avant: ", inegalites)
afficher_signes_sat(inegalites)
signe_finale = transformer_signes_bis(inegalites)
print ("transforme:",signe_finale)
fnc = generer_fnc(taille_grille, signe_finale)

solver = pysat.solvers.Minisat22()

# Ajoutez des clauses
for clause in fnc:
    solver.add_clause(clause)

# Vérifiez la satisfaisabilité
if solver.solve():
    print("Satisfiable")
    model = solver.get_model()
    grille_decode = decode_model(model)
    print("Model:", grille_decode)  # Model: [1, -2, 3]
else:
    print("Unsatisfiable")

reponse_grille = transformer_modelf_solution_grille(grille_decode)
print(reponse_grille)

# Utilisez la fonction pour décoder le modèle SAT et remplir la grille de jeu
grille_decodée = decode_model(model)

# Affichage de resoultion
print("Grille décodée :")
print(grille_decodée)
grille= []
for ligne in grille_decodée:
    grille.append(ligne % 10)
for x in range(taille_grille):
    for y in range(taille_grille):
        print(grille[x*taille_grille+y], "|", end="")
    print("\n" + "-" * taille_grille * taille_grille)
reponse_grille = transformer_modelf_solution_grille(grille_decodée)
print(reponse_grille)

"""
"""

taille_grille = 3

inegalites = initialisation_signes_sat(taille_grille,"facile")
inegalites_bis = transformer_signes_bis(inegalites)
print("signes:")
afficher_signes_sat(inegalites)
print(inegalites_bis)
grille_jeu = [[2, 3, 0], [0, 2, 0],[0, 1, 0]] # Exemple d'une grille de jeu
fnc = generer_fnc(taille_grille,inegalites_bis,grille_jeu)

print("exemple_fnc : ",fnc)

# Créez une instance du solveur
solver = pysat.solvers.Minisat22()

# Ajoutez des clauses
for clause in fnc:
    solver.add_clause(clause)

# Vérifiez la satisfaisabilité
if solver.solve():
    print("Satisfiable")
    model = solver.get_model()
    print("Model:", model)  # Model: [1, -2, 3]
else:
    print("Unsatisfiable")


# Utilisez la fonction pour décoder le modèle SAT et remplir la grille de jeu
grille_decodée = decode_model(model)

# Affichage de resoultion
print("Grille décodée :")
print(grille_decodée)
grille= []
for ligne in grille_decodée:
    grille.append(ligne % 10)
for x in range(taille_grille):
    for y in range(taille_grille):
        print(grille[x*taille_grille+y], "|", end="")
    print("\n" + "-" * taille_grille * taille_grille)

reponse_grille = transformer_modelf_solution_grille(grille_decodée)
print(reponse_grille)
"""

####################### En Utilisant fichier Dimacs#########################

"""
import subprocess


input_for_sat = "input_minisat.dimacs"
output_for_sat = "output_minisat.dimacs"
fnc_a_dimacs(fnc,input_for_sat)
with open(output_for_sat, "w") as file:
    subprocess.run(["minisat", input_for_sat], stdout=file)



from pysat.formula import CNF
from pysat.examples.lbx import LBX

formula = CNF(from_file='input_dimacs_for_minisat.cnf')
mcsls = LBX(formula)

for mcs in mcsls.enumerate():
     print(mcs)


"""

"""
from pycryptosat import Solver
s = Solver()
s.add_clause([-1])
s.add_clause([1, 2])
sat, solution = s.solve()
print (sat)
print (solution[1])
"""
"""
from z3 import *
s = Solver()

grid = [
        [ Int(f'cell_(r)-(c)') for c in range(9)]
        for r in range(9)
        ]

for r in range(9):
    for c in range(9):
        s.add(grid[r][c] >= 1)
        s.add(grid[r][c] <= 9)

    s.add(Distinct(grid[r]))

for c in range(9):
    s.add(Distinct( [ grid[r][c] for r in range(9) ] ))

for x in range(3):
    for y in range(3):
        s.add(Distinct([
            grid[x*3][y*3],
            grid[x*3][y*3+1],
            grid[x*3][y*3+2],
            grid[x*3+1][y*3],
            grid[x*3+1][y*3+1],
            grid[x*3+1][y*3+2],
            grid[x*3+2][y*3],
            grid[x*3+2][y*3+1],
            grid[x*3+2][y*3+2],
        ]))

s.check()
m = s.model()
print(m)




"""
##################################### Exemple d'utilisation avec une grille de jeu donnée ####################################
"""
from pysat.solvers import Minisat22
from pysat.formula import CNF


taille_grille = 3
inegalites = [(1, 1, 1, 2, '>')]  # Exemple d'une seule inégalité pour la démonstration
grille_jeu = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Exemple d'une grille de jeu
fnc = generer_fnc(taille_grille, inegalites)
#print("exemple_fnc : ",fnc)
#dimacs_file = "output_dimacs_for_minisat.dimacs"
#fnc_a_dimacs(fnc, dimacs_file)
# Créez une instance du solveur


cnf = CNF(from_clauses=fnc)
# Ajoutez des clauses
#solver.add_clause(fnc)  # clause: not x1 or x2

# create a SAT solver for this formula:
with Minisat22(bootstrap_with=cnf) as solver:
    # 1.1 call the solver for this formula:
    print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    # 1.2 the formula is satisfiable and so has a model:
    print('and the model is:', solver.get_model())

    # 2.1 apply the MiniSat-like assumption interface:
    print('formula is',
        f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
        'assuming x1 and x2')

    # 2.2 the formula is unsatisfiable,
    # i.e. an unsatisfiable core can be extracted:
    print('and the unsatisfiable core is:', solver.get_core())


# create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
cnf = CNF(from_clauses=[[-1, 2], [-1, -2]])

# create a SAT solver for this formula:
with Minisat22(bootstrap_with=cnf) as solver:
    # 1.1 call the solver for this formula:
    print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    # 1.2 the formula is satisfiable and so has a model:
    print('and the model is:', solver.get_model())

    # 2.1 apply the MiniSat-like assumption interface:
    print('formula is',
        f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
        'assuming x1 and x2')

    # 2.2 the formula is unsatisfiable,
    # i.e. an unsatisfiable core can be extracted:
    print('and the unsatisfiable core is:', solver.get_core())

solver.solve(dimacs_file)
# Vérifiez la satisfaisabilité
if solver.solve():
    print("Satisfiable")
    model = solver.get_model()
    print("Model:", model)  # Model: [1, -2, 3]
else:
    print("Unsatisfiable")



# Örneğin boyutu ve inegaliteleri
from pysat.solvers import Minisat22
from pysat.formula import CNF
taille_grille = 3
inegalites = [(1, 1, 1, 2, '>')]  # Örnek bir inegalite

# FNC'nin oluşturulması
fnc = generer_fnc(taille_grille, inegalites)

# FNC'nin DIMACS formatına dönüştürülmesi ve bir dosyaya yazılması
dimacs_file = "example.dimacs"
fnc_a_dimacs(fnc, dimacs_file)

# MiniSat ile çözüm
solver = Minisat22()
solver.solve(dimacs_file)

# Çözümün kontrolü
if solver.solve():
    print("Satisfiable")
    model = solver.get_model()
    print("Model:", model)
else:
    print("Unsatisfiable")
 



dene = Fal
if dene :
    # Créez un fichier DIMACS de test
    with open("test.dimacs", "w") as file:
        file.write("c This is a test DIMACS file\n")
        file.write("p cnf 5 3\n")
        file.write("1 -5 4 0\n")
        file.write("-1 5 3 4 0\n")
        file.write("-3 -4 0\n")
    
    # Appelez la fonction dimacs_to_3sat
    de_dimacs_a_3sat("test.dimacs", "output_3sat.dimacs")
    
    # Maintenant, vérifiez le contenu du fichier de sortie
    with open("output_3sat.sat", "r") as file:
        print(file.read())        
"""