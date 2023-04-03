import pygame
import sys

# creation de la classe GUI permettant l'affichage du menu et de l'écran de victoire


# creation de la classe boutton
class Boutton:

    def __init__(self, fenetre, couleur_boutton, couleur_texte, hover_color, x, y, x_txt, y_txt, width, eight, label):

        self.fenetre = fenetre
        
        # Différentes couleurs des bouttonts
        self.couleur = couleur_boutton
        self.hover_color = hover_color

        # Différentes dimensions des bouttons
        self.x = x
        self.y = y
        self.x_txt = x_txt
        self.y_txt = y_txt
        self.width = width
        self.eight = eight

        # Police d'écriture des boutons
        self.font = pygame.font.SysFont('Corbel',100)
        self.label = self.font.render(label , True , couleur_texte)

    def affiche(self, mouse_pos):
        '''Cette fonction affiche et anime les bouttons'''

        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.eight:
            pygame.draw.rect(self.fenetre, (24, 77, 71), (self.x + 5, self.y + 5, self.width, self.eight))
            pygame.draw.rect(self.fenetre, self.couleur, (self.x, self.y, self.width, self.eight))
            self.fenetre.blit(self.label, (self.x_txt, self.y_txt))
        else:
            pygame.draw.rect(self.fenetre, (0, 121, 101), (self.x + 5, self.y + 5, self.width, self.eight))
            pygame.draw.rect(self.fenetre, self.couleur, (self.x, self.y, self.width, self.eight))
            self.fenetre.blit(self.label, (self.x_txt, self.y_txt))


# Création de la classe Menu
class Menu:

    def __init__(self, fenetre):

        self.fenetre = fenetre
        
        # Dimension du menu
        self.width = 800
        self.eight = 800

        self.bg_color = (24, 77, 71)

        self.fin = False
        self.etat = None

        self.font = pygame.font.SysFont('Corbel', 50)
        self.text = self.font.render("", True, (37, 37, 37))

    def texte(self):
        '''Cette fonction permet d'afficher le texte présent sur la page'''
        font1 = pygame.font.SysFont('Corbel', 200)
        font2 = pygame.font.SysFont('Corbel', 40)
        titre = font1.render("Othello", True, (37, 37, 37))
        credit = font2.render(("Fait par Gabriel et Ilian. Astro Company" u"\u00A9" " 2018 - 2021"), True, (37, 37, 37))
        self.fenetre.blit(titre, (160, 20))
        self.fenetre.blit(credit, (40, 750))


    def update(self):
        '''Cette fonction permet de mettre a jour le menu'''
        if self.etat == 1:
            self.fenetre.fill((24, 77, 71))
            self.texte()
        if self.etat == 2:
            self.fenetre.fill((24, 77, 71))
            self.texte()


    def mode(self):
        '''Cette fonction renvoie l'état du menu, permettant de savoir quels actions effectuer'''
        return self.etat


    def boucle_principale(self):
        '''Cette fonctions contient la boucle principale du menu'''

        boutton_jouer = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 250, 300, 300, 320, 300, 100, "Jouer")
        boutton_quitter = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 50, 500, 80, 520, 300, 100, "Quitter")
        boutton_regles = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 450, 500, 490, 520, 300, 100, "Règles")

        boutton_JvsJ = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 50, 300, 100, 320, 300, 100, "J vs J")
        boutton_JvsIA = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 450, 300, 490, 320, 300, 100, "J vs IA")
        boutton_IAvsIA = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 450, 500, 480, 520, 300, 100, "IA vs IA")

        self.texte()
        clock = pygame.time.Clock()

        while not self.fin:

            clock.tick(60)
            mouse = pygame.mouse.get_pos()
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_c: # Partie sauvegardé JvsJ
                        self.etat = 6
                        self.fin = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 50 < mouse[0] < 350 and 500 < mouse[1] < 600: # click pour Quitter
                        sys.exit()

                    if 250 < mouse[0] < 550 and 300 < mouse[1] < 400 and self.etat == None: # click pour Jouer
                        self.etat = 1

                    if 450 < mouse[0] < 750 and 500 < mouse[1] < 600 and self.etat == None: # click pour Règles
                        self.etat = 2

                    if 50 < mouse[0] < 350 and 300 < mouse[1] < 400 and self.etat == 1: # click pour J vs J
                        self.etat = 3
                        self.fin = True

                    if 450 < mouse[0] < 750 and 300 < mouse[1] < 400 and self.etat == 1: # click pour J vs IA
                        self.etat = 4
                        self.fin = True

                    if 450 < mouse[0] < 750 and 500 < mouse[1] < 600 and self.etat == 1: # click pour IA vs IA
                        self.etat = 5
                        self.fin = True

            if self.etat == None:
                boutton_jouer.affiche(mouse)
                boutton_regles.affiche(mouse)

            if self.etat == 1:
                boutton_JvsJ.affiche(mouse)
                boutton_JvsIA.affiche(mouse)
                boutton_IAvsIA.affiche(mouse)

            if self.etat == 2:
                my_font = pygame.font.SysFont('liberationsansnarrow', 28, bold = 1)

                pygame.draw.rect(self.fenetre, (0, 175, 145), (50, 150, 700, 325))

                regles_0 = my_font.render("Le jeu se joue en 1 vs 1 et avec deux couleus : Noir et Blanc.", False, (0, 0, 0))
                self.fenetre.blit(regles_0, (60,160))

                regles_1 = my_font.render("Le joueur ayant le plus de pions de sa couleur lorsqu'il n'y a", False, (0, 0, 0))
                self.fenetre.blit(regles_1, (60,185))

                regles_2 = my_font.render("plus de coups possible, gagne la partie.", False, (0, 0, 0))
                self.fenetre.blit(regles_2, (60,207))

                regles_3 = my_font.render("Une contrainte:", False, (0, 0, 0))
                self.fenetre.blit(regles_3, (60,250))

                regles_4 = my_font.render("Les pions doivent être placer de manière a entourer au moins", False, (0, 0, 0))
                self.fenetre.blit(regles_4, (60,270))

                regles_5 = my_font.render("un pions de couleur adverse !", False, (0, 0, 0))
                self.fenetre.blit(regles_5, (60,290))

                regles_6 = my_font.render("Maintenant que vous savez tout, devenez un(e) pro !! SHEEESH", False, (0, 0, 0))
                self.fenetre.blit(regles_6, (60,335))


            boutton_quitter.affiche(mouse)
                
            pygame.display.update()


# Creation de la classe Gagnant permettant l'affichage d'un écran de victoire
class Gagnant:

    def __init__(self, joueur, fenetre, gagnant):

        self.joueur = joueur
        self.fenetre = fenetre
        self.gagnant = gagnant

        self.font = pygame.font.SysFont('Corbel', 100)
        self.title = self.font.render("Le gagnant est:", True, (37, 37, 37))
        self.title2 = self.font.render("Egalité:", True, (37, 37, 37))


    def affichage(self):
        '''Cette fonction contient la boucle affichant le fenetre des gagnants'''

        quitter = Boutton(self.fenetre, (0, 175, 145), (37, 37, 37), (24, 77, 71), 250, 600, 270, 615, 300, 100, "Quitter")
        fin = False

        while not fin:

            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 250 <= mouse[0] <= 550 and 600 <= mouse[1] <= 700: # boutton Quitter
                        fin = True   
            
            if self.gagnant == 1:
                self.fenetre.blit(self.title, (140, 20))
                pygame.draw.circle(self.fenetre, (34, 40, 49), (400, 400), 100, 100)
            if self.gagnant == 2:
                self.fenetre.blit(self.title, (140, 20))
                pygame.draw.circle(self.fenetre, (221, 221, 221), (400, 400), 100, 100)
            if self.gagnant == 3:
                self.fenetre.blit(self.title2, (10, 10))
                pygame.draw.circle(self.fenetre, (34, 40, 49), (200, 400), 100, 100)
                pygame.draw.circle(self.fenetre, (221, 221, 221), (600, 400), 100, 100)
            
            quitter.affiche(mouse)
            

            pygame.display.update()