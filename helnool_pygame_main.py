"""
Module à lancer pour jouer au jeu avec Pygame
"""
import pygame
import yaml
import helnool_menus_loop as h_mn
import helnool_constants as h_co
import helnool_cinematic as h_ci
import helnool_level_loop as h_lv
import colordata


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
    console[x, y] = colordata.colorlist[color]


def scale_and_show(pixel_array, surface):
    """
    Étire l'écran et l'applique à une surface.

    Paramètres
    ----------
    pixel_array :
        Écran du jeu
    surface :
        Surface sur laquelle appliquer l'écran
    """
    scaled_size = (h_co.SX * h_co.WINDOW_SCALE, h_co.SY * h_co.WINDOW_SCALE)
    
    scaled_surface = pygame.transform.scale(pixel_array.surface, scaled_size)

    surface.blit(scaled_surface, (0, 0))


def refresh_screen(console, window):
    """
    Affiche la nouvelle frame à l'écran

    Paramètres
    ----------
    console :
        Écran à raffraichir
    window :
        Fenêtre du jeu
    """
    scale_and_show(console, window)
    pygame.display.flip()


def play_music(music_file):
    """
    Joue une musique

    Paramètres
    ----------
    music_file :
        Fichier audio à jouer
    """
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)


def stop_music(music_play_object):
    """
    Arrête la musique

    Paramètres
    ----------
    music_play_object :
        Objet de la musique à arrêter
        Pas utilisé ici
    """
    pygame.mixer.music.stop()


def loop_music(music_play_object, music_file):
    """
    Relance une musique si elle est terminée.

    Paramètres
    ----------
    music_play_object :
        Objet de la musique à relancer
        Pas utilisé ici
    music_file :
        Fichier de la musique
    """
    if not pygame.mixer.music.get_busy():
        play_music(music_file)


def play_sound(sound_file):
    """
    Joue un effet sonore.

    Paramètres
    ----------
    sound_file :
        Fichier du son à jouer
    """
    sound = pygame.mixer.Sound(sound_file)
    pygame.mixer.Sound.play(sound)


def checkinput(keyboard):
    """
    Récupère les entrées du clavier.

    Paramètres
    ----------
    keyboard :
        Le clavier et l'information des touches appuyés
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keyboard["run"] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                keyboard["k_le"] = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                keyboard["k_rg"] = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                keyboard["k_up"] = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                keyboard["k_dw"] = 1
            if event.key == pygame.K_SPACE:
                keyboard["k_en"] = 1
            if event.key == pygame.K_LSHIFT:
                keyboard["k_sf"] = 1
            if event.key == pygame.K_ESCAPE:
                keyboard["k_es"] = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                keyboard["k_le"] = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                keyboard["k_rg"] = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                keyboard["k_up"] = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                keyboard["k_dw"] = 0
            if event.key == pygame.K_SPACE:
                keyboard["k_en"] = 0
            if event.key == pygame.K_LSHIFT:
                keyboard["k_sf"] = 0
            if event.key == pygame.K_ESCAPE:
                keyboard["k_es"] = 0


def get_mouse_move_x():
    """
    Récupère le mouvement de la souris
    lors d'une frame.

    Retourne
    --------
    int :
        Quantité de mouvement x de la souris
    """
    return pygame.mouse.get_rel()[0]


def main():
    """
    Fonction principale du jeu.
    """
    pygame.init()

    window = pygame.display.set_mode((230*h_co.WINDOW_SCALE, 120*h_co.WINDOW_SCALE))
    console = pygame.PixelArray(pygame.Surface((230, 120)))

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

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

    h_mn.title(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, window, checkinput)
    h_mn.brouillage(console, 0.25, False, write_pixel, refresh_screen, play_music, stop_music, window)

    with open("save.yaml") as f:
        savedata = yaml.safe_load(f)
        if savedata[0]["completed"] == True or savedata[2]["completed"] == True:
            h_ci.play_small_cinematic(console, write_pixel, refresh_screen, window)
        else:
            h_ci.play_full_cinematic(console, write_pixel, refresh_screen, window)

    new_level = "map/map_lobby.yaml"
    hard = False

    while 1:
        new_level, hard = h_lv.level(console, new_level, hard, keyboard, config["settings_pygame"], get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput)


if __name__ == "__main__":
    main()
