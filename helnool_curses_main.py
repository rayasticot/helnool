"""
Module à lancer pour jouer au jeu avec Curses dans le terminal
"""
import curses
import simpleaudio as sa
import pynput.keyboard
from pynput.mouse import Controller
import yaml
import helnool_menus_loop as h_mn
import helnool_constants as h_co
import helnool_cinematic as h_ci
import helnool_level_loop as h_lv


def write_pixel(console, color, y, x):
    """
    Dessine un pixel à l'écran

    Paramètres
    ----------
    console :
        Écran sur lequel dessiner le pixel
    color :
        Couleur à dessiner
    y :
        Position y du pixel
    x :
        Position x du pixel
    """
    console.addch(y, x, " ",curses.color_pair(color))


def refresh_screen(console, window):
    """
    Affiche la nouvelle frame à l'écran

    Paramètres
    ----------
    console :
        Écran à raffraichir
    window :
        Inutile dans curses, mais on doit le conserver
        pour faire fonctionner la fonction avec le reste
        des modules
    """
    console.refresh()


def play_music(music_file):
    """
    Joue une musique

    Paramètres
    ----------
    music_file :
        Fichier audio à jouer

    Retourne
    --------
    sa.PlayObject :
        Objet qui gère la musique
    """
    music = sa.WaveObject.from_wave_file(music_file)
    music_play = music.play()
    
    return music_play


def stop_music(music_play_object):
    """
    Arrête la musique

    Paramètres
    ----------
    music_play_object :
        Objet de la musique à arrêter
    """
    music_play_object.stop()


def loop_music(music_play_object, music_file):
    """
    Relance une musique si elle est terminée.

    Paramètres
    ----------
    music_play_object :
        Objet de la musique à relancer
    music_file :
        Fichier de la musique

    Retourne
    --------
    sa.PlayObject :
        Objet qui gère la musique
    """
    if not music_play_object.is_playing():
        music = sa.WaveObject.from_wave_file(music_file)
        music_play_object = music.play()
    return music_play_object


def play_sound(sound_file):
    """
    Joue un effet sonore.

    Paramètres
    ----------
    sound_file :
        Fichier du son à jouer
    """
    sound = sa.WaveObject.from_wave_file(sound_file)
    sound_play = sound.play()


def create_on_press(keyboard):
    """
    Crée une fonction permettant de gérer lorsqu'une
    touche du clavier est appuyée.

    Paramètres
    ----------
    keyboard :
        Dictionnaire du clavier.

    Retourne
    --------
    function :
        Fonction qui gère lorsqu'une touche est
        appuyée.
    """
    def on_press(key):
        try:
            if key.char == "w" or key.char == "W":
                keyboard["k_up"] = 1
            elif key.char == "s" or key.char == "S":
                keyboard["k_dw"] = 1
            elif key.char == "d" or key.char == "D":
                keyboard["k_rg"] = 1
            elif key.char == "a" or key.char == "A":
                keyboard["k_le"] = 1
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                keyboard["k_en"] = 1
            elif key == pynput.keyboard.Key.shift:
                keyboard["k_sf"] = 1
            elif key == pynput.keyboard.Key.up:
                keyboard["k_up"] = 1
            elif key == pynput.keyboard.Key.down:
                keyboard["k_dw"] = 1
            elif key == pynput.keyboard.Key.right:
                keyboard["k_rg"] = 1
            elif key == pynput.keyboard.Key.left:
                keyboard["k_le"] = 1
            elif key == pynput.keyboard.Key.esc:
                keyboard["k_es"] = 1
    return on_press


def create_on_release(keyboard):
    """
    Crée une fonction permettant de gérer lorsqu'une
    touche du clavier est relachée.

    Paramètres
    ----------
    keyboard :
        Dictionnaire du clavier.

    Retourne
    --------
    function :
        Fonction qui gère lorsqu'une touche est
        relachée.
    """
    def on_release(key):
        try:
            if key.char == "w" or key.char == "W":
                keyboard["k_up"] = 0
            elif key.char == "s" or key.char == "S":
                keyboard["k_dw"] = 0
            elif key.char == "d" or key.char == "D":
                keyboard["k_rg"] = 0
            elif key.char == "a" or key.char == "A":
                keyboard["k_le"] = 0
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                keyboard["k_en"] = 0
            elif key == pynput.keyboard.Key.shift:
                keyboard["k_sf"] = 0
            elif key == pynput.keyboard.Key.up:
                keyboard["k_up"] = 0
            elif key == pynput.keyboard.Key.down:
                keyboard["k_dw"] = 0
            elif key == pynput.keyboard.Key.right:
                keyboard["k_rg"] = 0
            elif key == pynput.keyboard.Key.left:
                keyboard["k_le"] = 0
            elif key == pynput.keyboard.Key.esc:
                keyboard["k_es"] = 0
    return on_release


def get_mouse_move_x():
    """
    Récupère le mouvement de la souris
    lors d'une frame.

    Retourne
    --------
    int :
        Quantité de mouvement x de la souris
    """
    mouse = Controller()
    mouse_move_x = mouse.position[0]-800
    mouse.position = (800, 400)
    return mouse_move_x


def checkinput(keyboard):
    """
    Ne fait rien dans curses.
    """
    pass # Pas utile dans curses


def main(console):
    """
    Fonction principale du jeu.

    Paramètre
    ---------
    console :
        Fenêtre de l'écran du jeu
    """
    scr_size = console.getmaxyx()
    if scr_size[0] < h_co.SY or scr_size[1] < h_co.SX:
        curses.endwin()
        print(f"Votre terminal doit avoir une résolution d'au moins {h_co.SX} de largeur par {h_co.SY} de hauteur.")
        print(f"Votre résolution actuelle est de {scr_size[1]} de largeur par {scr_size[0]} de hauteur.")
        exit()

    console.clear()
    console.nodelay(True)
    curses.noecho()
    curses.curs_set(0)

    for i in range(255):
        curses.init_pair(i+1, 0, i+1)

    keyboard = {
        "k_up": 0,
        "k_dw": 0,
        "k_le": 0,
        "k_rg": 0,
        "k_en": 0,
        "k_sf": 0,
        "k_es": 0
    }

    with open("settings.yaml", encoding="utf8") as file_data:
        config = yaml.safe_load(file_data)

    listener = pynput.keyboard.Listener(on_press=create_on_press(keyboard), on_release=create_on_release(keyboard))
    listener.start()

    h_mn.title(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, None, checkinput)
    h_mn.brouillage(console, 0.25, False, write_pixel, refresh_screen, play_music, stop_music, None)

    with open("save.yaml") as f:
        savedata = yaml.safe_load(f)
        if savedata[0]["completed"] == True or savedata[2]["completed"] == True:
            h_ci.play_small_cinematic(console, write_pixel, refresh_screen, None)
        else:
            h_ci.play_full_cinematic(console, write_pixel, refresh_screen, None)

    new_level = "map/map_lobby.yaml"
    hard = False

    while 1:
        new_level, hard = h_lv.level(console, new_level, hard, keyboard, config["settings_curses"], get_mouse_move_x, write_pixel, refresh_screen, None, play_music, stop_music, loop_music, play_sound, checkinput)


if __name__ == "__main__":
    curses.wrapper(main)
