import pygame
pygame.mixer.init()
from fonctions import afficher_ecran_chargement
from img import chargement

afficher_ecran_chargement(chargement[2])
print("Chargement des sons...")

son_gambling = pygame.mixer.Sound('data/son/lets_go_gambling.mp3')
son_fall = pygame.mixer.Sound('data/son/fall.mp3')
tire_balle = pygame.mixer.Sound('data/son/balle.mp3')
tire_balle_blanc = pygame.mixer.Sound('data/son/balle_a_blanc.mp3')
rire_maurice = pygame.mixer.Sound('data/son/rire_maurice.mp3')
click = pygame.mixer.Sound('data/son/son_click.mp3')
son_faux = pygame.mixer.Sound('data/son/son_faux.mp3')
son_piece = pygame.mixer.Sound('data/son/son_piece.mp3')
musique_de_fond = 'data/son/musique_de_fond.mp3'
musique_combat = 'data/son/combat.mp3'
musique_victoire = 'data/son/paradis.mp3'
son_epee = pygame.mixer.Sound('data/son/son_slash.wav')
aie_hero = pygame.mixer.Sound('data/son/mc-hurt.mp3')
aie_boss = pygame.mixer.Sound('data/son/degat_boss.mp3')
pioche_carte = pygame.mixer.Sound('data/son/pioche_carte.mp3')
rickr = 'data/son/rr.mp3'
shoot = pygame.mixer.Sound('data/son/shoot.mp3')
explosion = pygame.mixer.Sound('data/son/explosion.mp3')
bonus = pygame.mixer.Sound('data/son/bonus.mp3')
musique_invader = 'data/son/musique_invader.mp3'
coffre = pygame.mixer.Sound('data/son/coffre.mp3')