import pygame
from objets_et_variables import *
import sys

print("Chargement du jeu de platforme...")

#-------Niveau 1------#
def decor_niveau1():
    '''Définit tous les éléments du décor du niveau 1.
    Returns : 
        - dictionnaire (dict) avec les éléments de décor et leur position sur le terrain.'''
    pente1 = Decor(90,1600,625,'Sol')
    pente2 = Decor(90,1600,625,'Sol')
    rocher1 = Decor(90,1600,508,'Sol','Jeu_platforme/decor/rocher.png')
    platforme1 = Decor(40,1600,470,'Platforme','Jeu_platforme/decor/platforme2.png')
    platforme2 = Decor(20,1600,500,'Platforme','Jeu_platforme/decor/platforme2.png')
    platforme3 = Decor(40,1600,470,'Platforme','Jeu_platforme/decor/platforme.png')
    platforme4 = Decor(20,1600,420,'Platforme','Jeu_platforme/decor/platforme.png')
    return {rocher1:30, pente2:800, platforme1:180, platforme2:500,platforme3:400,platforme4:650}

def obs_niveau1():
    '''Définit tous les obstacles du niveau 1.
    Returns : 
        - dictionnaire (dict) avec les obstacles et leur position sur le terrain.'''
    pic1 = Pique(1600,550,'Jeu_platforme/Obs/Rocher.png')
    pic2 = Pique(1600,425,'Jeu_platforme/Obs/Requin.png',12)
    pic3 = Pique(1600,525,'Jeu_platforme/Obs/Requin2.png')
    pic4 = Pique(1600,625,'Jeu_platforme/Obs/rocher2.png')
    pic5 = Pique(1600,550,'Jeu_platforme/Obs/Rocher.png')
    pic6 = Pique(1600,425,'Jeu_platforme/Obs/Requin.png',12)
    pic7 = Pique(1600,525,'Jeu_platforme/Obs/Requin2.png')
    pic8 = Pique(1600,625,'Jeu_platforme/Obs/rocher2.png')
    poisson = Pique(1600,500,'Jeu_platforme/Obs/Poisson2.png',15)
    poisson3 = Pique(1600,300,'Jeu_platforme/Obs/poisson.png',15)
    poisson4 = Pique(1600,580,'Jeu_platforme/Obs/Poisson2.png',15)
    return {pic1:200, pic2:350, pic3:550, pic4:750, pic5:1100, pic6:820, pic7:890, pic8:970, poisson:250, poisson4:250, poisson3:350, poisson4:950}

#---------Fin---------#

class Voiture:
    def __init__(self) -> 'Voiture':
        self.x = 40
        self.y = 600
        self.saut = False
        self.cd = False # Lorsque la voiture retombe après le saut mais n'a pas encore touché le sol
        self.sprites = [pygame.image.load(f'Jeu_platforme/Voiture/_a_frm{i},40.png').convert_alpha() for i in range(4)]
        self.sprites_saut = [pygame.image.load(f'Jeu_platforme/Voiture/Saut/_a_frm{i},40.png').convert_alpha() for i in range(3)]
        self.frame = 0
        self.speed = 0.45
    def get_x(self) -> float:
        return self.x
    def get_y(self) -> float:
        return self.y
    def get_frame(self) -> int:
        return int(self.frame)
    def get_sprites(self) -> list:
        return self.sprites
    def get_saut(self) -> bool:
        return self.saut
    def set_cd(self, cd:bool): 
        self.cd = cd
    def get_cd(self) -> bool:
        return self.cd
    def set_frame(self, frame:float):
        self.frame = frame
    def set_saut(self, saut:bool):
        self.saut = saut
    def set_y(self,y:float):
        self.y = y
    def get_sprites_saut(self) -> list:
        return self.sprites_saut
    def anim(self):
        self.frame += self.speed
        if int(self.frame) >= len(self.sprites):
            self.frame = 0
    def anim_saut(self):
        self.frame += self.speed
        if int(self.frame) >= len(self.sprites_saut):
            self.frame = 0

class Pique:
    def __init__(self,x:float,y:float,img:str,s:float=10) -> 'Pique':
        self.x = x
        self.y = y
        self.actif = False
        self.img = pygame.image.load(img).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img)
        self.speed = s
    def get_speed(self) -> float:
        return self.speed
    def get_actif(self) -> bool:
        return self.actif
    def set_actif(self,actif:bool):
        self.actif = actif
    def get_y(self) -> float:
        return self.y
    def get_x(self) -> float:
        return self.x
    def modif_x(self,x:float):
        self.x = x
    def affiche(self):
        fenetre.blit(self.img, (self.x, self.y))
    def get_mask(self):
        return self.mask

class Decor:
    def __init__(self,h:int,x:float,y:float,typee:str,img:str='Jeu_platforme/Decor/pente1.png') -> 'Decor':
        self.x = x
        self.y = y
        self.hauteur = h
        self.actif = False
        self.img = pygame.image.load(img).convert_alpha()
        self.mask = pygame.mask.from_surface(self.img)
        self.typee = typee
    def get_actif(self) -> bool:
        return self.actif
    def set_actif(self,actif:bool):
        self.actif = actif
    def get_y(self) -> float:
        return self.y
    def get_x(self) -> float:
        return self.x
    def get_hauteur(self) -> int:
        return self.hauteur
    def modif_x(self,x:float):
        self.x = x 
    def affiche(self):
        fenetre.blit(self.img, (self.x, self.y))
    def get_mask(self):
        return self.mask
    def get_img(self):
        return self.img
    def get_typee(self) -> str:
        return self.typee
        
class BabelRace:
    def __init__(self) -> 'BabelRace':
        self.fond = pygame.image.load('Jeu_platforme/Fonds/fond.png').convert_alpha()
        self.run = False # Permet de savoir si le jeu est actif
        self.reussi = False # Permet de savoir si le joueur a réussi le niveau
        self.fond_x = 0 # Position du fond
        self.sol = 600  # Sol par défaut
        self.sol2 = 500 # Sol qui correspond aux platformes
        self.x_simule = 40  # On simule l'avancement de la voiture dans le niveau (élément déclencheur de l'apparition des obstacles, éléments divers et fin du niveau)
        self.pentes = decor_niveau1()   # On charge les éléments de décor du niveau
        self.obs = obs_niveau1()    # On charge les obstacles du niveau
        self.defaite = False
    def actif(self, etat:bool):
        self.run = etat
    def get_actif(self) -> bool:
        return self.run
    def def_sol(self, img:'pygame.Surface', x:int, obj:'Decor',hauteur_img:int,sol:int) -> int: 
        '''Permet de déterminer la hauteur de l'image et donc le niveau du sol
        Paramètres : 
            - img : Surface sur laquelle on cherche le sol
            - x (int): Position de l'image sur laquelle on cherche le sol
            - obj : Objet sur lequel on cherche le sol
            - hauteur_img (int): Hauteur de l'image
            - sol (int): Niveau du sol initial
        Returns :
            - La hauteur de l'image sur laquelle on cherche le sol
        '''
        assert isinstance(img, pygame.Surface), "L'argument img doit être une surface"
        assert isinstance(obj, Decor), "L'argument obj doit être un objet de type Decor"
        sol_initial = 600 # Niveau de sol initial
        image_rect = img.get_rect(topleft=(obj.get_x(), obj.get_y()))   # Rectangle de l'image
        relative_x = x - image_rect.x   # Position relative de l'image par rapport a la voiture

        if 0 <= relative_x < image_rect.width:  # Vérifie si le point x est dans les limites de l'image
            img_y = None    # Variable pour stocker la première hauteur non transparente trouvée

            for y in range(image_rect.height):  # Pour chaque pixel vertical de l'image à la position relative x
                pixel = img.get_at((relative_x, y))     # Récupérer la couleur
                if pixel.a > 0:  # Vérification de la transparence
                    if img_y is None:
                        img_y = y   # Mémorise la première hauteur non transparente si pas encore trouvée
                    if img_y is not None:
                        # Calculer la hauteur par rapport au bas de la pente
                        hauteur_surface = image_rect.y + img_y
                        return hauteur_surface-hauteur_img  # Si un point est trouvé, retourner la hauteur de la surface

        if sol < sol_initial:
            return sol + 3  # On fait descendre la voiture petit a petit
        else:
            return sol  # Si aucun point n'est trouvé, retourner le sol par défaut
        
    def lancer(self):
        '''Lancement du jeu
        - plat (bool) : Présence d'une platforme, et donc d'un potentiel 2e sol
        - hauteur_surface (int) : Hauteur de la surface sur laquelle on cherche le sol'''
        self.largeur, self.hauteur = 1700, 700  # Dimensions de la fenêtre
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))  # Création de la fenêtre
        self.clock = pygame.time.Clock()  # Gestion des FPS
        self.x_simule = 0  # Position simulée pour le défilement
        plat = False  # Indique si la voiture est sur une plateforme
        hauteur_surface = None  # Hauteur de la surface courante
        # Chargement des décors et obstacles du niveau 
        self.pentes = decor_niveau1()
        self.obs = obs_niveau1()
        x_fond = 0  # Position du fond d'écran
        # Boucle principale du jeu
        while self.run:
            # Gestion du fond défilant
            fenetre.blit(self.fond,(x_fond,0))
            x_fond -= 10  # Déplacement du fond vers la gauche
            self.x_simule += 1 # Augmentation de la position x simulée de la voiture
            # Condition de fin de niveau
            if self.x_simule >= 1500:
                self.run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Fermeture de la fenêtre
                    self.run = False
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Saut avec la barre d'espace
                        if not voiture.get_saut() and not voiture.get_cd():
                            voiture.set_frame(0)
                            voiture.set_saut(True)
            
            # Gestion du saut de la voiture
            if voiture.get_saut():
                voiture.set_y(voiture.get_y() - 9)  # Mouvement vers le haut
                if voiture.get_y() < self.sol-320:  # Hauteur maximum du saut
                    voiture.set_saut(False)     # Fin du saut
                    voiture.set_cd(True)
            # Gestion de la chute
            elif voiture.get_y() <= self.sol:
                if plat and voiture.get_y() >= hauteur_surface - 5:  # Atterrissage sur une plateforme
                    voiture.set_cd(False)
                    voiture.set_y(hauteur_surface + 15)
                else:
                    voiture.set_y(voiture.get_y() + 7)  # Chute
            else:
                voiture.set_cd(False)
            # Gestion des décors (pentes et plateformes)
            for decor, pos in self.pentes.items():
                # Activation du décor quand on arrive à sa position
                if self.x_simule >= pos:
                    decor.set_actif(True)
                if decor.get_actif():
                    # Déplacement et affichage du décor
                    decor.modif_x(decor.get_x() - 10)
                    decor.affiche()
                    # Désactivation si hors écran
                    if decor.get_x() <= -800:
                        decor.set_actif(False)
                        
                    # Calcul de la hauteur du sol pour le décor actuel
                    hauteur_surface = self.def_sol(decor.get_img(), voiture.get_x(), decor, decor.get_hauteur(), self.sol)
                    
                    if hauteur_surface is not None:
                        if decor.get_typee() == 'Sol':  # Gestion du sol
                            self.sol = hauteur_surface
                            if not voiture.get_saut() and not voiture.get_cd():
                                voiture.set_y(self.sol)
                        elif decor.get_typee() == 'Platforme':  # Gestion des plateformes
                            voiture_bottom = voiture.get_y() + voiture.get_sprites()[0].get_height()
                            plateforme_top = hauteur_surface
                            
                            # Vérification de la collision avec la plateforme
                            if (voiture.get_x() + voiture.get_sprites()[0].get_width() > decor.get_x() and voiture.get_x() < decor.get_x() + decor.get_img().get_width()):
                                
                                # Atterrissage sur la plateforme
                                if voiture_bottom >= plateforme_top and voiture.get_y() < plateforme_top:
                                    if not voiture.get_saut():
                                        plat = True
                                        self.sol2 = hauteur_surface
                                        voiture.set_y(plateforme_top - voiture.get_sprites()[0].get_height() + decor.get_hauteur())
                                else:
                                    plat = False
                            else:
                                plat = False

            # Gestion de l'animation de la voiture
            if voiture.get_saut():
                voiture.anim_saut()
                image = voiture.get_sprites_saut()[voiture.get_frame()]
            else:
                voiture.anim()
                image = voiture.get_sprites()[voiture.get_frame()]
                
            # Création du masque de collision pour la voiture
            mask = pygame.mask.from_surface(image)
            
            # Gestion des obstacles
            for obs,pos in self.obs.items():
                # Activation de l'obstacle à sa position
                if self.x_simule >= pos and not obs.get_actif():
                    obs.set_actif(True)
                if obs.get_actif():
                    # Déplacement et affichage de l'obstacle
                    obs.modif_x(obs.get_x() - obs.get_speed())
                    obs.affiche()
                    # Désactivation si hors écran
                    if obs.get_x() <= -100:
                        obs.set_actif(False)
                        
                    # Vérification des collisions avec la voiture
                    offset_x = voiture.get_x() - obs.get_x()
                    offset_y = voiture.get_y() - obs.get_y()
                    mask_overlap = mask.overlap(obs.get_mask(), (-offset_x, -offset_y))
                    if mask_overlap:
                        print(pos)
                        self.defaite = True
                        self.run = False
            
            # Affichage des éléments
            fenetre.blit(image,(voiture.get_x(),voiture.get_y()))  # Voiture
            clock.tick(60)  # Limitation à 60 FPS
            fenetre.blit(souris, pygame.mouse.get_pos())  # Curseur personnalisé
            pygame.display.flip()  # Mise à jour de l'écran
            
        # Gestion de fin de partie
        if self.defaite:
            # Perte d'argent en cas de défaite
            joueur1.modifier_cagnotte(-joueur1.get_cagnotte()/4-100)
        else:
            # Gain d'argent en cas de victoire
            joueur1.modifier_cagnotte(joueur1.get_cagnotte()/6+100)
            
        # Retour à la fenêtre de menu
        self.defaite = False
        pygame.display.set_mode((800,800))
        self.actif(False)
        
voiture = Voiture()
babelrace = BabelRace()