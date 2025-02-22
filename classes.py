# classes.py
import pygame
from img import fenetre,charger_et_agrandir

print("Chargement des classes...")

class Joueur:
    def __init__(self, pseudo:str = '') -> 'Joueur':
        self.pseudo = pseudo
        self.cagnotte = 200000
        self.roulette_active = False
        self.mdp = ' '
        self.code_cb = None
        self.num_cb = None
        self.inventaire = {'Biere' : 0, 'Whisky' : 0, 'Mojito' : 0, 'Crampons' : 0}
        self.heros = ['Night Hero']
        self.gains = {'Roulette': 1.0, 'Blackjack': 1.0, 'Pile ou Face': 1.0}
        self.probas = {'Roulette':0,'Blackjack':1.0,'Pile ou Face': 1.0}
        self.multis = 1
    def get_pseudo(self):
        return self.pseudo
    def get_multis_jeu_combat(self):
        return self.multis
    def get_cagnotte(self):
        return self.cagnotte
    def get_roulette_active(self):
        return self.roulette_active
    def get_mdp(self):
        return self.mdp
    def get_code_cb(self):
        return self.code_cb
    def get_num_cb(self):
        return self.num_cb
    def get_heros(self):
        return self.heros
    def get_inventaire(self):
        return self.inventaire
    def get_gains(self):
        return self.gains
    def get_probas(self):
        return self.probas
    def set_pseudo(self, pseudo:str):
        self.pseudo = pseudo
    def set_cagnotte(self, cagnotte:float):
        self.cagnotte = cagnotte
    def modifier_cagnotte(self, montant:float):   
        """
        Permet de modifier le solde du joueur.
        Paramètres :
            - montant (float) : le montant à ajouter ou à retirer de la cagnotte
        """
        self.cagnotte += montant
    def set_multis_jeu_combat(self,val):
        self.multis = val
    def set_roulette_active(self, actif:bool):
        self.roulette_active = actif
    def set_mdp(self, mdp:str):
        self.mdp = mdp
    def set_code_cb(self, code:str):
        self.code_cb = code
    def set_num_cb(self, num:str):
        self.num_cb = num
    def ajouter_inventaire(self,article:str):
        """Permet d'ajouter un objet à l'inventaire du joueur.
        Si le joueur ne possède pas, on l'ajoute, sinon, on met à jour la quantité associée.
        Paramètres :
            - article (str) : le nom de l'objet à ajouter à l'inventaire
        """
        if article in self.inventaire.keys():
            self.inventaire[article] += 1
        else:
            self.inventaire[article] = 1
    def set_heros(self,heros):
        self.heros = heros
    def ajouter_heros(self,heros):
        self.heros.append(heros)
    def set_inventaire(self,inventaire:dict):
        self.inventaire = inventaire
    def set_gains(self,jeu:str,gains:float):
        self.gains[jeu] = gains
    def set_probas(self,jeu:str,probas:float):
        self.probas[jeu] = probas


class Coin:
    def __init__(self, pos_x:int, pos_y:int) -> 'Coin':
        self.tourne_animation = False
        self.sprites = [charger_et_agrandir(f'pieces/coin-{i}.png.png') for i in range(1,5)]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.actuel_sprite = 0
        self.image = self.sprites[self.actuel_sprite]
    def activer_rotation(self):
        self.tourne_animation = True
    def get_image(self) -> 'pygame.Surface':
        return self.image
    def get_pos(self) -> tuple:
        return(self.pos_x,self.pos_y)
    def update(self, speed:float):
        '''Permet d'effectuer l'animation de la rotation de la piece.'''
        if self.tourne_animation:
            self.actuel_sprite += speed
            if int(self.actuel_sprite) >= len(self.sprites):
                self.actuel_sprite = 0
        self.image = self.sprites[int(self.actuel_sprite)]


class Bouton:
    def __init__(self, largeur:int, hauteur:int, x:int, y:int) -> 'Bouton':
        self.largeur = largeur
        self.hauteur = hauteur
        self.x = x
        self.y = y
    def get_largeur(self):
        return self.largeur
    def get_hauteur(self):
        return self.hauteur
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_largeur(self, largeur:int):
        self.largeur = largeur
    def set_hauteur(self, hauteur:int):
        self.hauteur = hauteur
    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y


class Button:
    def __init__(self, image1, image2, x:int, y:int) -> 'Button':
        '''Initialise la classe bouton.
        Chaque bouton possède deux images (1 pour lorsque le bouton est survolé par la souris un une autre pour le reste du temps)
        Paramètres : 
            - image1 (str) : le chemin de l'image du bouton survolé
            - image2 (str) : le chemin de l'image du bouton non survolé
            - x (int) : la position x du bouton
            - y (int) : la position y du bouton'''
        self.image1 = image1 
        self.image2 = image2  
        self.rect = self.image2.get_rect(topleft=(x, y))  # Rectangle pour la position
        self.mask = pygame.mask.from_surface(self.image2)  # Masque pour les collisions 

    def collision(self, souris_pos:tuple) -> tuple:
        '''Permet de vérifier si le clic est dans la zone du bouton'''
        # Convertir la position du clic dans le référentiel de l'image du bouton
        x = souris_pos[0] - self.rect.x
        y = souris_pos[1] - self.rect.y

        # Vérifier si le clic est dans le rectangle et dans le masque
        if 0 <= x < self.rect.width and 0 <= y < self.rect.height:
            return self.mask.get_at((x, y))
        return False

    def draw(self, surface, mouse_pos:tuple):
        '''Permet de dessiner le bouton et de gérer le changement d'image en fonction du survol de la souris'''
        # Si la position de la souris est au niveau du bouton
        if self.collision(mouse_pos):
            # On affiche l'image correspondante
            surface.blit(self.image1, self.rect.topleft)
        # Sinon
        else:
            # On affiche l'autre image
            surface.blit(self.image2, self.rect.topleft)

    def get_pos(self):
        '''Permet de récupérer la position du bouton'''
        return (self.rect.x, self.rect.y)

class Clic:
    def __init__(self) -> 'Clic':
        '''Permet de récupérer la position du dernier clic entre les différents fichiers du code.'''
        self.clic = (0,0)
    def get_clic(self):
        '''On récupère la position du dernier clic enregistré'''
        return self.clic
    def set_clic(self,clic:tuple):
        '''On met à jour le clic'''
        self.clic = clic

class Curseur:
    def __init__(self) -> 'Curseur':
        '''Class pour la croix de selection dans l'inventaire'''
        self.actif = False
        self.frames = [pygame.image.load(f'images/Inventaire/_a_UI_Flat_Select01a_{i}.png') for i in range(1,5)]    # Images de l'animation de la croix de selection
        self.x = 0
        self.y = 0
        self.frame = 0
    def get_actif(self):
        return self.actif
    def get_pos(self):
        return (self.x, self.y)
    def get_frame(self):
        return int(self.frame)
    def set_pos(self, pos:tuple):
        self.frame = 0
        self.x = pos[0]
        self.y = pos[1]
    def set_actif(self, actif:bool):
        self.actif = actif
    def update(self, speed:float):
        '''Permet de mettre à jour l'animation de la croix de selection,et d'afficher la dernière image si l'animation est terminée.'''
        if int(self.frame) < len(self.frames)-1:
            self.frame += speed
        fenetre.blit(self.frames[int(self.frame)], (self.x, self.y))

class Biere:
    def __init__(self) -> 'Biere':
        self.nom = 'Biere'
    def get_nom(self):
        return self.nom
    def boire(self,joueur1:Joueur):
        assert isinstance(joueur1,Joueur),'Erreur: joueur1 doit etre un objet de la classe Joueur'
        joueur1.set_gains('Roulette',0.9)
        joueur1.set_probas('Roulette',-1)

class Whisky:
    def __init__(self) -> 'Whisky':
        self.nom = 'Whisky'
    def get_nom(self):
        return self.nom
    def boire(self,joueur1:Joueur):
        assert isinstance(joueur1,Joueur),'Erreur: joueur1 doit etre un objet de la classe Joueur'
        joueur1.set_gains('Blackjack',1.1)

class Mojito:
    def __init__(self) -> 'Mojito':
        self.nom = 'Mojito'
    def get_nom(self):
        return self.nom
    def boire(self,joueur1:Joueur):
        assert isinstance(joueur1,Joueur),'Erreur: joueur1 doit etre un objet de la classe Joueur'
        joueur1.set_gains('Roulette',1.3)
        joueur1.set_probas('Roulette',1)

class Crampons:
    def __init__(self) -> 'Crampons':
        self.nom = 'Crampons Dorés'
    def get_nom(self) -> str:
        return self.nom
    def boire(self,joueur1:Joueur):
        assert isinstance(joueur1,Joueur),'Erreur: joueur1 doit etre un objet de la classe Joueur'
        joueur1.modifier_cagnotte(1000000)
        joueur1.set_multis_jeu_combat(2)