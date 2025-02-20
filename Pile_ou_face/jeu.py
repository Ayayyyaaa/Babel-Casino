import pygame
import sys
from fonctions import dessiner_zone_texte, rouletterusse, affiche_ecran1, affiche_ecran2, affiche_ecran3, affiche_ecran4, pseudos, lancement, affiche_ecran_fin
from img import *
from objets_et_variables import *
from sons import *

pygame.init()
pygame.mixer.init()

blanc = (255, 255, 255)
noir = (0, 0, 0)
gris = (128, 128, 128)

class Jeu():
    def __init__(self):
        self.run = True
        self.text = ""  
        self.nb_cb_actif = False  
        self.code_cb_actif = False  
        self.nom_actif = False 

    def running(self):
        while self.run:
            # Fermer la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Clic de souris
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Champ pour le numéro de carte bleue
                    if nb_cb.collidepoint(event.pos):
                        self.nb_cb_actif = not self.nb_cb_actif
                    else:
                        self.nb_cb_actif = False
                    # Champ pour le code de carte bleue
                    if code_cb.collidepoint(event.pos):
                        self.code_cb_actif = not self.code_cb_actif
                    else:
                        self.code_cb_actif = False
                    # Gérer les boutons pour accéder à l'écran 2 (écran principal)
                    if bouton1.get_x() <= event.pos[0] <= bouton1.get_x() + bouton1.get_largeur() and bouton1.get_y() <= event.pos[1] <= bouton1.get_y() + bouton1.get_hauteur():
                        if ecran_fin.get_actif():
                            ecran_fin.set_actif(False)
                            ecran2.set_actif(True)
                        else:
                            ecran1.set_actif(not ecran1.get_actif())
                            ecran2.set_actif(not ecran2.get_actif())

                    # Gérer les interactions de l'écran 2 (écran principal)
                    if ecran2.get_actif():
                        # Lancer la roulette russe
                        if ecran2.get_actif() and 330 <= event.pos[0] <= 390 and 45 <= event.pos[1] <= 75 :
                            joueur1.set_roulette_active(True)
                            rouletterusse()
                            joueur1.set_roulette_active(False)
                        # Affichage du jeu de pile ou face
                        if 335 <= event.pos[0] <= 385 and 100 <= event.pos[1] <= 150 :
                            pofactif = not pofactif
                            piece.set_cote(None)
                        
                        # Gestion des boutons de choix pour le pile ou face
                        elif not pofactif:
                            if 125 <= event.pos[0] <= 175 and 230 <= event.pos[1] <= 280 :
                                piece.set_choix('Face') 
                                choix_fait = True

                            elif 230 <= event.pos[0] <= 280 and 230 <= event.pos[1] <= 280 :
                                piece.set_choix('Pile')
                                choix_fait = True

                            if choix_fait:
                                pileouface.activer_animation()
                                choix_fait = False

                        # Affichage du jeu de machine à sous depuis l'écran principal
                        if 330 <= event.pos[0] <= 390 and 170 <= event.pos[1] <= 220 : 
                                ecran2.set_actif(not ecran2.get_actif())
                                ecran4.set_actif(not ecran4.get_actif())

                    # Affichage de l'écran principal depuis la machine à sous
                    elif ecran4.get_actif() and 340 <= event.pos[0] <= 390 and 20 <= event.pos[1] <= 70 :
                        ecran2.set_actif(not ecran2.get_actif())
                        ecran4.set_actif(not ecran4.get_actif())
                    
                    # Gérer le champ pour entrer son pseudo de joueur
                    if champ_joueur.collidepoint(event.pos):
                        self.nom_actif = not self.nom_actif
                    else:
                        self.nom_actif = False
                        
                # Touche pressée
                elif event.type == pygame.KEYDOWN:
                    # Gérer la saisie du nom de joueur
                    if self.nom_actif and ecran1.get_actif():
                        if event.key == pygame.K_RETURN:
                            joueur1.set_pseudo(self.text)
                            if joueur1.get_pseudo().lower() == 'abel':
                                joueur1.set_cagnotte(100)
                            self.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif len(self.text) <= 9:
                            self.text += event.unicode

                    if ecran3.get_actif():
                        # Gérer la saisie du numéro de carte bleue
                        if self.nb_cb_actif:
                            if event.key == pygame.K_BACKSPACE:
                                nbr_cb = nbr_cb[:-1]
                            elif len(nbr_cb) < 19 and event.unicode in "123456789":
                                L = [4,9,14]
                                for elem in L:
                                    if len(nbr_cb) == elem:
                                        nbr_cb += ' '
                                nbr_cb += event.unicode

                        elif self.code_cb_actif:
                            # Gérer la saisie du code de carte bleue
                            if event.key == pygame.K_RETURN:
                                if len(nbr_cb) == 19 and len(codee_cb) == 4:
                                    nbr_cb = ''
                                    codee_cb = ''
                                    joueur1.set_cagnotte(2000)
                                    ecran2.set_actif(True)
                                    ecran3.set_actif(False)
                            elif event.key == pygame.K_BACKSPACE:
                                codee_cb = codee_cb[:-1]
                            elif len(codee_cb) < 4 and event.unicode in "123456789":
                                codee_cb += event.unicode
                    
                    if ecran4.get_actif():
                        # Lancer la machine à sous
                        if event.key == pygame.K_SPACE and joueur1.get_cagnotte() >= 100:
                            son_gambling.play()
                            lancement() 
                            joueur1.modifier_cagnotte(-100)

            if not ecran2.get_actif():
                pofactif = True

            # Conditions de défaite
            if joueur1.get_cagnotte() <= 0:
                ecran1.set_actif(False), ecran2.set_actif(False), ecran4.set_actif(False), ecran3.set_actif(True) 
                if son_joue is False:
                    son_fall.play()
                    son_joue = True

            # Conditions de victoire
            if joueur1.get_cagnotte() >= 1000000 and not win:
                ecran1.set_actif(False), ecran2.set_actif(False), ecran4.set_actif(False), ecran_fin.set_actif(True)
                win = True 

            # Affichage de l'écran de début de jeu
            if ecran1.get_actif():
                affiche_ecran1()
                dessiner_zone_texte(fenetre, champ_joueur, self.text, self.nom_actif)

            # Affichage de l'écran principal
            if ecran2.get_actif():
                pseudos()
                affiche_ecran2()
                # Affichage des boutons des choix du pile ou face
                if not pofactif:
                    fenetre.blit(face2, (125, 230))
                    fenetre.blit(pile2, (230, 230))
                    if piece.get_cote() == 'Face':
                        fenetre.blit(face, (170, 140))
                    elif piece.get_cote() == 'Pile':
                        fenetre.blit(pile, (170, 140))
                    

            elif ecran3.get_actif():
                # Affichage de l'écran de défaite
                affiche_ecran3()
                dessiner_zone_texte(fenetre, nb_cb, self.nbr_cb, self.nb_cb_actif)
                dessiner_zone_texte(fenetre, code_cb, self.codee_cb, self.code_cb_actif)

            elif ecran4.get_actif():
                # Affichage de l'écran de la machine à sous
                affiche_ecran4()
            
            elif ecran_fin.get_actif():
                # Affichage de l'écran de victoire
                affiche_ecran_fin()

            pygame.display.flip()
