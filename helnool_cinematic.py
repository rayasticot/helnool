"""
Fonctions pour gérer les cinématiques du jeu.
"""
import time
import yaml
import helnool_engine as h_en
import helnool_utility as h_ut


def engine_cinematic(console, file_name, write_pixel, refresh_screen, window):
    """
    Exécute une cinématique à partir d'un fichier YAML.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher la cinématique

    file_name :
        Chemin du fichier YAML contenant les informations de la cinématique

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre d'affichage

    """
    with open(file_name, encoding="utf-8") as file_data:
        cinematic_info = yaml.safe_load(file_data)

    with open(cinematic_info["map_file_name"], encoding="utf-8") as file_data:
        map_file = yaml.safe_load(file_data)

    spr_list = []
    for sprite in map_file["map_spr_list"]:
        spr_list.append([sprite["pos_x"], sprite["pos_y"], 0, 0, 0, sprite["spr"]])
    actor_index = len(spr_list)
    actor_dir = []
    for actor in cinematic_info["actors"]:
        spr_list.append([actor[0]["pos_x"], actor[0]["pos_y"], 0, 0, 0, actor[0]["spr"]])
        delta_pos_x = actor[1]["pos_x"]-actor[0]["pos_x"]
        delta_pos_y = actor[1]["pos_y"]-actor[0]["pos_y"]
        actor_dir.append((delta_pos_x, delta_pos_y))
    actor_dir = tuple(actor_dir)

    map_data = h_ut.loadtexture(map_file["map_data_file"])
    if cinematic_info["height"]:
        height_map = h_ut.loadtexture("map/height.legba")

    cam_x = cinematic_info["cam"][0]["pos_x"]
    cam_y = cinematic_info["cam"][0]["pos_y"]
    cam_angle = cinematic_info["cam"][0]["angle"]
    cam_dir = (
        cinematic_info["cam"][1]["pos_x"]-cinematic_info["cam"][0]["pos_x"],
        cinematic_info["cam"][1]["pos_y"]-cinematic_info["cam"][0]["pos_y"],
    )
    elapsed_time = 0
    delta_time = 0

    while 1:
        t_initial = time.time()
        if cinematic_info["height"]:
            screen_dist = h_en.frame_with_height(console, write_pixel, map_data, height_map, cam_x, cam_y, cam_angle, (81, 28))
        else:
            screen_dist = h_en.frame(console, write_pixel, map_data, cam_x, cam_y, cam_angle, (238, 240))

        h_en.drawsprite(console, write_pixel, spr_list, cam_x, cam_y, cam_angle, screen_dist)

        for i in range(len(cinematic_info["actors"])):
            initial_pos_x = cinematic_info["actors"][i][0]["pos_x"]
            initial_pos_y = cinematic_info["actors"][i][0]["pos_y"]
            spr_list[actor_index+i][0] = initial_pos_x + actor_dir[i][0]*(elapsed_time/cinematic_info["time"])
            spr_list[actor_index+i][1] = initial_pos_y + actor_dir[i][1]*(elapsed_time/cinematic_info["time"])

            spr_list[actor_index+i][5] =  cinematic_info["actors_frame"][i+1][int(elapsed_time/cinematic_info["actors_frame"][0]["frequency"])%len(cinematic_info["actors_frame"][i+1])]

        cam_x = cinematic_info["cam"][0]["pos_x"] + cam_dir[0]*(elapsed_time/cinematic_info["time"])
        cam_y = cinematic_info["cam"][0]["pos_y"] + cam_dir[1]*(elapsed_time/cinematic_info["time"])

        refresh_screen(console, window)
        delta_time = time.time()-t_initial
        elapsed_time += delta_time
        if elapsed_time >= cinematic_info["time"]:
            break


def play_small_cinematic(console, write_pixel, refresh_screen, window):
    """
    Joue la petite cinématique.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher la cinématique

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre d'affichage

    """
    engine_cinematic(console, "cine/cine_lobby5.yaml", write_pixel, refresh_screen, window)
    engine_cinematic(console, "cine/cine_lobby6.yaml", write_pixel, refresh_screen, window)


def play_full_cinematic(console, write_pixel, refresh_screen, window):
    """
    Joue la cinématique complète.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher la cinématique

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre d'affichage

    """
    for i in range(5):
        engine_cinematic(console, "cine/cine_outside" + str(i+1) + ".yaml", write_pixel, refresh_screen, window)
    for i in range(4):
        engine_cinematic(console, "cine/cine_lobby" + str(i+1) + ".yaml", write_pixel, refresh_screen, window)

    play_small_cinematic(console, write_pixel, refresh_screen, window)
