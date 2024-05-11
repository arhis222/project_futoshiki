import sys
import subprocess
import os
from tkinter import *
import pygame
import os.path
import time

###########################IMPORTANT NOTE#####################################
#################################################################################
# Obtenir le chemin du module pygame en partant du répertoire actuel (SI C'EST DIFFERENT MÉTTRE VOTRE PROPRE CHEMIN )
pygame_path = os.path.abspath("venv/include/site/python3.7/pygame")

#Si on a une erreur lorsqu'on essaye de importer pygame mettre/enlever les commentaires ci dessous
# Appeler subprocess en ajoutant le chemin du module pygame à PYTHONPATH
# subprocess.call(["python", "-m", "pip", "install", "pygame"], env=dict(os.environ, PYTHONPATH=pygame_path))
# Installer pygame manuelement pour éviter une erreur d'importation de Pygame dans deux fichiers distincts
###############################################################################

# Initialisation de la variable de résolution

pygame.init()
pygame.mixer.init()

#####################Les Boutons de main menu###################

# Lancement de l'effet sonore du clic
click_sound = pygame.mixer.Sound("music/clickButton.mp3")

# Une varibale pour poursuivre l'état du musique (on/off)
est_musique = True

def musique_on_off_click():
    global est_musique
    click_sound.play()  # Lancement de l'effet sonore du clic

    if est_musique:
        pygame.mixer.music.pause()  # Pauser la musiqe
        est_musique = False  # mettre à jour l'état de la musique
    else:
        pygame.mixer.music.unpause()  # Continuer la musique
        est_musique = True  # mettre à jour l'état de la musique

def bouton_Jouer_click():
    click_sound.play() # Lancement de l'effet sonore du clic
    time.sleep(0.4)  # attendre 0.4 sec
    pygame.display.quit()  # fermer la fenêtre du main menu (pygame)

    init_tkinter_()  # Ouvrir la fenêtre du jeu (tkinter)
    pygame.quit() #fermer le Pygame


# Fonction ce qu'on utilise pour faire commencer la jeu en choissisant un solveur, une mode du jeu ,taille du tableau
def init_tkinter_():
    # Création de la fenêtre principale Tkinter pour choisir le solveur
    pygame.init()
    root = Tk()  # Création de la fenêtre principale Tkinter
    root.title("Choix du solveur")  # Définition du titre de la fenêtre
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Définition des dimensions et de la position de la fenêtre
    root.configure(bg="#23262B")  # Configuration de la couleur de fond de la fenêtre

    # Étiquette pour indiquer le choix du solveur
    label = Label(root, text="Choisissez le solveur", bg="#23262B", fg="white", font=("Fixedsys", 25, "bold"))  # Création de l'étiquette
    label.pack()  # Placement de l'étiquette dans la fenêtre

    def select_solver(solver):
        click_sound.play()  # Lancement de l'effet sonore du clic
        time.sleep(0.5)  # Attente de 0,5 seconde

        root.destroy()  # Fermeture de la fenêtre principale

        # Création de la fenêtre Tkinter pour choisir le mode de jeu après avoir choisi le solveur
        mode_root = Tk()  # Création de la fenêtre pour choisir le mode de jeu
        mode_root.title("Choix du mode de jeu")  # Définition du titre de la fenêtre
        mode_root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Définition des dimensions et de la position de la fenêtre
        mode_root.configure(bg="#23262B")  # Configuration de la couleur de fond de la fenêtre

        # Étiquette pour indiquer le choix du mode de jeu
        mode_label = Label(mode_root, text="Choisissez le mode de jeu", bg="#23262B", fg="white", font=("Fixedsys", 25, "bold"))  # Création de l'étiquette
        mode_label.pack()  # Placement de l'étiquette dans la fenêtre

        def select_mode(mode):
            click_sound.play()  # Lancement de l'effet sonore du clic
            time.sleep(0.5)  # Attente de 0,5 seconde

            mode_root.destroy()  # Fermeture de la fenêtre de sélection du mode de jeu

            # Création de la fenêtre Tkinter pour choisir la taille du tableau après avoir choisi le mode de jeu
            size_root = Tk()  # Création de la fenêtre pour choisir la taille du tableau
            size_root.title("Choix de la taille du tableau")  # Définition du titre de la fenêtre
            size_root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Définition des dimensions et de la position de la fenêtre
            size_root.configure(bg="#23262B")  # Configuration de la couleur de fond de la fenêtre

            # Étiquette pour indiquer le choix de la taille du tableau
            size_label = Label(size_root, text="Choisissez la taille du tableau", bg="#23262B", fg="white", font=("Fixedsys", 25, "bold"))  # Création de l'étiquette
            size_label.pack()  # Placement de l'étiquette dans la fenêtre

            def start_game(size):
                click_sound.play()  # Lancement de l'effet sonore du clic
                time.sleep(0.5)  # Attente de 0,5 seconde

                global jeu_solveur_selectionne, jeu_mode_selectionne, jeu_taille_selectionne
                jeu_solveur_selectionne = solver  # Sélection du solveur
                jeu_mode_selectionne = mode  # Sélection du mode de jeu
                jeu_taille_selectionne = f"{size}x{size}"  # Sélection de la taille du tableau
                size_root.destroy()  # Fermeture de la fenêtre de sélection de la taille du tableau

                pygame.quit()  # Fermeture de Pygame
                try:
                    # Appel de subprocess en ajoutant le chemin du module pygame à PYTHONPATH
                    # Ouvrir le fichier jeu.py avec l'argument taille_du_tableau et mode
                    subprocess.call(["python", "jeu.py", "--taille", jeu_taille_selectionne, "--mode", jeu_mode_selectionne, "--solveur", jeu_solveur_selectionne], env=dict(os.environ, PYTHONPATH=pygame_path))
                except Exception as e:
                    print("Erreur:", e)

            button_positions = [(150, 100), (470, 100), (150, 220), (470, 220), (150, 340), (470, 340), (310, 460)]
            button_width = 10
            button_height = 2

            for i in range(3, 10):
                button_text = f"{i}x{i}"  # Texte du bouton représentant la taille du tableau
                button = Button(size_root, text=button_text, command=lambda size=i: start_game(size), bg="#23262B", fg="#ba321a", width=button_width, height=button_height, font=("Fixedsys", 20,"bold"))  # Création du bouton
                button.place(x=button_positions[i - 3][0], y=button_positions[i - 3][1])  # Placement du bouton dans la fenêtre

        button_positions = [(265, 100), (265, 210), (265, 320), (265, 430)]
        button_width = 15
        button_height = 2
        mode_buttons = ["entrainement", "facile", "moyen", "difficile"]  # Options de mode de jeu
        colors = ["#5ec40a", "#1d9914", "#c97214", "#cc0606"]  # Couleurs des boutons de mode de jeu
        for idx, mode in enumerate(mode_buttons):
            mode_button = Button(mode_root, text=mode, command=lambda m=mode: select_mode(m), bg="#23262B", fg=colors[idx], width=button_width, height=button_height, font=("Fixedsys", 20,"bold"))  # Création du bouton
            mode_button.place(x=button_positions[idx][0], y=button_positions[idx][1])  # Placement du bouton dans la fenêtre

    button_positions = [(265, 170), (265, 310)]
    button_width = 15
    button_height = 2
    solver_buttons = ["Minisat22", "Notre Solveur"]  # Options de solveur

    # Boucle pour créer les boutons pour chaque solveur
    for idx, solver in enumerate(solver_buttons):
        solver_button = Button(root, text=solver, command=lambda s=solver: select_solver(s), bg="#23262B", fg="#14c920", width=button_width, height=button_height, font=("Fixedsys", 20,"bold"))  # Création du bouton
        solver_button.place(x=button_positions[idx][0], y=button_positions[idx][1])  # Placement du bouton dans la fenêtre

    root.mainloop()  # Lancement de la boucle principale Tkinter





##################### Partie musique #######################

def jouerMusic(nom_music, volume):
    pygame.mixer.music.load(nom_music)
    pygame.mixer.music.play(loops=-1)  # Pour ce qu'il joue tout le temps
    pygame.mixer.music.set_volume(volume)

# Initialise une musique pour le menu principal
jouerMusic("music/main_menu_theme.mp3", 0.4)

#########################Partie main menu #############################

# Taille de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Création de l'écran Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Définition des polices et couleurs
font_titre = pygame.font.Font("CustomFonts/Sankyu.ttf", 80)
font_text = pygame.font.Font("CustomFonts/Fixedsys.ttf", 15)
TITRE_COL = (218, 112, 214) # Couleur du titre (rose)
TEXT_COL = (162, 166, 171) # Couleur du texte (blanc)
# Fonction pour écrire du texte sur l'écran
def ecrire_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

run = True
while run:
    screen.fill((35, 38, 41))  # Couleur de fond

    # Dessine des boutons
    button_texts = ["JOUER", "MUSIQUE", "QUITTER"]
    button_rects = [pygame.Rect(302, 300 + i * 50, 200, 35) for i in range(len(button_texts))] #Rectangle transparent (pour mesurer aire du clic) du chaque button

    for i, text in enumerate(button_texts): # On utilse enumarate pour avoir les index aussi
        rect = button_rects[i]
        pygame.draw.rect(screen, (35, 38, 41), rect)  # Couleur du bouton (arrière-plan)

        # Écrire du texte du bouton à l'écran
        font = pygame.font.Font("CustomFonts/Fixedsys.ttf", 40)
        text_surface = font.render(text, True, (255, 255, 255))  # Téxte de couleur blanche
        text_rect = text_surface.get_rect(center=rect.center) # Listes des textes pour printer dans les rectangles indiqués
        screen.blit(text_surface, text_rect) # Combiner les deux

    # Écrire des autres textes à l'écran
    ecrire_text("FUTOSHIKI", font_titre, TITRE_COL, 185, 100)
    ecrire_text("Arhan UNAY", font_text, TEXT_COL, 10, 545)
    ecrire_text("Utku GEMICIOGLU", font_text, TEXT_COL, 10, 560)
    ecrire_text("Kivanc GULTEKIN", font_text, TEXT_COL, 10, 575)


    # Gestion des evenements
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:  # Détection du clic de la souris
            if event.button == 1:  # Bouton de souris gauche
                mouse_pos = event.pos # Avoir la position du souris quand on clic
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):  # Vérification si la position de la souris est à l'intérieur du rectangle du bouton
                        if button_texts[i] == "JOUER":
                            print("Ouverture de l'écran de jeu...")  # Action pour ouvrir l'écran de jeu
                            bouton_Jouer_click()
                        elif button_texts[i] == "MUSIQUE":
                            print("Ouverture de l'écran de réglages...")  # Action pour ouvrir l'écran de réglages
                            musique_on_off_click()
                        elif button_texts[i] == "QUITTER":
                            click_sound.play()  # Lancement de l'effet sonore du clic
                            time.sleep(0.4)  # attendre 0.4 sec
                            run = False  # Quitter la boucle principale

        elif event.type == pygame.QUIT: # Pour fermer la fenêtre avec la signe x en haut droite
            run = False  # Quitter la boucle principale

    # Mise à jour de l'affichage
    pygame.display.update()

pygame.quit()  # Fermer la fenêtre Pygame


