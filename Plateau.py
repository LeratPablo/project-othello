import pygame
import os
import sys
import time
import random
import ast

from pygame import constants

# creation de la classe Tableau qui contient la grille et ses fonction + les pions des joueurs

class Tableau:

    def __init__(self):

        # Les différentes dimensions utilisées
        self.width = 800
        self.colonne = 8
        self.ligne = 8

        # Les différentes couleurs utilisées
        self.couleur_ligne = (0, 175, 145)
        self.bg_color = (24, 77, 71)
        self.pion_noir = (34, 40, 49)
        self.pion_blanc = (221, 221, 221)

        # Les paramètres des dimensions des pions
        self.circle_radius = 35
        self.circle_width = 35

        # La grille et les pions de bases
        self.grille = [[0 for _ in range(self.ligne)] for _ in range(self.colonne)]
        self.grille[3][3] = 2
        self.grille[3][4] = 1
        self.grille[4][3] = 1
        self.grille[4][4] = 2

        self.directions = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))

        # D'autres variables utiles 
        self.gagnant = ""
        self.fin = False
        self.joueur = 1
        self.fps = 60
        self.secondes = 0
        self.minutes = 0
        self.heures = 0


    def dessine_tableau(self, fenetre):
        '''Cette fonction permet de créer le tableau et de l'afficher'''
        for x in range(0, 9):
            pygame.draw.line(fenetre, self.couleur_ligne, (0, x * 100), (self.width, x * 100), 15)
            pygame.draw.line(fenetre, self.couleur_ligne, (x * 100, 0), (x * 100, self.width), 15)


    def place_pion(self, lig, col, joueur):
        '''Cette fonction permet de placer un pion dans le tableau en placant un numero en fonction du joueur (Soit 1, soit 2)'''
        self.grille[lig][col] = joueur

        for direc in self.directions:
            voisins = [lig + direc[0], col + direc[1]]
            while 0 <= voisins[0] <= 7 and 0 <= voisins[1] <= 7:
                if self.grille[voisins[0]][voisins[1]] == joueur:
                    self.retourne_pion(joueur, lig, col, direc)
                    break

                voisins[0] += direc[0]
                voisins[1] += direc[1]


    def retourne_pion(self, joueur, lig, col, direction):
        '''Cette fonction permet de retourner les pions lorsqu'un joueur joue'''
        voisins = [lig + direction[0], col + direction[1]]
        while self.grille[voisins[0]][voisins[1]] == self.autre_joueur(joueur):
            self.grille[voisins[0]][voisins[1]] = joueur

            voisins[0] += direction[0]
            voisins[1] += direction[1]


    def autre_joueur(self, joueur):
        '''Cette fonction retourne le joueur inverse de celui qui joue'''
        return 2 if joueur == 1 else 1


    def coup_valide(self, joueur, lig, col):
        '''Cette fonction renvoie True si une case est jouable ou non'''
        if self.grille[lig][col] != 0:
            return False
        
        for direc in self.directions:
            voisins = [lig + direc[0], col + direc[1]]
            while 0 < voisins[0] < 7 and 0 < voisins[1] < 7 and self.grille[voisins[0]][voisins[1]] == self.autre_joueur(joueur):
                voisins[0] += direc[0]
                voisins[1] += direc[1]

                if self.grille[voisins[0]][voisins[1]] == joueur:
                    return True
        return False


    def affiche_coup_possible(self, joueur, fenetre):
        '''Cette fonction permet de placer des marqueur sur la grille, indiquant les coups possibles'''
        for lig in range(self.ligne):
            for col in range(self.colonne):
                pygame.draw.circle(fenetre, self.bg_color, (int(col * self.width / 8 + 50), int(lig * self.width / 8 + 50)), int(self.circle_radius / 4), int(self.circle_width / 4))
                if self.coup_valide(joueur, lig, col) and self.grille[lig][col] == 0:
                    pygame.draw.circle(fenetre, self.couleur_ligne, (int(col * self.width / 8 + 50), int(lig * self.width / 8 + 50)), int(self.circle_radius / 4), int(self.circle_width / 4))


    def meilleurs_coup(self, joueur):
        '''Cette fonction permet a l'IA de placer des pions et de jouer des coups'''
        
        liste_meilleurs_coup = []
        coup_valide = []
        
        for lig in range(self.ligne):
            for col in range(self.colonne):
                if self.coup_valide(joueur, lig, col):
                    coup_valide.append((lig, col))
        
        for c in coup_valide:
            n_max = 0
            for direc in self.directions:
                voisins = [c[0] + direc[0], c[1] + direc[1]]
                n = 0
                while 0 <= voisins[0] <= 7 and 0 <= voisins[1] <= 7 and self.grille[voisins[0]][voisins[1]] == self.autre_joueur(joueur):
                    n += 1
                    voisins[0] += direc[0]
                    voisins[1] += direc[1]

                    if 0 <= voisins[0] <= 7 and 0 <= voisins[1] <= 7:
                        if self.grille[voisins[0]][voisins[1]] == joueur:
                            n_max += n
                            break
            
            liste_meilleurs_coup.append((c[0], c[1], n_max))
            liste_meilleurs_coup.sort(key=lambda x:x[2], reverse=1)
            for x in liste_meilleurs_coup:
                if x[2] < liste_meilleurs_coup[0][2]:
                    liste_meilleurs_coup.remove(x)

        if liste_meilleurs_coup != []:
            liste = random.randint(0, len(liste_meilleurs_coup) - 1)
            self.place_pion(liste_meilleurs_coup[liste][0], liste_meilleurs_coup[liste][1], joueur)

    
    def fini(self, joueur):
        '''Cette fonction renvoie False si il n'y a plus de coups possible, True sinon'''
        for lig in range(self.ligne):
            for col in range(self.colonne):
                if self.coup_valide(joueur, lig, col):
                    return True
        return False


    def dessin_pion(self, fenetre):
        '''Cette fonction permet de dessiner les pions lorsque qu'un joueur joue'''
        for lig in range(self.ligne):
            for col in range(self.colonne):
                if self.grille[lig][col] == 1:
                    pygame.draw.circle(fenetre, self.pion_noir, (int(col * self.width / 8 + 50), int(lig * self.width / 8 + 50)), self.circle_radius, self.circle_width)

                if self.grille[lig][col] == 2:
                    pygame.draw.circle(fenetre, self.pion_blanc, (int(col * self.width / 8 + 50), int(lig * self.width / 8 + 50)), self.circle_radius, self.circle_width)


    def case_libre(self, lig, col):
        '''Cette fonction renvoie True si la case selectionner est libre et False sinon'''
        return self.grille[lig][col] == 0


    def sauvegarde(self):
        '''Cette fonction permet de sauvegarder la partie en cour'''
        save = open("save.txt", "w")
        save.write(str(self.grille) + "/" + str(self.joueur))


    def boucle_principale_JvsJ(self, fenetre, tableau, interface):
        '''Cette fonction contient la boucle principale du jeu lors du jeu contre un 2eme joueur humain'''
        self.joueur = 1
        self.fin = False
        clock = pygame.time.Clock()
        fps_ = clock.get_fps()
        # constante = 1 / self.fps

        while not self.fin:

            print(fps_)
            # try:
            #     constante = 1 / fps_
            #     clock.tick(self.fps)
            #     self.secondes += constante
            # except ZeroDivisionError:
            #     continue


            interface.nb_pion(fenetre, tableau.grille)
            interface.joueur_actuel(self.joueur, fenetre)
            interface.affiche_temps(fenetre, int(self.secondes), int(self.minutes), int(self.heures))

            tableau.affiche_coup_possible(self.joueur, fenetre)
            tableau.dessin_pion(fenetre)

            if self.secondes >= 60:
                self.secondes = 0
                self.minutes += 1
            if self.minutes >= 60:
                self.minutes = 0
                self.heures += 1

            if not tableau.fini(self.joueur):
                pygame.display.set_caption("Partie terminée")
                pion_noir = 0
                pion_blanc = 0
                self.fin = True

                for lig in range(self.ligne):
                    for col in range(self.colonne):
                        if self.grille[lig][col] == 1:
                            pion_noir += 1
                        elif self.grille[lig][col] == 2:
                            pion_blanc += 1

                if pion_noir > pion_blanc:
                    self.gagnant = 1
                if pion_blanc > pion_noir:
                    self.gagnant = 2
                if pion_noir == pion_blanc:
                    self.gagnant = 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_s:
                        self.sauvegarde()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_X = event.pos[0]
                    mouse_Y = event.pos[1]

                    colonne_selectionne = int(mouse_X // 100)
                    ligne_selectionne = int(mouse_Y // 100)

                    if colonne_selectionne <= 7 and ligne_selectionne <= 7:
                        if tableau.coup_valide(self.joueur, ligne_selectionne, colonne_selectionne):
                            if self.joueur == 1:
                                tableau.place_pion(ligne_selectionne, colonne_selectionne, 1)
                                self.joueur = 2
                            else:
                                if self.joueur == 2:
                                    tableau.place_pion(ligne_selectionne, colonne_selectionne, 2)
                                    self.joueur = 1

            pygame.display.update()

    def boucle_principale_JvsJ_save(self, fenetre, tableau, interface, grille, joueur):
        '''Cette fonction contient la boucle principale du jeu lors du jeu contre un 2eme joueur humain à partir d'une partie sauvegardé'''
        self.joueur = joueur
        self.grille = grille
        self.fin = False
        clock = pygame.time.Clock()
        # constante = 1 / self.fps

        while not self.fin:

            try:
                constante = 1 / fps
            except ZeroDivisionError:
                continue

            clock.tick(self.fps)
            self.secondes += constante

            interface.nb_pion(fenetre, tableau.grille)
            interface.joueur_actuel(self.joueur, fenetre)
            interface.affiche_temps(fenetre, int(self.secondes), int(self.minutes), int(self.heures))

            tableau.affiche_coup_possible(self.joueur, fenetre)
            tableau.dessin_pion(fenetre)

            if self.secondes >= 60:
                self.secondes = 0
                self.minutes += 1
            if self.minutes >= 60:
                self.minutes = 0
                self.heures += 1

            if not tableau.fini(self.joueur):
                pygame.display.set_caption("Partie terminée")
                pion_noir = 0
                pion_blanc = 0
                self.fin = True

                for lig in range(self.ligne):
                    for col in range(self.colonne):
                        if self.grille[lig][col] == 1:
                            pion_noir += 1
                        elif self.grille[lig][col] == 2:
                            pion_blanc += 1
                
                if pion_noir > pion_blanc:
                    self.gagnant = 1
                if pion_blanc > pion_noir:
                    self.gagnant = 2
                if pion_noir == pion_blanc:
                    self.gagnant = 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_s:
                        self.sauvegarde()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_X = event.pos[0]
                    mouse_Y = event.pos[1]

                    colonne_selectionne = int(mouse_X // 100)
                    ligne_selectionne = int(mouse_Y // 100)

                    if colonne_selectionne <= 7 and ligne_selectionne <= 7:
                        if tableau.coup_valide(self.joueur, ligne_selectionne, colonne_selectionne):
                            if self.joueur == 1:
                                tableau.place_pion(ligne_selectionne, colonne_selectionne, 1)
                                self.joueur = 2                            
                            else:
                                if self.joueur == 2:
                                    tableau.place_pion(ligne_selectionne, colonne_selectionne, 2)
                                    self.joueur = 1

            pygame.display.update()


    def boucle_principale_JvsIA(self, fenetre, tableau, interface):
        '''Cette fonciton contient la boucle principale du jeu lors du jeu contre l'IA'''
        self.joueur = 1
        self.fin = False
        clock = pygame.time.Clock()
        # constante = 1 / self.fps

        while not self.fin:

            try:
                constante = 1 / fps
            except ZeroDivisionError:
                continue

            clock.tick(self.fps)
            self.secondes += constante

            interface.nb_pion(fenetre, tableau.grille)
            interface.joueur_actuel(self.joueur, fenetre)
            interface.affiche_temps(fenetre, int(self.secondes), int(self.minutes), int(self.heures))

            tableau.affiche_coup_possible(self.joueur, fenetre)
            tableau.dessin_pion(fenetre)

            if self.secondes >= 60:
                self.secondes = 0
                self.minutes += 1
            if self.minutes >= 60:
                self.minutes = 0
                self.heures += 1

            if not tableau.fini(self.joueur):
                pygame.display.set_caption("Partie terminée")
                pion_noir = 0
                pion_blanc = 0
                self.fin = True
 
                for lig in range(self.ligne):
                    for col in range(self.colonne):
                        if self.grille[lig][col] == 1:
                            pion_noir += 1
                        elif self.grille[lig][col] == 2:
                            pion_blanc += 1
                
                if pion_noir > pion_blanc:
                    self.gagnant = 1
                if pion_blanc > pion_noir:
                    self.gagnant = 2
                if pion_noir == pion_blanc:
                    self.gagnant = 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_X = event.pos[0]
                    mouse_Y = event.pos[1]

                    colonne_selectionne = int(mouse_X // 100)
                    ligne_selectionne = int(mouse_Y // 100)

                    if colonne_selectionne <= 7 and ligne_selectionne <= 7:
                        if tableau.coup_valide(self.joueur, ligne_selectionne, colonne_selectionne):
                            if self.joueur == 1:
                                tableau.place_pion(ligne_selectionne, colonne_selectionne, 1)
                                self.joueur = 2
                            
            if self.joueur == 2:
                self.meilleurs_coup(self.joueur)
                self.joueur = 1

            pygame.display.update()


    def boucle_principale_IAvsIA(self, fenetre, tableau, interface):
        '''Cette fonciton contient la boucle principale du jeu lors du jeu IA contre IA'''
        self.joueur = 1
        self.fin = False
        clock = pygame.time.Clock()

        while not self.fin:

            clock.tick(5)
            interface.nb_pion(fenetre, tableau.grille)
            interface.joueur_actuel(self.joueur, fenetre)

            tableau.dessin_pion(fenetre)

            if not tableau.fini(self.joueur):
                pygame.display.set_caption("Partie terminée")
                pion_noir = 0
                pion_blanc = 0
                self.fin = True

                for lig in range(self.ligne):
                    for col in range(self.colonne):
                        if self.grille[lig][col] == 1:
                            pion_noir += 1
                        elif self.grille[lig][col] == 2:
                            pion_blanc += 1
                
                if pion_noir > pion_blanc:
                    self.gagnant = 1
                if pion_blanc > pion_noir:
                    self.gagnant = 2
                if pion_noir == pion_blanc:
                    self.gagnant = 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            if self.joueur == 1:
                self.meilleurs_coup(self.joueur)
                self.joueur = 2

            if self.joueur == 2:
                self.meilleurs_coup(self.joueur)
                self.joueur = 1

            pygame.display.update()
        
        time.sleep(2)


# Creation de la classe GUI qui permet l'affichages du score et autres informations

class GUI:

    def __init__(self):

        # Dimensions de la grille
        self.colonne = 8
        self.ligne = 8

        # Différentes couleurs utilisées
        self.couleur_ligne = (0, 175, 145)
        self.bg_color = (24, 77, 71)
        self.pion_noir = (34, 40, 49)
        self.pion_blanc = (221, 221, 221)

        self.circle_radius = 50
        self.circle_width = 50


    def joueur_actuel(self, joueur, fenetre):
        '''Cette fonction permet d'afficher a l'écran le joueur actuel'''

        if joueur == 1:
            pygame.draw.circle(fenetre, self.pion_noir, (1000, 650), int(self.circle_radius * 1.5), int(self.circle_width * 1.5))
        if joueur == 2:
            pygame.draw.circle(fenetre, self.pion_blanc, (1000, 650), int(self.circle_radius * 1.5), int(self.circle_width * 1.5))


    def nb_pion(self, fenetre, grille):
        '''Cette fonction permet de comptabiliser le nombre de pions de chaque joueur'''

        pion_noir = 0
        pion_blanc = 0
        for lig in range(self.ligne):
            for col in range(self.colonne):
                if grille[lig][col] == 1:
                    pion_noir += 1
                if grille[lig][col] == 2:
                    pion_blanc += 1
        self.affiche_nb_pion(str(pion_noir), str(pion_blanc), fenetre)
        return (pion_noir, pion_blanc)


    def affiche_nb_pion(self, nb_pion_noir, nb_pion_blanc, fenetre):
        '''Cette fonction permet d'afficher a l'écran le nombre de pion de chaque joueur'''

        my_font2 = pygame.font.SysFont('liberationsansnarrow', 30, bold = 1)

        pygame.draw.rect(fenetre, self.bg_color, (1088, 300, 45, 30))
        pygame.draw.rect(fenetre, self.bg_color, (1105, 400, 45, 30))

        nb_pion_noir = my_font2.render(f'Nombre de pions noir: {nb_pion_noir}', False, (0, 0, 0))
        fenetre.blit(nb_pion_noir, (820,300))

        nb_pion_blanc = my_font2.render(f'Nombre de pions blanc: {nb_pion_blanc}', False, (0, 0, 0))
        fenetre.blit(nb_pion_blanc, (820,400))

    def affiche_temps(self, fenetre, secondes, minutes, heures):
        '''Cette fonction permet d'afficher le temps de la partie'''
        my_font = pygame.font.SysFont('liberationsansnarrow', 30, bold = 1)

        pygame.draw.rect(fenetre, self.bg_color, (955, 50, 100, 30))
        pygame.draw.rect(fenetre, self.bg_color, (930, 100, 100, 30))
        pygame.draw.rect(fenetre, self.bg_color, (920, 150, 100, 30))

        secondes = my_font.render(f'Secondes : {secondes}', False, (0, 0, 0))
        fenetre.blit(secondes, (820,50))

        minutes = my_font.render(f'Minutes : {minutes}', False, (0, 0, 0))
        fenetre.blit(minutes, (820,100))

        heures = my_font.render(f'Heures : {heures}', False, (0, 0, 0))
        fenetre.blit(heures, (820,150))