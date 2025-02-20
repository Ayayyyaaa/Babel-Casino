import pygame
import time
from objets_et_variables import *
from sons import aie_hero
from random import randint,choice
from fonctions import distance

print("Chargement des boss...")

class Boss:
    def __init__(self,pv:int,y:int,speed:float,speedanim:float,cd1:float,cd2:float,cd3:float,element:str,fond,nom_fond:str) -> 'Boss':
        '''Initialise toutes les caractéristiques de base du boss.
        Paramètres : 
            - pv (int) : le nombre de pv du boss
            - y (int) : la position y (verticale) du boss
            - speedanim (float) : la vitesse d'animation des boss
            - cd1 (float) : le temps de recharge du la compétence 1 du boss
            - cd2 (float) : le temps de recharge du la compétence 2 du boss
            - cd3 (float) : le temps de recharge du la compétence 3 du boss
            - element (str) : l'élément du boss (sert pour les réactions élémentaires et multiplicateurs de dégâts)
            - fond : le fond à charger pour le combat (liste d'images)
            - nom_fond (str) : le nom du fond du boss (sert pour le décalage de hauteur à appliquer par rapport au sol)'''
        self.image = self.image = pygame.image.load('images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png')
        self.pv = pv
        self.pos_x = 1000
        self.pos_y = y
        self.cd_img = 0
        self.attaque1_dispo = True
        self.attaque2_dispo = True
        self.attaque3_dispo = True
        self.cd_attaque1 = 0
        self.cd_attaque2 = 0
        self.cd_attaque3 = 0
        self.victoire = False
        self.cd_ulti = 0
        self.mort = False
        self.pv_base = pv
        self.poison = False
        self.speed = speed
        self.speedanim = speedanim
        self.cd1 = cd1
        self.cd2 = cd2
        self.cd3 = cd3
        self.block = False
        self.type = element
        self.fond = fond
        self.nom_fond = nom_fond
        self.collision = False
    def get_collison(self) -> bool:
        return self.collision 
    def get_pv(self) -> float:
        return self.pv
    def get_pv_base(self) -> float:
        return self.pv_base
    def get_pos_x(self) -> float:
        return self.pos_x
    def get_pos_y(self) -> float:
        return self.pos_y
    def get_cd_attaque1(self) -> float:
        return time.time() - self.cd_attaque1
    def get_attaque1_dispo(self) -> bool:
        return self.attaque1_dispo
    def get_cd_attaque2(self) -> float:
        return time.time() - self.cd_attaque2
    def get_attaque2_dispo(self) -> bool:
        return self.attaque2_dispo
    def get_cd_attaque3(self) -> float:
        return time.time() - self.cd_attaque3
    def get_attaque3_dispo(self) -> bool:
        return self.attaque3_dispo
    def get_victoire(self) -> bool:
        return self.victoire
    def get_cd_ulti(self) -> float:
        return self.cd_ulti
    def get_mort(self) -> bool:
        return self.mort
    def get_portee(self) -> int:
        return self.portee
    def get_poison(self) -> float: # Le timestamp de l'application du poison
        return self.poison
    def get_speed(self) -> float:
        return self.speed
    def get_speed_anim(self) -> float:
        return (self.speedanim)
    def get_cd(self) -> tuple:
        return (self.cd1,self.cd2,self.cd3)
    def get_block(self) -> bool:
        return self.block
    def get_fond(self) -> list:
        return self.fond
    def get_type(self) -> str:
        return self.type
    def get_nomfond(self) -> str:
        return self.nom_fond
    def modif_pv(self, nb:float):
        self.pv += nb
    def modif_pos_x(self, nb:int):
        self.pos_x += nb
    def modif_pos_y(self, nb:int):
        self.pos_y += nb
    def modif_img(self, img):
        self.image = img
    def set_cd_img(self):
        self.cd_img = time.time()
    def set_cd_attaque1(self):
        self.cd_attaque1 = time.time()
    def set_attaque1_dispo(self, dispo:bool):
        self.attaque1_dispo = dispo
    def set_cd_attaque2(self):
        self.cd_attaque2 = time.time()
    def set_attaque2_dispo(self, dispo:bool):
        self.attaque2_dispo = dispo
    def set_cd_attaque3(self):
        self.cd_attaque3 = time.time()
    def set_attaque3_dispo(self, dispo:bool):
        self.attaque3_dispo = dispo
    def set_victoire(self, vict:bool):
        self.victoire = vict
    def set_cd_ulti(self, nb:float):
        self.cd_ulti = nb
    def set_mort(self,mort:bool):
        self.mort = mort
    def set_poison(self,poison:float): # Le timestamp de l'application du poison
        self.poison = poison
    def set_block(self,block:bool):
        self.block = block
    def set_collision(self,collision:bool):
        self.collision = collision

class Michel:
    def __init__(self) -> 'Michel':
        self.boss = Boss(100,360,3,0.15,4,0,0,'Neutre',chute,'Chute')
        self.images_attaque1 = [pygame.image.load(f'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm{i},70.png') for i in range(44,69)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/LancierBoss/Droite/Marche/_a_frm{i},70.png') for i in range(16)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/LancierBoss/Gauche/Marche/_a_frm{i},70.png') for i in range(16)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/LancierBoss/Mort/_a_frm{i},70.png') for i in range(83,100)]
        self.images_inaction = [pygame.image.load(f'images/Jeu de combat/LancierBoss/Gauche/Inaction/_a_frm{i},70.png') for i in range(16,28)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
    def attaque1(self,speed:float,j1):
        '''Permet de jouer l'attaque 1 du boss.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - j1 : le héros combattu
        '''
        # L'attaque 1 est en train d'être jouée.
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if self.frame >= len(self.images_attaque1)-1:
            if -160 < distance(j1,self) < 50 and not j1.hero.get_block():
                # Le héros perd 20 Pv
                j1.hero.modif_pv(-20)
                aie_hero.play()
                # Image des dégâts subis
                self.cd_dgt20 = time.time()
                print(f'Attaque2 : Pv hero : {j1.hero.get_pv()}')
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            # Si le héros se trouve à portée du boss :
        elif 3 <= self.frame <= 14:
            if -140 < distance(j1,self) < 100 and not j1.hero.get_block():
                # Le héros perd 10 Pv
                j1.hero.modif_pv(-0.2)
                print(f'Attaque : Pv hero {j1.hero.get_pv()}')
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        self.boss.modif_img(self.images_attaque1[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de l'inaction du boss (non utilisé pour ce boss)
        '''
        if int(self.frame) >= len(self.images_inaction)-1:
            self.frame = 0
        self.frame += speed
        self.boss.modif_img(self.images_inaction[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
                self.atk2 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        # Si le boss attaque, on fait progresser l'animation
        if self.atk1:
            self.attaque1(0.12,j1)
        # Si le boss n'attaque pas et qu'il n'est pas à portée
        elif not self.atk1 and not self.atk2 and not -140 < distance(j1,self) < 50:
            # Déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        # Sinon, on lance l'animation d'inaction
        else:
            self.inaction(0.12,'Gauche')
        # Si le héros est à portée du boss, on lance les attaques
        if -140 < distance(j1,self) < 50:
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
                
class TankBoss:
    def __init__(self) -> 'TankBoss':
        self.boss = Boss(230,350,4.5,0.16,5.7,10,0,'Foudre',temple,'Temple')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Droite/Attaque1/_a_{i},60.png').convert_alpha() for i in range(19)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Gauche/Attaque1/_a_{i},60.png').convert_alpha() for i in range(19)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Droite/Marche/_a_{i},60.png').convert_alpha() for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Gauche/Marche/_a_{i},60.png').convert_alpha() for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Mort/_a_{i},60.png').convert_alpha() for i in range(15)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Droite/Inaction/_a_{i},80.png').convert_alpha() for i in range(15)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/ThunderBoss/Gauche/Inaction/_a_{i},80.png').convert_alpha() for i in range(15)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False

    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
            # Réinitialiser le dictionnaire des dégâts par frame au début de l'attaque
            self.frames_degats = {}
        self.atk1 = True
        frame_actuelle = int(self.frame)
        if not j1.hero.get_block():
            # Si le joueur est à portée et que cette frame n'a pas encore infligé de dégâts
            if self.boss.get_collison() and frame_actuelle not in self.frames_degats.keys():
                # Infliger des dégâts différents selon la frame
                degats = 0  # Dégâts de base
                if frame_actuelle == 8:
                    degats = 22
                    aie_hero.play()
                if 8 < frame_actuelle < 14:  # Frames spéciales avec plus de dégâts
                    degats = randint(4,8)
                    aie_hero.play()
                j1.hero.modif_pv(-degats)
                # Marquer cette frame comme ayant infligé des dégâts
                self.frames_degats[frame_actuelle] = True
                print(f"Dégâts infligés à la frame {frame_actuelle}: -{degats} PV")
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            # Réinitialiser le dictionnaire des dégâts
            self.frames_degats = {}
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])
            
    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
                self.atk2 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        # Si le boss attaque
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        # Si le boss n'attaque pas et n'est pas à portée
        elif not self.atk1 and not self.boss.get_collison():
            # Déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        # Sinon, on lance l'animation d'inaction
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        # On lance l'attaque si le boss est à portée
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Cindera:
    def __init__(self) -> 'Cindera':
        self.boss = Boss(160,400,4,0.15,4.5,0,0,'Feu',lave,'Lave')
        self.images_attaque1 = [pygame.image.load(f'images/Jeu de combat/Cindera/Gauche/Attaque1/_a_{i},100.png') for i in range(40)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Cindera/Droite/Marche/_a_frm{i},0.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Cindera/Gauche/Marche/_a_frm{i},0.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Cindera/Mort/_a_frm{i},0.png') for i in range(26)]
        self.images_inaction = [pygame.image.load(f'images/Jeu de combat/Cindera/Gauche/Inaction/_a_frm{i},0.png') for i in range(12)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.ralenti = False
    def attaque1(self,speed:float,j1):
        '''Permet de jouer l'attaque 1 du boss.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - j1 : le héros combattu
        '''
        # L'attaque 1 est en train d'être jouée.
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if self.frame >= len(self.images_attaque1)-1:
            if self.boss.get_collison() and not j1.hero.get_block():
                # Le héros perd 20 Pv
                j1.hero.modif_pv(-90)
                aie_hero.play()
                # Image des dégâts subis
                self.cd_dgt20 = time.time()
                print(f'Attaque2 : Pv hero : {j1.hero.get_pv()}')
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            # Si le héros se trouve à portée du boss :
        elif 5 <= self.frame:
            if self.boss.get_collison() and not j1.hero.get_block():
                j1.hero.modif_pv(-0.28)
                print(f'Fournaise : Pv hero {j1.hero.get_pv()}')
                if not self.ralenti:
                    j1.hero.set_speed(j1.hero.get_speed()*0.6)
                    self.ralenti = True
            elif self.ralenti:
                self.ralenti = False
                j1.hero.set_speed(j1.hero.get_speed()/0.6)
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        self.boss.modif_img(self.images_attaque1[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de l'inaction du boss (non utilisé pour ce boss)
        '''
        if int(self.frame) >= len(self.images_inaction)-1:
            self.frame = 0
        self.frame += speed
        self.boss.modif_img(self.images_inaction[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        # Si le boss attaque
        if self.atk1:
            self.attaque1(0.15,j1)
        # Si le boss n'attaque pas et n'est pas à portée
        elif not self.atk1 and not self.atk2 and not self.boss.get_collison():
            # Déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        # Sinon, on lance l'animation d'inaction
        else:
            self.inaction(0.12)
        # On lance l'attaque si le boss est à portée
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class DarkLord:
    def __init__(self) -> 'DarkLord':
        self.boss = Boss(160,450,4,0.16,2.8,10,0,'Nuit',pluie,'Pluie')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/DarkLord/Droite/Attaque1/_a_frm{i},0.png') for i in range(23)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/DarkLord/Gauche/Attaque1/_a_frm{i},0.png') for i in range(23)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/DarkLord/Droite/Marche/_a_frm{i},0.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/DarkLord/Gauche/Marche/_a_frm{i},0.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/DarkLord/Mort/_a_frm{i},0.png') for i in range(20)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/DarkLord/Droite/Inaction/_a_frm{i},0.png') for i in range(16)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/DarkLord/Gauche/Inaction/_a_frm{i},0.png') for i in range(16)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if int(self.frame) == 7:
            if self.boss.get_collison() and not j1.hero.get_block():
                j1.hero.set_poison(True)
        elif int(self.frame) == 13:
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Astral:
    def __init__(self) -> 'Astral':
        self.boss = Boss(160,440,4,0.16,3.2,10,0,'Esprit',eglise,'Eglise')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Astral/Droite/Attaque1/_a_{i},100.png') for i in range(29)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Astral/Gauche/Attaque1/_a_{i},100.png') for i in range(29)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Astral/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Astral/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Astral/Mort/_a_frm{i},100.png') for i in range(12)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Astral/Droite/Inaction/_a_frm{i},100.png') for i in range(12)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Astral/Gauche/Inaction/_a_frm{i},100.png') for i in range(12)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if self.frame >= len(self.images_attaque1_d)-1:
            if self.boss.get_collison() and not j1.hero.get_block():
                aie_hero.play()
                j1.hero.set_poison(time.time())
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
        if self.boss.get_collison() and not j1.hero.get_block() and 16 <= self.frame <= 25:
                j1.hero.modif_pv(-1.5)
                aie_hero.play()
                # Image des dégâts subis
                self.cd_dgt20 = time.time()
                print(f'Attaque2 : Pv hero : {j1.hero.get_pv()}')
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class EternityPainter:
    def __init__(self) -> 'EternityPainter':
        self.boss = Boss(150,495,4,0.16,3.2,10,0,'Esprit',chute,'Chute')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Ep/Droite/Attaque1/_a_frm{i},60.png') for i in range(23)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Ep/Gauche/Attaque1/_a_frm{i},60.png') for i in range(23)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Ep/Droite/Marche/_a_frm{i},60.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Ep/Gauche/Marche/_a_frm{i},60.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Ep/Mort/_a_frm{i},60.png') for i in range(11)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Ep/Droite/Inaction/_a_frm{i},80.png') for i in range(12)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Ep/Gauche/Inaction/_a_frm{i},80.png') for i in range(12)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 5:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-8)
                    self.dgt1 = True
            elif self.boss.get_collison() and int(self.frame) == 11:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-10)
                    self.dgt2 = True
            elif self.boss.get_collison() and int(self.frame) == 17:
                if not self.dgt3:
                    aie_hero.play()
                    j1.hero.modif_pv(-20)
                    self.dgt3 = True    
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Shidai:
    def __init__(self) -> 'Shidai':
        self.boss = Boss(180,445,4,0.16,2.8,4,0,'Air',chute,'Chute')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Shidai/Droite/Attaque1/_a_{i},60.png') for i in range(20)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Shidai/Gauche/Attaque1/_a_{i},60.png') for i in range(20)]
        self.cp2_d = [pygame.image.load(f'images/Jeu de combat/Shidai/Droite/Attaque2/_a_{i},60.png') for i in range(6)]
        self.cp2_g = [pygame.image.load(f'images/Jeu de combat/Shidai/Gauche/Attaque2/_a_{i},60.png') for i in range(6)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Shidai/Droite/Marche/_a_frm{i},60.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Shidai/Gauche/Marche/_a_frm{i},60.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Shidai/Mort/_a_{i},60.png') for i in range(18)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Shidai/Droite/Inaction/_a_{i},80.png') for i in range(14)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Shidai/Gauche/Inaction/_a_{i},80.png') for i in range(14)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.bonus = 0
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 3:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-10-self.bonus/3)
                    self.dgt1 = True
            elif self.boss.get_collison() and int(self.frame) == 6:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-10-self.bonus/3)
                    self.dgt2 = True
            elif self.boss.get_collison() and int(self.frame) == 13:
                if not self.dgt3:
                    aie_hero.play()
                    j1.hero.modif_pv(-20-self.bonus/3)
                    self.dgt3 = True    
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
            self.bonus = 0
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j1):
        '''Permet de jouer la 2e compétence du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la compétence
            - j1 : le joueur
        '''
        self.atk2 = True
        if self.boss.get_pv() > 0:
            if self.frame >= len(self.cp2_d)-1:
                self.frame = 0
            if self.pv_actuels != self.boss.get_pv() or self.boss.get_pv() < 0:
                self.frame = 0
                self.boss.set_cd_attaque2()
                self.boss.set_attaque2_dispo(False)
                self.atk2 = False
            if sens == 'Gauche':
                self.boss.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.boss.modif_img(self.cp2_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed
            self.bonus += 0.05
            print(self.bonus)

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif self.atk2:
            if distance(j1,self) < 0:
                self.cp2(0.18,'Gauche',j1)
            else:
                self.cp2(0.18,'Droite',j1)
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
        if self.boss.get_attaque2_dispo() and not self.atk1 and abs(distance(j1,self)) < 320:
                if not self.atk2:
                    self.frame = 0
                    self.pv_actuels = self.boss.get_pv()
                self.atk2 = True

class Lilithe:
    def __init__(self) -> 'Lilithe':
        self.boss = Boss(200,455,4,0.16,3.8,5,2.7,'Feu',lave,'Lave')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Lilithe/Droite/Attaque1/_a_{i},100.png') for i in range(12)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Lilithe/Gauche/Attaque1/_a_{i},100.png') for i in range(12)]
        self.images_attaque2_d = [pygame.image.load(f'images/Jeu de combat/Lilithe/Droite/Attaque2/_a_{i},70.png') for i in range(25)]
        self.images_attaque2_g = [pygame.image.load(f'images/Jeu de combat/Lilithe/Gauche/Attaque2/_a_{i},70.png') for i in range(25)]
        self.cp2_d = [pygame.image.load(f'images/Jeu de combat/Lilithe/Droite/Attaque3/_a_{i},70.png') for i in range(14)]
        self.cp2_g = [pygame.image.load(f'images/Jeu de combat/Lilithe/Gauche/Attaque3/_a_{i},70.png') for i in range(14)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Lilithe/Droite/Marche/_a_frm{i},70.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Lilithe/Gauche/Marche/_a_frm{i},70.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Lilithe/Mort/_a_{i},70.png') for i in range(20)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Lilithe/Droite/Inaction/_a_{i},80.png') for i in range(20)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Lilithe/Gauche/Inaction/_a_{i},80.png') for i in range(20)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.atk3 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.bonus = 0
        self.pv_actuels = 160

    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 6:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-8)
                    self.dgt1 = True
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def attaque2(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque 2 du boss.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - j1 : le héros combattu
            - s (str) : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk2 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 6:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-10-self.bonus/2)
                    self.dgt1 = True
            elif self.boss.get_collison() and int(self.frame) == 17:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-20-self.bonus/2)
                    self.dgt2 = True
        if self.frame >= len(self.images_attaque2_d)-1:
            self.boss.set_cd_attaque2()
            self.boss.set_attaque2_dispo(False)
            self.atk2 = False
            self.dgt1 = False
            self.dgt2 = False
            self.bonus = 0
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque2_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque2_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j1):
        '''Permet de jouer la 2e compétence du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la compétence
            - j1 : le joueur
        '''
        if self.boss.get_pv() > 0:
            if self.frame >= len(self.cp2_d)-1:
                self.frame = 0
            if self.pv_actuels != self.boss.get_pv() or self.boss.get_pv() < 0:
                self.frame = 0
                self.boss.set_cd_attaque3()
                self.boss.set_attaque3_dispo(False)
                self.atk3 = False
            if sens == 'Gauche':
                self.boss.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.boss.modif_img(self.cp2_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed
            self.bonus += 0.21

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if not self.atk3:
            if int(self.frame) >= len(self.images_marche_d)-1:
                self.frame = 0
            self.frame += speed
            if sens == 'Gauche':
                self.boss.modif_img(self.images_marche_g[int(self.frame)])
            else:
                self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu
        '''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu
        '''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif self.atk2:
            if distance(j1,self) < 0:
                self.attaque2(0.18,j1,'Gauche')
            else:
                self.attaque2(0.18,j1,'Droite')
        elif self.atk3:
            if distance(j1,self) < 0:
                self.cp2(0.18,'Gauche',j1)
            else:
                self.cp2(0.18,'Droite',j1)
            if distance(j1,self) < 300 and self.bonus >= 25:
                self.frame = 0
                self.boss.set_cd_attaque3()
                self.boss.set_attaque3_dispo(False)
                self.atk3 = False
        elif not self.atk1 and not self.atk2 and not self.atk3 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2 and not self.atk3:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
            if self.boss.get_attaque2_dispo() and not self.atk1 and not self.atk3:
                if not self.atk2:
                    self.frame = 0
                self.atk2 = True
        if self.boss.get_attaque3_dispo() and not self.atk1 and not self.atk2 and abs(distance(j1,self)) < 400:
                if not self.atk3:
                    self.frame = 0
                    self.pv_actuels = self.boss.get_pv()
                self.atk3 = True

class Solfist:
    def __init__(self) -> 'Solfist':
        self.boss = Boss(260,450,4,0.16,4.5,10,0,'FeuImmune',lave,'Lave')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Solfist/Droite/Attaque1/_a_{i},100.png') for i in range(41)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Solfist/Gauche/Attaque1/_a_{i},100.png') for i in range(41)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Solfist/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Solfist/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Solfist/Mort/_a_{i},100.png') for i in range(25)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Solfist/Droite/Inaction/_a_{i},100.png') for i in range(12)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Solfist/Gauche/Inaction/_a_{i},100.png') for i in range(12)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            if 7 <= int(self.frame) <= 18:
                if self.boss.get_collison():
                    aie_hero.play()
                    j1.hero.modif_pv(-0.4)
            elif int(self.frame) == 30:
                if self.boss.get_collison():
                    if not self.dgt2:
                        aie_hero.play()
                        j1.hero.modif_pv(-45)
                        self.dgt2 = True  
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt2 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        """permet de bien orienter le boss"""
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Elyx:
    def __init__(self) -> 'Elyx':
        self.boss = Boss(240,470,3.5,0.16,5,10,0,'Neutre',chute,'Chute')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Elyx/Droite/Attaque1/_a_{i},100.png') for i in range(12)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Elyx/Gauche/Attaque1/_a_{i},100.png') for i in range(12)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Elyx/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Elyx/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Elyx/Mort/_a_{i},100.png') for i in range(11)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Elyx/Droite/Inaction/_a_{i},100.png') for i in range(11)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Elyx/Gauche/Inaction/_a_{i},100.png') for i in range(11)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if int(self.frame) == 7 and not self.dgt2:
                if self.boss.get_collison():
                    aie_hero.play()
                    j1.hero.modif_pv(-18)
                    self.dgt2 = True
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt2 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str,j1):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if abs(distance(j1,self)) <= 150 and not self.dgt3:
            j1.hero.modif_pv(-10)
            j1.hero.set_stun(True)
            j1.hero.set_speed(0)
            self.boss.set_cd_attaque2()
            self.dgt3 = True
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu
        '''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche',j1)
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite',j1)
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu
        '''
        if 1 < self.boss.get_cd_attaque2() < 1.5 :
            j1.hero.set_stun(False)
            j1.hero.set_speed(j1.hero.get_speed_base())
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
            self.boss.set_block(True)
        else:
            self.boss.set_block(False)
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                self.dgt3 = False
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Embla:
    def __init__(self) -> 'Embla':
        self.boss = Boss(150,440,4,0.16,2.8,4,0,'Glace',temple,'Temple')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Embla/Droite/Attaque1/_a_{i},60.png') for i in range(38)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Embla/Gauche/Attaque1/_a_{i},60.png') for i in range(38)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Embla/Droite/Marche/_a_{i},60.png') for i in range(10)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Embla/Gauche/Marche/_a_{i},60.png') for i in range(10)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Embla/Mort/_a_frm{i},60.png') for i in range(12)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Embla/Droite/Inaction/_a_{i},80.png') for i in range(18)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Embla/Gauche/Inaction/_a_{i},80.png') for i in range(18)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 7:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-12)
                    self.dgt1 = True
            elif self.boss.get_collison() and int(self.frame) == 14:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-12)
                    self.dgt2 = True
            elif self.boss.get_collison() and int(self.frame) == 27:
                if not self.dgt3:
                    aie_hero.play()
                    j1.hero.modif_pv(-35)
                    self.dgt3 = True    
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Sun:
    def __init__(self) -> 'Sun':
        self.boss = Boss(260,450,4,0.16,5,10,0,'FeuImmune',lave,'Lave')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Sun/Droite/Attaque1/_a_{i},100.png') for i in range(33)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Sun/Gauche/Attaque1/_a_{i},100.png') for i in range(33)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Sun/Droite/Marche/_a_{i},100.png') for i in range(5)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Sun/Gauche/Marche/_a_{i},100.png') for i in range(5)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Sun/Mort/_a_{i},100.png') for i in range(17)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Sun/Droite/Inaction/_a_{i},100.png') for i in range(26)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Sun/Gauche/Inaction/_a_{i},100.png') for i in range(26)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            if int(self.frame) == 19:
                if self.boss.get_collison():
                    if not self.dgt1:
                        aie_hero.play()
                        j1.hero.modif_pv(-40)
                        self.dgt1 = True  
            elif int(self.frame) == 20:
                if self.boss.get_collison():
                    if not self.dgt2:
                        aie_hero.play()
                        j1.hero.modif_pv(-45)
                        self.dgt2 = True  
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Skurge:
    def __init__(self) -> 'Skurge':
        self.boss = Boss(140,510,5,0.16,6.5,10,0,'Nature',chute,'Chute')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Skurge/Droite/Attaque1/_a_{i},100.png') for i in range(14)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Skurge/Gauche/Attaque1/_a_{i},100.png') for i in range(14)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Skurge/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Skurge/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Skurge/Mort/_a_{i},100.png') for i in range(9)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Skurge/Droite/Inaction/_a_{i},100.png') for i in range(11)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Skurge/Gauche/Inaction/_a_{i},100.png') for i in range(11)]
        self.image = pygame.image.load('images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png')
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.versladroite = False
        self.verslagauche = False
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if int(self.frame) == 9 and not j1.hero.get_block():
            if not self.dgt1 and self.sens == 'Gauche' and distance(j1,self) < 0 or not self.dgt1 and self.sens == 'Droite' and distance(j1,self) > 0:
                aie_hero.play()
                dgt = choice([40,40,40,40,80])
                if dgt == 80:
                    print("Coup critique !")
                j1.hero.modif_pv(-dgt)
                self.dgt1 = True  
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros
        Paramètres :
            - j1 : le héros combattu
        '''
        if distance(j1,self) > 0:
            if self.boss.get_pos_x() < 200:
                self.versladroite = True
            else:
                self.marche(self.boss.get_speed_anim(),'Gauche')
                self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) < 0:
            if self.boss.get_pos_x() > 1000:
                self.verslagauche = True
            else:
                self.marche(self.boss.get_speed_anim(),'Droite')
                self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        if self.boss.get_attaque1_dispo():
            if not self.atk1:
                self.frame = 0
            self.atk1 = True
        elif not self.atk1 and abs(distance(j1,self)) < 250:
            # Sinon, déplacement pour être à portée du héros
            if self.versladroite:
                self.marche(self.boss.get_speed_anim(),'Droite')
                self.boss.modif_pos_x(self.boss.get_speed())
            elif self.verslagauche:
                self.marche(self.boss.get_speed_anim(),'Gauche')
                self.boss.modif_pos_x(-self.boss.get_speed())
            else:
                self.boss_vers_hero(j1)
        else:
            self.versladroite = False
            self.verslagauche = False
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')

class NoshRak:
    def __init__(self) -> 'NoshRak':
        self.boss = Boss(150,470,4,0.16,2.8,4,0,'Foudre',desert,'Desert')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Droite/Attaque1/_a_{i},60.png') for i in range(35)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Gauche/Attaque1/_a_{i},60.png') for i in range(35)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Droite/Marche/_a_{i},60.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Gauche/Marche/_a_{i},60.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Mort/_a_{i},60.png') for i in range(24)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Droite/Inaction/_a_{i},80.png') for i in range(20)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Nosh-Rak/Gauche/Inaction/_a_{i},80.png') for i in range(20)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and int(self.frame) == 2:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-8)
                    self.dgt1 = True
            elif self.boss.get_collison() and int(self.frame) == 8:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-8)
                    self.dgt2 = True
                    if self.dgt1:
                        j1.hero.set_stun(True)
            elif self.boss.get_collison() and int(self.frame) == 23:
                if not self.dgt3:
                    aie_hero.play()
                    j1.hero.modif_pv(-30)
                    self.dgt3 = True    
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
            j1.hero.set_stun(False)
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if self.frame >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Purgatos:
    def __init__(self) -> 'Purgatos':
        self.boss = Boss(150,420,4,0.16,2.0,0,0,'Esprit',eglise,'Desert')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Purgatos/Droite/Attaque1/_a_{i},100.png') for i in range(23)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Purgatos/Gauche/Attaque1/_a_{i},100.png') for i in range(23)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Purgatos/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Purgatos/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Purgatos/Mort/_a_{i},100.png') for i in range(17)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Purgatos/Droite/Inaction/_a_{i},100.png') for i in range(14)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Purgatos/Gauche/Inaction/_a_{i},100.png') for i in range(14)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            print("aaaaaaa",self.boss.get_collison(),self.frame)
            if self.boss.get_collison() and int(self.frame) == 15:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-35)
                    self.dgt1 = True 
                    j1.hero.set_poison(True)
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            j1.hero.set_stun(False)
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if self.frame >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        else:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.25,j1,'Gauche')
            else:
                self.attaque1(0.25,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Ciphyron:
    def __init__(self) -> 'Ciphyron':
        self.boss = Boss(150,420,4,0.16,2.0,0,0,'Foudre',desert,'Desert')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Droite/Attaque1/_a_{i},60.png') for i in range(22)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Gauche/Attaque1/_a_{i},60.png') for i in range(22)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Droite/Marche/_a_{i},60.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Gauche/Marche/_a_{i},60.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Mort/_a_{i},60.png') for i in range(17)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Droite/Inaction/_a_{i},80.png') for i in range(16)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Ciphyron/Gauche/Inaction/_a_{i},80.png') for i in range(16)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block():
            # Si toutes les images ont été jouées :
            if self.boss.get_collison() and not j1.hero.get_block():
                if int(self.frame) == 9:
                    if not self.dgt1:
                        aie_hero.play()
                        j1.hero.modif_pv(-10)
                        self.dgt1 = True 
                elif int(self.frame) == 10:
                    if not self.dgt2:
                        aie_hero.play()
                        j1.hero.modif_pv(-5)
                        self.dgt2 = True 
                elif int(self.frame) == 14:
                    if not self.dgt3:
                        aie_hero.play()
                        j1.hero.modif_pv(-10)                       
                        self.dgt3 = True 
                        j1.hero.set_stun(True)
                elif int(self.frame) == 15:
                    if not self.dgt4:
                        aie_hero.play()
                        j1.hero.modif_pv(-5)
                        self.dgt4 = True 
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
            self.dgt4 = False
            j1.hero.set_stun(False)
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if self.frame >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.25,j1,'Gauche')
            else:
                self.attaque1(0.25,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Golem:
    def __init__(self) -> 'Golem':
        self.boss = Boss(350,357,2.8,0.16,6.8,4,0,'Foudre',temple,'Temple')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Golem/Droite/Attaque1/_a_{i},70.png') for i in range(28)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Golem/Gauche/Attaque1/_a_{i},70.png') for i in range(28)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Golem/Droite/Marche/_a_{i},70.png') for i in range(12)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Golem/Gauche/Marche/_a_{i},70.png') for i in range(12)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Golem/Mort/_a_{i},70.png') for i in range(20)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Golem/Droite/Inaction/_a_{i},80.png') for i in range(16)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Golem/Gauche/Inaction/_a_{i},80.png') for i in range(16)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque 1 du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le héros combattu
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
            # Réinitialiser le dictionnaire des dégâts par frame au début de l'attaque
            self.frames_degats = {}
            
        self.atk1 = True
        frame_actuelle = int(self.frame)
        
        if not j1.hero.get_block():
            # Si le joueur est à portée et que cette frame n'a pas encore infligé de dégâts
            if self.boss.get_collison() and frame_actuelle not in self.frames_degats:
                # Infliger des dégâts différents selon la frame
                degats = 0  # Dégâts de base
                if frame_actuelle == 10:
                    degats = 20
                    aie_hero.play()
                elif frame_actuelle == 12:
                    degats = 25
                    aie_hero.play()
                if 13 < frame_actuelle < 22:  # Frames spéciales avec plus de dégâts
                    degats = randint(1,8)
                
                j1.hero.modif_pv(-degats)
                # Marquer cette frame comme ayant infligé des dégâts
                self.frames_degats[frame_actuelle] = True
                print(f"Dégâts infligés à la frame {frame_actuelle}: -{degats} PV")
        
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            # Réinitialiser le dictionnaire des dégâts
            self.frames_degats = {}
            
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
            
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Soji:
    def __init__(self):
        self.boss = Boss(210,480,4,0.16,5,7,4.5,'Foudre',desert,'Desert')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Soji/Droite/Attaque1/_a_{i},100.png') for i in range(22)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Soji/Gauche/Attaque1/_a_{i},100.png') for i in range(22)]
        self.images_attaque2_d = [pygame.image.load(f'images/Jeu de combat/Soji/Droite/Attaque2/_a_{i},70.png') for i in range(25)]
        self.images_attaque2_g = [pygame.image.load(f'images/Jeu de combat/Soji/Gauche/Attaque2/_a_{i},70.png') for i in range(25)]
        self.cp2_d = [pygame.image.load(f'images/Jeu de combat/Soji/Droite/Attaque3/_a_{i},70.png') for i in range(12)]
        self.cp2_g = [pygame.image.load(f'images/Jeu de combat/Soji/Gauche/Attaque3/_a_{i},70.png') for i in range(12)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Soji/Droite/Marche/_a_{i},70.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Soji/Gauche/Marche/_a_{i},70.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Soji/Mort/_a_{i},70.png') for i in range(19)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Soji/Droite/Inaction/_a_{i},80.png') for i in range(14)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Soji/Gauche/Inaction/_a_{i},80.png') for i in range(14)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.atk3 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.bonus = 0
        self.pv_actuels = 160

    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        if not j1.hero.get_block() and self.boss.get_collison():
            # Si toutes les images ont été jouées :
            if int(self.frame) == 8:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-5)
                    self.dgt1 = True
            elif int(self.frame) == 17:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-25)
                    self.dgt2 = True
        if self.frame >= len(self.images_attaque1_d)-1:
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
            self.dgt2 = False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def attaque2(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque 2 du boss.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - j1 : le héros combattu
            - s (str) : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk2 = True
        if not j1.hero.get_block() and self.boss.get_collison():
            # Si toutes les images ont été jouées :
            if int(self.frame) == 7:
                if not self.dgt1:
                    aie_hero.play()
                    j1.hero.modif_pv(-10-self.bonus/3)
                    self.dgt1 = True
            elif int(self.frame) == 11:
                if not self.dgt2:
                    aie_hero.play()
                    j1.hero.modif_pv(-10-self.bonus/3)
                    self.dgt2 = True
            elif int(self.frame) == 16:
                if not self.dgt3:
                    aie_hero.play()
                    j1.hero.modif_pv(-30-self.bonus/3)
                    self.dgt3 = True
        if self.frame >= len(self.images_attaque2_d)-1:
            self.boss.set_cd_attaque2()
            self.boss.set_attaque2_dispo(False)
            self.atk2 = False
            self.dgt1 = False
            self.dgt2 = False
            self.dgt3 = False
            self.bonus = 0
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            # Image du block
            j1.cd_block_img = time.time()
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque2_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque2_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j1):
        '''Permet de jouer la 2e compétence du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la compétence
            - j1 : le joueur
        '''
        self.atk3 = True
        if self.boss.get_pv() > 0:
            if self.frame >= len(self.cp2_d)-1:
                self.frame = 0
            if self.pv_actuels != self.boss.get_pv() or self.boss.get_pv() < 0:
                self.frame = 0
                self.boss.set_cd_attaque3()
                self.boss.set_attaque3_dispo(False)
                self.atk3 = False
            if sens == 'Gauche':
                self.boss.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.boss.modif_img(self.cp2_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed
            self.bonus += 0.18

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif self.atk2:
            if distance(j1,self) < 0:
                self.attaque2(0.18,j1,'Gauche')
            else:
                self.attaque2(0.18,j1,'Droite')
        elif self.atk3:
            if distance(j1,self) < 0:
                self.cp2(0.18,'Gauche',j1)
            else:
                self.cp2(0.18,'Droite',j1)
            if self.boss.get_collison() and self.bonus >= 25:
                self.frame = 0
                self.boss.set_cd_attaque3()
                self.boss.set_attaque3_dispo(False)
                self.atk3 = False
        elif not self.atk1 and not self.atk2 and not self.atk3 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo() and not self.atk2 and not self.atk3:
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
            if self.boss.get_attaque2_dispo() and not self.atk1 and not self.atk3:
                if not self.atk2:
                    self.frame = 0
                self.atk2 = True
        if self.boss.get_attaque3_dispo() and not self.atk1 and not self.atk2 and abs(distance(j1,self)) < 400:
                if not self.atk3:
                    self.frame = 0
                    self.pv_actuels = self.boss.get_pv()
                self.atk3 = True
class Prophet:
    def __init__(self) -> 'Prophet':
        self.boss = Boss(200,500,2.8,0.16,5.5,4,0,'Foudre',temple,'Temple')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Prophet/Droite/Attaque1/_a_{i},100.png') for i in range(34)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Prophet/Gauche/Attaque1/_a_{i},100.png') for i in range(34)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Prophet/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Prophet/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Prophet/Mort/_a_{i},100.png') for i in range(19)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Prophet/Droite/Inaction/_a_{i},100.png') for i in range(18)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Prophet/Gauche/Inaction/_a_{i},100.png') for i in range(18)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.sens = 'Droite'
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.pv_actuels = self.boss.get_pv()
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if 8<int(self.frame)<15:
            if distance(j1,self) < 0:
                j1.hero.modif_pos_x(8)
            else:
                j1.hero.modif_pos_x(-8)
        
        if int(self.frame) == 16 and not self.dgt1:
            if self.boss.get_collison() and not j1.hero.get_block():
                j1.hero.modif_pv(-55)
                self.dgt1 = True
        elif int(self.frame) >= len(self.images_attaque1_d)-1:
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1=False
        # Si le héros a bloqué l'attaque :
        if j1.hero.get_block():
            print("Bloqué !")
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens:str):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens:str='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not abs(distance(j1,self)) < 200:
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if abs(distance(j1,self)) < 200:
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
"""class Minion:
    def __init__(self,nom):
        self.boss = Boss(80,480,4,0.16,2.1,10,0,'Nuit',pluie,'Pluie')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Droite/Attaque1/_a_{i},100.png') for i in range(20)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Gauche/Attaque1/_a_{i},100.png') for i in range(20)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Droite/Inaction/_a_{i},100.png') for i in range(12)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Pandora/{nom}/Gauche/Inaction/_a_{i},100.png') for i in range(12)]
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.compteur = 0
        self.atk1 = False
        self.dgt1 = False
        self.sens = 'Droite'
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if int(self.frame) == 15 and not self.dgt1:
            self.compteur += 1
            if self.boss.get_collison() and not j1.hero.get_block():
                # Le héros perd 20 Pv
                j1.hero.set_poison(True)
                j1.hero.modif_pv(-10)
                aie_hero.play()
                self.dgt1 = True
        if self.frame >= len(self.images_attaque1_d)-1:
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,j1):
        if self.boss.get_cd_attaque1() > self.boss.get_cd()[0]:
            self.boss.set_attaque1_dispo(True)
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and not self.boss.get_collison():
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if self.boss.get_collison():
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True

class Pandora:
    def __init__(self):
        self.boss = Boss(160,480,4,0.16,6,10,0,'Nuit',pluie,'Pluie')
        self.images_attaque1_d = [pygame.image.load(f'images/Jeu de combat/Pandora/Droite/Attaque1/_a_{i},100.png') for i in range(23)]
        self.images_attaque1_g = [pygame.image.load(f'images/Jeu de combat/Pandora/Gauche/Attaque1/_a_{i},100.png') for i in range(23)]
        self.images_marche_d = [pygame.image.load(f'images/Jeu de combat/Pandora/Droite/Marche/_a_{i},100.png') for i in range(8)]
        self.images_marche_g = [pygame.image.load(f'images/Jeu de combat/Pandora/Gauche/Marche/_a_{i},100.png') for i in range(8)]
        self.images_mort = [pygame.image.load(f'images/Jeu de combat/Pandora/Mort/_a_{i},100.png') for i in range(13)]
        self.images_inaction_d = [pygame.image.load(f'images/Jeu de combat/Pandora/Droite/Inaction/_a_frm{i},100.png') for i in range(10)]
        self.images_inaction_g = [pygame.image.load(f'images/Jeu de combat/Pandora/Gauche/Inaction/_a_frm{i},100.png') for i in range(10)]
        self.dgt10 = pygame.image.load("images/Jeu de combat/-10.png")
        self.dgt20 = pygame.image.load("images/Jeu de combat/-20.png")
        self.image = 'images/Jeu de combat/LancierBoss/Gauche/Attaque1/_a_frm44,70.png'
        self.cd_dgt10 = 0
        self.cd_dgt20 = 0
        self.frame = 0
        self.frame_mort = 0
        self.atk1 = False
        self.atk2 = False
        self.dgt1 = False
        self.minion = None
        self.minion_spawn_x = 0
        self.minion_spawn_y = 0
    def attaque1(self,speed:float,j1,s:str):
        '''Permet de jouer l'attaque au poing du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : le joueur
            - s : le sens de l'attaque
        '''
        # L'attaque 1 est en train d'être jouée.
        if self.frame < 1:
            self.sens = s
        self.atk1 = True
        # Si toutes les images ont été jouées :
        if int(self.frame) == 15 and not self.dgt1:
            if self.boss.get_collison() and not j1.hero.get_block():
                # Le héros perd 20 Pv
                j1.hero.modif_pv(-20)
                aie_hero.play()
                # Image des dégâts subis
                self.cd_dgt20 = time.time()
                print(f'Attaque : Pv hero : {j1.hero.get_pv()}')
            if not self.minion:
                self.minion = choice([Minion('Envy'),Minion('Fear')])
                self.minion.compteur = 0
                # Position du minion par rapport à la position et l'orientation de Pandora
                if self.sens == 'Gauche':
                    self.minion_spawn_x = self.boss.get_pos_x() - 100
                else:
                    self.minion_spawn_x = self.boss.get_pos_x() + 100
                self.minion_spawn_y = self.boss.get_pos_y()+60
                self.minion.boss.modif_pos_x(-self.minion.boss.get_pos_x() + self.minion_spawn_x)
                self.minion.boss.modif_pos_y(-self.minion.boss.get_pos_y() + self.minion_spawn_y)
                self.dgt1 = True
        if self.frame >= len(self.images_attaque1_d)-1:
            # On remet tout à 0
            self.boss_sprite_attaque1 = 0
            self.boss.set_cd_attaque1()
            self.boss.set_attaque1_dispo(False)
            self.atk1 = False
            self.dgt1 = False
        # Faire progresser les images pour l'animation
        self.frame += speed        
        if self.sens == 'Gauche':
            self.boss.modif_img(self.images_attaque1_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_attaque1_d[int(self.frame)])

    def marche(self,speed:float,sens):
        '''Permet de jouer l'animation de marche du boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss'''
        if int(self.frame) >= len(self.images_marche_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_marche_d[int(self.frame)])

    def inaction(self,speed:float,sens='Gauche'):
        '''Permet de jouer l'animation d'inaction du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : le sens de la marche du boss
        '''
        if int(self.frame) >= len(self.images_inaction_d)-1:
            self.frame = 0
        self.frame += speed
        if sens == 'Gauche':
            self.boss.modif_img(self.images_inaction_g[int(self.frame)])
        else:
            self.boss.modif_img(self.images_inaction_d[int(self.frame)])

    def mort(self,speed:float,j1):
        '''Permet de jouer l'animation de mort du Boss.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j1 : héros combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.boss.get_mort():
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) >= len(self.images_mort)-1:
                self.boss.set_mort(True)
                # On déclare le héros vainqueur, le combat prend fin
                j1.hero.set_victoire(True)
                self.frame_mort = 0
                self.frame = 0
                self.atk1 = False
            else:
                # Faire progresser les images pour l'animation
                self.frame_mort += speed
                self.boss.modif_img(self.images_mort[int(self.frame_mort)])

    def boss_vers_hero(self,j1):
        '''Permet au boss de se diriger vers le héros.
        Paramètres :
            - j1 : le héros combattu'''
        if distance(j1,self) < 0:
            self.marche(self.boss.get_speed_anim(),'Gauche')
            self.boss.modif_pos_x(-self.boss.get_speed())
        elif distance(j1,self) > 0:
            self.marche(self.boss.get_speed_anim(),'Droite')
            self.boss.modif_pos_x(self.boss.get_speed())

    def patern_boss(self,xhero:float,j1):
        '''Définit le comportement du boss
        Paramètres :
            - xhero (float) : la position du héros en x
            - j1 : le héros combattu'''
        if self.atk1:
            if distance(j1,self) < 0:
                self.attaque1(0.18,j1,'Gauche')
            else:
                self.attaque1(0.18,j1,'Droite')
        elif not self.atk1 and abs(distance(j1,self)) > 470:
            # Sinon, déplacement pour être à portée du héros
            self.boss_vers_hero(j1)
        else:
            if distance(j1,self) < 0:
                self.inaction(0.14,'Gauche')
            else:
                self.inaction(0.14,'Droite')
        if abs(distance(j1,self)) <= 470:
            if self.boss.get_attaque1_dispo():
                if not self.atk1:
                    self.frame = 0
                self.atk1 = True
        if self.minion:
            if self.minion.compteur > 1:
                self.minion = None
            else:
                self.minion.patern_boss(j1)"""