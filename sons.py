import pygame
pygame.mixer.init()
from fonctions import afficher_ecran_chargement
from img import chargement

afficher_ecran_chargement(chargement[2])
print("Chargement des sons...")

son_gambling = pygame.mixer.Sound('son/lets_go_gambling.mp3')
son_fall = pygame.mixer.Sound('son/fall.mp3')
tire_balle = pygame.mixer.Sound('son/balle.mp3')
tire_balle_blanc = pygame.mixer.Sound('son/balle_a_blanc.mp3')
rire_diabolique = pygame.mixer.Sound('son/rire_maurice.mp3')
click = pygame.mixer.Sound('son/son_click.mp3')
son_faux = pygame.mixer.Sound('son/son_faux.mp3')
son_piece = pygame.mixer.Sound('son/son_piece.mp3')
son_champignon = 'son/Le champignon de Paris.wav'
musique_de_fond = 'son/musique_de_fond.mp3'
musique_combat = 'son/combat.mp3'
musique_victoire = 'son/paradis.mp3'
son_epee = pygame.mixer.Sound('son/son_slash.wav')
aie_hero = pygame.mixer.Sound('son/mc-hurt.mp3')
aie_boss = pygame.mixer.Sound('son/degat_boss.mp3')
pioche_carte = pygame.mixer.Sound('son/pioche_carte.mp3')
vodkaaa = 'son/Vodka.mp3'
rickr = 'son/rr.mp3'