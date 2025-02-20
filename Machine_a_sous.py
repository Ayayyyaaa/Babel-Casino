import pygame
import numpy
from fonctions import *
from Ecrans import Ecran,ecran2
from objets_et_variables import joueur1
from sons import click

afficher_ecran_chargement(chargement[7])
print("Chargement du Babel Gambling")

class Emplacement(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = charger_et_agrandir('machine_a_sou/pomme_doree.png') #image par default a changer
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def set_image(self, image):
        self.image = image

class EcranMachineASous:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = charger_et_agrandir('machine_a_sou/slot.png')
        self.image_test = charger_et_agrandir('machine_a_sou/orange.png')
        self.hauteur_emplacement = 300
        self.emplacement_x_milieu = 800/3 + 86
        self.emplacement_x_gauche = self.emplacement_x_milieu - self.image_test.get_width() -20
        self.emplacement_x_droite = self.emplacement_x_milieu + self.image_test.get_width() +16
        self.emplacements = pygame.sprite.Group()
        self.emplacement_gauche = Emplacement(self.emplacement_x_gauche, self.hauteur_emplacement)
        self.emplacement_milieu = Emplacement(self.emplacement_x_milieu, self.hauteur_emplacement)
        self.emplacement_droite = Emplacement(self.emplacement_x_droite, self.hauteur_emplacement)
        # rangement des emplacements dans le groupe
        self.emplacements.add(self.emplacement_gauche)
        self.emplacements.add(self.emplacement_milieu)
        self.emplacements.add(self.emplacement_droite)
    def affiche(self):
        '''
        Permet d'afficher l'écran du mini-jeu Machine à sous.
        '''
        fenetre.fill(blanc)
        fenetre.blit(self.fond, (0, 0))
        self.emplacements.draw(fenetre)
        comic = pygame.font.SysFont("comicsansms", 60)
        text = comic.render(str(int(joueur1.get_cagnotte())) + " pièces", True, blanc)
        fenetre.blit(text, (10, 0))
        btn_fleche.draw(fenetre, pygame.mouse.get_pos())
        if btn_fleche.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0, 0))
            ecran2.ecran.set_actif(not ecran2.ecran.get_actif())
            ecran_machine_a_sous.ecran.set_actif(not ecran_machine_a_sous.ecran.get_actif())

    def lancement(self):
        '''
        Permet de lancer la machine à sous.
        '''
        fruits_dict = {
            "cerise": charger_et_agrandir('machine_a_sou/cerise.png'),
            "pomme": charger_et_agrandir('machine_a_sou/pomme.png'),
            "orange": charger_et_agrandir('machine_a_sou/orange.png'),
            "pasteque": charger_et_agrandir('machine_a_sou/pasteque.png'),
            "pomme_dore": charger_et_agrandir('machine_a_sou/pomme_doree.png')
        }
        fruits = ["pomme", "cerise", "orange", "pasteque", "pomme_dore"]
        proba_fruits = [0.2, 0.25, 0.4, 0.12, 0.03]

        fruits_dict_gains = {
            "orange": 800 + joueur1.get_cagnotte()/40,
            "cerise": 1400 + joueur1.get_cagnotte()/25,
            "pomme": 2100 + joueur1.get_cagnotte()/15,
            "pasteque": 5000 + joueur1.get_cagnotte()/5,
            "pomme_dore": 8000000
        }
        global jetons
        hasard = numpy.random.choice(fruits, 3, p=proba_fruits)
        
        # Récupérer les images directement depuis le dictionnaire
        self.emplacement_gauche.set_image(fruits_dict[hasard[0]])
        self.emplacement_milieu.set_image(fruits_dict[hasard[1]])
        self.emplacement_droite.set_image(fruits_dict[hasard[2]])

        if hasard[0] == hasard[1] == hasard[2]:
            fruit = hasard[0]
            jetons_gagnes = fruits_dict_gains[fruit]
            joueur1.modifier_cagnotte(jetons_gagnes)

ecran_machine_a_sous = EcranMachineASous()