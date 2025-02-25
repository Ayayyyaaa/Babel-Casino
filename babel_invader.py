import pygame
import random
from objets_et_variables import *
import sys
import numpy as np

clock = pygame.time.Clock() 

class Explosion:
    def __init__(self, x: int, y: int, frames: list) -> 'Explosion':
        '''Initialise une explosion.
        Paramètres:
            - x: (int) Position x de l'explosion
            - y: (int) Position y de l'explosion
            - frames: (list) Liste des images de l'animation'''
        self.x = x
        self.y = y
        self.frames = frames
        self.frame_actuelle = 0
        self.temps_derniere_frame = pygame.time.get_ticks()
        self.delai_animation = 100  # Animation plus rapide que les ennemis
        self.img = self.frames[self.frame_actuelle]
        self.actif = True
    
    def update(self):
        '''Met à jour l'animation de l'explosion'''
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.temps_derniere_frame > self.delai_animation: # Temps entre les frames
            self.frame_actuelle += 1    # On fait progresser l'animation
            if self.frame_actuelle >= len(self.frames): # Fin de l'animation
                self.actif = False  # Fin de l'esxplosion
            self.img = self.frames[self.frame_actuelle] # Met a jour l'image
            self.temps_derniere_frame = temps_actuel    # Met a jour le temps pour le cd entre les images
    
    def dessiner(self, fenetre: pygame.display):
        '''Affiche l'explosion à l'écran'''
        fenetre.blit(self.img, (self.x, self.y))

class Ennemi:
    def __init__(self, x:int,vitesse:int, img:list, vie:int, dgt:int, pieces:int) -> 'Ennemi':
        self.x = x # Position x de l'ennemi
        self.y = -50  # Commence au-dessus de l'écran
        self.vitesse = vitesse # Vitesse de l'annemi
        self.actif = True # Actif
        self.frames = img # Images de l'ennemi
        self.frame_actuelle = 0 # Image actuelle de l'ennemi
        self.temps_derniere_frame = pygame.time.get_ticks()
        self.delai_animation = 500  # Changement de frame toutes les 500ms
        self.img = self.frames[self.frame_actuelle]
        self.vie = vie # Pv de l'ennemi
        self.dgt = dgt  # Dégâts de l'ennemi
        self.pieces = pieces    # Pieces que fait gagner l'ennemi
        
    def update(self,vaisseau:'Vaisseau'):
        '''Permet de faire avancer les ennemis. Si l'ennemi arrive en bas de l'écran, on le supprime et on inflige
        des dégâts au vaisseau. 
        Paramètres :
            - vaisseau : un objet de la classe Vaisseau'''
        self.y += self.vitesse # On fait avancer l'ennemi
        temps_actuel = pygame.time.get_ticks()  # Couldown
        if temps_actuel - self.temps_derniere_frame > self.delai_animation: # Si le couldown est atteint
            self.frame_actuelle = (self.frame_actuelle + 1) % 2 # On change d'indice (2 images par ennemi, donc %2 pour avoir soit 0 soit 1)
            self.img = self.frames[self.frame_actuelle] # On change l'image
            self.temps_derniere_frame = temps_actuel    # On met a jour le couldown
        if self.y > hauteur:  # Si l'ennemi sort de l'écran par le bas
            self.actif = False # On le désactive
            vaisseau.set_vie(self.dgt) # On inflige des dégâts au vaisseau
            
    def dessiner(self, fenetre:'pygame.display'):
        '''Permet d'affichager l'ennemi à sa position sur l'écran'''
        fenetre.blit(self.img, (self.x, self.y))
        
    def collision(self, projectile:'Projectile') -> bool:
        '''Permet de vérifier la collision entre les projectiles du vaisseau et l'ennemi.
        Paramètres :
            - projectile : un objet de la classe Projectile'''
        # Hitbox rectangle de l'ennemi
        rect_ennemi = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        # Hitbox rectangle du projectile
        rect_projectile = pygame.Rect(projectile.get_x(), projectile.get_y(), 
                                    projectile.img.get_width(), projectile.img.get_height())
        return rect_ennemi.colliderect(rect_projectile) # Return la collision entre le projectile et l'ennemi
    
    def get_vie(self) -> int:
        return self.vie
    def set_vie(self, vie:int):
        self.vie += vie
    def set_actif(self, act:bool):
        self.actif = act
    def get_actif(self) -> bool:
        return self.actif
    def get_pieces(self) -> int:
        return self.pieces

class Projectile:
    def __init__(self, x:int, y:int, vitesse:int, img:pygame.image,dgt:int):
        '''Initialise un projectile.
        Paramètres :
            - x  : (int) La position x du projectile
            - y  : (int) La position y du projectile
            - vitesse : (int) La vitesse du projectile
            - img : (pygame.image) L'image du projectile
            - dgt : dégâts infligés par le projectile à la collision'''
        self.x = x 
        self.y = y 
        self.vitesse = vitesse
        self.actif = True
        self.img = img
        self.dgt = dgt
    
    def update(self):
        '''Permet de faire avancer le projectile. S'il sort de l'écran, on le supprime'''
        # On fait avancer le projectile
        self.y -= self.vitesse
        # S'il sort de l'écran
        if self.y < 0:
            # On le définit à False
            self.actif = False
    
    def dessiner(self, fenetre:pygame.display):
        '''Permet d'afficher le projectile à sa position sur l'écran.'''
        fenetre.blit(self.img, (self.x, self.y))

    def get_dgt(self) -> int:
        '''Permet de récuperer les dégâts que le projectile inflige'''
        return self.dgt
    
    def set_dgt(self, dgt:int):
        '''Permet d'augmenter les dégâts que le projectile inflige'''
        self.dgt += dgt

    def set_actif(self,act:bool):
        '''Permet de définir l'état du projectile'''
        self.actif = act

    def get_x(self):
        '''Permet de récupérer la position x du projectile'''
        return self.x
    
    def get_y(self):
        '''Permet de récupérer la position y du projectile'''
        return self.y

class Vaisseau:
    def __init__(self) -> 'Vaisseau':
        '''Initialise le vaisseau.
            - self.vie_max (int) : la vie maximum du vaisseau
            - self.vie (int) : la vie actuelle du vaisseau
            - self.x (int) : la position x du vaisseau
            - self.y (int) : la position y du vaisseau
            - self.vitesse_projectile (int) : la vitesse du projectile
            - self.cd (float) : le cooldown du tir
            - self.police (pygame.font) : la police de texte
            - self.frames (list[pygame.image]) : les images du vaisseau
            - self.frame (pygame.image) : l'image actuelle du vaisseau
            - self.projectiles (list[Projectile]) : les projectiles lancés par le vaisseau
            - self.dernier_tir (float) : le temps depuis le dernier tir
            - self.score (int) : le score du joueur
            - self.projectile_lvl (int) : le niveau des projectiles (dégâts + nombre)
            - self.pieces (int) : le nombre de pièces du joueur
            - self.multi (int) : le multiplicateur des pièces gagnées par le joueur
            - self.dgt (int) : les dégâts infligés par le joueur
            - self.lvl (dict) : les paramètres du vaisseau par niveau
        '''
        self.vie_max = 100
        self.vie = 100
        self.x = 375
        self.y = 750
        self.vitesse_projectile = 5
        self.cd = 0.5
        self.vitesse = 3
        self.police = pygame.font.Font('babelcasino.ttf', 16)
        self.frames = [pygame.image.load("Babel Invader/vaisseau1.png").convert_alpha(),
                      pygame.image.load("Babel Invader/vaisseau2.png").convert_alpha(),
                      pygame.image.load("Babel Invader/vaisseau3.png").convert_alpha(),
                      pygame.image.load("Babel Invader/vaisseau4.png").convert_alpha()]
        self.frame = self.frames[0]
        self.projectiles = []
        self.dernier_tir = 0
        self.score = 0
        self.projectile_lvl = 1
        self.pieces = 0
        self.multi = 1
        self.dgt = 1
        self.lvl = {'Vie max':1,'Vie':1,'Vitesse projectile':1,'Couldown':1,'Vitesse':1,'Projectile':1,'Multiplicateur':1,'Dégâts':1}
    def reset(self):
        '''Permet de réinitialiser toutes les caractéristiques du vaisseau à son état de base pour une nouvelle partie'''
        self.vie_max = 100
        self.vie = self.vie_max
        self.x = 375
        self.y = 750
        self.vitesse_projectile = 5
        self.cd = 0.5
        self.vitesse = 3
        self.projectiles = []
        self.dernier_tir = 0
        self.score = 0
        self.projectile_lvl = 1
        self.pieces = 0
        self.multi = 1
        self.dgt = 1
        self.lvl = {'Vie max':1,'Vie':1,'Vitesse projectile':1,'Couldown':1,'Vitesse':1,'Projectile':1,'Multiplicateur':1,'Dégâts':1}
    def get_pieces(self) -> int:
        return self.pieces
    def set_pieces(self, pieces:int):
        self.pieces += pieces
    def get_vie(self) -> int:
        return self.vie
    def set_vie(self, vie: int):
        '''Permet d'ajouter de la vie au vaisseau, si la vie actuelle est inferieure à la vie max du vaisseau.'''
        if self.vie + vie <= self.vie_max:
            self.vie += vie
        else:
            self.vie = self.vie_max
    def get_x(self) -> int:
        return self.x
    def set_x(self, x: int):
        self.x = x
    def get_vitesse_projectile(self) -> int:
        return self.vitesse_projectile
    def set_vitesse_projectile(self,v) -> int:
        self.vitesse_projectile += v
    def set_vitesse(self, vitesse: float):
        self.vitesse += vitesse
    def get_vitesse(self) -> float:
        return self.vitesse
    def get_cd(self) -> int:
        return self.cd
    def set_cd(self, cd: int):
        self.cd += cd
    def set_vie_max(self, vie_max: int):
        self.vie_max += vie_max
    def get_vie_max(self) -> int:
        return self.vie_max
    def get_score(self) -> int:
        return self.score
    def set_tir(self,valeur:int):
        self.projectile_lvl += valeur
    def get_tir_lvl(self) -> int:
        return self.projectile_lvl
    def get_multi(self) -> int:
        return self.multi
    def set_multi(self, multi: int):
        self.multi *= multi
    def get_lvl(self) -> dict:
        '''Permet de récupérer le dictionnaire de tous les niveaux du vaisseau'''
        return self.lvl
    def set_lvl(self, clef:str, lvl: int):
        '''Permet d'améliorer de lvl niveaux la compétence clef du vaisseau'''
        self.lvl[clef] += lvl        
    def set_dgt(self,dgt:int):
        self.dgt += dgt
    def jouer(self, fenetre:pygame.display, ennemis:'Ennemi'):
        self.frame = self.frames[self.projectile_lvl-1] # Image des projectiles tirés selon le niveau de ceux-ci
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and self.x > 210: # Déplacements gauche
            self.x -= self.vitesse
        elif touches[pygame.K_RIGHT] and self.x < 750: # Déplacements droite
            self.x += self.vitesse
            
        temps_actuel = pygame.time.get_ticks() / 1000 # Temps en secondes (millisecondes/1000=secondes)
        if temps_actuel - self.dernier_tir >= self.cd: # Couldown
            # On ajoute un projectile à la liste, avec toutes les inofs nécessaires
            self.projectiles.append(Projectile(self.x + (self.frames[0].get_width() - pygame.image.load(f"Babel Invader/missile{self.projectile_lvl}.png").get_width()) // 2, self.y, self.vitesse_projectile, pygame.image.load(f"Babel Invader/missile{self.projectile_lvl}.png").convert_alpha(),self.dgt))
            # On met à jour le cd
            self.dernier_tir = temps_actuel
            
        # Mise à jour et collision des projectiles
        for projectile in self.projectiles:
            # On met à jour le projectile (déplacement)
            projectile.update()
            # On vérifie si le projectile est en dehors de la fenêtre
            if not projectile.actif:
                # On enleve le projectile de la liste
                self.projectiles.remove(projectile)
            else:
                # Pour chaque ennemi sur l'écran
                for ennemi in ennemis:
                    # Si un ennemi est touché par un projectile
                    if ennemi.collision(projectile):
                        # On décrémente la vie de l'ennemi et on désactive le projectile
                        ennemi.set_vie(-projectile.get_dgt())
                        projectile.set_actif(False)
                        # Si l'ennemi n'a plus de vie
                        if ennemi.get_vie() <= 0:
                            # On décative l'ennemi, on gagne des pièces et du score
                            ennemi.set_actif(False)
                            self.score += ennemi.get_pieces()*10
                            self.pieces += ennemi.get_pieces()*self.multi
                # On dessine le projectile
                projectile.dessiner(fenetre)
        
        # On dessine le vaisseau à sa position sur l'écran
        fenetre.blit(self.frame, (self.x, self.y))
        
        # Affichage du score, de la vie et des pièces
        score_text = self.police.render(f'Score: {self.score}', True, (255, 255, 255))
        vie_text = self.police.render(f'Vie: {int(self.vie)}', True, (255, 255, 255))
        pieces_text = self.police.render(f'Pieces: {int(self.pieces)}', True, (255, 255, 255))
        fenetre.blit(score_text, (30, 15))
        fenetre.blit(vie_text, (30, 45))
        fenetre.blit(pieces_text, (30,75))

class BabelInvader:
    def __init__(self):
        '''Initialise le jeu
            - self.run (bool) : statut du jeu (actif ou non)
            - self.vaisseau (Vaisseau) : le vaisseau du joueur
            - self.ennemis (list) : la liste des ennemis en jeu
            - self.explosions (list) : la liste des explosions en jeu
            - self.temps_dernier_ennemi (float) : le temps depuis le dernier ennemi apparu
            - self.intervalle_spawn (float) : l'intervalle entre chaque apparition d'ennemi
            - self.temps_debut (float) : le temps de début du jeu
            - self.boutique (surface) : l'image de la boutique
            - self.explosion_frames (list) : les images des explosions
            - self.achats (dict) : les achats dispo pour joueur
            - self.achat_tir (Button) : le bouton de l'achat du tir
            - self.police (pygame.font) : la police d'écriture
            - self.police2 (pygame.font) : la police d'écriture pour l'ecran final
            - self.ennemi_... (fonction) : permet de générer un ennemi avec les caractéristiques voulues'''
        self.run = False
        self.vaisseau = Vaisseau()
        self.ennemis = []
        self.explosions = []
        self.temps_dernier_ennemi = 0
        self.intervalle_spawn = 2.0
        self.temps_debut = 0
        self.boutique = pygame.image.load('Babel Invader/boutique2.png').convert_alpha()
        self.explosion_frames = [pygame.image.load('Babel Invader/explosion0.png').convert_alpha(),pygame.image.load('Babel Invader/explosion1.png').convert_alpha(), pygame.image.load('Babel Invader/explosion2.png').convert_alpha(),pygame.image.load('Babel Invader/explosion1.png').convert_alpha()]
        self.achats = {}
        self.achat_tir = tir2
        self.police = pygame.font.Font('babelcasino.ttf', 16)
        self.police2 = pygame.font.Font('babelcasino.ttf', 32)
        self.ennemi_faible = lambda x: Ennemi(x, 3, [pygame.image.load("Babel Invader/ennemi.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/ennemi2.png").convert_alpha()], 1, -5, 10)
        self.ennemi_moyen = lambda x: Ennemi(x, 2.5, [pygame.image.load("Babel Invader/ennemi3.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi4.png").convert_alpha()], 3, -10, 20)
        self.ennemi_rapide = lambda x: Ennemi(x, 4, [pygame.image.load("Babel Invader/ennemi5.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/ennemi6.png").convert_alpha()], 1, -2.5, 15)
        self.ennemi_tank = lambda x: Ennemi(x, 2, [pygame.image.load("Babel Invader/ennemi7.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi8.png").convert_alpha()], 7, -18, 25)
        self.ennemi_attaquant = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/ennemi9.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi10.png").convert_alpha()], 6, -20, 30)
        self.ennemi_boss = lambda x: Ennemi(x, 1, [pygame.image.load("Babel Invader/ennemi11.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi11.png").convert_alpha()], 40, -50, 100)
        self.ennemi_moyen2 = lambda x: Ennemi(x, 2.8, [pygame.image.load("Babel Invader/ennemi12.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi13.png").convert_alpha()], 4, -8, 20)
        self.ennemi_tank2 = lambda x: Ennemi(x, 1.5, [pygame.image.load("Babel Invader/ennemi14.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi15.png").convert_alpha()], 10, -25, 30)
        self.ennemi_faible2 = lambda x: Ennemi(x, 3, [pygame.image.load("Babel Invader/ennemi16.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/ennemi17.png").convert_alpha()], 2, -6, 12)
        self.ennemi_kamikaze = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/ennemi18.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/ennemi19.png").convert_alpha()], 4, -18, 25)
        self.caillou1 = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/caillou4.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/caillou4.png").convert_alpha()], 2, -6, 0)
        self.caillou2 = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/caillou3.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/caillou3.png").convert_alpha()], 4, -10, 0)
        self.caillou3 = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/caillou2.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/caillou2.png").convert_alpha()], 8, -14, 0)
        self.caillou4 = lambda x: Ennemi(x, 3.5, [pygame.image.load("Babel Invader/caillou1.png").convert_alpha(), 
                                                    pygame.image.load("Babel Invader/caillou1.png").convert_alpha()], 16, -18, 0)
        # Définition des phases sous forme de dictionnaire
        self.phases = {
            (0, 15):    {self.ennemi_faible: 60, self.ennemi_moyen: 20, self.caillou1: 20},
            (15, 45):   {self.ennemi_faible: 40, self.ennemi_moyen: 25, self.ennemi_rapide: 15, self.caillou1: 10, self.caillou2: 10},
            (45, 90):   {self.ennemi_faible2: 20, self.ennemi_moyen2: 20, self.ennemi_rapide: 15, self.ennemi_tank: 15, 
                        self.ennemi_moyen: 10, self.caillou1: 10, self.caillou2: 5, self.caillou3: 5},
            (90, 120):  {self.ennemi_faible2: 20, self.ennemi_moyen2: 20, self.ennemi_tank2: 15, self.ennemi_kamikaze: 15, 
                        self.ennemi_tank: 10, self.caillou2: 10, self.caillou3: 10},
            (120, 160): {self.ennemi_moyen2: 20, self.ennemi_tank2: 20, self.ennemi_kamikaze: 18, self.ennemi_attaquant: 15, 
                        self.caillou3: 12, self.caillou4: 10, self.ennemi_boss: 5},
            (160, float('inf')): {self.ennemi_tank2: 25, self.ennemi_attaquant: 23, self.ennemi_kamikaze: 17, 
                                self.caillou3: 15, self.caillou4: 10, self.ennemi_boss: 10}
        }


    def calculer_prix(self, niveau_base:float, multi:float=3):
        '''Calcul du prix en fonction du niveau de base et du multiplificateur'''
        return int(20 * multi**(niveau_base)//2)
    
    def reset(self):
        '''Permet de réinitialiser les caractéristiques du jeu, pour une nouvelle partie'''
        self.vaisseau.reset()
        self.ennemis = []
        self.explosions = []
        self.temps_dernier_ennemi = 0
        self.intervalle_spawn = 2.0
        self.temps_debut = 0
        self.achats = {}
        self.achat_tir = tir2

    def get_run(self) -> bool:
        return self.run
        
    def jouer(self):
        '''Permet de lancer le jeu'''
        self.run = True
        self.temps_debut = pygame.time.get_ticks() / 1000
        # Conditions pour que le jeu continue 
        while self.run and self.vaisseau.get_vie() > 0:
            # Image pour le vaisseau tant qu'il est de niveau < 4
            if self.vaisseau.get_tir_lvl() < 4:
                self.achat_tir = tirs[self.vaisseau.get_tir_lvl()-1]
            else:
                self.achat_tir = None  # Désactiver l'achat de tirs si niveau 4+
            # Dictionnaire des achats : bouton / prix
            self.achats = {
                pieces_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Multiplicateur'],3.5),
                vitesse_proj_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vitesse projectile'],2),
                vitesse_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vitesse'],1.2),
                cd_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Couldown'],4),
                heal_bouton: 50,  # Prix fixe pour les soins
                max_hp_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vie max'])
            }
            # Si self.achat_tir (donc si le tir est lvl < a 4)
            if self.achat_tir:
                # On met l'image correspondante au prix correspondant
                self.achats[self.achat_tir] = self.calculer_prix(self.vaisseau.get_lvl()['Projectile'],6)
            # Boucle events pygame
            for event in pygame.event.get():
                # Fermeture du jeu
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                # Si le joueur clique
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Pour tous les bonus achetables de la boutique
                    for achat, prix in self.achats.items():
                        # Si le joueur a assez de pièces pour l'achat du bonus correspondant et clique sur celui-ci
                        if achat.collision(pygame.mouse.get_pos()) and self.vaisseau.get_pieces() >= prix:
                            # On enlève les pièces du joueur du montant du bonus
                            self.vaisseau.set_pieces(-prix)
                            # On lui fait profiter du bonus correspondant
                            if achat == self.achat_tir:
                                self.vaisseau.set_lvl('Projectile',1)
                                self.vaisseau.set_tir(1), self.vaisseau.set_dgt(1)
                            elif achat == pieces_bouton:
                                self.vaisseau.set_lvl('Multiplicateur',1)
                                self.vaisseau.set_multi(1.5)
                            elif achat == vitesse_proj_bouton:
                                self.vaisseau.set_vitesse_projectile(2)
                                self.vaisseau.set_lvl('Vitesse projectile',1)
                            elif achat == vitesse_bouton:
                                self.vaisseau.set_vitesse(1.5)
                                self.vaisseau.set_lvl('Vitesse',1)
                            elif achat == cd_bouton:
                                self.vaisseau.set_lvl('Couldown',1)
                                self.vaisseau.set_cd(-0.08)
                            elif achat == heal_bouton:
                                self.vaisseau.set_lvl('Vie',1)
                                self.vaisseau.set_vie(25)
                            elif achat == max_hp_bouton:
                                self.vaisseau.set_lvl('Vie max',1)
                                self.vaisseau.set_vie_max(50)
            
            temps_actuel = pygame.time.get_ticks() / 1000 # Temps en secondes
            temps_ecoule = temps_actuel - self.temps_debut # Temps en secondes depuis le début du jeu
            # Intervalle de temps entre les apparitions d'ennemis
            self.intervalle_spawn = max(0.35, 2.0 - (temps_ecoule / 45))
            # Si le temps entre le dernier ennemi apparu et maintenant atteint la valeur du couldown entre deux apparitions
            if temps_actuel - self.temps_dernier_ennemi >= self.intervalle_spawn:
                # Choix aléatoire de la position x de l'ennemi
                x_ennemi = random.randint(210, largeur - 50)
                # Sélection des ennemis basée sur le temps écoulé
                for (debut, fin), ennemis in self.phases.items():
                    # SI c'est la phase actuelle
                    if debut <= temps_ecoule < fin:
                        # On récupère les ennemis possibles pour cette phase
                        ennemis_possibles = np.concatenate([np.repeat(e, n) for e, n in ennemis.items()])
                # Ajout d'un ennemi au jeu aléatoirement parmi ceux de la phase sur l'écran
                self.ennemis.append(random.choice(ennemis_possibles)(x_ennemi))
                # Mise à jour du temps de l'ennemi le plus récent
                self.temps_dernier_ennemi = temps_actuel
            # Fond noir
            fenetre.fill((0, 0, 0))
            # Image de la boutique
            fenetre.blit(self.boutique, (0,0))
            # Pour chaque ennemi
            for ennemi in self.ennemis:
                # On met à jour les ennemis (déplacements, animation, dégâts)
                ennemi.update(self.vaisseau)
                if not ennemi.get_actif():
                    # Création des explosions à l'endroit ou l'ennemi a été tué
                    self.explosions.append(Explosion(
                        ennemi.x, 
                        ennemi.y,
                        self.explosion_frames
                    ))
                    # On enlève l'ennemi de la liste
                    self.ennemis.remove(ennemi)
                else:
                    # Sinon on le dessine
                    ennemi.dessiner(fenetre)

            # Mise à jour et dessin des explosions
            for explosion in self.explosions:
                # Animation de l'explosion
                explosion.update()
                # Si l'explosion prend fin
                if not explosion.actif:
                    # On enlève l'explosion de la liste
                    self.explosions.remove(explosion)
                else:
                    # Sinon on dessine l'explosion
                    explosion.dessiner(fenetre)
            # Pour chaque bonus de la boutique
            for achat, prix in self.achats.items():
                # On affiche le bouton
                achat.draw(fenetre, pygame.mouse.get_pos())
                # Text du prix du bonus
                prix_text = self.police.render(f"{int(prix)} pièces", True, (255, 255, 255))
                # On affiche le prix
                fenetre.blit(prix_text, (achat.rect.x-20, achat.rect.y + 60))
            # Permet de gérer les actions du vaisseau
            self.vaisseau.jouer(fenetre, self.ennemis)
            # On affiche la souris
            fenetre.blit(souris, pygame.mouse.get_pos())
            # On actualise
            pygame.display.flip()
            clock.tick(60)
        # Texte de fin de jeu
        game_over_text = self.police2.render('Perdu', True, (255, 0, 0))
        score_text = self.police2.render(f'Score final: {self.vaisseau.score}', True, (255, 255, 255))
        # On affiche le score à la fin du jeu
        fenetre.blit(game_over_text, (largeur//2 - 150, hauteur//2 - 50))
        fenetre.blit(score_text, (largeur//2 - 150, hauteur//2 + 50))
        # On attend 3 secondes avant de fermer le jeu
        pygame.display.flip()
        pygame.time.wait(3000)
        # On met à jour le solde du joueur 
        if self.vaisseau.get_score() < 5000:
            # S'il a moins de 5000 de score, il perd 12% de son solde - 1000 pièces
            joueur1.modifier_cagnotte(-joueur1.get_cagnotte()//8 - 1000)
        # Sinon
        else:
            # Il gagne 10% de son solde + 2500 pièces + son score en pièces
            joueur1.modifier_cagnotte(self.vaisseau.get_score() + 2500 + joueur1.get_cagnotte()//10)
        # Fin du jeu
        self.run = False