import os
import ast
import sys
import pygame

import Plateau
import GUI

os.environ['SDL_VIDEO_CENTERED'] = '1'

save = open("save.txt", "r")

# Création de la fenetre du menu
pygame.init()
pygame.display.set_caption("Othello")
fenetre_menu = pygame.display.set_mode((800, 800)) # fenetre de l'écran du menu
fenetre_menu.fill((24, 77, 71))

menu = GUI.Menu(fenetre_menu)
menu.boucle_principale()

# création de la fenêtre du plateau
if menu.fin:
    tableau = Plateau.Tableau()
    fenetre = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("OTHELLO")
    fenetre.fill((24, 77, 71))

    tableau.dessine_tableau(fenetre)
    affichage = Plateau.GUI()

    if menu.etat == 3:
        tableau.boucle_principale_JvsJ(fenetre, tableau, affichage)

    if menu.etat == 4:
       tableau.boucle_principale_JvsIA(fenetre, tableau, affichage)

    if menu.etat == 5:
        tableau.boucle_principale_IAvsIA(fenetre, tableau, affichage)

    if menu.etat == 6:
        if os.path.getsize("save.txt") > 0: # Vérifie que le fichier de suvegarde n'est pas vide
            # Lecture du fichier
            grille = ""
            j = ""
            for x in save:
                j += str(x)
                for i in x:
                    if i == "/":
                        grille = ast.literal_eval(grille)
                        j = int(j[-1])
                        break
                    else:
                        grille = grille + i
            tableau.boucle_principale_JvsJ_save(fenetre, tableau, affichage, grille, j)
        else:
            print("Pas de sauvegarde disponible")


fenetre_victoire = pygame.display.set_mode((800, 800))
fenetre_menu.fill((24, 77, 71))

if tableau.fin:
    ecran_victoire = GUI.Gagnant(tableau.gagnant, fenetre, tableau.gagnant)
    ecran_victoire.affichage()