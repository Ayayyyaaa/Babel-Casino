import pygame
import time
import sys
from objets_et_variables import *
from sons import son_epee,aie_boss,aie_hero
from random import randint,choice
from fonctions import afficher_ecran_chargement, distance

print("Chargement des héros...")

class Hero:
    def __init__(self,pv:int,y:int,speed:float,spanim1:float,marche:int,cd1:float,cd2:float,element:str) -> 'Hero':
        '''Permet d'initialiser la classe héros.
        Paramètres :
            - pv (int) : la vie du héros
            - y (int) : la position y du héros
            - speed (float) : la vitesse du héros
            - spanim1 (float) : la vitesse de l'animation du héros
            - marche (int) : la vitesse de marche du héros
            - cd1 (float) : le temps de rechargement de la compétence 1
            - cd2 (float) : le temps de rechargement de la compétence 2
            - element (str) : l'élément du héros
        '''
        self.image = None
        self.pv = pv
        self.pv_base = pv   # Pv max du héros
        self.pos_x = 50
        self.pos_y = y
        self.cd_img = 0
        self.attaque = False    # Bool qui indique si les héros est en train de joueur l'attaque
        self.victoire = False   #Bool qui indique si le héros a gagné le combat
        self.cp2 = False
        self.block = False  # Bool qui indique si le héros est en train de bloquer les attaques
        self.cd_cp2 = time.time()
        self.cd_atk = time.time()
        self.mort = False
        self.speed = speed
        self.speed_base = speed
        self.speed_anim1 = spanim1
        self.speed_anim4 = marche
        self.combo = False
        self.cd = (cd1,cd2)
        self.poison = False
        self.stun = False   # Bool qui indique si le héros est stun
        self.type = element  # Type du héros (pour les réactions élémentaire)
        self.collision = False  # Bool qui indique si le héros est en collision avec le boss
    def get_collison(self) -> bool:
        return self.colision 
    def get_img(self):
        return self.image
    def get_pv(self) -> float:
        return self.pv
    def get_pv_base(self) -> int:
        return self.pv_base
    def get_pos_x(self) -> float:
        return self.pos_x
    def get_pos_y(self) -> float:
        return self.pos_y
    def get_attaque(self) -> bool:
        return self.attaque
    def get_victoire(self) -> bool:
        return self.victoire
    def get_cp2(self) -> float:
        return self.cp2
    def get_cd_cp2(self) -> float:
        return time.time() - self.cd_cp2    # Temps depuis la dernière compétence
    def get_cd_atk(self) -> float:
        return time.time() - self.cd_atk    # Temps depuis la dernière compétence
    def get_mort(self) -> bool:
        return self.mort
    def get_speed(self) -> float:
        return self.speed
    def get_speed_base(self) -> float:
        return self.speed_base
    def get_speed_anim(self) -> tuple:
        return (self.speed_anim1,self.speed_anim4)
    def get_block(self) -> bool:
        return (self.block)
    def get_combo(self) -> bool:
        return self.combo
    def get_portee(self) -> int:
        return self.portee
    def get_cd(self) -> tuple:
        return self.cd
    def get_poison(self) -> float:
        return self.poison
    def get_stun(self) -> bool:
        return self.stun
    def get_type(self) -> str:
        return self.type
    def set_mort(self,mort:bool):
        self.mort = mort
    def modif_pv(self, nb:float):
        self.pv += nb
    def modif_pos_x(self, nb:float):
        self.pos_x += nb
    def modif_pos_y(self, nb:float):
        self.pos_y += nb
    def set_attaque(self, actif:bool):
        self.attaque = actif
    def modif_img(self, img:str):
        self.image = pygame.image.load(img).convert_alpha()
    def set_cd_img(self):
        self.cd_img = time.time()
    def set_victoire(self,vict:bool):
        self.victoire = vict
    def set_cp2(self, actif:bool):
        self.cp2 = actif
    def set_cd_cp2(self):
        self.cd_cp2 = time.time()
    def set_cd_atk(self):
        self.cd_atk = time.time()
    def set_block(self,block:bool):
        self.block = block
    def set_combo(self,combo:bool):
        self.combo = combo
    def set_speed(self,s:float):
        self.speed = s
    def set_poison(self,poison:float):
        self.poison = poison
    def set_stun(self,stun:bool):
        self.stun = stun
    def set_collision(self,collision:bool):
        self.colision = collision

class Night_Hero:
    def __init__(self) -> 'Night_Hero':
        self.hero = Hero(100,540,4,0.25,0.2,1.2,5,'Nuit')
        self.images_coup_depee_d = [f'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque{i}.png' for i in range(1,13)]
        self.images_coup_depee_g = [f'images/Jeu de combat/Hero/Attaque/Attaque_Gauche/Attaque{i}.png' for i in range(1,13)]
        self.images_marche_d = [f'images/Jeu de combat/Hero/Marche/Droite/Hero_course{i}.png' for i in range(1,7)] 
        self.images_marche_g = [f'images/Jeu de combat/Hero/Marche/Gauche/Hero_course{i}.png' for i in range(1,7)]
        self.images_parade = [f'images/Jeu de combat/Hero/Block/Block ({i}).png' for i in range(1,19)]
        self.images_mort = [f'images/Jeu de combat/Hero/Mort/_afrm{i},70.png' for i in range(1,23)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0

    def inaction(self,sens:str):
        return None

    def attaque(self,speed:float,sens,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.frame >= len(self.images_coup_depee_d)-1:
                son_epee.play()
                # Si le boss est à portée du héros
                if self.hero.get_collison() and not j2.boss.get_block():
                    # Le boss perd 5 Pv
                    aie_boss.play()
                    j2.boss.modif_pv(-5*multis*joueur1.get_multis_jeu_combat())
                    print(f"Attaque Épée Héros : Pv boss : {j2.boss.get_pv()}")
                    # Affichage des dégâts subis
                    self.cd_dgt5 = time.time()
                self.frame = 0
                self.hero.set_attaque(False)
            if sens == 'Gauche':
                self.hero.modif_img(self.images_coup_depee_g[int(self.frame)])
            else:
                self.hero.modif_img(self.images_coup_depee_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])
        

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_block(True)
        # On ne joue l'animation que si le héros n'est pas en train d'attaquer
        if not self.hero.get_attaque() and  self.hero.get_pv() > 0:
            self.hero.modif_img(self.images_parade[int(self.frame_parade)])
        # Si toutes les images ont été jouées :
        if int(self.frame_parade) >= len(self.images_parade)-1:
            # On remet tout à 0
            self.frame_parade = 0
            self.hero.set_block(False)
            self.hero.set_cp2(False)
        # Faire progresser les images pour l'animation
        self.frame_parade += speed

    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

class Zukong:
    def __init__(self):
        self.hero = Hero(160,495,4.5,0.18,0.14,4.5,3,'Neutre')
        self.atk1_d = [f'images/Jeu de combat/Zukong/Droite/Attaque1/_a_frm{i},60.png' for i in range(19)]
        self.atk1_g = [f'images/Jeu de combat/Zukong/Gauche/Attaque1/_a_frm{i},60.png' for i in range(19)]
        self.images_marche_d = [f'images/Jeu de combat/Zukong/Droite/Marche/_a_frm{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Zukong/Gauche/Marche/_a_frm{i},60.png' for i in range(8)]
        self.cp2_d = [f'images/Jeu de combat/Zukong/Droite/Attaque2/_a_frm{i},60.png' for i in range(19,32)]
        self.cp2_g = [f'images/Jeu de combat/Zukong/Gauche/Attaque2/_a_frm{i},60.png' for i in range(19,32)]
        self.images_mort = [f'images/Jeu de combat/Zukong/Mort/_a_frm{i},60.png' for i in range(31)] 
        self.inaction_g = [f'images/Jeu de combat/Zukong/Gauche/Inaction/_a_frm{i},80.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Zukong/Droite/Inaction/_a_frm{i},80.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and 5 <= self.frame <= 11 and not j2.boss.get_block():
                # Le boss perd 5 Pv
                aie_boss.play()
                j2.boss.modif_pv(-0.55*multis*joueur1.get_multis_jeu_combat())
                print(f"Attaque Masse Héros : Pv boss : {j2.boss.get_pv()}")
                # Affichage des dégâts subis
                self.cd_dgt5 = time.time()
            if self.frame >= len(self.atk1_d)-1:
                son_epee.play()
                # Si le boss est à portée du héros
                self.frame = 0
                self.hero.set_attaque(False)
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0 :
            if self.frame >= len(self.cp2_d)-1:
                son_epee.play()
                if self.hero.get_collison() and not j2.boss.get_block():
                    aie_boss.play()
                    j2.boss.modif_pv(-8*multis*joueur1.get_multis_jeu_combat())
                self.frame = 0
                self.hero.set_cp2(False)
            if sens == 'Gauche':
                self.hero.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.hero.modif_img(self.cp2_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Maehv:
    def __init__(self):
        self.hero = Hero(125,440,3.2,0.18,0.14,5,1,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Maehv/Droite/Attaque1/_a_frm{i},60.png' for i in range(33)]
        self.atk1_g = [f'images/Jeu de combat/Maehv/Gauche/Attaque1/_a_frm{i},60.png' for i in range(33)]
        self.images_marche_d = [f'images/Jeu de combat/Maehv/Droite/Marche/_a_{i},60.png' for i in range(10)] 
        self.images_marche_g = [f'images/Jeu de combat/Maehv/Gauche/Marche/_a_{i},60.png' for i in range(10)]
        self.cp2_d = [f'images/Jeu de combat/Maehv/Droite/Attaque3/_a_{i},60.png' for i in range(4)]
        self.cp2_g = [f'images/Jeu de combat/Maehv/Gauche/Attaque3/_a_{i},60.png' for i in range(4)]
        self.images_mort = [f'images/Jeu de combat/Maehv/Mort/_a_{i},60.png' for i in range(11)] 
        self.inaction_g = [f'images/Jeu de combat/Maehv/Gauche/Inaction/_a_{i},80.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Maehv/Droite/Inaction/_a_{i},80.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.bonus = 0

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 4 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv((-6-self.bonus/3)*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 8 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv((-10-self.bonus/3)*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True
            elif self.hero.get_collison() and int(self.frame) == 23 and not j2.boss.get_block():
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv((-15-self.bonus/3)*multis*joueur1.get_multis_jeu_combat())
                    self.dgt3 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.dgt3 = False
                self.bonus = 0
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        keys = pygame.key.get_pressed()
        if self.hero.get_pv() > 0:
            if self.frame >= len(self.cp2_d)-1:
                self.frame = 0
            if self.hero.get_attaque() or self.hero.get_pv() < 0 or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                self.frame = 0
                self.hero.set_cp2(False)
            if sens == 'Gauche':
                self.hero.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.hero.modif_img(self.cp2_d[int(self.frame)])
            # Faire progresser les images pour l'animation
            self.frame += speed
            self.bonus += 0.15
            print(self.bonus)
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Zendo:
    def __init__(self):
        self.hero = Hero(130,440,5,0.18,0.14,4.5,3,'Air')
        self.atk1_d = [f'images/Jeu de combat/Zendo/Droite/Attaque/_a_{i},60.png' for i in range(38)]
        self.atk1_g = [f'images/Jeu de combat/Zendo/Gauche/Attaque/_a_{i},60.png' for i in range(38)]
        self.images_marche_d = [f'images/Jeu de combat/Zendo/Droite/Marche/_a_{i},60.png' for i in range(6)] 
        self.images_marche_g = [f'images/Jeu de combat/Zendo/Gauche/Marche/_a_{i},60.png' for i in range(6)]
        self.images_mort = [f'images/Jeu de combat/Zendo/Mort/_a_{i},60.png' for i in range(15)] 
        self.inaction_g = [f'images/Jeu de combat/Zendo/Gauche/Inaction/_a_frm{i},60.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Zendo/Droite/Inaction/_a_frm{i},60.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            # On inflige UNE fois les dégâts quand la frame atteint les frames de dégâts (12,18,24,30)
            if self.hero.get_collison() and int(self.frame) == 12 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-6*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 18 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-8*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True
            elif self.hero.get_collison() and int(self.frame) == 24 and not j2.boss.get_block():
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv(-10*multis*joueur1.get_multis_jeu_combat())
                    self.dgt3 = True    
                    self.hero.set_block(True)
            elif self.hero.get_collison() and int(self.frame) == 30 and not j2.boss.get_block():
                if not self.dgt4:
                    aie_boss.play()
                    j2.boss.modif_pv(-16*multis*joueur1.get_multis_jeu_combat())
                    self.dgt4 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.dgt3 = False
                self.dgt4 = False
                self.hero.set_block(False)
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Klaxon:
    def __init__(self):
        self.hero = Hero(120,520,4,0.18,0.14,4.5,1000,'Esprit')
        self.atk1_d = [f'images/Jeu de combat/Klaxon/Droite/Attaque1/_a_{i},60.png' for i in range(33)]
        self.atk1_g = [f'images/Jeu de combat/Klaxon/Gauche/Attaque1/_a_{i},60.png' for i in range(33)]
        self.images_marche_d = [f'images/Jeu de combat/Klaxon/Droite/Marche/_a_frm{i},60.png' for i in range(7)] 
        self.images_marche_g = [f'images/Jeu de combat/Klaxon/Gauche/Marche/_a_frm{i},60.png' for i in range(7)]
        self.images_mort = [f'images/Jeu de combat/Klaxon/Mort/_a_{i},60.png' for i in range(20)] 
        self.inaction_g = [f'images/Jeu de combat/Klaxon/Gauche/Inaction/_a_{i},80.png' for i in range(18)]
        self.inaction_d = [f'images/Jeu de combat/Klaxon/Droite/Inaction/_a_{i},80.png' for i in range(18)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 23 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-18*multis*joueur1.get_multis_jeu_combat())
                    j2.boss.set_poison(time.time())
                    self.dgt1 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Windcliffe:
    def __init__(self):
        self.hero = Hero(220,490,3.5,0.18,0.14,4.5,1000,'Neutre')
        self.atk1_d = [f'images/Jeu de combat/Windcliffe/Droite/Attaque1/_a_{i},70.png' for i in range(21)]
        self.atk1_g = [f'images/Jeu de combat/Windcliffe/Gauche/Attaque1/_a_{i},70.png' for i in range(21)]
        self.images_marche_d = [f'images/Jeu de combat/Windcliffe/Droite/Marche/_a_{i},70.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Windcliffe/Gauche/Marche/_a_{i},70.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Windcliffe/Mort/_a_{i},70.png' for i in range(14)] 
        self.inaction_g = [f'images/Jeu de combat/Windcliffe/Gauche/Inaction/_a_{i},80.png' for i in range(9)]
        self.inaction_d = [f'images/Jeu de combat/Windcliffe/Droite/Inaction/_a_{i},80.png' for i in range(9)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 12 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-25*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Reeju:
    def __init__(self):
        self.hero = Hero(180,470,4,0.18,0.14,3.8,1000,'Esprit')
        self.atk1_d = [f'images/Jeu de combat/Reeju/Droite/Attaque1/_a_{i},100.png' for i in range(25)]
        self.atk1_g = [f'images/Jeu de combat/Reeju/Gauche/Attaque1/_a_{i},100.png' for i in range(25)]
        self.images_marche_d = [f'images/Jeu de combat/Reeju/Droite/Marche/_a_{i},100.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Reeju/Gauche/Marche/_a_{i},100.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Reeju/Mort/_a_{i},100.png' for i in range(22)] 
        self.inaction_g = [f'images/Jeu de combat/Reeju/Gauche/Inaction/_a_{i},100.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Reeju/Droite/Inaction/_a_{i},100.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 7 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-5*multis*joueur1.get_multis_jeu_combat())
                    j2.boss.set_poison(time.time())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 12 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-2*multis*joueur1.get_multis_jeu_combat())
                    j2.boss.set_poison(time.time())
                    self.dgt2 = True
            elif self.hero.get_collison() and int(self.frame) == 18 and not j2.boss.get_block():
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv(-8*multis*joueur1.get_multis_jeu_combat())
                    j2.boss.set_poison(time.time())
                    self.dgt3 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt3 = False
                self.dgt2 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Cryoblade:
    def __init__(self):
        self.hero = Hero(140,520,4,0.18,0.14,4.5,1000,'Glace')
        self.atk1_d = [f'images/Jeu de combat/Cryoblade/Droite/Attaque1/_a_{i},60.png' for i in range(19)]
        self.atk1_g = [f'images/Jeu de combat/Cryoblade/Gauche/Attaque1/_a_{i},60.png' for i in range(19)]
        self.images_marche_d = [f'images/Jeu de combat/Cryoblade/Droite/Marche/_a_{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Cryoblade/Gauche/Marche/_a_{i},60.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Cryoblade/Mort/_a_{i},60.png' for i in range(20)] 
        self.inaction_g = [f'images/Jeu de combat/Cryoblade/Gauche/Inaction/_a_{i},80.png' for i in range(16)]
        self.inaction_d = [f'images/Jeu de combat/Cryoblade/Droite/Inaction/_a_{i},80.png' for i in range(16)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 8 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-22*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Pureblade:
    def __init__(self):
        self.hero = Hero(100,440,4,0.18,0.14,5.5,1000,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Pureblade/Droite/Attaque1/_a_{i},60.png' for i in range(34)]
        self.atk1_g = [f'images/Jeu de combat/Pureblade/Gauche/Attaque1/_a_{i},60.png' for i in range(34)]
        self.images_marche_d = [f'images/Jeu de combat/Pureblade/Droite/Marche/_a_{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Pureblade/Gauche/Marche/_a_{i},60.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Pureblade/Mort/_a_{i},60.png' for i in range(20)] 
        self.inaction_g = [f'images/Jeu de combat/Pureblade/Gauche/Inaction/_a_frm{i},80.png' for i in range(10)]
        self.inaction_d = [f'images/Jeu de combat/Pureblade/Droite/Inaction/_a_frm{i},80.png' for i in range(10)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and 5 <= int(self.frame) <= 13 and not j2.boss.get_block():
                aie_boss.play()
                j2.boss.modif_pv(-0.55*multis*joueur1.get_multis_jeu_combat())
            elif self.hero.get_collison() and int(self.frame) == 23 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-20*multis*joueur1.get_multis_jeu_combat())
                    j2.boss.set_poison(time.time())
                    self.dgt2 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt2 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Hsuku:
    def __init__(self):
        self.hero = Hero(100,450,5,0.18,0.14,3.5,3,'Neutre')
        self.atk1_d = [f'images/Jeu de combat/Hsuku/Droite/Attaque1/_a_{i},70.png' for i in range(24)]
        self.atk1_g = [f'images/Jeu de combat/Hsuku/Gauche/Attaque1/_a_{i},70.png' for i in range(24)]
        self.images_marche_d = [f'images/Jeu de combat/Hsuku/Droite/Marche/_a_{i},70.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Hsuku/Gauche/Marche/_a_{i},70.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Hsuku/Mort/_a_frm{i},70.png' for i in range(20)] 
        self.inaction_g = [f'images/Jeu de combat/Hsuku/Gauche/Inaction/_a_{i},80.png' for i in range(28)]
        self.inaction_d = [f'images/Jeu de combat/Hsuku/Droite/Inaction/_a_{i},80.png' for i in range(28)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 2 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-6*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 5 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-6*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True
            elif int(self.frame) == 12 and not j2.boss.get_block(): 
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv(-8*multis*joueur1.get_multis_jeu_combat())
                    self.dgt3 = True    
            elif int(self.frame) == 18 and not j2.boss.get_block():
                if not self.dgt4:
                    aie_boss.play()
                    j2.boss.modif_pv(-8*multis*joueur1.get_multis_jeu_combat())
                    self.dgt4 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.dgt3 = False
                self.dgt4 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Sanguinar:
    def __init__(self):
        self.hero = Hero(100,450,5,0.18,0.14,5,3,'Neutre')
        self.atk1_d = [f'images/Jeu de combat/Sanguinar/Droite/Attaque1/_a_{i},60.png' for i in range(33)]
        self.atk1_g = [f'images/Jeu de combat/Sanguinar/Gauche/Attaque1/_a_{i},60.png' for i in range(33)]
        self.images_marche_d = [f'images/Jeu de combat/Sanguinar/Droite/Marche/_a_{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Sanguinar/Gauche/Marche/_a_{i},60.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Sanguinar/Mort/_a_{i},60.png' for i in range(17)] 
        self.inaction_g = [f'images/Jeu de combat/Sanguinar/Gauche/Inaction/_a_{i},80.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Sanguinar/Droite/Inaction/_a_{i},80.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and 5 <= int(self.frame) <= 11 and not j2.boss.get_block():
                aie_boss.play()
                j2.boss.modif_pv(-0.25)
            elif self.hero.get_collison() and int(self.frame) == 16:
                if not j2.boss.get_block() and not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-6*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
                self.hero.set_block(True)
            elif 20 <= int(self.frame) <= 24 and not j2.boss.get_block(): 
                aie_boss.play()
                j2.boss.modif_pv(-0.38*multis*joueur1.get_multis_jeu_combat())
            elif int(self.frame) == 26 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-20*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.hero.set_block(False)
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Whistler:
    def __init__(self):
        self.hero = Hero(80,515,6,0.18,0.2,2.5,3,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Whistler/Droite/Attaque1/_a_{i},100.png' for i in range(31)]
        self.atk1_g = [f'images/Jeu de combat/Whistler/Gauche/Attaque1/_a_{i},100.png' for i in range(31)]
        self.images_marche_d = [f'images/Jeu de combat/Whistler/Droite/Marche/_a_{i},100.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Whistler/Gauche/Marche/_a_{i},100.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Whistler/Mort/_a_{i},100.png' for i in range(20)] 
        self.inaction_g = [f'images/Jeu de combat/Whistler/Gauche/Inaction/_a_{i},100.png' for i in range(18)]
        self.inaction_d = [f'images/Jeu de combat/Whistler/Droite/Inaction/_a_{i},100.png' for i in range(18)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if int(self.frame) == 12 and not j2.boss.get_block():
                if not self.dgt4:
                    dgt = choice([30, 30, 60])
                    if dgt == 60:
                        print("Coup critique !")
                    aie_boss.play()
                    j2.boss.modif_pv(-dgt*multis*joueur1.get_multis_jeu_combat())
                    self.dgt4 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt4 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Tethermancer:
    def __init__(self):
        self.hero = Hero(130,410,3.5,0.18,0.14,3.5,3,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Tethermancer/Droite/Attaque1/_a_{i},100.png' for i in range(27)]
        self.atk1_g = [f'images/Jeu de combat/Tethermancer/Gauche/Attaque1/_a_{i},100.png' for i in range(27)]
        self.images_marche_d = [f'images/Jeu de combat/Tethermancer/Droite/Marche/_a_{i},100.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Tethermancer/Gauche/Marche/_a_{i},100.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Tethermancer/Mort/_a_{i},100.png' for i in range(18)] 
        self.inaction_g = [f'images/Jeu de combat/Tethermancer/Gauche/Inaction/_a_{i},100.png' for i in range(17)]
        self.inaction_d = [f'images/Jeu de combat/Tethermancer/Droite/Inaction/_a_{i},100.png' for i in range(17)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if int(self.frame) == 6:
                self.hero.set_block(True)
            elif self.hero.get_collison() and int(self.frame) == 14:
                if not j2.boss.get_block() and not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-22*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
                self.hero.set_block(True)
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.hero.set_block(False)
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.125

class Aether:
    def __init__(self):
        self.hero = Hero(125,520,4,0.18,0.14,5,1,'Air')
        self.atk1_d = [f'images/Jeu de combat/Aether/Droite/Attaque1/_a_{i},100.png' for i in range(26)]
        self.atk1_g = [f'images/Jeu de combat/Aether/Gauche/Attaque1/_a_{i},100.png' for i in range(33)]
        self.images_marche_d = [f'images/Jeu de combat/Aether/Droite/Marche/_a_{i},100.png' for i in range(6)] 
        self.images_marche_g = [f'images/Jeu de combat/Aether/Gauche/Marche/_a_{i},100.png' for i in range(6)]
        self.images_mort = [f'images/Jeu de combat/Aether/Mort/_a_{i},100.png' for i in range(18)] 
        self.inaction_g = [f'images/Jeu de combat/Aether/Gauche/Inaction/_a_{i},100.png' for i in range(12)]
        self.inaction_d = [f'images/Jeu de combat/Aether/Droite/Inaction/_a_{i},100.png' for i in range(12)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.bonus = 0

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 12 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv((-6-self.bonus)*multis*joueur1.get_multis_jeu_combat())
                    print(self.bonus)
                    self.dgt1 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.bonus = 0
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        self.bonus = 0
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2
        self.bonus += 0.25
        print(self.bonus)

class Twilight:
    def __init__(self):
        self.hero = Hero(100,450,8.5,0.15,0.25,5,3,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Twilight/Droite/Attaque1/_a_{i},60.png' for i in range(22)]
        self.atk1_g = [f'images/Jeu de combat/Twilight/Gauche/Attaque1/_a_{i},60.png' for i in range(22)]
        self.images_marche_d = [f'images/Jeu de combat/Twilight/Droite/Marche/_a_{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Twilight/Gauche/Marche/_a_{i},60.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Twilight/Mort/_a_{i},60.png' for i in range(19)] 
        self.inaction_g = [f'images/Jeu de combat/Twilight/Gauche/Inaction/_a_{i},80.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Twilight/Droite/Inaction/_a_{i},80.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and 9 <= int(self.frame) <= 16 and not j2.boss.get_block():
                aie_boss.play()
                j2.boss.modif_pv(-0.60*multis*joueur1.get_multis_jeu_combat())
                j2.boss.set_poison(time.time())
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.165

class Yggdra:
    def __init__(self):
        self.hero = Hero(175,490,5,0.18,0.14,5.5,3,'Esprit')
        self.atk1_d = [f'images/Jeu de combat/Yggdra/Droite/Attaque1/_a_{i},70.png' for i in range(21)]
        self.atk1_g = [f'images/Jeu de combat/Yggdra/Gauche/Attaque1/_a_{i},70.png' for i in range(21)]
        self.images_marche_d = [f'images/Jeu de combat/Yggdra/Droite/Marche/_a_{i},70.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Yggdra/Gauche/Marche/_a_{i},70.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Yggdra/Mort/_a_{i},70.png' for i in range(21)] 
        self.inaction_g = [f'images/Jeu de combat/Yggdra/Gauche/Inaction/_a_{i},80.png' for i in range(7)]
        self.inaction_d = [f'images/Jeu de combat/Yggdra/Droite/Inaction/_a_{i},80.png' for i in range(7)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 9 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-45*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.12

class Suzumebachi:
    def __init__(self):
        self.hero = Hero(150,440,4.5,0.18,0.14,4.3,1000,'Feu')
        self.atk1_d = [f'images/Jeu de combat/Suzumebachi/Droite/Attaque1/_a_{i},60.png' for i in range(26)]
        self.atk1_g = [f'images/Jeu de combat/Suzumebachi/Gauche/Attaque1/_a_{i},60.png' for i in range(26)]
        self.images_marche_d = [f'images/Jeu de combat/Suzumebachi/Droite/Marche/_a_{i},60.png' for i in range(8)] 
        self.images_marche_g = [f'images/Jeu de combat/Suzumebachi/Gauche/Marche/_a_{i},60.png' for i in range(8)]
        self.images_mort = [f'images/Jeu de combat/Suzumebachi/Mort/_a_{i},60.png' for i in range(17)] 
        self.inaction_g = [f'images/Jeu de combat/Suzumebachi/Gauche/Inaction/_a_{i},80.png' for i in range(32)]
        self.inaction_d = [f'images/Jeu de combat/Suzumebachi/Droite/Inaction/_a_{i},80.png' for i in range(32)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.coups = 1

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if j2.boss.get_pv() <= 0:
            self.coups = 0
        elif self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 3 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-3.5*multis*joueur1.get_multis_jeu_combat()-self.coups*1.5)
                    self.dgt1 = True
                    self.coups += 1
            elif self.hero.get_collison() and int(self.frame) == 23 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-15*multis*joueur1.get_multis_jeu_combat()-self.coups*2.5)
                    self.dgt2 = True
                    self.coups +=1
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt2 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            self.coups = 0
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class Dusk:
    def __init__(self):
        self.hero = Hero(180,440,5.5,0.18,0.14,5.3,1.5,'Foudre')
        self.atk1_d = [f'images/Jeu de combat/Dusk/Droite/Attaque1/_a_{i},60.png' for i in range(28)]
        self.atk1_g = [f'images/Jeu de combat/Dusk/Gauche/Attaque1/_a_{i},60.png' for i in range(28)]
        self.images_marche_d = [f'images/Jeu de combat/Dusk/Droite/Marche/_a_{i},60.png' for i in range(6)] 
        self.images_marche_g = [f'images/Jeu de combat/Dusk/Gauche/Marche/_a_{i},60.png' for i in range(6)]
        self.images_mort = [f'images/Jeu de combat/Dusk/Mort/_a_{i},60.png' for i in range(11)] 
        self.inaction_g = [f'images/Jeu de combat/Dusk/Gauche/Inaction/_a_{i},80.png' for i in range(14)]
        self.inaction_d = [f'images/Jeu de combat/Dusk/Droite/Inaction/_a_{i},80.png' for i in range(14)]
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.cd_block_img = 0
        self.atk2 = False
        self.atk2 = False
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False
        self.dgt4 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 4 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-9*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 18 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-10*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True
            elif self.hero.get_collison() and int(self.frame) == 21 and not j2.boss.get_block():
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv(-10*multis*joueur1.get_multis_jeu_combat())
                    self.dgt3 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.dgt3 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        self.hero.set_cp2(False)
        return None
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.2

class MauriceTicket:
    def __init__(self):
        self.hero = Hero(250,480,5.75,0.18,0.1,1.8,0.5,'Neutre')
        self.atk1_d = [f'images/Jeu de combat/MauriceTicket/Droite/Attaque1/_a_frm{i},70.png' for i in range(33,50)]
        self.atk1_g = [f'images/Jeu de combat/MauriceTicket/Gauche/Attaque1/_a_frm{i},70.png' for i in range(33,50)]
        self.images_marche_d = [f'images/Jeu de combat/MauriceTicket/Droite/Marche/_a_frm{i},100.png' for i in range(10,18)] 
        self.images_marche_g = [f'images/Jeu de combat/MauriceTicket/Gauche/Marche/_a_frm{i},100.png' for i in range(10,18)]
        self.cp2_d = [f'images/Jeu de combat/MauriceTicket/Droite/Saut/_a_frm{i},120.png' for i in range(18,21)]
        self.cp2_g = [f'images/Jeu de combat/MauriceTicket/Gauche/Saut/_a_frm{i},120.png' for i in range(18,21)]
        self.inaction_g = [f'images/Jeu de combat/MauriceTicket/Gauche/Inaction/_a_frm{i},130.png' for i in range(10)]
        self.inaction_d = [f'images/Jeu de combat/MauriceTicket/Droite/Inaction/_a_frm{i},130.png' for i in range(10)]
        self.images_mort = [f'images/Jeu de combat/Dusk/Mort/_a_{i},60.png' for i in range(11)] 
        self.image = 'images/Jeu de combat/Hero/Attaque/Attaque_Droite/Attaque1.png'
        self.frame = 0
        self.frame_mort = 0
        self.frame_parade = 0
        self.dgt1 = False
        self.dgt2 = False
        self.dgt3 = False

    def attaque(self,speed:float,sens:str,j2,multis:float):
        '''Permet de jouer l'animation d'attaque du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de l'attaque ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            if self.hero.get_collison() and int(self.frame) == 3 and not j2.boss.get_block():
                if not self.dgt1:
                    aie_boss.play()
                    j2.boss.modif_pv(-12*multis*joueur1.get_multis_jeu_combat())
                    self.dgt1 = True
            elif self.hero.get_collison() and int(self.frame) == 7 and not j2.boss.get_block():
                if not self.dgt2:
                    aie_boss.play()
                    j2.boss.modif_pv(-12*multis*joueur1.get_multis_jeu_combat())
                    self.dgt2 = True
            elif self.hero.get_collison() and int(self.frame) == 13 and not j2.boss.get_block():
                if not self.dgt3:
                    aie_boss.play()
                    j2.boss.modif_pv(-24*multis*joueur1.get_multis_jeu_combat())
                    self.dgt3 = True    
            if self.frame >= len(self.atk1_d)-1:
                self.frame = 0
                self.hero.set_attaque(False)
                self.dgt1 = False
                self.dgt2 = False
                self.dgt3 = False
            elif sens == 'Gauche':
                self.hero.modif_img(self.atk1_g[int(self.frame)])
            elif sens == 'Droite':
                self.hero.modif_img(self.atk1_d[int(self.frame)])
            self.frame += speed

    def mort(self,speed:float,j2):
        '''Permet de jouer l'animation de mort du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - j2 : le boss combattu
        '''
        # Permet d'attendre la fin de l'animation de mort pour mettre fin au combat
        if not self.hero.get_mort():
            # Faire progresser les images pour l'animation
            self.frame_mort += speed
            self.hero.modif_img(self.images_mort[int(self.frame_mort)])
            # Si toutes les images ont été jouées :
            if int(self.frame_mort) == len(self.images_mort)-1:
                # On déclare le boss vainqueur, le combat prend fin
                self.hero.set_mort(True)
                j2.boss.set_victoire(True)
                self.frame_mort = 0

    def marche(self,speed:float,sens:str,j2):
        '''Permet de jouer l'animation de marche du héros.
        Paramètres :
            - speed (float) : la vitesse à laquelle va se jouer l'animation
            - sens (str) : la direction de la marche ('Gauche' ou 'Droite')
            - j2 : le boss combattu
        '''
        # Si toutes les images ont été jouées :
        if not self.hero.get_cp2():
            self.frame += speed
        if int(self.frame) >= len(self.images_marche_d)-1:
            # On remet tout à 0
            self.frame = 0
        # Faire progresser les images pour l'animation
        if sens == 'Gauche':
            self.hero.modif_img(self.images_marche_g[int(self.frame)])
        else:
            self.hero.modif_img(self.images_marche_d[int(self.frame)])

    def cp2(self, speed:float, sens:str, j2,multis:float):
        '''Permet de jouer la compétence 2 du héros.
        Paramètres :
            - speed (float) : la vitesse de l'animation
            - sens (str) : la direction de la compétence ('Gauche' ou 'Droite')
            - j2 : le boss combattu
            - multis (float) : le multiplicateur de dégâts
        '''
        if self.hero.get_pv() > 0:
            self.hero.set_block(True)
            if self.frame < len(self.cp2_d)-1:
                self.hero.modif_pos_y(-8)
                self.frame += speed/1.5
            elif self.frame >= len(self.cp2_d)-1:
                if self.hero.get_pos_y() <= 480:
                    self.hero.modif_pos_y(8)
                else:
                    self.frame = 0
                    self.hero.set_cp2(False)
                    self.hero.set_block(False)
            if sens == 'Gauche':
                self.hero.modif_img(self.cp2_g[int(self.frame)])
            else:
                self.hero.modif_img(self.cp2_d[int(self.frame)])
            
    
    def reset_frame(self):
        '''Permet de remettre le frame à 0'''
        self.frame=0

    def inaction(self,j2):
        '''Permet de jouer l'animation d'inaction du héros.
        Paramètres :
            - j2 : le boss combattu'''
        if int(self.frame) >= len(self.inaction_d)-1:
            # On remet tout à 0
            self.frame = 0
        if distance(self,j2) < 0:
            self.hero.modif_img(self.inaction_d[int(self.frame)])
        else:
            self.hero.modif_img(self.inaction_g[int(self.frame)])
        self.frame += 0.1
