from tkinter import *
import sys
import pygame

from modelisation_2 import *
from mode_dimacs import *

###########################IMPORTANT NOTE#####################################
#Si on a une erreur lorsqu'on essaye de importer pygame mettre/enlever les commentaires ci dessous
#########################################################################################

#import subprocess
#import os
# Obtenir le chemin absolu du répertoire contenant le module pygame
#pygame_path = os.path.abspath("venv/include/site/python3.7/pygame")
#pysat_path = os.path.abspath("venv/include/site/python3.7/python-sat")

# Ajouter le chemin du module pygame à PYTHONPATH et appeler subprocess
#subprocess.call(["python", "-m", "pip", "install", "pygame"], env=dict(os.environ, PYTHONPATH=pygame_path))
#subprocess.call(["python", "-m", "pip", "install", "python-sat"], env=dict(os.environ, PYTHONPATH=pysat_path))

#############################################################################################


pygame.init()
args = sys.argv  # pour prendre les arguments de l'autre fichier ce qu'on met dans la ligne de command
# Recherchez le paramètre "taille" dans les arguments
if "--taille" in args:
    # Trouver l'index du paramètre "--taille"
    index = args.index("--taille")
    # Récupérer la valeur du paramètre "--taille" à l'index suivant (ce devrait être taille_du_tableau)
    taille_du_tableau = args[index + 1]

# Recherchez le paramètre "mode" dans les arguments
if "--mode" in args:
    # Trouver l'index du paramètre "--mode"
    index = args.index("--mode")
    # Récupérer la valeur du paramètre "--mode" à l'index suivant (ce devrait être mode)
    mode = args[index + 1]

# Recherchez le paramètre "solveur" dans les arguments
if "--solveur" in args:
    # Trouver l'index du paramètre "--solveur"
    index = args.index("--solveur")
    # Récupérer la valeur du paramètre "--solveur" à l'index suivant (ce devrait être solveur)
    solveur = args[index + 1]


################# Partie de la musique #################

def jouerMusic(nom_music, volume):
    pygame.mixer.music.load(nom_music)
    pygame.mixer.music.play(loops=-1)  # Pour ce qu'il joue tout le temps
    pygame.mixer.music.set_volume(volume)

def changerMusic():
    global music_actuel
    index = musics.index(music_actuel)
    next_index = (index + 1) % len(musics)
    music_actuel = musics[next_index]
    pygame.mixer.music.fadeout(800)  # changement entre les musiques
    jouerMusic(music_actuel, 0.2)

################# La fenêtre de jeu #################

# Création de la fenêtre tkinter (interface de jeu)
root = Tk()  # ouvrir une fenêtre
root.title("Tableau de Futoshiki")  # titre de la fenêtre
root.geometry("1920x1080")  # taille de la fenêtre

# wallpaper
bg = PhotoImage(file="wallpaper/game_wp2.png")
my_label = Label(root, image=bg)
my_label.place(x=-200, y=-150, relwidth=1.2, relheight=1.2)  # on a ajusté la taille

# Initialise les musiques
musics = ["music/CastleMist.mp3", "music/DarkCloud.mp3", "music/NiNoKuni.mp3", "music/Hornet.mp3"]
music_actuel = musics[0]
pygame.mixer.init()
jouerMusic(music_actuel, 0.2)

################# Les boutons du jeu #################

est_musique = True # Une variable pour l'état du musique (On par défaut)
def bouton_changerMusic_click():
    global est_musique
    sound = pygame.mixer.Sound("music/clickButton.mp3")
    sound.play()  # L'effet du clique
    if est_musique:
        changerMusic()
def bouton_on_off_Music_click():
    global est_musique
    sound = pygame.mixer.Sound("music/clickButton.mp3")
    sound.play()  # L'effet du clicque
    if est_musique:
        pygame.mixer.music.pause()  # Arrêter la musique
        est_musique = False  # mettre à jour l'état de la musique
    else:
        pygame.mixer.music.unpause()  # Continuer la musique
        est_musique = True  # mettre à jour l'état de la musique

def bouton_resoudre_click(frame, taille):
    global jeu_grille, signes, hint_grille
    sound = pygame.mixer.Sound("music/clickButton.mp3")
    sound.play()  # Effet du clic
    # Supprime des entrées d'utilisateur et conserve uniquement des indices/hints
    for widget in frame.winfo_children():
        if isinstance(widget, Entry):
            # Si l'entrée utilisateur est vide (la valeur dans hint_grille est 0), supprimer le contenu de l'entrée
            row = widget.grid_info()['row'] // 2
            column = widget.grid_info()['column'] // 2
            if hint_grille[row][column] == 0:
                widget.delete(0, END)
    # Affichage du tableau avec toutes les valeurs (indices et entrées utilisateur)
    print_board(jeu_grille, signes, hint_grille, taille, affiche_tous=True)

def bouton_nouveauJeu_click(frame, taille, mode):
    global jeu_grille, signes, hint_grille, solveur
    sound = pygame.mixer.Sound("music/clickButton.mp3")
    sound.play()  # l'effet du clique
    for widget in frame.winfo_children():
        widget.destroy()
    frame = Frame(root)  # créer une frame couvrant tableau
    frame.pack(padx=20, pady=40)  # on utilise padx et pady pour règler les éspaces autour du tableau
    if solveur == "Notre Solveur":
        jeu_grille, signes, hint_grille = generer_jeu_valide(taille, mode)  # Creation du Table du Jeu
    else :
        jeu_grille, signes, hint_grille = generer_jeu_valide_sat(taille, mode)  # Creation du Table du Jeu

    print_board(jeu_grille, signes, hint_grille, taille)
    return jeu_grille, signes, hint_grille

def effacer_message_reussi(frame):  # Pour effacer les messages quand on recommence à jouer avec le bouton 'Effacer'
    for widget in frame.winfo_children():
        if isinstance(widget, Label) and widget.cget("text") in ["Vous avez réussi!", "Vous avez perdu!"]:
            widget.destroy()

def bouton_effacer_click(frame, taille): #Permet d'effacer les chiffres saisis par le joueur et recommencer
    global jeu_grille, signes, hint_grille
    sound = pygame.mixer.Sound("music/clickButton.mp3")
    sound.play()  # L'effet du clique
    for widget in frame.winfo_children(): # Effacer le contenu des widgets Entry
        if isinstance(widget, Entry):
            widget.delete(0, END)
            # Comme nous avons effacé les entrées de l'utilisateur, nous devons également mettre à jour tout le tableau
            row = widget.grid_info()['row'] // 2  # Trouver la ligne où se trouve l'entrée utilisateur
            column = widget.grid_info()['column'] // 2  # et sa colonne
            hint_grille[row][column] = 0  # Réinitialiser la cellule correspondante dans hint_grille
    effacer_message_reussi(frame)

    print_board(jeu_grille, signes, hint_grille, taille)
    frame = Frame(root)  # creer une frame couvrant tableau
    frame.pack(padx=20, pady=40)  # on utilise padx et pady pour regler les espaces autour du tableau

def bouton_valider_click(reponse_grille, signes_grille):  # Compare la réponse du joueur avec la solution
    global solveur, taille
    # On controlle tout d'abord si l'utilisateur met des valeurs unique (contrainte 1) afin de mettre dans la fonction (Pour l'optimisation de performance)
    for ligne in range(len(reponse_grille)):
        for colonne in range(len(reponse_grille)):
            if not est_numeros_valides(reponse_grille, ligne, colonne, reponse_grille[ligne][colonne]):
                print("Ohnoo vous avez perdu!")
                return False
    if solveur == "Notre Solveur":
        if not valider_solution(reponse_grille, signes_grille):
            print("Ohnoo vous avez perdu!")
            return False

    else: # MiniSat22
        if not valider_solution_sat(reponse_grille, signes_grille):
            return False
    print("Wuhuu vous avez réussi!")
    return True

################# Fonction pour afficher le tableau ####################

def validate_entry(content): # Contrôle si le saisi est un chiffre ou pas, on peut saisir que des chiffres
    if content == "": # si l'utilisateur efface le contenu de la cellule
        return True
    if content in "123456789" and len(content) == 1:
        return True
    return False

def print_board(jeu_grille, signes, hint_grille, taille, affiche_tous=False):
    afficher_signes(signes)
    afficher_grille(jeu_grille)
    pad_x = 1   # Variables (pad_x , pad_y) pour stocker la quantité d'espace calculée
    pad_y = 1
    if affiche_tous:
        for i in range(taille):
            for j in range(taille): # Affichage des numeros
                cell_label = Label(frame, text=str(jeu_grille[i][j]), font=("Helvetica", 13), width=4, height=2, relief="groove")
                cell_label.grid(row=i * 2, column=j * 2, padx=pad_x, pady=pad_y)
                if j < taille - 1:  # Contrôler les signes ">" et "<"
                    if signes[i][j].get('comparaison_ligne', '') == '>':
                        arrow_label = Label(frame, text=">", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                    elif signes[i][j].get('comparaison_ligne', '') == '<':
                        arrow_label = Label(frame, text="<", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                    else: # Sinon on mets " "
                        blank_label = Label(frame, text=" ", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        blank_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                if i < taille - 1: # Contrôler les signes "v" et "^"
                    if signes[i][j].get('comparaison_colonne', '') == 'v':
                        arrow_label = Label(frame, text="v", font=("Helvetica", 12), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)
                    elif signes[i][j].get('comparaison_colonne', '') == '^':
                        arrow_label = Label(frame, text="^", font=("Helvetica", 15), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)
                    else: # Sinon on mets " "
                        blank_label = Label(frame, text=" ", font=("Helvetica", 12), width=1, height=1, relief="flat")
                        blank_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)
    else:
        for i in range(taille):
            for j in range(taille): # Si la cellule est vide, print " "
                if not hint_grille[i][j]: # Avec le widget 'Entry',on demande à l'utilisateur de taper un chiffre dans les cellules
                    entry_var = StringVar(); # Pour stocker la valeur de l'entrée (way interactive)

                    cell_entry = Entry(frame, font=("Helvetica", 20), width=2, relief="groove", validate="key", justify='center', state="normal", bg="#F0F0F0", textvariable=entry_var)
                    cell_entry.grid(row=i * 2, column=j * 2, padx=5, pady=5)
                    cell_entry.config(justify='center')

                    vcmd = (frame.register(validate_entry), '%P') # On contrôle l'entrée d'utilisateur si c'est un chiffre ou pas
                    cell_entry.config(validatecommand=vcmd)

                    # Permet d'effacer le contenu du cellule avec les touches Delete et Backspace
                    def clear_on_delete(event, var=entry_var):
                        var.set("")
                    cell_entry.bind("<Delete>", clear_on_delete)
                    cell_entry.bind("<BackSpace>", clear_on_delete)

                else: # Affichage des chiffres
                    cell_label = Label(frame, text=str(jeu_grille[i][j]), font=("Helvetica", 19), width=2, height=1, relief="groove")
                    cell_label.grid(row=i * 2, column=j * 2, padx=pad_x, pady=pad_y)

                if j < taille - 1: # Contrôler les signe ">" et "<"
                    if signes[i][j].get('comparaison_ligne', '') == '>':
                        arrow_label = Label(frame, text=">", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                    elif signes[i][j].get('comparaison_ligne', '') == '<':
                        arrow_label = Label(frame, text="<", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                    else: # Sinon on mets " "
                        blank_label = Label(frame, text=" ", font=("Helvetica", 13), width=1, height=1, relief="flat")
                        blank_label.grid(row=i * 2, column=j * 2 + 1, padx=0, pady=0)
                if i < taille - 1: # Contrôler la signe "v" et "^"
                    if signes[i][j].get('comparaison_colonne', '') == 'v':
                        arrow_label = Label(frame, text="v", font=("Helvetica", 12), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)
                    elif signes[i][j].get('comparaison_colonne', '') == '^':
                        arrow_label = Label(frame, text="^", font=("Helvetica", 15), width=1, height=1, relief="flat")
                        arrow_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)
                    else: # Sinon on mets " "
                        blank_label = Label(frame, text=" ", font=("Helvetica", 12), width=1, height=1, relief="flat")
                        blank_label.grid(row=i * 2 + 1, column=j * 2, padx=0, pady=0)

        def create_and_validate():
            sound = pygame.mixer.Sound("music/clickButton.mp3")
            sound.play()  # L'effect du click
            reponse_grille = creer_reponse_grille(hint_grille)
            if bouton_valider_click(reponse_grille, signes):    # Si le joueur a réussi le jeu
                reussi_label = Label(frame, text="Vous avez réussi!", font=("Helvetica", 14), fg="green")
                reussi_label.grid(row=taille * 2 + 1, column=0, columnspan=taille * 2, padx=5, pady=5)
            else:   # Si le joueur n'a pas réussi
                reussi_label = Label(frame, text="Vous avez perdu!", font=("Helvetica", 14), fg="red")
                reussi_label.grid(row=taille * 2 + 1, column=0, columnspan=taille * 2, padx=5, pady=5)

        buton_valider = Button(frame, text="Valider", width=15, fg="dark blue", bg="#F0F0F0", font=("Trebuchet MS", 11),
                               command=create_and_validate)
        buton_valider.grid(row=taille * 2, column=0, columnspan=taille * 2, padx=5, pady=5)


def creer_reponse_grille(hint_grille):
    reponse_grille = hint_grille  # Initialise reponse_grille avec hint_grille
    entry_indexes = {}  # Dictionnaire pour stocker les index correspondant aux Entry
    for widget in frame.winfo_children():    # Trouve les index correspondant aux Entry
        if isinstance(widget, Entry):
            row = widget.grid_info()['row'] // 2  # Trouve la ligne où se trouve l'Entry
            column = widget.grid_info()['column'] // 2  # Trouve la colonne où se trouve l'Entry
            entry_indexes[widget] = (row, column)  # Stocke la ligne et la colonne correspondant à l'Entry
    for widget, (row, column) in entry_indexes.items():    # Place les valeurs entrées dans les Entry dans reponse_grille
        value = widget.get()  # Récupère la valeur entrée dans l'Entry
        if value.isdigit():  # Si la valeur entrée est un nombre
            reponse_grille[row][column] = int(value)  # Ajoute le nombre dans la cellule correspondante

    print(reponse_grille)  # Affiche reponse_grille
    return reponse_grille

def creer_board_list(taille_du_tableau): # Crée une liste pour le tableau
    board = []
    taille = int(taille_du_tableau[0])
    for i in range(taille):
        ligne = []
        for j in range(taille):
            ligne.append(0)
        board.append(ligne)
    return board

# Cadre principal contenant le tableau et les boutons
main_frame = Frame(root)
main_frame.pack()

# Ajout du tableau
frame = Frame(root)  # creer une frame couvrant tableau
frame.pack(padx=20, pady=40)  # on utilise padx et pady pour regler les espaces autour du tableau
taille = int(taille_du_tableau[0])

# Version avec notre propre solveur
if solveur == "Notre Solveur":
    jeu_grille, signes, hint_grille = generer_jeu_valide(taille, mode)  # Creation du Table du Jeu
    print_board(jeu_grille, signes, hint_grille, taille)

#version avec minisat22
else:
    jeu_grille, signes, hint_grille = generer_jeu_valide_sat(taille, mode)  # Creation du Table du Jeu
    print_board(jeu_grille, signes, hint_grille, taille)


################# Affichage/Utilisation des boutons #################

# Cadre contenant les boutons
button_frame = Frame(main_frame)
button_frame.pack()

bouton_resoudre = Button(button_frame, text="Resoudre", width=15, fg="dark blue", bg="light gray",
                         font=("Trebuchet MS", 15), command=lambda: bouton_resoudre_click(frame, taille))
bouton_resoudre.pack(side=LEFT, padx=1, pady=1)

bouton_nouveauJeu = Button(button_frame, text="Nouveau Jeu", width=15, fg="dark blue", bg="light gray",
                           font=("Trebuchet MS", 15), command=lambda: bouton_nouveauJeu_click(frame, taille, mode))
bouton_nouveauJeu.pack(side=LEFT, padx=1, pady=1)

bouton_effacer = Button(button_frame, text="Effacer", width=15, fg="dark blue", bg="light gray",
                        font=("Trebuchet MS", 15), command=lambda: bouton_effacer_click(frame, taille))
bouton_effacer.pack(side=LEFT, padx=1, pady=1)

bouton_changerMusic = Button(button_frame, text="Changer Musique", width=15, fg="dark blue", bg="light gray",
                             font=("Trebuchet MS", 15), command=bouton_changerMusic_click)
bouton_changerMusic.pack(side=LEFT, padx=1, pady=1)

bouton_on_off_Music = Button(button_frame, text="On/Off Musique", width=15, fg="dark blue", bg="light gray",
                             font=("Trebuchet MS", 15), command=bouton_on_off_Music_click)
bouton_on_off_Music.pack(side=LEFT, padx=1, pady=1)

root.mainloop()  # affichage de la fenêtre
