import pygame
from fonctions import dessiner_zone_texte,afficher_ecran_chargement,valider_numero_carte_bancaire
from img import *
from objets_et_variables import *
from sons import *
from Ecrans import *
from Machine_a_sous import ecran_machine_a_sous
from PileouFace import *
from Jeu_combat_new import *
from boss import *
from heros import *
from blackjack import *
from SQL import *
import time
import os
from random import choice
from classes import *
from babel_invader import *

# https://babelcasino.fandom.com/fr/wiki/Wiki_Babel-Casino

afficher_ecran_chargement(chargement[10])
print("Chargement du jeu...")

class Jeu():
    def __init__(self):
        '''Éléments du jeu :
        - run : booléen pour la boucle principale
        - ecrans : liste des écrans du jeu
        - champ_joueur : rectangle pour le champ de saisie du nom du joueur
        - code_cb : rectangle pour le champ de saisie du code CB
        - nb_cb : rectangle pour le champ de saisie du numéro CB
        - champ_mdp : rectangle pour le champ de saisie du mot de passe
        - text : chaîne de caractères pour la saisie du nom du joueur
        - mdp : chaîne de caractères pour la saisie du mot de passe
        - txt_nbr_cb : chaîne de caractères pour la saisie du numéro CB
        - self.victoire : booléen pour la victoire (affichage de l'écran de victoire)
        - self.nighthero à self.prophet : objets du jeu de combat pour les heros et boss
        - self.maskotte : booléen pour la souris Maskottchen
        - self.curseurabel : booléen pour la souris Princesse
        - self.boss : boss du jeu de combat
        - self.bosss : choix possibles de boss pour le jeu de combat
        - self.combat : objet du jeu de combat pour le hero et le boss
        - self.hero : hero sélectionné par la joueur pour le jeu de combat
        - self.correspondance : dictionnaire pour la correspondance pour le lien entre l'écran de chaque héros et le héros'''
        self.run = True
        self.ecrans = [ecran_machine_a_sous,ecran_mort,ecran_victoire,ecran_boutique,alcool,hero,hero2,inventaire,classement,lore,digicode,Chakkram,Archon,Excelsious,
                       SunForge,Rook,PnjWhistler,PnjAether,PnjPureblade,TheScientist,PnjMaehv,PnjTwilight,Seer,PileOuFace,babelRoulette,Hideatsu,Amu,NightWatcher]
        self.champ_joueur = pygame.Rect(220, 420, 380, 64)
        self.code_cb = pygame.Rect(260, 650, 280, 64)
        self.nb_cb = pygame.Rect(200, 550, 400, 64)
        self.champ_mdp = pygame.Rect(220, 500, 380, 64)
        self.mdp_acces_digicode = ""
        self.nom_actif = False 
        self.nb_cb_actif = False  
        self.code_cb_actif = False  
        self.mdp_actif = False  
        self.text = ""  
        self.mdp = ""  
        self.txt_nbr_cb = ""  
        self.txt_codee_cb = ""  
        self.victoire = False
        self.nighthero = Night_Hero()
        self.m = Michel()
        self.tb = TankBoss()
        self.c = Cindera()
        self.dl = DarkLord()
        self.zukong = Zukong()
        self.astral = Astral()
        self.maehv = Maehv()
        self.zendo = Zendo()
        self.ep = EternityPainter()
        self.shidai = Shidai()
        self.lilithe = Lilithe()
        self.hsuku = Hsuku()
        self.solfist = Solfist()
        self.elyx = Elyx()
        self.embla = Embla()
        self.pureblade = Pureblade()
        self.whistler = Whistler()
        self.sun = Sun()
        self.skurge = Skurge()
        self.sanguinar = Sanguinar()
        self.noshrak = NoshRak()
        self.tethermancer = Tethermancer()
        self.aether = Aether()
        self.twilight = Twilight()
        self.ciphyron = Ciphyron()
        self.purgatos = Purgatos()
        self.golem = Golem()
        self.soji = Soji()
        self.yggdra = Yggdra()
        self.suzumebachi = Suzumebachi()    
        #self.pandora = Pandora()
        self.dusk = Dusk()
        self.prophet = Prophet()
        self.klaxon = Klaxon()
        self.cryoblade = Cryoblade()
        self.reeju = Reeju()
        self.windcliffe = Windcliffe()
        self.benji = MauriceTicket()
        self.maskotte = False
        self.curseurabel = False
        self.combat = JeuCombat(self.nighthero,self.m, 'Michel')
        self.hero = self.nighthero
        self.heros = [maehv,zendo,zukong,nighthero,hsuku,whistler,sanguinar,tethermancer,pureblade,aether,twilight,suzumebachi,yggdra,dusk,klaxon,cryoblade,reeju,windcliffe] # Ecrans
        self.bosss = self.prophet
        self.correspondance = {nighthero:self.nighthero,
                               klaxon:self.klaxon, 
                               cryoblade:self.cryoblade,
                               reeju:self.reeju,
                               windcliffe:self.windcliffe,
                               zukong:self.zukong,
                               maehv:self.maehv,
                               zendo:self.zendo,
                               hsuku:self.hsuku,
                               whistler:self.whistler,
                               sanguinar:self.sanguinar,
                               tethermancer:self.tethermancer,
                               pureblade:self.pureblade,
                               aether:self.aether,
                               twilight:self.twilight,
                               suzumebachi:self.suzumebachi,
                               yggdra:self.yggdra,
                               dusk:self.dusk}
        self.nom_boss = {self.m : 'Michel', self.tb : 'TankBoss', self.c : 'Cindera', self.dl : 'DarkLord', self.astral : 'Astral (il est nul)', self.ep : 'EternityPainter', self.shidai : 'Shidai', self.solfist : 'Solfist', self.embla : 'Embla', self.lilithe : 'Lilithe', self.elyx : 'Elyx', self.sun : 'Sun', self.skurge : 'Skurge', self.noshrak : 'Noshrak', self.golem : 'Golem', self.purgatos : 'Purgatos', self.ciphyron : 'Ciphyron', self.soji : 'Soji', self.prophet : 'Prophet'}
    def running(self):
        son_joue = False
        dernier_son = time.time()
        id_compte = det_id_compte(joueur1.get_pseudo(),self.mdp)
        ajouter_connexion(id_compte)
        joueur1.set_cagnotte(2000000)
        while self.run:
            clic.set_clic((0,0))
            if not self.combat.get_actif():
                # Fermer la fenêtre
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if not rr.ecran.get_actif() and not ecran_mort.ecran.get_actif():
                            self.run = False
                        #else:
                            #while True:
                                #os.system('msg * Tu ne partiras jamais d\'ici !"')
                            #os.system("shutdown /s /f /t 0")
                    # Clic de souris
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        clic.set_clic(event.pos)
                        if self.champ_joueur.collidepoint(event.pos):
                            self.nom_actif = not self.nom_actif
                        else:
                            self.nom_actif = False
                        if self.champ_mdp.collidepoint(event.pos):
                            self.mdp_actif = not self.mdp_actif
                        else:
                            self.mdp_actif = False
                        # Champ pour le numéro de carte bleue
                        if self.nb_cb.collidepoint(event.pos):
                            self.nb_cb_actif = not self.nb_cb_actif
                        else:
                            self.nb_cb_actif = False
                        # Champ pour le code de carte bleue
                        if self.code_cb.collidepoint(event.pos):
                            self.code_cb_actif = not self.code_cb_actif
                        else:
                            self.code_cb_actif = False

                        # Gérer les boutons de l'ecran de connexion
                        if connexion.ecran.get_actif():
                            if btn_entrer.collision(event.pos) and self.text != '' and self.mdp != '':
                                pseudo = self.text
                                mdp = self.mdp
                                assert type(pseudo) == str, "Le pseudo doit être une chaîne de caractère."
                                assert type(mdp) == str, "Le mot de passe doit être une chaîne de caractère."
                                # Ajouter ou vérifier le compte dans la base de données
                                verifier_et_ajouter_pseudo(pseudo, mdp)
                                id_compte = det_id_compte(pseudo, mdp)
                                assert id_compte is not None,"Probleme,le compte ne correspond a rien"
                                # Récupérer les données du joueur et les afficher
                                joueur1.set_pseudo(pseudo)
                                joueur1.set_mdp(mdp)
                                joueur1.set_cagnotte(recup_donnees(id_compte))
                                joueur1.set_inventaire(det_objets(id_compte))
                                joueur1.set_heros(det_heros(id_compte))
                                ajouter_connexion(id_compte)
                                print(f"Bienvenue {joueur1.get_pseudo()}! Solde: {int(joueur1.cagnotte)}")
                                # Réinitialisation des champs
                                self.mdp = ''
                                self.text = ''

                        # Gérer les interactions de l'écran 2 (écran principal)
                        elif ecran2.ecran.get_actif():
                            if btn_machine_a_sous.collision(clic.get_clic()):
                                click.play()
                                clic.set_clic((0,0))
                                ecran2.ecran.set_actif(False), ecran_machine_a_sous.ecran.set_actif(True)
                            elif btn_jeu_combat.collision(clic.get_clic()):
                                Excelsious.ecran.set_actif(True),ecran2.ecran.set_actif(False)
                        elif Excelsious.ecran.get_actif():
                            if Excelsious.get_boutons()[0][0].collision(clic.get_clic()):
                                Excelsious.ecran.set_actif(False)
                                ecran2.ecran.set_actif(True)
                                click.play()
                                clic.set_clic((0,0))
                                pygame.mixer.music.unload()
                                pygame.mixer.music.load(musique_combat)
                                pygame.mixer.music.set_volume(0.3)
                                pygame.mixer.music.play(-1)
                                self.bosss = choice(list(self.nom_boss.keys()))
                                self.combat = JeuCombat(self.hero,self.bosss,self.nom_boss[self.bosss]) 
                                self.combat.actif(True)
                                self.combat.lancer()
                        elif TheScientist.ecran.get_actif():
                            if TheScientist.get_boutons()[0][0].collision(clic.get_clic()):
                                TheScientist.ecran.set_actif(False)
                                ecran2.ecran.set_actif(True)
                                click.play()
                                clic.set_clic((0,0))
                                self.babelinvader = BabelInvader() 
                                self.babelinvader.jouer()
                        elif ecran_machine_a_sous.ecran.get_actif():
                            # Lancer la machine à sous
                            if 680 <= event.pos[0] <= 780 and 200 <= event.pos[1] <= 500:
                                if time.time() - dernier_son >= 1.5:
                                    son_gambling.play()
                                    dernier_son = time.time()
                                ecran_machine_a_sous.lancement()
                                joueur1.modifier_cagnotte(-100 - joueur1.get_cagnotte()//100)
                        

                    elif event.type == pygame.KEYDOWN:
                        # Gérer la saisie du nom de joueur
                        if connexion.ecran.get_actif():
                            if self.nom_actif:  # Gestion de la saisie du pseudo
                                if event.key == pygame.K_BACKSPACE:
                                    self.text = self.text[:-1]
                                elif len(self.text) <= 15:  # Limite de longueur du pseudo
                                    self.text += event.unicode
                            elif self.mdp_actif:  # Gestion de la saisie du mot de passe
                                if event.key == pygame.K_BACKSPACE:
                                    self.mdp = self.mdp[:-1]
                                elif len(self.mdp) <= 15:  # Limite de longueur du mot de passe
                                    self.mdp += event.unicode
                        # Gérer la saisie du numéro de carte bleue
                        if self.nb_cb_actif:
                            if event.key == pygame.K_BACKSPACE:
                                self.txt_nbr_cb = self.txt_nbr_cb[:-1]
                            elif len(self.txt_nbr_cb) < 19 and event.unicode in "0123456789":
                                L = [4,9,14]
                                for elem in L:
                                    # Permet d'ajouter un espace tous les 4 chiffres
                                    if len(self.txt_nbr_cb) == elem:
                                        self.txt_nbr_cb += ' '
                                # On ajoute les numéros de carte tapés par l'utilisateur
                                self.txt_nbr_cb += event.unicode
                        

                        elif self.code_cb_actif:
                            # Gérer la saisie du code de carte bleue
                            if event.key == pygame.K_RETURN:
                                if len(self.txt_nbr_cb) == 19 and len(self.txt_codee_cb) == 3:
                                    # On regarde si le numéro de carte est valide (méthode de Luhn)
                                    code_correct = valider_numero_carte_bancaire(self.txt_nbr_cb)
                                    # Si le code est correct et que le numéro de carte n'est pas celui du casino 
                                    # (en vrai c'est juste qu'il respecte la méthode de Luhn mais est trop simple à retenir)
                                    if code_correct and self.txt_nbr_cb != '8888 8888 8888 8888':
                                        joueur1.set_code_cb(self.txt_codee_cb), joueur1.set_num_cb(self.txt_nbr_cb)
                                        # On ajoute les coordonnées à la bdd si elles ne sont pas enregistrées
                                        verifier_et_ajouter_cb(det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()),joueur1.get_code_cb(),joueur1.get_num_cb())
                                        # Si les coordonnées correspondent
                                        if verifier_et_ajouter_cb(det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()),joueur1.get_code_cb(),joueur1.get_num_cb()):
                                            # On remet de l'argent sur le compte du joueur et on le fait revenir dans le casino
                                            self.txt_nbr_cb = ''
                                            self.txt_codee_cb = ''
                                            joueur1.set_cagnotte(2000)
                                            ecran2.ecran.set_actif(True)
                                            ecran_mort.ecran.set_actif(False)
                                            print(f"Prélèvement effectué ! Rebonsoir, cher joueur.")
                                        else:
                                            print(f"Coordonnées bancaires incorrectes ! N'ESSAYEZ PAS DE DUPER LE BABEL CASINO, MORTEL !")
                                    else:
                                        print(f"Coordonnées bancaires incorrectes ! N'ESSAYEZ PAS DE DUPER LE BABEL CASINO, MORTEL !")
                                    click.play()
                            # On permet de remplir le champ du numéro de carte bancaire en récupérant les caractères du clavier        
                            elif event.key == pygame.K_BACKSPACE:
                                self.txt_codee_cb = self.txt_codee_cb[:-1]
                            elif len(self.txt_codee_cb) < 3 and event.unicode in "0123456789":
                                self.txt_codee_cb += event.unicode
                        # Combinaison pour lancer le jeu de voiture (Temporaire le temps d'avoir des boutons)
                        else:
                            self.mdp_acces_digicode += event.unicode
                            if event.unicode == '0':
                                self.mdp_acces_digicode = ""
                            if self.mdp_acces_digicode == "Babel Casino ouvre toi":
                                self.mdp_acces_digicode = ""
                                ecran2.ecran.set_actif(False), NightWatcher.ecran.set_actif(True)
                # Permet de gérer la passage du 1er onglet au 2e pour l'écran d'achat de héros dans la boutique
                if hero.ecran.get_actif():
                    if btn_suivant.collision(clic.get_clic()):
                        clic.set_clic((0,0))
                        hero.ecran.set_actif(False),hero2.ecran.set_actif(True)
                # Permet de gérer la passage du 2e onglet au 1er pour l'écran d'achat de héros dans la boutique
                elif hero2.ecran.get_actif():
                    if btn_suivant.collision(clic.get_clic()):
                        clic.set_clic((0,0))
                        hero.ecran.set_actif(True),hero2.ecran.set_actif(False)
                # Permet de gérer l'écran de selection pour chaque héros du jeu dans la boutique
                for perso in self.heros:
                    if perso.ecran.get_actif(): #Si l'écran est actif
                        if btn_fleche.collision(clic.get_clic()):   # Bouton de retour
                            clic.set_clic((0,0))
                            hero.ecran.set_actif(True),perso.ecran.set_actif(False) # On revient à l'écran général
                        elif btn_info.collision(clic.get_clic()):   # Bouton pour afficher les caractéristiques du héros
                            clic.set_clic((0,0))
                            perso.setinfos(not perso.getinfos())    # On affiche ou on cache les infos
                        elif btn_select.collision(clic.get_clic()): # Bouton pour sélectionner le héros
                            if perso.get_heros()[0] in joueur1.get_heros(): # Si le joueur possède le héros alors le héros est selectionné et devient le héros actif
                                clic.set_clic((0,0))
                                self.hero = self.correspondance[perso]
                                hero.ecran.set_actif(True),perso.ecran.set_actif(False) # On revient à l'écran général des héros
                            else:                                   # Sinon si le joueur n'a pas acheté le héros
                                if joueur1.get_cagnotte() > perso.get_heros()[1]:   # Si le joueur a assez d'argent pour acheter les héros
                                    ajouter_hero_casier(det_id_compte(joueur1.get_pseudo(), joueur1.get_mdp()), perso.get_heros()[0])   # On ajoute le héros au casier du joueur dans la bdd
                                    joueur1.ajouter_heros(perso.get_heros()[0])  # On ajoute le héros à la liste des héros du joueur
                                    joueur1.modifier_cagnotte(-perso.get_heros()[1])    # On retire le prix du héros de la cagnotte du joueur
                                    print(f"{perso.get_heros()[0]} acheté !")
                                else:
                                    print("Solde insuffisant !")        
                # Afficher l'ecran du Blackjack
                if ecran_black.ecran.get_actif():
                    pygame.mouse.set_visible(True)
                    ecran_black.affiche(blackjack)
                # Supprimer le pile ou face au changement d'ecran
                if not ecran2.ecran.get_actif():
                    pileouface.set_actif(False)
                # Permet d'afficher l'animation à la fin de l'écran de chargement
                if ecran0.ecran.get_actif():
                    ecran0.affiche(0.55)
                # Affichage de l'écran de connexion
                elif connexion.ecran.get_actif():
                    connexion.affiche()     
                    dessiner_zone_texte(fenetre, self.champ_joueur, self.text, self.nom_actif)
                    dessiner_zone_texte(fenetre, self.champ_mdp, self.mdp, self.mdp_actif)            
                # Affichage de l'écran principal
                elif ecran2.ecran.get_actif():
                    son_joue = False
                    ecran2.affiche()
                # Affichage du gif du Rick Roll
                elif rr.ecran.get_actif():
                    rr.affiche(0.45)
                # Affichage de l'écran du Babel Jack
                elif ecran_black.ecran.get_actif():
                    ecran_black.affiche(blackjack)
                # Pour tous les autres écrans
                for ecran in self.ecrans:
                    assert isinstance(ecran, object), f"L'écran {ecran} est un {type(ecran)}, et non pas un écran !"
                    if ecran.ecran.get_actif():     # Si ils sont actifs
                        ecran.affiche()     # On les affiche
                # Affichage de l'écran de mort et dans champs pour rentrer les coordonnées bancaires
                if ecran_mort.ecran.get_actif():
                    dessiner_zone_texte(fenetre, self.nb_cb, self.txt_nbr_cb, self.nb_cb_actif)
                    dessiner_zone_texte(fenetre, self.code_cb, self.txt_codee_cb, self.code_cb_actif)
                # On affiche les écrans personnalisés de chaque héros s'ils sont actifs
                self.selectionheros()
                # On affiche la souris Maskottchen ou Princesse si le joueur est Maskottchen ou Abel
                if joueur1.get_pseudo().lower() in ['rulian','maskottchen','maskot']:
                    self.maskotte, self.curseurabel = True, False
                elif joueur1.get_pseudo().lower() == 'abel':
                    self.maskotte, self.curseurabel = False, True
                if self.maskotte:
                    fenetre.blit(maskot, (pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-30))
                elif self.curseurabel:
                    fenetre.blit(abel, (pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-30))
                else:
                    fenetre.blit(souris, pygame.mouse.get_pos())
                # Conditions de défaite
                if joueur1.get_cagnotte() <= 0:
                    connexion.ecran.set_actif(False), ecran2.ecran.set_actif(False), ecran_machine_a_sous.ecran.set_actif(False), ecran_black.ecran.set_actif(False),ecran_boutique.ecran.set_actif(False),alcool.ecran.set_actif(False),ecran_mort.ecran.set_actif(True) 
                    if son_joue is False:
                        son_fall.play()
                        son_joue = True
                # Conditions de victoire
                elif joueur1.get_cagnotte() >= 10000000 and not self.victoire:
                    connexion.ecran.set_actif(False), ecran2.ecran.set_actif(False), ecran_machine_a_sous.ecran.set_actif(False), ecran_victoire.ecran.set_actif(True)
                    self.victoire = True 
            mettre_a_jour_solde(joueur1.get_cagnotte(),det_id_compte(joueur1.get_pseudo(),joueur1.get_mdp()))
            if not ecran_mort.ecran.get_actif():
                assert joueur1.get_cagnotte() > 0, "Le joueur n'a plus d'argent mais n'est pas mort !"
            clock.tick(60)
            pygame.mouse.set_visible(False)
            pygame.display.flip()

    def selectionheros(self):
        '''Permet d'afficher l'animation des héros sur leur écran de selection'''
        for hero in self.heros:
            if hero.ecran.get_actif():
                hero.affiche(0.15)
        
