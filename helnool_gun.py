"""
Fonctions pour gérer l'interaction avec le fusil.
"""
import math
import time
import helnool_utility as h_ut

def gun_check_collision(gunx, guny, posx, posy):
    """
    Vérifie s'il y a une collision entre le fusil et une position donnée.

    Paramètres
    ----------
    gunx :
        Coordonnée X du fusil

    guny :
        Coordonnée Y du fusil

    posx :
        Coordonnée X de la position à vérifier

    posy :
        Coordonnée Y de la position à vérifier

    Retourne
    --------
    bool :
        True si une collision est détectée, False sinon.
    """
    delta_x = gunx-posx
    delta_y = guny-posy
    if math.sqrt(delta_x**2 + delta_y**2) <= 1:
        return True
    return False


def shoot_bullet(level_map, posx, posy, angle, monx, mony):
    """
    Effectue un tir de balle à partir d'une position donnée dans une direction donnée.

    Paramètres
    ----------
    level_map :
        Carte du niveau

    posx :
        Coordonnée X de la position de départ du tir

    posy :
        Coordonnée Y de la position de départ du tir

    angle :
        Angle du tir en degrés

    monx :
        Coordonnée X du monstre

    mony :
        Coordonnée Y du monstre

    Retourne
    --------
    int
        0 si la balle n'a pas atteint de cible, 1 sinon.
    """
    direction = (math.cos(math.radians(angle))*0.25, math.sin(math.radians(angle))*0.25)
    pntx = posx
    pnty = posy
    while 1:
        pntx += direction[0]
        pnty += direction[1]
        if level_map[int(pnty)][int(pntx)] != 0:
            return 0
        delta_x = pntx-monx-0.5
        delta_y = pnty-mony-0.5
        if math.sqrt(delta_x**2 + delta_y**2) <= 5:
            return 1


def gun(console, level_map, posx, posy, angle, monx, mony, last_shoot_time, keyboard, write_pixel, play_sound):
    """
    Gère le fusil du joueur.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le fusil

    level_map :
        Carte du niveau

    posx :
        Coordonnée X de la position du joueur

    posy :
        Coordonnée Y de la position du joueur

    angle :
        Angle de rotation du joueur

    monx :
        Coordonnée X du monstre

    mony :
        Coordonnée Y du monstre

    last_shoot_time :
        Temps du dernier tir effectué

    keyboard :
        État du clavier

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    play_sound :
        Fonction pour jouer un son

    Retourne
    --------
    int :
        Indique si le tir a touché

    float :
        Dernier temps du tir
    """
    h_ut.createimage(console, write_pixel, "img/aim.legba", 60, 75)
    if keyboard["k_en"] == 1 and time.time()-last_shoot_time > 0.75:
        keyboard["k_en"] = 0
        play_sound("snd/shot.wav")
        last_shoot_time = time.time()

        return shoot_bullet(level_map, posx, posy, angle, monx, mony), last_shoot_time
    return 0, last_shoot_time
