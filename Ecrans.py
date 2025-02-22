import pygame
from fonctions import dessiner_bouton, agrandir_liste_images
from random import randint
from objets_et_variables import *
from img import *
from Roulette_Russe import pistolet
from PileouFace import pileouface
from sons import *
from SQL import *
from fonctions import achat

afficher_ecran_chargement(chargement[6])
print("Chargement des Ecrans...")

class Ecran:
    def __init__(self, actif:bool = False) -> 'Ecran':
        self.actif = actif
    def get_actif(self) -> bool:
        return self.actif
    def set_actif(self, actif:bool):
        self.actif = actif

class Ecran1:
    def __init__(self) -> 'Ecran1':
        self.ecran = Ecran()
        self.ancien_pseudo = joueur1.get_pseudo()
        self.fin_combat = False
    def affiche(self):
        '''Permet d'afficher l'écran de connexion et de passer à l'écran principal.
        '''
        # Si l'écran est actif
        if self.ecran.get_actif():    
            # On dessine tous les éléments      
            fenetre.blit(fond, (0, 0))          
            btn_entrer.draw(fenetre,pygame.mouse.get_pos())
            # Si on clique sur le bouton entrer
            if btn_entrer.collision(clic.get_clic()):           
                click.play()
                # Si le joueur a entré ses identifiants
                if joueur1.get_pseudo() != '':          
                    # On passe à l'écran suivant, en mettant a jour la musique
                    connexion.ecran.set_actif(False) , ecran2.ecran.set_actif(True)
                    clic.set_clic((0,0))
                    # On met à jour la musique de fond
                    self.choisir_musique()
    def choisir_musique(self):
        '''Permet de chosir la musique de fond
        Paramètres : 
            - combat (bool) : Détermine si le combat face au boss à été réussi
        Post-conditions :
            - Si le joueur s'appelle Fredou et qu'il n'y a pas de musique de fond, que le joueur change de pseudo ou que le combat a été réussi, on charge un nouvelle musique (son_champignon)
            - Si le joueur a un pseudo qui s'apparente a un RickRoll, on lance celui-ci.
            - Sinon, s'il n'y a pas de musique de fond, que le joueur change de pseudo ou que le combat a été réussi, on charge un nouvelle musique (musique_de_fond)
        '''
        # Si le joueur s'appelle fredou
        if joueur1.get_pseudo().lower() == 'fredou':
            # S'il n'y a pas du musique de fond ou que le joueur a changé de pseudo (Il se connecte avec le pseudo fredou)
            if not pygame.mixer.music.get_busy() or self.ancien_pseudo != joueur1.get_pseudo():
                # On enelève la musique de fond
                pygame.mixer.music.unload()
                # On charge la musique de fredou
                pygame.mixer.music.load(son_champignon)
                # On met le volume à 0.1
                pygame.mixer.music.set_volume(0.1)
                # On la joue en boucle
                pygame.mixer.music.play(-1)
                # On met à jour l'ancien pseudo
                self.ancien_pseudo = joueur1.get_pseudo()
                self.fin_combat = True
        # Si le joueur s'appelle Rick Astley (Pour la musique du Rick Roll)
        elif joueur1.get_pseudo().lower() in ['rick','rickroll','rick roll', 'rickastley', 'rick astley']:
            # S'il n'y a pas du musique de fond ou que le joueur a changé de pseudo (Il se connecte avec le pseudo Rick)
            if not pygame.mixer.music.get_busy() or self.ancien_pseudo != joueur1.get_pseudo():
                # On passe à l'écran du Rick Roll
                rr.ecran.set_actif(True),ecran2.ecran.set_actif(False)
                # On enlève la musique de fond
                pygame.mixer.music.unload()
                # On charge le Rick Roll
                pygame.mixer.music.load(rickr)
                # On met le volume à 1
                pygame.mixer.music.set_volume(1)
                # On la joue en boucle
                pygame.mixer.music.play(-1)
                # On met à jour l'ancien pseudo
                self.ancien_pseudo = joueur1.get_pseudo()
                self.fin_combat = True
        # Sinon
        else:
            # S'il n'y a pas du musique de fond ou que le joueur a changé de pseudo (Il se connecte avec un autre pseudo)
            if not pygame.mixer.music.get_busy() or self.ancien_pseudo != joueur1.get_pseudo():
                # On enlève la musique de fond
                pygame.mixer.music.unload()
                # On charge la musique de fond générale
                pygame.mixer.music.load(musique_de_fond)
                # On met le volume à 0.3
                pygame.mixer.music.set_volume(0.3)  # Volume pour la musique de fond générale
                # On la joue en boucle
                pygame.mixer.music.play(-1)
                # On met à jour l'ancien pseudo
                self.ancien_pseudo = joueur1.get_pseudo()
                self.fin_combat = True


class Ecran2:
    def __init__(self) -> 'Ecran2':
        self.ecran = Ecran()
        self.fond = pygame.image.load('images/Fonds d\'ecran/casino.png').convert()
        self.musique = False
        self.btns = [btn_boutique, btn_retour, btn_roulette, btn_pile_ou_face, btn_machine_a_sous, btn_blackjack, btn_jeu_combat, btn_inventaire]  # Boutons à afficher
        self.choix_fait = False     # Pour le Babel Face
        self.btn_classement = [f'images/Bouton Classement/_a_frm{i},40.png' for i in range(18)]  # Animatin de bouton
        self.btn = pygame.image.load(self.btn_classement[0]).convert_alpha()     # Image du bouton
        self.anim = False
        self.frame = 0
    def set_musique(self):
        self.musique = False
    def affiche(self):
        '''
        Permet d'afficher l'écran principal et de gérer l'animation des boutons et mettre à jour les animations des jeux.
        '''
        # On gère les effets spécifiques à certains pseudos 
        if joueur1.get_pseudo().lower() == 'fredou':
            # On affiche le fond d'écran spécial de Fredou
            self.fond = pygame.image.load('images/Fonds d\'ecran/coeurfredou.png').convert()
        # Cas du joueur Mr Morrhysse
        elif joueur1.get_pseudo().lower() == 'mr.maurice' or joueur1.get_pseudo().lower() == 'mr maurice' or joueur1.get_pseudo().lower() == 'maurice':
            # On change le pseudo pour gratter des tickets
            joueur1.set_pseudo('Le meilleur')  # Mettez nous des tickets et un 20/20 svp
            # On refait les vérifications de compte avec le nouveau pseudo
            verifier_et_ajouter_pseudo(joueur1.get_pseudo(),joueur1.get_mdp()) 
            # On récupère l'identifiant du compte
            id_compte = det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp())
            # On récupère le solde du compte
            joueur1.set_cagnotte(recup_donnees(id_compte))
            # On met à jour la dernière connexion du compte
            ajouter_connexion(id_compte)
        # Cas de joueur Mr Mhorrhyce quand le changement de pseudo a été effectué
        elif joueur1.get_pseudo() == 'Le meilleur':
            # On charge le fond d'écran spécifique de toute beauté
            self.fond = pygame.image.load('images/Fonds d\'ecran/Metteznous20sur20svp.jpg').convert()
        # Si le joueur est un démon (un arbre dégénéré)
        elif joueur1.get_pseudo().lower() == 'abel':
            # On affiche le fond d'écran spécifique de l'arbre dégénéré Abel
            self.fond = pygame.image.load('images/Fonds d\'ecran/FondAbel.png').convert()
        # Sinon
        else:
            # On charge le fond d'écran normal
            self.fond = pygame.image.load('images/Fonds d\'ecran/casino.png').convert()
        # On affiche le fond d'écran
        fenetre.blit(self.fond, (0, 0))
        # On fait progresser l'animation de la toute pitite piece à côté du solde du joueur (Elle est trop chou)
        coin.activer_rotation()
        # On affiche les boutons (affichage du pseudo et du solde du joueur)
        dessiner_bouton(fenetre, joueur1.get_pseudo(), bouton2.get_x(), bouton2.get_y(), bouton2.get_largeur(), bouton2.get_hauteur(), blanc, noir, 30)
        dessiner_bouton(fenetre, f"Solde : {int(joueur1.get_cagnotte())}", bouton3.get_x(), bouton3.get_y(), bouton3.get_largeur(), bouton3.get_hauteur(), blanc, noir, 30)
        # Si on clique sur le bouton pour accéder à la boutique
        if btn_boutique.collision(clic.get_clic()):
            ecran_boutique.ecran.set_actif(True),ecran2.ecran.set_actif(False)
            clic.set_clic((0,0))
        # Si on clique sur le bouton pour lancer la roulette russe
        elif btn_roulette.collision(clic.get_clic()):
            click.play()
            pistolet.set_actif(True)
            joueur1.set_roulette_active(True)
            pileouface.set_actif(False)
            pistolet.rouletterusse(joueur1)
            joueur1.set_roulette_active(False)
            clic.set_clic((0,0))
        # Si on clique sur le bouton pour lancer la pile ou face
        elif btn_pile_ou_face.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0,0))
            pileouface.set_actif(not pileouface.get_actif())
            pileouface.set_cote(None)
        # Si on clique sur le bouton pour lancer le blackjack de mort d'abel plus jamais je touche à ça vraiment c'est une horreur en plus la doc est inexistante c'est juste des commentaires et des commentaires vraiment je suis traumatisé aled
        elif btn_blackjack.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0,0))
            Chakkram.ecran.set_actif(True),ecran2.ecran.set_actif(False)
        # Si on clique sur le bouton pour retourner à l'écran de connexion
        elif btn_retour.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0,0))
            connexion.ecran.set_actif(True)
            ecran2.ecran.set_actif(False)
        # Si on ouvre l'inventaire
        elif btn_inventaire.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0,0))
            ecran2.ecran.set_actif(False), inventaire.ecran.set_actif(True) # On définit l'inventaire comme ecran actif
        # Si on ouvre le classement
        elif btn_classement.collision(clic.get_clic()):   
            print("aled")
            Archon.ecran.set_actif(True), ecran2.ecran.set_actif(False)
            classement.actualiser_classement()  
            clic.set_clic((0,0))
        elif pileouface.get_actif():
            # Pari sur le côté Face de la piece
            if btn_face.collision(clic.get_clic()):
                click.play()
                pileouface.set_choix('Face') 
                self.choix_fait = True
            # Pari sur le côté Pile de la piece
            elif btn_pile.collision(clic.get_clic()):
                click.play()
                pileouface.set_choix('Pile')
                self.choix_fait = True
            # Lancer l'animation de Pile ou Face quand le joueur a effectué son choix
            if self.choix_fait:
                pileouface.activer_animation()
                self.choix_fait = False
        # On lance l'animation du bouton du classement
        elif btn_classement.collision(pygame.mouse.get_pos()):
            self.anim = True
        else:
            btn_classement.draw(fenetre,pygame.mouse.get_pos())
        fenetre.blit(coin.get_image(),coin.get_pos())
        coin.update(0.04)
        fenetre.blit(pistolet.get_image(),pistolet.get_pos())
        pistolet.update_def(0.16,joueur1)  
        pistolet.update_vict(0.16,joueur1)  
        fenetre.blit(pileouface.get_image(),(340,280))
        # On joue l'animation du bouton du classement
        if self.anim:
            self.btn_classement_anim(0.3)
        if pileouface.get_actif():
            pileouface.update(0.20, joueur1)
        # Petit Easter egg
        if joueur1.get_pseudo() == '666' or joueur1.get_pseudo() == 'Satan':
            fenetre.blit(diable, (200, 4))
        # Affichage des boutons des jeux
        for btn in self.btns:
            btn.draw(fenetre,pygame.mouse.get_pos())
        # Affichage des boutons des choix du pile ou face
        if pileouface.get_actif():
            btn_pile.draw(fenetre,pygame.mouse.get_pos()),btn_face.draw(fenetre,pygame.mouse.get_pos())
        # Si le joueur est Mr Meaurisse 
        if joueur1.get_pseudo().lower() == 'Le meilleur' and not self.benji in joueur1.get_heros():
            # On ajoute le héros Benji à la liste des héros du joueur
            joueur1.ajouter_hero(self.benji)
    def btn_classement_anim(self,speed:float):
        '''
        Permet d'animer le bouton des héros. On dait progresser l'indice de l'image, si on arrive à la fin on le remet à 0.
        Paramètres :
            - speed (float) : Vitesse de l'animation
        '''
        self.frame += speed
        # Si on arrive au bout de l'animation on recommence
        if self.frame >= len(self.btn_classement)-1:
            self.frame = 0
            self.anim = False
        fenetre.blit(charger_et_agrandir(self.btn_classement[int(self.frame)]), (376, -10))

class EcranMort:
    def __init__(self):
        self.ecran = Ecran()
        self.fond =  pygame.image.load('images/Fonds d\'ecran/enfer2.png').convert()
    def affiche(self):
        '''
        Permet d'afficher l'écran de mort.
        '''
        fenetre.blit(self.fond, (0, 0))

class EcranVictoire:
    def __init__(self):
        self.ecran = Ecran()
        self.retour1 = pygame.image.load('images/Boutons_autre/Retour-1.png').convert_alpha()
        self.retour2 = pygame.image.load('images/Boutons_autre/Retour-2.png').convert_alpha()
    def affiche(self):
        '''
        Permet d'afficher l'écran de victoire.
        '''
        # On affiche le fond
        fenetre.blit(paradis, (0, 0))
        # Nouvelle musique propre au paradis
        if not pygame.mixer.music.get_busy():
            # On enlève l'ancienne musique
            pygame.mixer.music.unload()
            # On met la nouvelle et on la joue
            pygame.mixer.music.load(musique_victoire)
            pygame.mixer.music.play(-1)
        # On affiche le bouton de retour
        btn_retour.draw(fenetre,pygame.mouse.get_pos())
        # Si on clique sur le bouton retour
        if btn_retour.collision(clic.get_clic()):
            # On enlève la musique de victoire et on remet l'ancienne
            clic.set_clic((0,0))
            pygame.mixer.music.unload()
            connexion.choisir_musique()
            # On remet l'écran principal en tant qu'écran actif
            ecran_victoire.ecran.set_actif(False)
            ecran2.ecran.set_actif(True)

class EcranBlack:
    def __init__(self):
        self.ecran = Ecran()
    def affiche(self,blackjack):
        blackjack.set_actif(True)
        blackjack.main()

class EcranBoutique:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = pygame.image.load('images/Fonds d\'ecran/Boutique.png').convert_alpha()
        self.btn_heros = [f'images/Btn_heros/_a_frm{i},70.png' for i in range(13)]
        self.btn = pygame.image.load(self.btn_heros[0]).convert_alpha()
        self.frame = 0

    def affiche(self):
        '''
        Permet d'afficher l'écran de la boutique, ainsi que gérer les interactions avec les boutons.
        '''
        # Affichage du fond et des boutons
        fenetre.blit(self.fond, (0, 0))
        btn_fleche.draw(fenetre,pygame.mouse.get_pos())
        btn_alcool.draw(fenetre,pygame.mouse.get_pos())
        # Bouton retour
        if btn_fleche.collision(clic.get_clic()):
            ecran_boutique.ecran.set_actif(False),ecran2.ecran.set_actif(True)
            clic.set_clic((0,0))
        # Bouton pour la page d'achat des héros
        elif btn_hero.collision(clic.get_clic()):
            ecran_boutique.ecran.set_actif(False),SunForge.ecran.set_actif(True)
            clic.set_clic((0,0))
        # Bouton pour la page d'achat des alcools
        elif btn_alcool.collision(clic.get_clic()):
            ecran_boutique.ecran.set_actif(False),Rook.ecran.set_actif(True)
            clic.set_clic((0,0))
        # Animation du bouton des héros
        elif btn_hero.collision(pygame.mouse.get_pos()):
            self.anim(0.1)
        else:
            btn_hero.draw(fenetre,pygame.mouse.get_pos())
            self.frame = 0

    def anim(self,speed:float):
        '''
        Permet d'animer le bouton des héros'''
        self.frame += speed
        # Si on arrive au bout de l'animation on recommence
        if self.frame >= len(self.btn_heros)-1:
            self.frame = 0
        fenetre.blit(pygame.image.load(self.btn_heros[int(self.frame)]).convert_alpha(), (430, 260))

class EcranClassement:
    def __init__(self):
        self.ecran = Ecran()  # Assure-toi que cette classe est définie ailleurs dans ton code
        self.fond = pygame.image.load('images/Fonds d\'ecran/fond_classement5.png').convert_alpha()
        self.police = pygame.font.Font('babelcasino.ttf', 30)
        self.frame = 0
        self.sprites = agrandir_liste_images([f'images/Fonds d\'ecran/Demon_classement/_a_{i},80.png' for i in range(14)])
        self.gens = []
        self.cartouche0 = Button(cartouche_classement2, (cartouche_classement), 20, 150)
        self.cartouche1 = Button(cartouche_classement2, cartouche_classement, 20, 230)
        self.cartouche2 = Button(cartouche_classement2, cartouche_classement, 20, 310)
        self.cartouche3 = Button(cartouche_classement2, cartouche_classement, 20, 390)
        self.cartouche4 = Button(cartouche_classement2, cartouche_classement, 20, 470)
        self.cartouches = [self.cartouche0, self.cartouche1, self.cartouche2, self.cartouche3, self.cartouche4]

    def actualiser_classement(self):
        # Mise à jour de la liste des joueurs avec leurs informations
        self.gens = [(ordre_classement()[0][0], int(ordre_classement()[0][1])),  # 1er joueur et son solde
                     (ordre_classement()[1][0], int(ordre_classement()[1][1])),  # 2ème joueur et son solde
                     (ordre_classement()[2][0], int(ordre_classement()[2][1])),  # 3ème joueur et son solde
                     (ordre_classement()[3][0], int(ordre_classement()[3][1])),  # 4ème joueur et son solde
                     (ordre_classement()[4][0], int(ordre_classement()[4][1]))]  # 5ème joueur et son solde

    def affiche(self):
        '''
        Permet d'afficher l'écran du classement, ainsi que gérer les interactions avec les boutons.
        '''
        # Affichage du fond et des boutons
        fenetre.blit(self.fond,(0,0))  # Remplir l'écran avec une couleur de fond
        #fenetre.fill((0,0,0))
        btn_fleche.draw(fenetre, pygame.mouse.get_pos())  # Affichage du bouton 
        # Bouton retour
        if btn_fleche.collision(clic.get_clic()):
            print("aled")
            classement.ecran.set_actif(False)  # Passage à l'écran de la boutique
            ecran2.ecran.set_actif(True)  # Passage à un autre écran
            clic.set_clic((0, 0))  # Réinitialisation du clic

        # Affichage des informations du classement
        x = 60
        y = 161  # Position de départ pour l'affichage
        # Affichage des cartouches
        for cartouche in self.cartouches:
            cartouche.draw(fenetre, pygame.mouse.get_pos())
        # On affiche le pseudo et le solde de chaque joueur du top 5
        for i, (nom_joueur, solde) in enumerate(self.gens):
            # Affichage du classement et du solde de chaque joueur
            fenetre.blit(self.police.render(f"{i+1}. {nom_joueur} - {solde} Babel Coins", True, (255, 255, 255)), (x, y))
            y += 80  # Décalage pour afficher les informations du joueur suivant
        # Animation du démon
        self.anim(0.1)

    def anim(self,speed:float):
        '''
        Permet d'animer le démon du classement'''
        # On fait progresser l'animation
        self.frame += speed
        # Si on arrive au bout de l'animation on recommence
        if self.frame >= len(self.sprites)-1:
            self.frame = 0
        # On affiche l'image actuelle
        fenetre.blit(self.sprites[int(self.frame)].convert_alpha(), (200, 460))

class EcranAlcool:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = pygame.image.load('images/Fonds d\'ecran/Boutique.png').convert_alpha()
        self.vodka = False
        self.biere = False
        self.whisky = False
        self.mojito = False
        self.btns = [btn_whisky, btn_biere, btn_vodka, btn_mojito, btn_fleche]

    def affiche(self):
        '''
        Permet d'afficher l'écran des alcools, ainsi que gérer les interactions avec les boutons pour l'achat de ceux-ci.'''
        fenetre.blit(self.fond, (0, 0))
        # Quand on survole un bouton, on affiche les effets de l'alcool
        if btn_whisky.collision(pygame.mouse.get_pos()):
            self.whisky = True
        elif btn_biere.collision(pygame.mouse.get_pos()):
            self.biere = True
        elif btn_vodka.collision(pygame.mouse.get_pos()):
            self.vodka = True
        elif btn_mojito.collision(pygame.mouse.get_pos()):
            self.mojito = True
        # Sinon, on désactive tous les effets
        else:
            self.vodka,self.biere,self.whisky,self.mojito = False,False,False,False
        # Bouton retour
        if btn_fleche.collision(clic.get_clic()):
            clic.set_clic((0,0))
            alcool.ecran.set_actif(False),ecran_boutique.ecran.set_actif(True)
        # Si on clique sur un bouton d'achat de la vodka, on lance le gif de Poutine
        elif btn_vodka.collision(clic.get_clic()):
            print("L'alcool est à consommer avec modération. Ne vous faites pas avoir pas des prix alléchants, ne tombez pas dans l'alcoolisme héros !")
        # Si on clique sur un alcool, on lance l'achat
        elif btn_biere.collision(clic.get_clic()):
            achat('Biere')
        elif btn_whisky.collision(clic.get_clic()):
            achat('Whisky')
        elif btn_mojito.collision(clic.get_clic()):
            achat('Mojito')
        for btn in self.btns:
            btn.draw(fenetre,pygame.mouse.get_pos())
        self.affiche_effets()

    def affiche_effets(self):
        '''Permet d'afficher les effets des alcools lors du survol de la souris.'''
        if self.vodka:
            fenetre.blit(effet_vodka, (pygame.mouse.get_pos()[0]+80, pygame.mouse.get_pos()[1]-60))
        elif self.biere:
            fenetre.blit(effet_biere, (pygame.mouse.get_pos()[0]+80, pygame.mouse.get_pos()[1]-60))
        elif self.whisky:
            fenetre.blit(effet_whisky, (pygame.mouse.get_pos()[0]-360, pygame.mouse.get_pos()[1]-60))
        elif self.mojito:
            fenetre.blit(effet_mojito, (pygame.mouse.get_pos()[0]-360, pygame.mouse.get_pos()[1]-60))

class EcranSelection:
    def __init__(self, caracteristiques_hero:'pygame.Surface', liste:list, hero:tuple, y:int, x:int = 100):
        self.police = pygame.font.Font('babelcasino.ttf', 15)
        self.ecran = Ecran()
        self.fond = pygame.image.load('images/Fonds d\'ecran/arene.png').convert_alpha()
        self.anim = liste
        self.frame = 0
        self.valider = self.police.render(("Val ider"), True, noir)
        self.hero = hero
        self.prix = self.police.render((str(self.hero[1])), True, noir)
        self.y = y
        self.x = x
        self.infos = False
        self.caracteristiques = caracteristiques_hero
    def getinfos(self):
        return self.infos
    def setinfos(self,actif:bool):
        self.infos = actif
    def affiche(self,speed:float):
        '''Permet d'afficher l'écran de selection pour chaque heros, avec :
            - Les infos et caractéristiques du personnages
            - Un bouton pour selectionner/acheter le personnage
            - Un bouton pour afficher les informations du personnage
            - Un bouton pour revenir en arrière
        '''
        fenetre.blit(self.fond, (0, 0))
        # On joue l'animation de chaque héros pendant l'écran de selection
        fenetre.blit(self.anim[int(self.frame)], (self.x, self.y))
        self.frame += speed
        if self.frame >= len(self.anim)-1:
            self.frame = 0
        # On affiche les caractéristiques du héros si le joueur a cliqué sur le bouton
        if self.infos:
            fenetre.blit(self.caracteristiques, (60, 100))
        # Si le joueur possède le héros on écrit 'Valider' sur le bouton
        elif self.hero[0] in joueur1.get_heros():
            btn_select.draw(fenetre,pygame.mouse.get_pos())
            fenetre.blit(self.valider, (370, 680))
        # Sinon on écrit le prix du héros sur le bouton
        else:
            btn_select.draw(fenetre,pygame.mouse.get_pos())
            fenetre.blit(self.prix, (370, 680))
        # On affiche les boutons
        btn_fleche.draw(fenetre,pygame.mouse.get_pos())
        btn_info.draw(fenetre,pygame.mouse.get_pos())
    def get_heros(self) -> tuple:
        return self.hero
        

class EcranRR:
    def __init__(self) -> 'EcranRR':
        self.ecran = Ecran()
        self.frames =  agrandir_liste_images([f'RR/rickroll ({i}).png' for i in range(1,148)]) # Images du gif 
        self.frame = self.frames[0] # Image actuelle
        self.num_frame = 0 # Indice de l'image actuelle
    def affiche(self,speed:float):
        '''Permet d'afficher l'écran de rickroll.
        Paramètres :
            - speed (float) : la vitesse de l'animation.'''
        self.num_frame += speed # Fait progresser l'animation
        self.frame = self.frames[int(self.num_frame)] # Met à jour l'image actuelle
        # Si toutes les images ont été jouées :
        if int(self.num_frame) == len(self.frames)-1:
            # On remet tout à 0
            self.num_frame = 0
        fenetre.blit(self.frame,(0,0)) # Affiche l'image

class EcranChargement:
    def __init__(self):
        self.ecran = Ecran(True)
        self.frames = [f'images/Fonds d\'ecran/Chargement/frm ({i}).png' for i in range(2,117)]
        self.frame = 'images/Fonds d\'ecran/Chargement/frm (2).png'
        self.num_frame = 0
        self.stop = True
    def affiche(self,speed:float):
        '''Permet d'afficher l'animation l'écran de chargement.'''
        if self.num_frame <= 73 or not self.stop:
            self.num_frame += speed
        if clic.get_clic() != (0,0) and self.num_frame >= 56:
            self.stop = False
        # Si toutes les images ont été jouées :
        if int(self.num_frame) == len(self.frames)-1:
            # On remet tout à 0
            self.num_frame = 0
            lore.ecran.set_actif(True),self.ecran.set_actif(False)
        self.frame = self.frames[int(self.num_frame)]
        fenetre.blit(pygame.image.load(self.frame),(0,0))

class EcranInventaire:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = pygame.image.load("images/Fonds d'ecran/inventaire.png").convert()
        self.items = [item_biere, item_whisky, item_mojito, item_crampons]
        self.alcools = {item_biere : 'Biere', item_whisky : 'Whisky', item_mojito : 'Mojito', item_crampons : 'Crampons'}
        self.alcools_effets = {'Biere' : biere, 'Whisky' : whisky, 'Mojito' : mojito, 'Crampons' : crampons}
        self.police = pygame.font.Font('babelcasino.ttf', 30)
        self.police2 = pygame.font.Font('babelcasino.ttf', 24)
        self.selectione = None
    def affiche(self):
        '''Permet d'afficher l'écran de l'inventaire du joueur.
        Pour chaque alcool dispo, on affiche le bouton correspondant avec la qté en dessous.
        Si le bouton est cliqué, l'alcool est sélectionné et peut être utilisé.
        '''
        # On affiche les boutons
        fenetre.blit(self.fond,(0,0))
        btn_valider.draw(fenetre,pygame.mouse.get_pos())
        btn_flecheretour.draw(fenetre,pygame.mouse.get_pos())
        fenetre.blit(banniere,(272,570))
        # Pour chaque item dispo
        for item in self.items:
            item.draw(fenetre,pygame.mouse.get_pos())
            # On affiche la quantité de l'objet présente dans l'inventaire du joueur
            if self.alcools[item] in joueur1.get_inventaire().keys():
                fenetre.blit(self.police.render(('x ' + str(joueur1.get_inventaire()[self.alcools[item]])), True, noir),(item.get_pos()[0]+30, item.get_pos()[1]+120))
            else:
                fenetre.blit(self.police.render(('x 0'), True, noir),(item.get_pos()[0]+30, item.get_pos()[1]+120))
            # Si on clique sur un item
            if item.collision(clic.get_clic()):
                # On affiche le croix de sélection à l'emplacement du l'item
                click.play()
                self.selectione = self.alcools[item]
                curseur_selection.set_pos(item.get_pos())
                curseur_selection.set_actif(True)
                clic.set_clic((0,0))
            elif btn_valider.collision(clic.get_clic()):
                # Si l'item selectionné est présent dans l'inventaire du joueur
                if self.selectione in joueur1.get_inventaire().keys() and joueur1.get_inventaire()[self.selectione] > 0:
                    # On l'enlève de l'inventaire et de la bdd, puis on active l'effet
                    joueur1.get_inventaire()[self.selectione] -= 1
                    ajouter_objet_inventaire(-1, det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()), self.selectione)
                    self.alcools_effets[self.selectione].boire(joueur1)
                curseur_selection.set_actif(False)
                clic.set_clic((0,0))
            # Si on clique ailleurs, on desselectionne les items
            elif clic.get_clic() != (0,0):
                curseur_selection.set_actif(False)
                self.selectione = None
            # On affiche le nom de l'alcool selectionné
            if self.selectione:
                texte = self.police2.render((self.selectione), True, noir)
                fenetre.blit(texte,(276 + (256 - texte.get_width()) // 2, 600))
        # Bouton de retour
        if btn_flecheretour.collision(clic.get_clic()):
            click.play()
            clic.set_clic((0,0))
            ecran2.ecran.set_actif(True), inventaire.ecran.set_actif(False)
        # On joue l'animation de la croix de selection
        if curseur_selection.get_actif():
            curseur_selection.update(0.2)

class Intro:
    def __init__(self):
        self.ecran = Ecran()
        self.i_ecran = 0
        self.txt = ""
        self.indice = 0
        self.texte1 = "Oyez brave héros ! Durant votre voyage, vous arrivez sur le territoire\n du Royaume. En ces périodes troublées, marquées de raids de pillards \nqui s'intensifient, de démons qui terrorisent les populations, de disparitions \ninexpliquées et de la guerre qui gronde aux frontières, le roi Harold vous \nconfie une mission : Faire chuter un mystérieux casino qui s'est implanté \ndans la région. Son nom : Le Babel Casino. \nDes nombreuses expéditions lancées, pourtant menées par la garde du roi ou \ndes aventuriers chevronnés, aucune n'est revenue...Si bien qu'on raconte \ntoutes sortes de légendes sur ce casino mystérieux, selon lesquelles le \ncasino serait géré par le diable lui même. Alors, n'attendez plus héros ! \nL'avenir du Royaume dépend de vous ! Accompagné de votre fidèle ami \nNight Hero, formé à l'art du combat, vous poussez les lourdes portes du \nBabel Casino...Le plan : mener le Babel Casino à la faillite : pour cela, il \nfaut prendre la casino à son propre jeu : soyez malins,faites preuve \nde chance et investiguez pour réussir à rassembler la somme de \n10 000 000 Babel Coins. Le roi Harold vous a fourni un bourse contenant \n200 000 Babel Coins, à vous d'en faire bon usage ! Ainsi, vous pourrez jouer \naux divers jeux proposés par le Babel Casino : votre chance sera de mise si \nvous vous laissez tenter par la Babel Roulette, le Babel Face ou encore\nle Babel Gambling. Vous préférez vous reposer sur votre habilité seule ? "
        self.texte2 = "Soit, la Babel Race est faite pour vous. Enfin, vous pourrez mettre à l'épreuve \nvos capacités guerrières (enfin celles de votre ami, Night Hero : c'est à peine \nsi vous savez tenir une arme.) Vous serez face aux démons et pécheurs du \nBabel Casino, ceux ayant échoué face à celui-ci...Mais prenez garde : un seul \nfaux pas et vous les rejoindrez ! Vous rencontrerez peut-être certains \nvoyageurs de passage pour vous prêter main forte contre quelque \nrémunération, en mettant leurs habilités au combat à votre service. Pour finir, \nexplorez le Babel Casino, investiguez, peut être parviendrez vous à trouver \ndes objets qui vous aideront dans votre quête, tels que les alcools du bar, ou \nmême les crampons dorés, l'arme de prédilection du légendaire guerrier \nBenyamine, surnommé la Meaurylle aux mille victoires. Alors héros, au nom de la \nsurvie du Royaume...\nBonne chance ! "
        self.police = pygame.font.Font('babelcasino.ttf', 16)
        self.page = 0
        self.pages = [self.texte1,self.texte2]
        self.fond = fond_intro

    def affiche(self):
        fenetre.blit(self.fond,(0,0))
        if self.indice < len(self.pages[self.page]) - 1:  # Si le texte n'est pas entièrement affiché
            self.indice += 0.48  # On incrémente l'index du texte affiché
        elif clic.get_clic() != (0,0):
            if self.page == 0:
                self.page += 1
                self.indice = 0  # Réinitialiser l'index pour afficher le texte entier à nouveau
            else:
                lore.ecran.set_actif(False),connexion.ecran.set_actif(True)
            clic.set_clic((0,0))
        if clic.get_clic() != (0,0):
            self.indice = len(self.pages[self.page]) - 1
            clic.set_clic((0,0))
        self.txt = self.pages[self.page][:int(self.indice)]  # Affichage lettre par lettre

        # Utilisation de textwrap pour gérer les retours à la ligne
        lignes = self.txt.splitlines()  # Diviser le texte par les retours à la ligne

        # Affichage ligne par ligne avec un décalage vertical
        y_offset = 15  # Position de départ pour afficher le texte (au pixel y=15)
        for ligne in lignes:
            fenetre.blit(self.police.render(ligne, True, blanc), (22, y_offset))
            y_offset += 39  # Augmenter le décalage vertical pour la prochaine ligne

class CoffreFort:
    def __init__(self):
        self.ecran = Ecran()
        self.fond = charger_et_agrandir('images/Digicode/fond.png')
        self.combinaison = ""
        self.code_a_trouver = self.definir_code()
        self.trouve = False
        self.boutons = [btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btnvalider, btneffacer]
        self.chiffres = {btn0 : '0', btn1 : '1', btn2 : '2', btn3 : '3', btn4 : '4', btn5 : '5', btn6 : '6', btn7 : '7', btn8 : '8', btn9 : '9'}
    def definir_code(self):
        combi = ""
        for i in range(3):
            combi += str(randint(0,9))
        print("Chargement des codes secrets...")
        return combi
    def affiche(self):
        fenetre.blit(self.fond, (0, 0))
        btn_fleche.draw(fenetre, pygame.mouse.get_pos())  # Affichage du bouton 
        # Bouton retour
        if btn_fleche.collision(clic.get_clic()):
            digicode.ecran.set_actif(False)  # Mettre l'écran actif non actif
            ecran2.ecran.set_actif(True)  # Passage à un autre écran
            clic.set_clic((0, 0))  # Réinitialisation du clic
        for bouton in self.boutons:
            bouton.draw(fenetre,pygame.mouse.get_pos())
            if bouton.collision(clic.get_clic()):
                click.play()
                clic.set_clic((0,0))
                if bouton == btnvalider:
                    if self.combinaison == self.code_a_trouver:
                        print("code trouvé")
                        joueur1.ajouter_inventaire('Crampons')
                        ajouter_objet_inventaire(1,det_id_compte(joueur1.get_pseudo(), joueur1.get_mdp()),'Crampons')
                        self.trouve = True
                        self.combinaison = ""
                        self.code_a_trouver = self.definir_code()
                        print(self.code_a_trouver)
                    else:
                        self.combinaison = ""
                elif bouton == btneffacer:
                    self.combinaison = ""
                else:
                    self.combinaison += self.chiffres[bouton]
    def get_code(self):
        return self.code_a_trouver




ecran0 = EcranChargement()
lore = Intro()
connexion = Ecran1()
ecran2 = Ecran2()
inventaire = EcranInventaire()
classement = EcranClassement()
ecran_boutique = EcranBoutique()
ecran_mort = EcranMort()
ecran_victoire = EcranVictoire()
ecran_black = EcranBlack()
rr = EcranRR()
digicode = CoffreFort()
alcool = EcranAlcool()
klaxon = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Maehv.png'),
                        agrandir_liste_images([f'images/Jeu de combat/Klaxon/Droite/Inaction/_a_{i},80.png' for i in range(18)]),
                        ('Klaxon', 35000), 180, 224)

cryoblade = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Maehv.png'),
                           agrandir_liste_images([f'images/Jeu de combat/Cryoblade/Droite/Inaction/_a_{i},80.png' for i in range(16)]),
                           ('Cryoblade', 35000), 160, 210)

reeju = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Maehv.png'),
                       agrandir_liste_images([f'images/Jeu de combat/Reeju/Droite/Inaction/_a_{i},100.png' for i in range(14)]),
                       ('Reeju', 40000), 50, 100)

windcliffe = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Maehv.png'),
                            agrandir_liste_images([f'images/Jeu de combat/Windcliffe/Droite/Inaction/_a_{i},80.png' for i in range(9)]),
                            ('Windcliffe', 70000), 110, 150)

maehv = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Maehv.png'),
                       agrandir_liste_images([f'images/Jeu de combat/Maehv/Droite/Inaction/_a_{i},80.png' for i in range(14)]),
                       ('Maehv', 350000), 10)

zendo = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Zendo.png'),
                       agrandir_liste_images([f'images/Jeu de combat/Zendo/Droite/Inaction/_a_frm{i},60.png' for i in range(14)]),
                       ('Zendo', 200000), 10)

zukong = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/NightHero.png'),
                        agrandir_liste_images([f'images/Jeu de combat/Zukong/Droite/Inaction/_a_frm{i},80.png' for i in range(14)]),
                        ('Zukong', 45000), 112, 150)

nighthero = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/NightHero.png'),
                           agrandir_liste_images([f'images/Jeu de combat/Hero/Block/Block ({i}).png' for i in range(1,19)]),
                           ('Night Hero', 0), 200, 200)

hsuku = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Hsuku.png'),
                       agrandir_liste_images([f'images/Jeu de combat/Hsuku/Droite/Inaction/_a_{i},80.png' for i in range(28)]),
                       ('Hsuku', 300000), 20)

sanguinar = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/NightHero.png'),
                           agrandir_liste_images([f'images/Jeu de combat/Sanguinar/Droite/Inaction/_a_{i},80.png' for i in range(14)]),
                           ('Sanguinar', 400000), 20)

whistler = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Whistler.png'),
                          agrandir_liste_images([f'images/Jeu de combat/Whistler/Droite/Inaction/_a_{i},100.png' for i in range(18)]),
                          ('Whistler', 400000), 160, 190)

tethermancer = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Whistler.png'),
                              agrandir_liste_images([f'images/Jeu de combat/Tethermancer/Droite/Inaction/_a_{i},100.png' for i in range(17)]),
                              ('Tethermancer', 250000), 40)

aether = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Aether.png'),
                        agrandir_liste_images([f'images/Jeu de combat/Aether/Droite/Inaction/_a_{i},100.png' for i in range(12)]),
                        ('Aether', 175000), 194, 186)

pureblade = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Pureblade.png'),
                           agrandir_liste_images([f'images/Jeu de combat/Pureblade/Droite/Inaction/_a_frm{i},80.png' for i in range(10)]),
                           ('Pureblade', 275000), 20)

twilight = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Twilight.png'),
                          agrandir_liste_images([f'images/Jeu de combat/Twilight/Droite/Inaction/_a_{i},80.png' for i in range(14)]),
                          ('Twilight', 180000), 40)

suzumebachi = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Suzumebachi.png'),
                             agrandir_liste_images([f'images/Jeu de combat/Suzumebachi/Droite/Inaction/_a_{i},80.png' for i in range(32)]),
                             ('Suzumebachi', 150000), 40)

dusk = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Suzumebachi.png'),
                      agrandir_liste_images([f'images/Jeu de combat/Dusk/Droite/Inaction/_a_{i},80.png' for i in range(14)]),
                      ('Dusk', 200000), 40)

yggdra = EcranSelection(charger_et_agrandir('images/Jeu de Combat/Infos/Suzumebachi.png'),
                        agrandir_liste_images([f'images/Jeu de combat/Yggdra/Droite/Inaction/_a_{i},80.png' for i in range(7)]),
                        ('Yggdra', 450000), 140, 140)
class EcranHeros:
    def __init__(self,btns:dict):
        self.ecran = Ecran()
        self.fond = pygame.image.load('images/Fonds d\'ecran/Boutique.png').convert_alpha()
        self.btns = btns
    def affiche(self):
        '''Permet d'afficher l'écran de la boutique des héros, et de passer de chaque bouton de hero et l'écran du heros corrsepondant'''
        fenetre.blit(self.fond, (0, 0))
        btn_suivant.draw(fenetre,pygame.mouse.get_pos())    # Pour passer à l'onglet 2
        for btn,ecran in self.btns.items():    # Pour chaque bouton de héros
            btn.draw(fenetre,pygame.mouse.get_pos())    # On affiche le bouton
            if btn.collision(clic.get_clic()):  # Si on clique dessus
                clic.set_clic((0,0))    # On reset le clic
                ecran.ecran.set_actif(True),self.ecran.set_actif(False)   # On affiche l'écran du héros

class EcranPnj:
    def __init__(self, img_pnj:list, dialogue:str, boutons_dialogue:list, boutons:list, pos:tuple, jeu, salle, nom:str, fond='images/Fonds d\'ecran/casino.png'):
        '''Paramètres :
            - img_pnj : une liste de pygame.images du pnj à afficher
            - dialogue : le texte de base du personnage non joueur
            - boutons_dialogue : Une liste de tuples contenant les boutons à afficher (bouton:'Button', texte_btn:str, reponse_pnj:str)
            - boutons : Une liste de boutons contenant les boutons d'action à afficher : bouton retour, etc...
            - pos : La position du personnage non joueur sur l'écran
            - jeu : l'ecran à lancer si le joueur veut y acceder
            - salle : La salle dans laquelle se trouve le pnj (pour la remettre quand le joueur met fin au dialogue)
            - nom : Le nom du pnj
            - fond : L'image du fond de salle à utiliser'''
        self.ecran = Ecran()
        self.fond = pygame.image.load(fond).convert()
        self.img_pnj = img_pnj # Les images du png à afficher
        self.dialogue = dialogue # Le texte de base du personnage non joueur
        self.boutons_dialogue = boutons_dialogue # Une liste de tuples contenant les boutons à afficher (bouton:'Button', texte_btn:str, reponse_pnj:str)
        self.boutons = boutons # Une liste de boutons contenant les boutons d'action à afficher : bouton retour, etc...
        self.pos = pos # La position du personnage non joueur sur l'écran
        self.frame = 0
        self.police = pygame.font.Font('babelcasino.ttf', 16)
        self.police2 = pygame.font.Font('babelcasino.ttf', 24)
        self.txt = ""
        self.indice = 0
        self.txt_a_afficher = self.dialogue
        self.jeu = jeu
        self.nom = nom
        self.salle = salle
    def affiche(self):
        '''Permet d'afficher l'écran du personnage non joueur, avec les dialogues et les boutons d'actions.'''
        fenetre.blit(self.fond, (0,0))
        if self.frame < len(self.img_pnj)-1:
            self.frame += 0.15
        else:
            self.frame = 0
        if self.indice < len(self.txt_a_afficher):
            self.indice += 1
        fenetre.blit(fond_dialogues, (50,50))
        fenetre.blit(self.img_pnj[int(self.frame)],(self.pos))
        self.txt = self.txt_a_afficher[:int(self.indice)]  # Affichage lettre par lettre
        # Utilisation de textwrap pour gérer les retours à la ligne
        lignes = self.txt.splitlines()  # Diviser le texte par les retours à la ligne
        # Affichage ligne par ligne avec un décalage vertical
        y_offset = 70  # Position de départ pour afficher le texte (au pixel y=70)
        for ligne in lignes:
            fenetre.blit(self.police.render(ligne, True, blanc), (346, y_offset))
            y_offset += 25  # Augmenter le décalage vertical pour la prochaine ligne
        # Boutons de dialogue
        for bouton in self.boutons_dialogue:
            bouton[0].draw(fenetre, pygame.mouse.get_pos())
            # Texte du bouton
            texte_surface = self.police.render(bouton[1], True, blanc)
            texte_rect = texte_surface.get_rect(center=(bouton[0].get_pos()[0] + 187.5, bouton[0].get_pos()[1] + 15))
            fenetre.blit(texte_surface, texte_rect)
            # Si le bouton est cliqué, on change le dialogue et on reset le compteur d'indice
            if bouton[0].collision(clic.get_clic()):
                clic.set_clic((0,0))
                self.txt_a_afficher = bouton[2]
                self.indice = 0
        # Boutons d'interaction
        for bouton in self.boutons:
            bouton[0].draw(fenetre, pygame.mouse.get_pos())
            # Texte du bouton
            texte_surface = self.police.render(bouton[1], True, blanc)
            texte_rect = texte_surface.get_rect(center=(bouton[0].get_pos()[0] + 187.5, bouton[0].get_pos()[1] + 15))
            fenetre.blit(texte_surface, texte_rect)
            # Si le bouton est cliqué reset le compteur d'indice   
            if bouton[0].collision(clic.get_clic()):
                clic.set_clic((0,0))
                self.txt_a_afficher = self.dialogue
                self.indice = 0
                # Si le joueur met fin au dialogue, on remet tout comme avant en mettant l'écran du pnj a False
                if bouton[1] == 'Au revoir':
                    self.ecran.set_actif(False),self.salle.ecran.set_actif(True)
                # Si le joueur veut jouer, on lui donne accès à l'écran
                elif bouton[1] == 'Je veux jouer' or bouton[1] == 'Je veux y acceder':
                    self.ecran.set_actif(False), self.jeu.ecran.set_actif(True)
        # On affiche le nom du pnj
        nom_surface = self.police2.render(self.nom, True, blanc)
        nom_rect = nom_surface.get_rect(center=(200, 82))
        fenetre.blit(nom_surface, nom_rect)
    def get_boutons(self) -> list:
        return self.boutons



hero = EcranHeros({
            btn_fleche : ecran_boutique,
            btn_nighthero : nighthero,
            btn_klaxon : klaxon,
            btn_reeju : reeju,
            btn_cryoblade :cryoblade,
            btn_windcliffe : windcliffe,
            btn_zukong : zukong,
            btn_zendo : zendo,
            btn_maehv : maehv,
            btn_hsuku : hsuku,
            btn_sanguinar : sanguinar,
            btn_whistler : whistler,
            btn_tethermancer : tethermancer})

hero2 = EcranHeros({btn_fleche : ecran_boutique,
                    btn_aether : aether,
                    btn_twilight : twilight,
                    btn_pureblade : pureblade,
                    btn_suzumebachi : suzumebachi,
                    btn_dusk : dusk,
                    btn_yggdra : yggdra
                    })

Chakkram = EcranPnj([pygame.image.load(f'images/Pnj/Chakkram/_a_{i},100.png') for i in range(22)], 
"Bonsoir bonsoir cher joueur ! \nUne petite partie de Babel Jack ?", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 380), 'Comment jouer ?', 'Ici vous jouerez au légendaire Babel \nJack ! Affrontez le croupier du Babel \nCasino et ne dépassez pas le score \nde 21.'), 
(Button(boutons_dialogue2, boutons_dialogue1, 350, 430), 'J\'ai entendu un cri...', 'Oh, ne vous en souciez pas, ce doit juste \nêtre quelque joueur qui a cru pouvoir \nduper le casino. Quelle erreur. \nUne partie ?')], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 330), 'Je veux jouer'),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 480), 'Au revoir')], (0,50),ecran_black,ecran2,"Chakkram")

Archon = EcranPnj([pygame.image.load(f'images/Pnj/Archon/_a_frm{i},100.png') for i in range(11)], 
"Bonjour voyageur ! Comment puis-je \nt'aider ? Ici, tu retrouveras le \nclassement des joueurs du Babel \nCasino, qui possèdent le plus de Babel \nCoins.", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 380), 'Quelque chose à partager ?', 'Vous savez voyageur, je vois passer \nnombre de joueurs ici...j\'entends \nhistoires, mystères et rumeurs...Nombre\nsont ceux qui sont à la recherche\nd\'une salle secrète qui serait cachée\n dans le casino...On raconte qu\'il faudrait\n murmurer le nom du casino suivi d\'une\n formule magique...Je n\'en sais pas plus.'), 
(Button(boutons_dialogue2, boutons_dialogue1, 350, 430), 'Parle de la Meaurylle', 'Haha, vous vous interessez à lui à ce \nque je vois...C\'était un grand et puissant \nguerrier, craint et respecté de tous. \nNul ne sait ce qu\'il est devenu, mais \non raconte que ses légendaires \ncrampons seraient encore cachés \ndans le casino...')], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 330), 'Je veux y acceder'),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 480), 'Au revoir')], (10,60),classement,ecran2,"Archon")

Excelsious = EcranPnj([pygame.image.load(f'images/Pnj/Excelsious/_a_{i},80.png') for i in range(13)], 
"Bonjour héros...Préparez-vous... \nIci, vous combattrez au péril de votre \nvie de redoutables démons...\nne faillissez pas...\nBonne chance, combattant.", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 330), 'Comment jouer ?', 'Chaque héros possède des \ncaractéristiques uniques :\n- Flèche droite/gauche : déplacements \n-Touche 0 : attaque normale \n-Touche 1 : capacité secondaire \n(si le héros en possède une)\nDe plus, certains héros possèdent des \npassifs uniques.'), 
(Button(boutons_dialogue2, boutons_dialogue1, 350, 380), 'Quelle est votre plus grande peur ?', 'Pff. Quelle question. Un guerrier ne \ncraint pas la peur. Il ne la connait pas.\nIl ne la cotoie jamais. Cependant...\nméfiez-vous du diable Maurice...'),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 430), 'Les crampons dorés ?', 'Pauvre fou ! Perdus que vous êtes ! \nAbandonnez toute recherche si vous \ntenez à votre vie. Maintenant, partez !')], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 280), 'Je veux jouer'),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 480), 'Au revoir')], (10,80),ecran2,ecran2,"Excelsious")

SunForge = EcranPnj([pygame.image.load(f'images/Pnj/SunForge/_a_frm{i},100.png') for i in range(14)], 
"Un grand combattant sait en reconnaitre \nun autre quand il en voit un ! Que venez\nvous faire ici héros ?", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 330), "Je veux engager des héros", "Bien sur ! Ici vous pourrez engager \ncombattants et voyageurs, en échange\n d\'une somme d\'argent. \nChoisissez bien !"), 
(Button(boutons_dialogue2, boutons_dialogue1, 350, 380), "Je cherche des informations", "Oh, vous savez, je ne sors pas \nbeaucoup d\'ici moi...je crains de n\'avoir \npas grand chose à vous raconter...en \nrevanche, si un problème peut être\n résolu par la force,\n n\'hésitez pas !"),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 430), "La salle secrète ?", f"Vous la cherchez ? Cela me rappelle \nma jeunesse...c\'est peine perdue : pour \nma part, j\'ai abandonné...Si cela vous \ntient à coeur, j\'avais entendu dire que \nle second chiffre serait {digicode.get_code()[1]}")], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 280), "Je veux y acceder"),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 480), 'Au revoir')], (10,80),hero,ecran_boutique,"Sun Forge",'images/Fonds d\'ecran/Boutique.png')

Rook = EcranPnj([pygame.image.load(f'images/Pnj/Rook/_a_frm{i},100.png') for i in range(14)], 
"Hahaha ! Qu'est-ce qui vous amène, l'ami ? \nAllons, venez prendre un verre !", 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 330), "Que vend-on ici ?", "Bienvenue au bar du Babel Casino l'ami !\nVenez donc vous reposer et vous \ndésaltérer ici. Allons nous raconter \nquelques histoires haha ! N'hésite pas à \npasser !"), 
(Button(boutons_dialogue2, boutons_dialogue1, 350, 380), "Je cherche des informations", f"Je ne sais pas grand chose, à part\nles dires de quelques ivrognes...\nQuoique,je crois me souvenir d'avoir \nentendu que le premier chiffre était {digicode.get_code()[0]}. \nCependant, aucune idée de ce que ça \nvoulait dire."),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 430), "Qui êtes-vous ?", "Comment, vous ne me connaissez pas ?\nVoyons, je suis Rook, le célèbre \nvainqueur incontesté de la Babel Arena ! \nJ'ai même battu le terrible démon \nNoshRak...Un conseil : si vous devez le combattre\n dans l'arene, fuiyez.")], 
[(Button(boutons_dialogue2, boutons_dialogue1, 350, 280), "Je veux y acceder"),
(Button(boutons_dialogue2, boutons_dialogue1, 350, 480), 'Au revoir')], (10,80),alcool,ecran_boutique,"Rook",'images/Fonds d\'ecran/Boutique.png')

#https://create.kahoot.it/share/kahoot-de-la-saint-valentin/4c40967a-24dd-492c-b28a-c0a9bd0376b7