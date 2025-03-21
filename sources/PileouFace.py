import pygame
from random import randint
from objets_et_variables import *
from sons import *

afficher_ecran_chargement(chargement[4])
print("Chargement du Babel Face...")

class Pile_ou_face:
    def __init__(self):
        self.animation = False
        self.sprites = [charger_et_agrandir('pistolet_blanc/vide.png')] + [charger_et_agrandir(f'Pile_ou_face/Piece animation ({i}).png') for i in range(1,17)]
        self.actuel_sprite = 0
        self.image = self.sprites[self.actuel_sprite]
        self.cote = None
        self.choix = None
        self.actif = False

    def activer_animation(self):
        """
        permet d'activer l'animation
        """
        self.animation = True

    def desactiver_animation(self):
        """
        permet de desactiver l'animation
        """
        self.animation = False

    def pile_ou_face(self):
        """
        permet de randomiser le coté de la piece
        """
        cote = randint(1, 2)
        if cote == 1:
            self.set_cote('Face')
        else:
            self.set_cote('Pile')

    def update(self, speed, joueur):
        """
        permet de jouer l'animation 
        speed(float): la vitesse de l'animation
        joueur(object): l'objet joueur1
        pièce(objet): aled la docu cest chiant quand y a enormement de def aleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed
        """
        if self.animation:
            self.actuel_sprite += speed
            if int(self.actuel_sprite) >= len(self.sprites):
                self.actuel_sprite = 0
                self.pile_ou_face()
                if self.victoire():
                    print(self.get_choix(), self.get_cote())
                    print('vict')
                    self.set_choix(None) 
                    joueur.modifier_cagnotte(100 + joueur.get_cagnotte()/20)
                    son_piece.play()
                else:
                    joueur.modifier_cagnotte(-150 - joueur.get_cagnotte()/18)
                    son_faux.play()
                    print('def')
                    print(self.get_choix(), self.get_cote())
                self.animation = False
            self.image = self.sprites[int(self.actuel_sprite)]
        elif not self.animation and self.actif:
            if self.get_cote() == 'Face':
                fenetre.blit(face, (340, 280))
            elif self.get_cote() == 'Pile':
                fenetre.blit(pile, (340, 280))
    
    def get_image(self):
        return self.image
    
    def get_cote(self):
        return self.cote

    def get_choix(self):
        return self.choix
    
    def get_actif(self):
        return self.actif

    def set_cote(self,cote):
        self.cote = cote

    def set_choix(self, choix):
        self.choix = choix

    def set_actif(self,actif):
        self.actif = actif

    def victoire(self):
        """
        permet de determiner si le joueur a gagné
        """
        if self.get_cote() == self.get_choix():
            return True
        else:
            return False

pileouface = Pile_ou_face()