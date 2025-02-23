import pygame
import random
from objets_et_variables import *

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
        if temps_actuel - self.temps_derniere_frame > self.delai_animation:
            self.frame_actuelle += 1
            if self.frame_actuelle >= len(self.frames):
                self.actif = False
                return
            self.img = self.frames[self.frame_actuelle]
            self.temps_derniere_frame = temps_actuel
    
    def dessiner(self, fenetre: pygame.display):
        '''Affiche l'explosion à l'écran'''
        fenetre.blit(self.img, (self.x, self.y))

class Ennemi:
    def __init__(self, x:int,vitesse:int, img:list, vie:int, dgt:int, pieces:int) -> 'Ennemi':
        self.x = x # Position x de l'ennemi
        self.y = -50  # Commence au-dessus de l'écran
        self.vitesse = vitesse # Vitesse de l'annemi
        self.actif = True # Actif
        self.frames = img
        self.frame_actuelle = 0
        self.temps_derniere_frame = pygame.time.get_ticks()
        self.delai_animation = 500  # Changement de frame toutes les 500ms
        self.img = self.frames[self.frame_actuelle]
        self.vie = vie # Pv de l'ennemi
        self.dgt = dgt
        self.pieces = pieces
        
    def update(self,vaisseau:'Vaisseau'):
        '''Permet de faire avancer les ennemis. Si l'ennemi arrive en bas de l'écran, on le supprime et on inflige
        des dégâts au vaisseau. 
        Paramètres :
            - vaisseau : un objet de la classe Vaisseau'''
        self.y += self.vitesse # On fait avancer l'ennemi
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - self.temps_derniere_frame > self.delai_animation:
            self.frame_actuelle = (self.frame_actuelle + 1) % 2
            self.img = self.frames[self.frame_actuelle]
            self.temps_derniere_frame = temps_actuel
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
        return rect_ennemi.colliderect(rect_projectile)
    
    def get_vie(self) -> int:
        return self.vie
    def set_vie(self, vie:int):
        self.vie += vie
    def set_actif(self, act):
        self.actif = act
    def get_pieces(self) -> int:
        return self.pieces

class Projectile:
    def __init__(self, x:int, y:int, vitesse:int, img:pygame.image,dgt):
        '''Initialise un projectile.
        Paramètres :
            - x  : (int) La position x du projectile
            - y  : (int) La position y du projectile
            - vitesse : (int) La vitesse du projectile
            - img : (pygame.image) L'image du projectile'''
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
    
    def set_dgt(self, dgt:int) -> None:
        '''Permet d'augmenter les dégâts que le projectile inflige'''
        self.dgt += dgt

    def set_actif(self,act):
        self.actif = act

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

class Vaisseau:
    def __init__(self) -> 'Vaisseau':
        self.vie_max = 100
        self.vie = 100
        self.x = 375
        self.y = 750
        self.vitesse_projectile = 5
        self.cd = 0.5
        self.vitesse = 3
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
    def get_pieces(self):
        return self.pieces
    def set_pieces(self, pieces):
        self.pieces += pieces
    def get_vie(self) -> int:
        return self.vie
    def set_vie(self, vie: int):
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
    def set_vitesse(self, vitesse: int):
        self.vitesse += vitesse
    def get_vitesse(self):
        return self.vitesse
    def get_cd(self) -> int:
        return self.cd
    def set_cd(self, cd: int):
        self.cd += cd
    def set_vie_max(self, vie_max):
        self.vie_max += vie_max
    def get_vie_max(self):
        return self.vie_max
    def get_score(self):
        return self.score
    def set_tir(self,v):
        self.projectile_lvl += v
    def get_tir_lvl(self):
        return self.projectile_lvl
    def get_multi(self):
        return self.multi
    def set_multi(self, multi: int):
        self.multi *= multi
    def get_lvl(self):
        return self.lvl
    def set_lvl(self, clef, lvl: int):
        self.lvl[clef] += lvl        
    def set_dgt(self,dgt):
        self.dgt += dgt
    def jouer(self, fenetre, ennemis):
        self.frame = self.frames[self.projectile_lvl-1]
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and self.x > 210:
            self.x -= self.vitesse
        elif touches[pygame.K_RIGHT] and self.x < 750:
            self.x += self.vitesse
            
        temps_actuel = pygame.time.get_ticks() / 1000
        if temps_actuel - self.dernier_tir >= self.cd:
            self.projectiles.append(Projectile(self.x + (self.frames[0].get_width() - pygame.image.load(f"Babel Invader/missile{self.projectile_lvl}.png").get_width()) // 2, self.y, self.vitesse_projectile, pygame.image.load(f"Babel Invader/missile{self.projectile_lvl}.png").convert_alpha(),self.dgt))
            self.dernier_tir = temps_actuel
            
        # Mise à jour et collision des projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            if not projectile.actif:
                self.projectiles.remove(projectile)
            else:
                for ennemi in ennemis[:]:
                    if ennemi.collision(projectile):
                        ennemi.set_vie(-projectile.get_dgt())
                        projectile.set_actif(False)
                        if ennemi.get_vie() <= 0:
                            ennemi.set_actif(False)
                            self.score += ennemi.get_pieces()*10
                            self.pieces += ennemi.get_pieces()*self.multi
                projectile.dessiner(fenetre)
        
        fenetre.blit(self.frame, (self.x, self.y))
        
        # Affichage du score et de la vie
        font = pygame.font.Font(None, 24)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        vie_text = font.render(f'Vie: {int(self.vie)}', True, (255, 255, 255))
        pieces_text = font.render(f'Pieces: {int(self.pieces)}', True, (255, 255, 255))
        fenetre.blit(score_text, (30, 15))
        fenetre.blit(vie_text, (30, 45))
        fenetre.blit(pieces_text, (30,75))

class BabelInvader:
    def __init__(self):
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
        self.ennemi_boss = lambda x: Ennemi(x, 2.8, [pygame.image.load("Babel Invader/ennemi11.png").convert_alpha(), 
                                                     pygame.image.load("Babel Invader/ennemi11.png").convert_alpha()], 50, -50, 100)
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

    def calculer_prix(self, niveau_base, multi=3):
        return int(20 * multi**(niveau_base)//2)
    
    def reset(self):
        self.vaisseau.reset()
        self.ennemis = []
        self.explosions = []
        self.temps_dernier_ennemi = 0
        self.intervalle_spawn = 2.0
        self.temps_debut = 0
        self.achats = {}
        self.achat_tir = tir2

    def get_run(self):
        return self.run
        
    def jouer(self):
        #if self.ecran.get_actif():
        self.run = True
        self.temps_debut = pygame.time.get_ticks() / 1000
        
        while self.run and self.vaisseau.get_vie() > 0:
            if self.vaisseau.get_tir_lvl() < 4:
                self.achat_tir = tirs[self.vaisseau.get_tir_lvl()-1]
            else:
                self.achat_tir = None  # Désactiver l'achat de tirs si niveau 4+
            
            self.achats = {
                pieces_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Multiplicateur'],3.5),
                vitesse_proj_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vitesse projectile'],2),
                vitesse_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vitesse'],1.2),
                cd_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Couldown'],4),
                heal_bouton: 50,  # Prix fixe pour les soins
                max_hp_bouton: self.calculer_prix(self.vaisseau.get_lvl()['Vie max'])
            }
            if self.achat_tir:
                self.achats[self.achat_tir] = self.calculer_prix(self.vaisseau.get_lvl()['Projectile'],6)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for achat, prix in self.achats.items():
                        if achat.collision(pygame.mouse.get_pos()) and self.vaisseau.get_pieces() >= prix:
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
                            self.vaisseau.set_pieces(-prix)
            
            temps_actuel = pygame.time.get_ticks() / 1000
            temps_ecoule = temps_actuel - self.temps_debut
            
            self.intervalle_spawn = max(0.5, 2.0 - (temps_ecoule / 40))
            
            if temps_actuel - self.temps_dernier_ennemi >= self.intervalle_spawn:
                x_ennemi = random.randint(210, largeur - 50)
                # Sélection des ennemis basée sur le temps écoulé
                if temps_ecoule < 15:
                    ennemis_possibles = [self.ennemi_faible] * 60 + \
                                        [self.ennemi_moyen] * 20 + \
                                        [self.caillou1] * 20

                # Phase 2: 30-60 secondes - Premiers défis
                elif temps_ecoule < 45:
                    ennemis_possibles = [self.ennemi_faible] * 40 + \
                                        [self.ennemi_moyen] * 25 + \
                                        [self.ennemi_rapide] * 15 + \
                                        [self.caillou1] * 10 + \
                                        [self.caillou2] * 10

                # Phase 3: 60-120 secondes - Montée en difficulté
                elif temps_ecoule < 90:
                    ennemis_possibles = [self.ennemi_faible2] * 20 + \
                                        [self.ennemi_moyen2] * 20 + \
                                        [self.ennemi_rapide] * 15 + \
                                        [self.ennemi_tank] * 15 + \
                                        [self.ennemi_moyen] * 10 + \
                                        [self.caillou1] * 10 + \
                                        [self.caillou2] * 5 + \
                                        [self.caillou3] * 5

                # Phase 4: 120-180 secondes - Défi intermédiaire
                elif temps_ecoule < 120:
                    ennemis_possibles = [self.ennemi_faible2] * 20 + \
                                        [self.ennemi_moyen2] * 20 + \
                                        [self.ennemi_tank2] * 15 + \
                                        [self.ennemi_kamikaze] * 15 + \
                                        [self.ennemi_tank] * 10 + \
                                        [self.caillou2] * 10 + \
                                        [self.caillou3] * 10

                # Phase 5: 180-240 secondes - Haute difficulté
                elif temps_ecoule < 160:
                    ennemis_possibles = [self.ennemi_moyen2] * 20 + \
                                        [self.ennemi_tank2] * 20 + \
                                        [self.ennemi_kamikaze] * 18 + \
                                        [self.ennemi_attaquant] * 15 + \
                                        [self.caillou3] * 12 + \
                                        [self.caillou4] * 10 + \
                                        [self.ennemi_boss] * 5

                # Phase 6: 240+ secondes - Phase finale
                else:
                    ennemis_possibles = [self.ennemi_tank2] * 25 + \
                                        [self.ennemi_attaquant] * 23 + \
                                        [self.ennemi_kamikaze] * 17 + \
                                        [self.caillou3] * 15 + \
                                        [self.caillou4] * 10 + \
                                        [self.ennemi_boss] * 10
                    
                
                self.ennemis.append(random.choice(ennemis_possibles)(x_ennemi))
                self.temps_dernier_ennemi = temps_actuel
            
            fenetre.fill((0, 0, 0))
            fenetre.blit(self.boutique, (0,0))
            
            for ennemi in self.ennemis:
                ennemi.update(self.vaisseau)
                if not ennemi.actif:
                    # Création de deux explosions à des positions légèrement décalées
                    self.explosions.append(Explosion(
                        ennemi.x, 
                        ennemi.y,
                        self.explosion_frames
                    ))
                    self.ennemis.remove(ennemi)
                else:
                    ennemi.dessiner(fenetre)

            # Mise à jour et dessin des explosions
            for explosion in self.explosions:
                explosion.update()
                if not explosion.actif:
                    self.explosions.remove(explosion)
                else:
                    explosion.dessiner(fenetre)
            
            for achat, prix in self.achats.items():
                achat.draw(fenetre, pygame.mouse.get_pos())
                font = pygame.font.Font(None, 24)
                prix_text = font.render(f"{int(prix)} pièces", True, (255, 255, 255))
                fenetre.blit(prix_text, (achat.rect.x, achat.rect.y + 40))
            
            self.vaisseau.jouer(fenetre, self.ennemis)
            fenetre.blit(souris, pygame.mouse.get_pos())
            pygame.display.flip()
            clock.tick(60)
        
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Perdu', True, (255, 0, 0))
        score_text = font.render(f'Score final: {self.vaisseau.score}', True, (255, 255, 255))
        fenetre.blit(game_over_text, (largeur//2 - 150, hauteur//2 - 50))
        fenetre.blit(score_text, (largeur//2 - 150, hauteur//2 + 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        if self.vaisseau.get_score() < 3500:
            joueur1.modifier_cagnotte(-joueur1.get_cagnotte()//8 - 1000)
        else:
            joueur1.modifier_cagnotte(self.vaisseau.get_score() + 2500 + joueur1.get_cagnotte()//12)
        
        self.run = False