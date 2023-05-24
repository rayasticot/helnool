"""
Boucles qui gèrent tout le fonctionnement d'un niveau.
"""
import time
import random
import helnool_utility as h_ut
import helnool_engine as h_eng
import helnool_entity as h_ent
import helnool_ui as h_ui
import helnool_menus_loop as h_mn
import helnool_gun as h_gu


def safe_level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, checkinput):
    """
    Gère la boucle de jeu du lobby.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le jeu

    level_map :
        Données de la map

    player_pos_x :
        Position du joueur en X
    
    player_pos_y :
        Position du joueur en Y
    
    player_angle :
        L'angle du joueur

    sprint_level :
        Niveau actuel du sprint

    max_sprint_level :
        Valeur maximale du sprint

    sprite_list :
        Liste des sprites
        
    keyboard :
        État du clavier

    config :
        Dictionnaire qui contient les configurations

    get_mouse_move_x :
        Récupère les mouvements de la souris sur l'axe horizontal

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre de l'application

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    loop_music :
        Fonction pour relancer une musique si elle est terminée

    Retourne
    --------
    string :
        Nouveau niveau à charger

    bool :
        Difficulté du nouveau niveau

    """
    delta_time = 0
    while 1:
        t_initial = time.time()
        checkinput(keyboard)
        screen_wall_distance = h_eng.frame(console, write_pixel, level_map, player_pos_x, player_pos_y, player_angle, (238, 240))
        h_eng.drawsprite(console, write_pixel, sprite_list, player_pos_x, player_pos_y, player_angle, screen_wall_distance)
        player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, touch_elevator = h_ent.player(level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, delta_time, keyboard, get_mouse_move_x, config)
        h_ui.sprint_bar_update(console, max_sprint_level, sprint_level, write_pixel)
        if touch_elevator == 1:
            return h_mn.elevator(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, window, checkinput)
        refresh_screen(console, window)
        delta_time = time.time()-t_initial
        if config["limit_fps"]:
            if delta_time < 0.033333:
                time.sleep(0.033333-delta_time)


def level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, timer_value, key_number, key_pool, monster_activate, monster_pos_x, monster_pos_y, monster_speed, path_map, level_id, hard, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput):
    """
    Gère la boucle des niveaux à l'intérieur du bâtiment.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le jeu

    level_map :
        Données de la map

    player_pos_x :
        Position du joueur en X
    
    player_pos_y :
        Position du joueur en Y
    
    player_angle :
        L'angle du joueur

    sprint_level :
        État actuel du sprint

    max_sprint_level :
        Valeur maximale du sprint

    sprite_list :
        Liste des sprites

    timer_value :
        Valeur du temps restant

    key_number :
        Nombre de clés restantes
    
    key_pool :
        Positions des clés dans le niveau

    monster_activate :
        État actuel du monstre (est en train de chasser ou pas)

    monster_pos_x :
        Position actuelle du monstre en X

    monster_pos_y :
        Position actuelle du monstre en Y

    monster_speed :
        Vitesse du monstre dans le niveau actuel

    path_map :
        Carte du niveau dans un format lisible par la libraire pathfinding

    level_id :
        ID du niveau

    hard :
        Mode difficile activé ou non
        
    keyboard :
        État du clavier

    config :
        Dictionnaire qui contient les configurations

    get_mouse_move_x :
        Récupère les mouvements de la souris sur l'axe horizontal

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre de l'application

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    loop_music :
        Fonction pour jouer un fichier audio en boucle

    play_sound :
        Fonction pour jouer un bruitage

    Retourne
    --------
    string :
        Nouveau niveau à charger

    bool :
        Difficulté du nouveau niveau
    """
    music_file = "snd/helnoolarrive.wav"
    music_play_object = play_music(music_file)
    stop_music(music_play_object)
    anim_num = 0

    old_player_pos_x = player_pos_x
    old_player_pos_y = player_pos_y

    delta_time = 0

    while 1:
        t_initial = time.time()
        checkinput(keyboard)
        screen_wall_distance = h_eng.frame(console, write_pixel, level_map, player_pos_x, player_pos_y, player_angle, (238, 240))
        h_eng.drawsprite(console, write_pixel, sprite_list, player_pos_x, player_pos_y, player_angle, screen_wall_distance)
        player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, touch = h_ent.player(level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, delta_time, keyboard, get_mouse_move_x, config)

        if touch == 1 and (key_number == 0) and level_id != 9:
            stop_music(music_play_object)
            if not hard:
                h_ut.save_game("save.yaml", level_id, "completed")
                h_ut.save_game("save.yaml", level_id+1, "unlocked")
            else:
                h_ut.save_game("save.yaml", level_id, "h_completed")
                h_ut.save_game("save.yaml", level_id+1, "h_unlocked")
            return h_mn.elevator(console, keyboard, write_pixel, refresh_screen, play_music, stop_music, loop_music, window, checkinput)

        if touch == 2:
            stop_music(music_play_object)
            play_sound("snd/brise.wav")
            return "map/map_dehors.yaml", hard

        if monster_activate and level_id != 0:
            music_play_object = loop_music(music_play_object, music_file)
            monster_pos_x, monster_pos_y, anim_num, end_game = h_ent.monster(monster_pos_x, monster_pos_y, player_pos_x, player_pos_y, path_map, monster_speed, anim_num, sprite_list, delta_time)
            if end_game:
                stop_music(music_play_object)
                h_mn.brouillage(console, 2, True, write_pixel, refresh_screen, play_music, stop_music, window)
                return "map/map_lobby.yaml", hard

        h_ui.sprint_bar_update(console, max_sprint_level, sprint_level, write_pixel)
        key_number, timer_value, monster_speed = h_ent.key(key_pool, sprite_list, key_number, player_pos_x, player_pos_y, timer_value, monster_speed, play_sound)
        h_ui.ui_update(console, timer_value, key_number, len(key_pool), sprite_list[0][3], write_pixel)

        if timer_value > 0:
            if old_player_pos_x == player_pos_x and old_player_pos_y == player_pos_y:
                pass
            else:
                timer_value -= delta_time
                timer_value = max(timer_value, 0)

        elif not monster_activate:
            monster_activate = True

        refresh_screen(console, window)
        pre_dt = time.time()-t_initial
        if config["limit_fps"]:
            if pre_dt < 0.033333:
                time.sleep(0.033333-pre_dt)
        delta_time = time.time()-t_initial


def outside_level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, monster_pos_x, monster_pos_y, monster_speed, path_map, level_id, hard, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput):
    """
    Gère la boucle du niveau à l'extérieur du bâtiment.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le jeu

    level_map :
        Données de la map

    player_pos_x :
        Position du joueur en X
    
    player_pos_y :
        Position du joueur en Y
    
    player_angle :
        L'angle du joueur

    sprint_level :
        État actuel du sprint

    max_sprint_level :
        Valeur maximale du sprint

    sprite_list :
        Liste des sprites

    timer_value :
        Valeur du temps restant

    key_number :
        Nombre de clés restantes
    
    key_pool :
        Positions des clés dans le niveau

    monster_activate :
        État actuel du monstre (est en train de chasser ou pas)

    monster_pos_x :
        Position actuelle du monstre en X

    monster_pos_y :
        Position actuelle du monstre en Y

    monster_speed :
        Vitesse du monstre dans le niveau actuel

    path_map :
        Carte du niveau dans un format lisible par la libraire pathfinding

    level_id :
        ID du niveau

    hard :
        Mode difficile activé ou non
        
    keyboard :
        État du clavier

    config :
        Dictionnaire qui contient les configurations

    get_mouse_move_x :
        Récupère les mouvements de la souris sur l'axe horizontal

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre de l'application

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    loop_music :
        Fonction pour jouer un fichier audio en boucle

    play_sound :
        Fonction pour jouer un bruitage

    Retourne
    --------
    string :
        Nouveau niveau à charger

    bool :
        Difficulté du nouveau niveau
    """
    delta_time = 0
    monster_activate = False
    monster_life = 1
    anim_num = 0
    last_shoot_time = 0

    music_file = "snd/mince.wav"
    music_play_object = play_music(music_file)
    stop_music(music_play_object)

    height_map = h_ut.loadtexture("map/height.legba")
    while 1:
        t_initial = time.time()
        checkinput(keyboard)
        screen_wall_distance = h_eng.frame_with_height(console, write_pixel, level_map, height_map, player_pos_x, player_pos_y, player_angle, (232, 28))
        h_eng.drawsprite(console, write_pixel, sprite_list, player_pos_x, player_pos_y, player_angle, screen_wall_distance)
        player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, _ = h_ent.player(level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, delta_time, keyboard, get_mouse_move_x, config)
        h_ui.sprint_bar_update(console, max_sprint_level, sprint_level, write_pixel)
        if not monster_activate and h_gu.gun_check_collision(sprite_list[1][0], sprite_list[1][1], player_pos_x, player_pos_y):
            sprite_list[1][5] = -1
            music_play_object = play_music(music_file)
            monster_activate = True
        if monster_activate:
            hit, last_shoot_time = h_gu.gun(console, level_map, player_pos_x, player_pos_y, player_angle, monster_pos_x, monster_pos_y, last_shoot_time, keyboard, write_pixel, play_sound)
            monster_life -= hit
            if monster_life <= 0:
                sprite_list[0][5] = 5
                stop_music(music_play_object)
                if sprite_list[2][0]+0.5 >= player_pos_x >= sprite_list[2][0]-0.5:
                    if sprite_list[2][1]+0.5 >= player_pos_y >= sprite_list[2][1]-0.5:
                        return h_mn.ending(console, hard, keyboard, write_pixel, refresh_screen, play_music, stop_music, window, checkinput)
        if monster_activate and monster_life > 0:
            music_play_object = loop_music(music_play_object, music_file)
            monster_pos_x, monster_pos_y, anim_num, end_game = h_ent.monster(monster_pos_x, monster_pos_y, player_pos_x, player_pos_y, path_map, monster_speed, anim_num, sprite_list, delta_time)
            if end_game:
                h_mn.brouillage(console, 2, True, write_pixel, refresh_screen, play_music, stop_music, window)
                return "map/map_dehors.yaml", hard
        refresh_screen(console, window)
        delta_time = time.time()-t_initial
        if config["limit_fps"]:
            if delta_time < 0.033333:
                time.sleep(0.033333-delta_time)


def level(console, level_file_name, hard, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput):
    """
    Gère le chargement des autres niveaux à l'intérieur du bâtiment.

    Paramètres
    ----------
    console :
        Ecran sur lequel afficher le jeu

    level_file_name :
        Nom du fichier du niveau

    hard :
        Mode difficile activé ou non
    
    keyboard :
        État du clavier

    config :
        Dictionnaire qui contient les configurations

    get_mouse_move_x :
        Récupère les mouvements de la souris sur l'axe horizontal

    write_pixel :
        Fonction pour dessiner des pixels sur l'écran

    refresh_screen :
        Fonction pour rafraîchir l'écran

    window :
        Fenêtre de l'application

    play_music :
        Fonction pour jouer un fichier audio

    stop_music :
        Fonction pour arrêter la lecture d'un fichier audio

    loop_music :
        Fonction pour jouer un fichier audio en boucle

    play_sound :
        Fonction pour jouer un bruitage

    Retourne
    --------
    string :
        Nouveau niveau à charger

    bool :
        Difficulté du nouveau niveau
    """

    map_file = h_ut.loadmap(level_file_name)
    sprite_list = []
    key_list = []
    player_pos_x = map_file["player_spawn_point"]["pos_x"]
    player_pos_y = map_file["player_spawn_point"]["pos_y"]
    player_angle = map_file["player_spawn_point"]["angle"]
    sprint_level = 100.0
    max_sprint_level = 100.0
    key_number = -1
    monster_activate = False
    monster_speed = 0
    monster_pos_x = map_file["monstre_spawn_point"]["pos_x"]
    monster_pos_y = map_file["monstre_spawn_point"]["pos_y"]
    level_map = h_ut.loadtexture(map_file["map_data_file"])
    path_map = h_ut.map2pathmap(map_file["map_data_file"])
    timer_value = map_file["monstre_spawn_time"]

    if map_file["monstre_spawn_time"] == -2:
        monster_speed = map_file["monster_speed_init"]
        sprite_list.append([229, 229, 0, 0, 0, 0])

    elif map_file["monstre_spawn_time"] >= 0:
        key_number = len(map_file["key_pool"])
        monster_speed = map_file["monster_speed_init"]
        sprite_list.append([229, 229, 0, 0, 0, 0])
        for keys in map_file["key_pool"]:
            key = random.randrange(0, len(keys))
            key_list.append(key)
            sprite_list.append([keys[key][0], keys[key][1], 0, 0, 0, 3])

    for spr in map_file["map_spr_list"]:
        sprite_list.append([spr["pos_x"], spr["pos_y"], 0, 0, 0, spr["spr"]])

    if map_file["monstre_spawn_time"] >= 0:
        return level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, timer_value, key_number, map_file["key_pool"], monster_activate, monster_pos_x, monster_pos_y, monster_speed, path_map, map_file["level_id"], hard, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput)
    if map_file["monstre_spawn_time"] == -2:
        return outside_level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, monster_pos_x, monster_pos_y, monster_speed, path_map, map_file["level_id"], hard, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, play_sound, checkinput)
    return safe_level_update(console, level_map, player_pos_x, player_pos_y, player_angle, sprint_level, max_sprint_level, sprite_list, keyboard, config, get_mouse_move_x, write_pixel, refresh_screen, window, play_music, stop_music, loop_music, checkinput)
