import pygame
from random import randint
import sys
from fonctions import dessiner_bouton,afficher_ecran_chargement
from objets_et_variables import *
from img import souris
from sons import pioche_carte, click
from Ecrans import ecran2,ecran_black,ecran_mort



afficher_ecran_chargement(chargement[9])
print("Chargement du Babel Jack...")

class Blackjack:
    def __init__(self):
        self.valeur_joueur = 0
        self.valeur_croupier = 0
        #fonction qui définit si le joueur doit jouer
        self.j_jouer = True
        #fonction qui définit si le croupier doit jouer
        self.c_jouer = True
        #fonction pour empêcher le croupier de jouer
        self.c_block = True
        self.score_j = "score: " + str(self.valeur_joueur)
        self.score_croupier = "score: " + str(self.valeur_croupier)
        self.bouton_val1 = pygame.Rect(278, 14, 380, 100)
        self.bouton_val11 = pygame.Rect(278, 124, 380, 100)
        self.tirer = pygame.Rect(342, 342, 116, 176)
        self.arreter = pygame.Rect(14, 14, 250, 100)
        self.bouton_rejouer = pygame.Rect(30, 580, 160, 100)
        self.score = pygame.Rect(14, 686, 200, 100)
        self.croupier = pygame.Rect(566, 686, 220, 100)
        self.actif = False
        self.img_joker = charger_et_agrandir("cartes/joker.png")
        self.img = [[f"cartes/{couleur}/carte-{i}.png" for i in range(2, 11)] for couleur in ['Carreau', 'Coeur', 'Pique', 'Trefle']] 
        self.dos_de_carte = charger_et_agrandir("cartes/dos_de_carte.png")
        self.solde = charger_et_agrandir("images/Jeu de combat/valider.png")
        self.police = pygame.font.Font('babelcasino.ttf',30)
        self.retour = False # Booléen qui determine si la souris est sur la fleche
        self.img_carte = charger_et_agrandir("images/None.png")
        self.fin = False

    def set_actif(self,valeur):
        self.actif = valeur
        
        
    
    def tirer_carte_joueur(self):

        """Cette fonction permet de faire tirer une carte du côté du joueur"""
        if self.actif:
            #empêche le croupier de sauter le tour du joueur (le tricheur)
            self.c_block = True
            #tirer une carte
            val_j = randint(1, 10)
            fenetre.blit(souris, pygame.mouse.get_pos())
            #vérification si la carte tirée est un joker
            if val_j == 1:
                # créer le bouton pour mettre la valeur de la carte à 11
                dessiner_bouton(fenetre, "le joker prend la valeur 1", self.bouton_val1.x, self.bouton_val1.y, self.bouton_val1[2], self.bouton_val1[3], blanc, noir, 30)
                # créer le bouton pour mettre la valeur de la carte à 11
                dessiner_bouton(fenetre, "le joker prend la valeur 11", self.bouton_val11.x, self.bouton_val11.y, self.bouton_val11[2], self.bouton_val11[3], blanc, noir, 30)
                fenetre.blit(self.img_joker, (342, 574))
                fenetre.blit(souris, pygame.mouse.get_pos())
                # Mettre à jour l'affichage pour que les boutons soient visibles
                pygame.display.update()  
                
                # changer la valeur de val_j pour mettre la variable en argument
                val_j = 0 
                
                while val_j != 1 and val_j != 11:   
                    fenetre.blit(souris, pygame.mouse.get_pos())
                    #permettre au joueur de quitter le jeux sans qu'il plante
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        #vérification de la collision
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.bouton_val1.collidepoint(event.pos):
                                click.play()
                                val_j = 1
                                self.img_carte = self.img_joker
                            elif self.bouton_val11.collidepoint(event.pos):
                                click.play()
                                val_j = 11
                                self.img_carte = self.img_joker
            
            
            #additionner la valeur de la carte à la valeur totale
            self.valeur_joueur += val_j
            #on enlève les boutons du joker
            self.nettoyer_ecran()
            fenetre.blit(souris, pygame.mouse.get_pos())
            # montrer la carte en fonction de sa valeur
            if val_j >= 2 and val_j <= 10:
                self.img_carte = charger_et_agrandir(self.img[randint(0,3)][val_j - 2])
                self.nettoyer_ecran()
                fenetre.blit(self.img_carte, (342, 574))
                # Mettre à jour l'affichage après avoir tiré la carte
            pygame.display.update()  
            #autorise le croupier à jouer
            self.c_block = False
            #print dans la console pour débugger
            print("j= ",self.valeur_joueur)

    
    def tirer_carte_croupier(self):
        """Cette fonction permet de faire tirer une carte du côté du croupier"""
        if self.actif:
            #tirer une carte
            val_c = randint(1, 10)
            #vérification si la carte tirée est un joker
            if val_c == 1:
                #choisir 11 si ça ne fait pas perdre sinon choisir 1
                val_c = 11 if self.valeur_croupier <= 10 else 1
            #additionner la valeur de la carte à la valeur totale
            self.valeur_croupier += val_c
            self.nettoyer_ecran()
            #print dans la console pour débugger
            print("c= ", self.valeur_croupier)

    
    def tour_joueur(self):
        """Cette fonction permet de jouer le tour du joueur"""
        if self.actif:
            # Mettre à jour l'affichage
            self.nettoyer_ecran()

            for event in pygame.event.get():
                #permettre au joueur de quitter le jeux sans qu'il plante
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #vérification de la colision
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tirer.collidepoint(event.pos):
                        pioche_carte.play()
                        self.tirer_carte_joueur()
                        #fait arrêter le joueur si il a perdu
                        if self.valeur_joueur > 21:
                            self.j_jouer = False
                            #la partie s'arrête si le joueur a perdu
                            self.c_jouer = False
                    #fait arrêter le joueur si il veut arrêter
                    elif self.arreter.collidepoint(event.pos):
                        click.play()
                        self.j_jouer = False

    
    def tour_croupier(self):
        """Cette fonction permet de jouer le tour du croupier"""
        if self.actif:
            #permet au croupier de jouer autant qu'il veut si le joueur arrête
            if self.j_jouer == False:
                self.c_block = False
            #permet au croupier de jouer quand c'est son tour
            if self.c_block == False:
                #si le croupier a moins de 16 il pioche sinon il s'arrête
                if self.valeur_croupier <= 16:
                    self.tirer_carte_croupier()
                elif self.valeur_croupier < self.valeur_joueur:
                    self.tirer_carte_croupier()
                else: 
                    self.c_jouer = False
                #la partie s'arrête si le croupier perd
                if self.valeur_croupier > 21:
                    self.j_jouer = False
            #empêche le croupier de rejouer si c'est pas son tour (il essaie de tricher)
            self.c_block = True
            self.nettoyer_ecran()

    
    def main(self):
        if self.actif:
            # le joueur et le croupier commencent avec 1 cartes chacun
            self.tirer_carte_croupier()
            # On actualise l'écran
            self.nettoyer_ecran()
            #la partie continue tant qu'au moins un des deux joueurs veut continuer
            while self.j_jouer == True and self.actif or self.c_jouer == True and self.actif:
                pygame.mouse.set_visible(False)
                fenetre.blit(souris, pygame.mouse.get_pos())
                #fait jouer le joueur si il veut continuer
                if self.j_jouer == True:
                    self.tour_joueur()
                #fait jouer le croupier si il veut continuer
                if self.c_jouer == True:
                    self.tour_croupier()
            
            #print dans la console pour débugger
            print("arrêt")
            #conditions de victoire
            if self.valeur_joueur > self.valeur_croupier and self.valeur_joueur <= 21 or self.valeur_joueur <= 21 and self.valeur_croupier > 21:
                print((-joueur1.get_cagnotte()/12 - 150)*joueur1.get_gains()['Blackjack'],joueur1.get_gains()['Blackjack'])
                joueur1.modifier_cagnotte((joueur1.get_cagnotte()/8 + 200)*joueur1.get_gains()['Blackjack'])
                print("le joueur gagne")
            #condition d'égalité
            elif self.valeur_joueur == self.valeur_croupier:
                print((-joueur1.get_cagnotte()/12 - 150)*joueur1.get_gains()['Blackjack'],joueur1.get_gains()['Blackjack'])
                joueur1.modifier_cagnotte(-100*joueur1.get_gains()['Blackjack'])
                print("égalité")
            #conditions de défaite
            else:
                print((-joueur1.get_cagnotte()/12 - 150)*joueur1.get_gains()['Blackjack'],joueur1.get_gains()['Blackjack'])
                joueur1.modifier_cagnotte((-joueur1.get_cagnotte()/12 - 150)*joueur1.get_gains()['Blackjack'])
                print("le croupier gagne")
            
            #lance la fonction qui permet de rejouer
            pygame.display.flip()
            self.rejouer()
          
            
    def rejouer(self): 
        """cette fonction permet au joueur de rejouer"""
        #créer une boucle pour permettre au joueur de rejouer autant qu'il veut
        while self.actif:
            self.fin = True
            #remêt tout à 0 pour rejouer
            self.nettoyer_ecran()
            pygame.display.update()
            if joueur1.get_cagnotte() <= 1:
                self.actif = False
                ecran_black.ecran.set_actif(False), ecran_mort.ecran.set_actif(True)
            #permettre au joueur de quitter le jeu sans qu'il plante
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #vérification de si le joueur veut rejouer
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bouton_rejouer.collidepoint(event.pos):
                        click.play()
                        #on enlève le bouton "rejouer"
                        self.nettoyer_ecran()
                        self.fin = False
                        self.fermer()
                        #relancement du jeu
                        self.main()
                    if 660 <= event.pos[0] <= 760 and 150 <= event.pos[1] <= 230:
                        click.play()
                        self.fermer()
                        self.actif = False
                        ecran2.ecran.set_actif(True), ecran_black.ecran.set_actif(False)

    def fermer(self):
        # remet tout à 0
        self.valeur_joueur = 0
        self.valeur_croupier = 0
        self.j_jouer = True
        self.c_jouer = True

    def nettoyer_ecran(self):
        """cette fonction permet netoyer l'ecran"""
        # Efface l’écran en remplissant avec une couleur de fond
        fenetre.blit(fondbj, (0, 0))
        # Redessiner les éléments permanents
        fenetre.blit(self.dos_de_carte, (272, 272))
        fenetre.blit(self.solde, (560, 30))
        solde = self.police.render(str(int(joueur1.get_cagnotte())), True, noir)
        texte_rect = solde.get_rect(center=(670, 80))
        fenetre.blit(solde, texte_rect)
        #on change le score du joueur
        self.score_j = "score: " + str(self.valeur_joueur)
        dessiner_bouton(fenetre, self.score_j , self.score.x, self.score.y, self.score[2], self.score[3], blanc, noir, 30)
        #on affiche le score du croupier
        self.score_croupier = "croupier: " + str(self.valeur_croupier)
        dessiner_bouton(fenetre, self.score_croupier , self.croupier.x, self.croupier.y, self.croupier[2], self.croupier[3], blanc, noir, 30)
        fenetre.blit(self.img_carte, (342, 574))
        if 14 <= pygame.mouse.get_pos()[0] <= 174 and 34 <= pygame.mouse.get_pos()[1] <= 144 and not self.retour:
                fenetre.blit(bouton_stop_bj2, (14, 14))
        else:
            fenetre.blit(bouton_stop_bj, (14, 14))
        if self.fin:
            if 660 <= pygame.mouse.get_pos()[0] <= 760 and 150 <= pygame.mouse.get_pos()[1] <= 230 and not self.retour:
                fenetre.blit(fleche_retour2, (664, 142))
            else:
                fenetre.blit(fleche_retour, (660, 140))  
            #dessine le bouton pour pouvoir rejouer
            if 30 <= pygame.mouse.get_pos()[0] <= 190 and 580 <= pygame.mouse.get_pos()[1] <= 670 and not self.retour:
                fenetre.blit(bouton_play_bj2, (30, 570))
                
            else:
                fenetre.blit(bouton_play_bj, (30, 570)) 
        fenetre.blit(souris, pygame.mouse.get_pos())
        # Mettre à jour l’affichage
        pygame.display.update()

#créer un objet pour pas que le programme plante
blackjack = Blackjack() 