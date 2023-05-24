"""
Fonctions qui gèrent les différents menus/écrans du jeu.
"""
import time
import random
import yaml
import helnool_utility as h_ut
import helnool_constants as h_co

def ending(console, hard, keyboard, write_pixel, refresh_screen, play_music, stop_music, window, checkinput):
    """
    Gère l'écran de fin de jeu.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le message de fin

    hard :
        Indicateur du mode de difficulté (True si difficulté élevée, False sinon)

    keyboard :
        État du clavier

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    window :
        Fenêtre du jeu

    checkinput :
        Fonction pour vérifier l'état du clavier

    Retourne
    --------
    string :
        Nouvelle map à charger
    bool :
        Difficulté de la map
    """
    if not hard:
        h_ut.save_game("save.yaml", 9, "completed")
        h_ut.createimage(console, write_pixel, "img/endgame.legba", 0, 0)
    else:
        h_ut.save_game("save.yaml", 9, "h_completed")
        h_ut.createimage(console, write_pixel, "img/endgamehard.legba", 0, 0)
    refresh_screen(console, window)

    while 1:
        checkinput(keyboard)
        if keyboard["k_en"] == 1:
            brouillage(console, 0.25, False, write_pixel, refresh_screen, play_music, stop_music, window)
            return "map/map_lobby.yaml", hard


def brouillage(console, seconds, helnool, write_pixel, refresh_screen, play_music, stop_music, window):
    """
    Génère un effet de brouillage sur l'écran pendant un certain nombre de secondes.

    Paramètres
    ----------
    console :
        Ecran sur lequel appliquer l'effet de brouillage

    seconds :
        Nombre de secondes pendant lesquelles l'effet de brouillage est appliqué

    helnool :
        Indicateur de présence de "helnool" sur l'écran (True pour afficher "helnool", False sinon)

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    window :
        Fenêtre du jeu
    """
    music_play_object = play_music("snd/brouille.wav")
    t1 = time.time()
    while time.time()-t1 < seconds:
        for col in range(h_co.SY):
            for lin in range(h_co.SX):
                pixel_color = random.randrange(231, 255)
                write_pixel(console, pixel_color, col, lin)
        if helnool:
            h_ut.createimage(console, write_pixel, "img/helnool.legba", 0, 55)
        refresh_screen(console, window)
    stop_music(music_play_object)


def create_check_elevator(console, sauvegarde, hard, write_pixel):
    """
    Crée les images des coches de progression et des rubans adhésifs pour les niveaux de l'ascenseur.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher les coches de progression et les rubans adhésifs

    sauvegarde :
        Données de sauvegarde contenant l'état de progression des niveaux

    hard :
        Indicateur du mode de difficulté (True si difficulté élevée, False sinon)

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran
    """
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)

    for i, _ in enumerate(sauvegarde):
        if hard:
            complete = sauvegarde[i]["h_completed"]
            unlocked = sauvegarde[i]["h_unlocked"]
        else:
            complete = sauvegarde[i]["completed"]
            unlocked = sauvegarde[i]["unlocked"]
        if complete:
            h_ut.createimage(console, write_pixel, "img/check.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))]+73)

        if not unlocked:
            h_ut.createimage(console, write_pixel, "img/warning.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))])

    if not sauvegarde[9]["completed"]:
        h_ut.createimage(console, write_pixel, "img/heltape.legba", 98, XPOS[0])


def move_elevator_arrow(keyboard, sauvegarde, arrow_index):
    """
    Gère le déplacement de la flèche de sélection de niveau de l'ascenseur.

    Paramètres
    ----------
    keyboard :
        État du clavier

    sauvegarde :
        Données de sauvegarde contenant l'état de progression des niveaux

    arrow_index :
        Index de la flèche de sélection

    Retourne
    --------
    int :
        Nouvelle index de la flèche de sélection

    int :
        Position x du sprite de la flèche

    int :
        Position y du sprite de la flèche
    """
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)

    if keyboard["k_up"] == 1:
        keyboard["k_up"] = 0
        arrow_index += 1

    if keyboard["k_dw"] == 1:
        keyboard["k_dw"] = 0
        arrow_index -= 1

    if keyboard["k_rg"] == 1:
        keyboard["k_rg"] = 0
        arrow_index += len(YPOS)

    if keyboard["k_le"] == 1:
        keyboard["k_le"] = 0
        arrow_index -= len(YPOS)

    if sauvegarde[9]["completed"]:
        arrow_index %= len(XPOS)*len(YPOS)+1
    else:
        arrow_index %= len(XPOS)*len(YPOS)

    if arrow_index == 10:
        arrow_sprite_x = XPOS[0]
        arrow_sprite_y = 93
    else:
        arrow_sprite_x = XPOS[int(arrow_index/len(YPOS))]
        arrow_sprite_y = YPOS[arrow_index%len(YPOS)]

    return arrow_index, arrow_sprite_x, arrow_sprite_y


def elevator(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, window, checkinput):
    """
    Gère l'écran de l'ascenseur permettant de choisir un niveau.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher l'écran de l'ascenseur

    keyboard :
        État du clavier

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    play_music :
        Fonction pour jouer de la musique

    stop_music :
        Fonction pour arrêter la musique

    loop_music :
        Fonction pour gérer la boucle de lecture de la musique

    window :
        Fenêtre de l'application

    checkinput :
        Fonction pour vérifier l'état du clavier

    Retourne
    --------
    string :
        Nouveau niveau à charger

    bool :
        Difficulté du niveau
    """
    arrow_index = 1
    brouillage(console, 0.25, False, write_pixel, refresh_screen, play_music, stop_music, window)

    with open("save.yaml", "r", encoding="utf8") as file_data:
        sauvegarde = yaml.safe_load(file_data)
    with open("levels.yaml", "r", encoding="utf8") as file_data:
        levels = yaml.safe_load(file_data)
    with open("levels_hard.yaml", "r", encoding="utf8") as file_data:
        levels_hard = yaml.safe_load(file_data)

    music_file = "snd/ascenseur.wav"
    music_play_object = play_music(music_file)

    hard = False

    while 1:
        checkinput(keyboard)
        music_play_object = loop_music(music_play_object, music_file)
        arrow_index, arrow_sprite_x, arrow_sprite_y = move_elevator_arrow(keyboard, sauvegarde, arrow_index)

        if not hard:
            h_ut.createimage(console, write_pixel, "img/elevatorbg.legba", 0, 0)
        else:
            h_ut.createimage(console, write_pixel, "img/elevatorburnbg.legba", 0, 0)

        create_check_elevator(console, sauvegarde, hard, write_pixel)

        if keyboard["k_en"] == 1:
            brouillage(console, 0.25, False, write_pixel, refresh_screen, play_music, stop_music, window)
            if arrow_index == 10:
                stop_music(music_play_object)
                hard = not hard
                if hard:
                    music_file = "snd/ascenseurfeu.wav"
                    music_play_object = play_music(music_file)
                else:
                    music_file = "snd/ascenseur.wav"
                    music_play_object = play_music(music_file)
            elif not hard and sauvegarde[arrow_index]["unlocked"]:
                stop_music(music_play_object)
                return levels[arrow_index], False
            elif hard and sauvegarde[arrow_index]["h_unlocked"]:
                stop_music(music_play_object)
                return levels_hard[arrow_index], True

        h_ut.createimage(console, write_pixel, "img/arrow.legba", arrow_sprite_y, arrow_sprite_x-21)
        refresh_screen(console, window)


def title(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, window, checkinput):
    """
    Affiche l'écran du titre du jeu.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher l'écran du titre

    keyboard :
        État du clavier

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    play_music :
        Fonction pour jouer de la musique

    stop_music :
        Fonction pour arrêter la musique

    loop_music :
        Fonction pour gérer la boucle de lecture de la musique

    window :
        Fenêtre de l'application

    checkinput :
        Fonction pour vérifier le clavier

    """
    music_file = "snd/helpeur.wav"
    music_play_object = play_music("snd/helpeur.wav")
    h_ut.createimage(console, write_pixel, "img/title.legba", 0, 0)
    h_ut.createimage(console, write_pixel, "img/t0.legba", 9, 2)
    refresh_screen(console, window)
    frameindex = 1
    while 1:
        checkinput(keyboard)
        h_ut.createimage(console, write_pixel, f"img/t{frameindex}.legba", 9, 2)
        refresh_screen(console, window)
        time.sleep(0.03333)
        frameindex += 1
        if frameindex == 5:
            frameindex = 0
        music_play_object = loop_music(music_play_object, music_file)
        if keyboard["k_en"] == 1:
            stop_music(music_play_object)
            break
