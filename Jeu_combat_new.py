import pygame
import time
import sys
from objets_et_variables import *
from sons import son_epee,aie_boss,aie_hero
from random import randint,choice
from fonctions import afficher_ecran_chargement
from SQL import maj_stats, det_id_compte
from boss import *
from heros import *

afficher_ecran_chargement(chargement[8])
print("Chargement de la Babel Arena...")

class JeuCombat:
    def __init__(self,j1,j2,nom_boss:str) -> 'JeuCombat':
        '''Initialise les attributs du jeu de combat.
        Paramètres :
            - j1 : le héros du joueur1
            - j2 : le boss (joueur2)
            - nom_boss (str) : le nom du boss combattu (joueur2)
        Returns :
            - Le multiplicateur du dictionnaire, avec 1 comme valeur par défaut si la combinaison n'existe pas
        - self.fond : Image du fond du jeu
        - self.fonds : dictionnaire des images des fond du jeu, avec les clés correspondant aux noms des fond du jeu et les valeurs correspondant au sol du fond
        - self.run : booléen indiquant si le jeu est en cours
        - self.vie_hero : Image du compteur de vie du héros
        - self.vie_boss : Image du compteur de vie du boss
        - self.police : police utilisée pour afficher les textes
        - self.dmg : booléen indiquant si un dégât a été subi
        - self.j1 : instance de la classe Hero, héros du joueur 1
        - self.j2 : instance de la classe Boss, boss combattu par le heros du joueur 1
        - self.reussi : booléen indiquant si le combat est réussi
        - self.frame : compteur pour l'animation'''
        self.fond = j2.boss.get_fond()
        self.fonds = {'Temple':0,'Desert':50,'Eglise':15,'Chute':10,'Lave':50,'Pluie':25,'Dojo':20}
        self.run = False
        self.vie_hero = pygame.image.load("images/Jeu de combat/compteur.png")
        self.vie_boss = pygame.image.load("images/Jeu de combat/compteur.png")
        self.police = pygame.font.Font('babelcasino.ttf', 15)
        self.dmg = False
        self.j1 = j1
        self.j2 = j2
        self.reussi = False
        self.frame = 0
        self.nom_boss = nom_boss
    def actif(self, etat:bool):
        self.run = etat
    def get_actif(self):
        return self.run
    def set_reussi(self:bool):
        self.reussi = True
    def get_reussi(self):
        return self.reussi
    def multis(self, j1, j2) -> float:
        '''Fonction qui permet de calculer les multiplicateurs de dégâts en fonction des éléments du boss et du héros.
        Paramètres :
            - j1 : le joueur1 (héros)
            - j2 : le joueur2 (boss)'''
        multis_elements = {
            'Feu': {
                'FeuImmune' : 0,
                'Feu': 0.7,
                'Glace': 1.75,
                'Eau': 1.45,
                'Nature': 1.25,
                'Esprit': 1.1,
                'Air': 0.9,
                'Nuit': 0.8,
                'Foudre' : 1.4
            },
            'Esprit': {
                'Feu': 1.1,
                'Glace': 0.9,
                'Eau': 1.1,
                'Nature': 1.25,
                'Air': 0.8,
                'Esprit': 0.4,
                'Nuit': 1.45,
                'Foudre' : 0.95
            },
            'Air': {
                'Feu': 1.2,
                'Glace': 1.1,
                'Eau': 1.15,
                'Nature': 0.9,
                'Air': 0.6,
                'Esprit': 1.45,
                'Nuit': 1.05,
                'Foudre' : 0.95
            },
            'Nuit': {
                'Feu': 1.65,
                'Glace': 1.05,
                'Eau': 1.1,
                'Nature': 0.9,
                'Air': 1.2,
                'Esprit': 0.75,
                'Nuit': 0.5,
                'Foudre' : 0.85
            },
            'Foudre': {
                'Feu': 1.4,
                'Glace': 1.12,
                'Eau': 1.2,
                'Nature': 0.9,
                'Air': 0.7,
                'Esprit': 1.14,
                'Nuit': 1.05,
                'Foudre' : 0.5
            }
        }
        
        el1 = j1.hero.get_type()
        el2 = j2.boss.get_type()
        
        # Return le multiplicateur du dictionnaire, avec 1 comme valeur par défaut si la combinaison n'existe pas
        return multis_elements.get(el1, {}).get(el2, 1.0)

    def lancer(self):
        '''La boucle principale du jeu, elle permet les déplacements et actions du héros et du boss tant que le combat n'est pas fini.'''
        # Boucle principale du jeu
        self.largeur, self.hauteur = 1200, 700
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.clock = pygame.time.Clock()
        # On réinitialise tout
        self.j2.boss.modif_pv(-self.j2.boss.get_pv()+self.j2.boss.get_pv_base())
        self.j1.hero.modif_pv(-self.j1.hero.get_pv()+self.j1.hero.get_pv_base())
        self.j2.boss.modif_pos_x(-self.j2.boss.get_pos_x()+1000)
        self.j1.hero.modif_pos_x(-self.j1.hero.get_pos_x()+50)
        self.j1.hero.modif_img(self.j1.images_marche_d[0])
        self.j1.hero.set_victoire(False)
        self.j2.boss.set_victoire(False)
        self.j2.boss.set_mort(False)
        self.j1.hero.set_mort(False)
        while not self.j1.hero.get_victoire() and not self.j2.boss.get_victoire() and self.run:
            self.frame += 0.14
            # Permet de détermnier les collisions entre le héros et le boss grace aux sprites de ceux-ci
            mask1 = pygame.mask.from_surface(self.j1.hero.image)
            mask2 = pygame.mask.from_surface(self.j2.boss.image)
            offset_x = self.j2.boss.get_pos_x() - self.j1.hero.get_pos_x()
            offset_y = self.j2.boss.get_pos_y() - self.j1.hero.get_pos_y()
            # Regarde si il y a des pixels non transparents des masques du héros et du boss qui se superposent
            # (Pour déterminer la collision entre les deux, et donc pouvoir appliquer les différents effets, notamment les dégâts)
            mask1_overlap = mask1.overlap(mask2, (offset_x, offset_y))
            mask2_overlap = mask2.overlap(mask1, (-offset_x, -offset_y))

            # Mettre à jour les collisions
            self.j1.hero.set_collision(mask1_overlap)
            self.j2.boss.set_collision(mask2_overlap)

            if self.frame >= len(self.fond)-1:
                # On remet tout à 0
                self.frame = 0
            fenetre.blit(self.fond[int(self.frame)],(0,0))
            multis = self.multis(self.j1,self.j2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Touche pour la compétence 1 du héros
                    if event.key == pygame.K_KP1:
                        # On vérifie si le héros est déjà en train d'attaquer et n'est pas stun
                        if self.j1.hero.get_attaque() and self.j1.hero.get_cd_atk() > 0.5 and not self.j1.hero.get_stun():
                            # On active le combo pour les héros qui le peuvent
                            self.j1.hero.set_combo(True)
                        # Si le héros a son attaque disponible (temps depuis la dernière attaque > temps de recharge de la compétence) et s'il n'est pas stun
                        if self.j1.hero.get_cd_atk() > self.j1.hero.get_cd()[0] and not self.j1.hero.get_cp2() and not self.j1.hero.get_stun():
                            # On réinitialise le frame du héros, on met a jour le temps depuis la dernière attaque et on lance son attaque
                            self.j1.reset_frame()
                            self.j1.hero.set_cd_atk()
                            self.j1.hero.set_attaque(True)
                    # Touche pour la compétence 2 du héros
                    # Si le héros a son attaque disponible (temps depuis la dernière attaque > temps de recharge de la compétence) 
                    # et s'il n'est pas stun et s'il n'est pas en train d'attaquer avec sa compétence 1
                    elif event.key == pygame.K_KP0 and self.j1.hero.get_cd_cp2() > self.j1.hero.get_cd()[1] and not self.j1.hero.get_attaque() and not self.j1.hero.get_stun():
                        # On réinitialise le frame du héros, on met a jour le temps depuis la dernière attaque et on lance son attaque
                        self.j1.reset_frame()
                        self.j1.hero.set_cd_cp2()
                        self.j1.hero.set_cp2(True)
            
            # Si le boss n'est pas mort
            if not self.j2.boss.get_pv() <= 0:
                # Si le héros est en vie, on lance le patern du boss
                if self.j1.hero.get_pv() > 0:
                    self.j2.patern_boss(self.j1.hero.get_pos_x(),self.j1)
                # Sinon, on lance l'animation d'inaction pendant l'animation de mort du héros
                else:
                    self.j2.inaction(self.j2.boss.get_speed_anim(),'Gauche')
            # Sinon on fait progresser l'animation de mort du boss
            else:
                self.j2.mort(0.1,self.j1)

            # Si le héros est mort, on fait progresser l'animation de mort
            if self.j1.hero.get_pv() <= 0:
                self.j1.mort(0.1,self.j2)

            keys = pygame.key.get_pressed()
            # Si le joueur n'est pas stun
            if not self.j1.hero.get_stun():
                # Si le joueur n'est pas en train d'attaquer et qu'il n'est pas mort
                if not self.j1.hero.get_attaque() and not self.j1.hero.get_pv() <= 0:     
                    # Flèche de gauche  
                    if keys[pygame.K_LEFT]:
                        # On modifie sa position pour le faire aller a gauche s'il n'est pas à la limite de l'écran
                        if self.j1.hero.get_pos_x() > 0:
                            self.j1.hero.modif_pos_x(-self.j1.hero.get_speed())
                        # On lance l'animation de marche
                        self.j1.marche(self.j1.hero.get_speed_anim()[1],'Gauche',self.j2)
                    # Flèche de droite
                    if keys[pygame.K_RIGHT]:
                        # On modifie sa position pour le faire aller a droite s'il n'est pas à la limite de l'écran
                        if self.j1.hero.get_pos_x() < 1000:
                            self.j1.hero.modif_pos_x(self.j1.hero.get_speed())
                        # On lance l'animation de marche
                        self.j1.marche(self.j1.hero.get_speed_anim()[1],'Droite',self.j2)

            # Si le boss est affecté par du poison
            if self.j2.boss.get_poison() != False:
                # On lui fait perdre de la vie petit à petit
                self.j2.boss.modif_pv(-0.02*multis)
                # Au bout de 5 secondes, la poison s'en va
                if time.time() - self.j2.boss.get_poison() > 5:
                    self.j2.boss.set_poison(False)
            # Si le héros est affecté par du poison
            if self.j1.hero.get_poison() != False:
                # On lui fait perdre de la vie petit à petit
                self.j1.hero.modif_pv(-0.02)
                # Au bout de 7 secondes, la poison s'en va
                if time.time() - self.j1.hero.get_poison() > 7:
                    self.j1.hero.set_poison(False)

            # On vérifie les temps de recharge du boss, pour savoir si ses compétences sont disponibles
            if self.j2.boss.get_cd_attaque1() > self.j2.boss.get_cd()[0]:
                self.j2.boss.set_attaque1_dispo(True)
            if self.j2.boss.get_cd_attaque2() > self.j2.boss.get_cd()[1]:
                self.j2.boss.set_attaque2_dispo(True)
            if self.j2.boss.get_cd_attaque3() > self.j2.boss.get_cd()[2]:
                self.j2.boss.set_attaque3_dispo(True)

            # Si le héros est en train d'attaquer avec sa compétence 1
            if self.j1.hero.get_attaque():
                # On détermine la position du boss par rapport à celle du héros : Droite
                if self.j2.boss.get_pos_x() > self.j1.hero.get_pos_x():
                    self.j1.attaque(self.j1.hero.get_speed_anim()[0],'Droite',self.j2,multis)
                # On détermine la position du boss par rapport à celle du héros : Gauche
                else:
                    self.j1.attaque(self.j1.hero.get_speed_anim()[0],'Gauche',self.j2,multis)

            # Si le héros est en train d'attaquer avec sa compétence 2 
            elif self.j1.hero.get_cp2():
                # On détermine la position du boss par rapport à celle du héros : Droite
                if self.j2.boss.get_pos_x() > self.j1.hero.get_pos_x():
                    self.j1.cp2(self.j1.hero.get_speed_anim()[0],'Droite',self.j2,multis)
                # On détermine la position du boss par rapport à celle du héros : Gauche
                else:
                    self.j1.cp2(self.j1.hero.get_speed_anim()[0],'Gauche',self.j2,multis)
            # Si le héros n'est ni en train de bouger, ni en train d'attaquer, ni en train de mourir, ou alors qu'il est stun mais pas mort :
            # On joue son animation d'inaction
            elif not self.j1.hero.get_attaque() and not self.j1.hero.get_cp2() and self.j1.hero.get_pv() > 0 and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] or self.j1.hero.get_stun() and self.j1.hero.get_pv() > 0:
                self.j1.inaction(self.j2)

            # On affiche les images du boss et du héros en fonction de leur position
            self.fenetre.blit(self.j2.boss.image, (self.j2.boss.get_pos_x(), self.j2.boss.get_pos_y()-self.fonds[self.j2.boss.get_nomfond()]))
            self.fenetre.blit(self.j1.hero.image, (self.j1.hero.get_pos_x(), self.j1.hero.get_pos_y()-self.fonds[self.j2.boss.get_nomfond()]))
            '''if isinstance(self.j2, Pandora) and self.j2.minion:          #Cas du boss Pandora, qui invoque des serviteurs pour ce battre, mais le boss comporte des problèmes donc il n'est pas actif
                mask3 = pygame.mask.from_surface(self.j2.minion.boss.image)
                offset_x = self.j2.minion.boss.get_pos_x() - self.j1.hero.get_pos_x()
                offset_y = self.j2.minion.boss.get_pos_y() - self.j1.hero.get_pos_y()
                mask3_overlap = mask3.overlap(mask1, (offset_x, offset_y))
                self.j2.minion.boss.set_collision(mask3_overlap)
                self.fenetre.blit(
                    self.j2.minion.boss.image,
                    (self.j2.minion.boss.get_pos_x(), self.j2.minion.boss.get_pos_y()-self.fonds[self.j2.boss.get_nomfond()])
                )'''
            # On affiche les cadres pour la vie du boss et du héros
            self.fenetre.blit(self.vie_hero, (0, -50))
            self.fenetre.blit(self.vie_boss, (950, -50))
            # On affiche la vie du boss et du héros
            pvheros = self.police.render("Pv du heros : " + str(int(self.j1.hero.get_pv())), True, noir)
            pvboss = self.police.render("Pv du boss : " + str(int(self.j2.boss.get_pv())), True, noir)
            fenetre.blit(pvheros, (52, 70))
            fenetre.blit(pvboss, (1010, 70))
            # On affiche la souris
            fenetre.blit(souris, pygame.mouse.get_pos())
            # On rafraîchit l'écran
            pygame.display.flip()
            # On attend avant de faire un tour de boucle
            self.clock.tick(60)
        # Si la boucle prend fin, on met fin au jeu
        self.actif(False)
        # On remet tout comme avant, pour revenir au jeu de base
        self.largeur, self.hauteur = 800, 800
        pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.mixer.music.unload()

        # Si le boss a gagné, on fait mourir le joueur et on met à jour les stats du joueur dans la base de données
        if self.j2.boss.get_victoire():
            joueur1.set_cagnotte(0)
            maj_stats(det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()),0,1,self.nom_boss)
        # Si le héros a gagné, on fait augmente le solde du joueur et on met à jour les stats du joueur dans la base de données
        elif self.j1.hero.get_victoire():
            self.set_reussi()
            joueur1.modifier_cagnotte(joueur1.get_cagnotte()/4+15000)
            maj_stats(det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()),1,0,self.nom_boss)
        # Sinon on ferme la fenêtre
        else:
            pygame.quit()



