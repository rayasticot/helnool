"""
Fonctions pour gérer l'affichage tête haute.
"""
import helnool_utility as h_ut
import helnool_constants as h_co

def sprint_bar_update(console, max_sprint_level, sprint_level, write_pixel):
    """
    Met à jour et dessine la barre de sprint

    Paramètres
    ----------
    console :
        Ecran sur lequel dessiner la barre

    max_sprint_level :
        Niveau de sprint maximal

    sprint_level :
        Niveau de sprint

    write_pixel :
        Fonction pour dessiner des pixels

    """
    for i in range(round(max_sprint_level)):
        if sprint_level >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            write_pixel(console, couleur, h_co.SY-i_b-1, i)


def seconds_to_minutes(time_seconds):
    """
    Transforme du temps en secondes en format
    minutes, secondes

    Paramètres
    ----------
    time_seconds :
        Temps en secondes

    Retourne
    --------
    int:
        Temps en minutes
    int:
        Temps en secondes
    
    """
    left_minutes = int(time_seconds/60)
    left_seconds = int(time_seconds%60)
    return left_minutes, left_seconds


def create_digit_sprite(console, minutes, seconds, write_pixel):
    """
    Crée les chiffres pour l'affichage du temps

    Paramètres
    ----------
    console :
        Ecran sur lequel dessiner le sprite

    minutes :
        Minutes du temps

    seconds :
        Secondes du temps

    write_pixel :
        Fonction pour dessiner des pixels

    """
    DIGIT_SIZE = 8
    FIRST_DIGIT_POS = 206
    DIGIT_POSY = 107
    WHITE = 231
    BLACK = 232
    YELLOW = 226
    RED = 160

    chiffre_texture = h_ut.loadtexture("img/chiffre.legba")

    digit_color = WHITE
    if minutes == 0 and seconds <= 15:
        digit_color = RED
    elif minutes == 0 and seconds <= 30:
        digit_color = YELLOW

    for i in range(3):
        if i == 0:
            digit = minutes
        elif i == 2:
            digit = int(seconds%10)
        else:
            digit = int(seconds/10)
        for col in range(12):
            for lin in range(8):
                if chiffre_texture[col][lin+(digit*DIGIT_SIZE)] == 201:
                    continue
                write_pixel(console, digit_color, col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i))
    write_pixel(console, BLACK, DIGIT_POSY+4, FIRST_DIGIT_POS+8)
    write_pixel(console, BLACK, DIGIT_POSY+9, FIRST_DIGIT_POS+8)


def create_key_numbers(console, key_number, total_keys, write_pixel):
    """
    Crée les chiffres du nombre de clés collectées

    Paramètres
    ----------
    console :
        Ecran sur lequel dessiner les chiffres

    key_number :
        Nombre de clés collectées

    total_keys :
        Nombre total de clés

    write_pixel :
        Fonction pour dessiner des pixels

    """
    DIGIT_SIZE = 8
    FIRST_DIGIT_POS = 206
    DIGIT_POSY = -2

    chiffre_texture = h_ut.loadtexture("img/chiffre.legba")
    slash_texture = h_ut.loadtexture("img/slash.legba")

    for i in range(3):
        if i == 0:
            digit = total_keys-key_number
        elif i == 2:
            digit = total_keys
        if i != 1:
            for col in range(12):
                for lin in range(8):
                    if chiffre_texture[col][lin+(digit*DIGIT_SIZE)] == 201:
                        continue
                    write_pixel(console, 231, col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i))
        else:
            for col in range(13):
                for lin in range(8):
                    if slash_texture[col][lin] == 201:
                        continue
                    write_pixel(console, 231, col+DIGIT_POSY+1, lin+FIRST_DIGIT_POS+(8*i))


def create_hand(console, monster_distance, write_pixel):
    """
    Crée l'image de la main en fonction de la distance du monstre

    Paramètres
    ----------
    console :
        Ecran sur lequel dessiner l'image de la main

    monster_distance :
        Distance du monstre

    write_pixel :
        Fonction pour dessiner des pixels

    """
    if monster_distance > 16:
        h_ut.createimage(console, write_pixel, "img/handgood.legba", 0, 0)
    elif monster_distance > 8:
        h_ut.createimage(console, write_pixel, "img/handmid.legba", 0, 0)
    else:
        h_ut.createimage(console, write_pixel, "img/handbad.legba", 0, 0)


def ui_update(console, timer_value, key_number, total_keys, monster_distance, write_pixel):
    """
    Met à jour l'interface utilisateur

    Paramètres
    ----------
    console :
        Ecran de l'interface utilisateur

    timer_value :
        Valeur du chronomètre en secondes

    key_number :
        Nombre de clés collectées

    total_keys :
        Nombre total de clés

    monster_distance :
        Distance du monstre

    write_pixel :
        Fonction pour dessiner des pixels

    """
    minutes, seconds = seconds_to_minutes(timer_value)
    create_digit_sprite(console, minutes, seconds, write_pixel)
    create_key_numbers(console, key_number, total_keys, write_pixel)
    create_hand(console, monster_distance, write_pixel)
