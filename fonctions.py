import pygame
from objets_et_variables import *
from SQL import ajouter_objet_inventaire,det_id_compte

print("Chargement des fonctions...")

fond2 = pygame.image.load('images/Fonds d\'ecran/casino.png').convert()

def dessiner_bouton(fenetre, message:str, x: int, y:int, largeur:int, hauteur:int, couleur_fond:tuple, couleur_texte:tuple, taille:int):
    '''
    Permet de dessiner un bouton.
    Paramètres:
        - fenetre : la fenetre pygame concernée
        - message (str) : Le texte à écrire
        - x (float or int) : la position x du bouton
        - y (float or int) : la position y du bouton
        - largeur (float or int) : la largeur du bouton
        - hauteur (float or int) : la hauteur du bouton
        - couleur_fond (tuple) : la couleur de fond du bouton
        - couleur_texte (tuple) : la couleur du texte du bouton
        - taille (int) : la taille de la police d'écriture
    '''
    assert type(message) == str,'Erreur: message doit etre une chaine de caracteres'
    assert type(x) == int,'Erreur: x doit etre un entier'
    assert type(y) == int,'Erreur: y doit etre un entier'
    assert type(largeur) == int,'Erreur: largeur doit etre un entier'
    assert type(hauteur) == int,'Erreur: hauteur doit etre un entier'
    assert type(couleur_fond) == tuple,'Erreur: couleur_fond doit etre un tuple'
    assert type(couleur_texte) == tuple,'Erreur: couleur_texte doit etre un tuple'
    assert type(taille) == int,'Erreur: taille doit etre un entier'
    pygame.draw.rect(fenetre, couleur_fond, (x, y, largeur, hauteur))
    police = pygame.font.Font('babelcasino.ttf', taille)
    texte = police.render(message, True, couleur_texte)
    fenetre.blit(texte, (x + 10, y + (hauteur - texte.get_height()) // 2))


def dessiner_zone_texte(fenetre, rect, texte:str, actif:bool):
    '''
    Permet de dessiner une zone de texte.
    Paramètres:
        - fenetre : la fenetre pygame concernée
        - rect : Le rectangle à dessiner, contenant la position x et y, ainsi que la largeur et la hauteur
        - texte (str) : Le texte à écrire
        - actif (bool) : Le booléen indiquant si le champ est actif (si on peut écrire)
    '''
    pygame.draw.rect(fenetre, blanc, rect)
    couleur = gris
    if actif:
        couleur = noir
    pygame.draw.rect(fenetre, couleur, rect, 4)
    police = pygame.font.Font('babelcasino.ttf', 30)
    texte_surface = police.render(texte, True, noir)
    fenetre.blit(texte_surface, (rect.x + 10, rect.y + 10))

def achat(article:str) -> None:
    '''Permet d'acheter un article en fonction de son prix.
    Paramètres:
        - article (str) : Le nom de l'article à acheter'''
    if joueur1.get_cagnotte() >= boutique[article]:
        joueur1.modifier_cagnotte(-boutique[article])
        joueur1.ajouter_inventaire(article)
        ajouter_objet_inventaire(1, det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()), article)
        print("Achat effectué !")
    else:
        print("Solde insuffisant !")

def afficher_ecran_chargement(img) -> None:
    '''Permet d'afficher l'écran de chargement
    Paramètres:
        - img : L'image à afficher'''
    fenetre.blit(img, (0, 0))  # Afficher le fond
    pygame.display.flip()

def valider_numero_carte_bancaire(numero:str) -> bool:
    "Fonction qui permet de valider un numéro de carte bancaire avec la methode de Luhn (oui on est motivés)"
    assert type(numero) == str, "Le numéro de carte bancaire doit être une chaîne de caractères"
    numero = ''.join(filter(str.isdigit, numero))
    assert len(numero) == 16, "Le numéro de carte bancaire n'est pas valide"
    somme = 0
    inverse = numero[::-1]
    for i, chiffre in enumerate(inverse):
        n = int(chiffre)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9  
        somme += n
    return somme % 10 == 0

def distance(j1,j2):
    return j1.hero.get_pos_x()-j2.boss.get_pos_x()

def agrandir_liste_images(chemins_images):
    return [pygame.transform.scale(pygame.image.load(chemin).convert_alpha(),(pygame.image.load(chemin).get_width() * 2, pygame.image.load(chemin).get_height() * 2)) for chemin in chemins_images]