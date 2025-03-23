import pygame
import numpy
from fonctions import *
from Ecrans import Ecran,ecran2,EcranPnj
from objets_et_variables import joueur1
from sons import click

afficher_ecran_chargement(chargement[7])
print("Chargement du Babel Gambling")

class Emplacement(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = charger_et_agrandir('data/machine_a_sou/pomme_doree.png') #image par default a changer
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def set_image(self, image):
        self.image = image

class EcranMachineASous:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = charger_et_agrandir('data/machine_a_sou/slot.png')
        self.image_test = charger_et_agrandir('data/machine_a_sou/orange.png')
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
            "cerise": charger_et_agrandir('data/machine_a_sou/cerise.png'),
            "pomme": charger_et_agrandir('data/machine_a_sou/pomme.png'),
            "orange": charger_et_agrandir('data/machine_a_sou/orange.png'),
            "pasteque": charger_et_agrandir('data/machine_a_sou/pasteque.png'),
            "pomme_dore": charger_et_agrandir('data/machine_a_sou/pomme_doree.png')
        }
        fruits = ["pomme", "cerise", "orange", "pasteque", "pomme_dore"]
        proba_fruits = [0.2, 0.25, 0.4, 0.12, 0.03]

        fruits_dict_gains = {
            "orange": 8000 + joueur1.get_cagnotte()/40,
            "cerise": 14000 + joueur1.get_cagnotte()/25,
            "pomme": 21000 + joueur1.get_cagnotte()/15,
            "pasteque": 50000 + joueur1.get_cagnotte()/5,
            "pomme_dore": 10000000
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

Moonlit = EcranPnj([pygame.image.load(f'data/images/Pnj/Moonlit/_a_frm{i},80.png') for i in range(14)], 
"Ksssst...Intrus...tu es attiré ici par \nl'appat du gain...Ici se trouvent les \nMachines à sous du Babel Casino, le \nBabel Gambling. Amuse toi mais...garde \nun oeil sur ta bourse, ou elle se \nvidera avant que tu ne t'en rendes \ncomptes...ou peut-etre qu'elle se \nremplira, qui sait ?", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 440), "Comment jouer ?", 
  "Appuie sur le levier : ton solde sera \nautomatiquement débité, et tu \nobtiendras un lancer de Babel Gambling. \nSi tu as 3 fruits identiques, c'est le \njackpot ! Tu gagnes une grande somme \nd'argent, selon la rareté du fruit."),
 (Button(boutons_dialogue2, boutons_dialogue1, 350, 490), "Les sommes en jeu ?", 
  "Intrus...ces machines mythiques \npourront t'offrir une richesse dont \ntu n'as pas idée...mais pourront aussi \ncauser ta perte. Un lancer te coutera \n100 Babel Coins + 10% de ton solde. \nPour les gains : \n- Oranges : 8 000 + 2.5% du solde  \n- Cerise : 14 000 + 4% du solde \n- Pomme : 21 000 + 6,6% du solde \n- Pastèque : 50 000 + 20% du solde \n- Babel Apple : 10 000 000 "),
 (Button(boutons_dialogue2, boutons_dialogue1, 350, 540), "Qui es-tu ?", 
  "Je suis Moonlit, dragon du vent et des \neaux. Je pourrais te déchiqueter ton \ncorps d'une multitude de lames de vents...\nCependant, je suis le serviteur du \ndiable Maurice. Ici, je ne suis pas libre, \net je suis les ordres qu'il me donne. Je \nsupervise donc les machines de Babel \nGambling, pour éviter que des \navortons en ton genre ne trichent au vu \ndes sommes astronomiques en jeu. Va, \njoue, et meurs. Tu as de la chance \nque je ne te dévorre pas sur place, car \nle diable Maurice tient à son profit...\n")  ], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 390), "Je veux y acceder"),
 (Button(boutons_dialogue2, boutons_dialogue1, 350, 590), 'Au revoir')], 
(50,80),ecran_machine_a_sous,ecran2,"Moonlit")
