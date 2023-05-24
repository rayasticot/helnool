"""
Fonctions pour gérer les différentes entités présentes
dans le jeu. (joueur, monstre)
"""
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import helnool_utility as h_ut


def player(map_data, pos_x, pos_y, angle, sprint_level, max_sprint_level, delta_time, keyboard, get_mouse_move_x, config):
    """
    Fonction pour mettre à jour le joueur.

    Paramètres
    ----------
    map_data :
        Données de la map

    pos_x :
        Position x du joueur

    pos_y :
        Position y du joueur

    angle :
        Angle du joueur

    sprint_level :
        Valeur d'endurance du joueur

    max_sprint_level :
        Valeur maximale d'endurance du joueur

    delta_time :
        Temps écoulé lors de la dernière frame

    keyboard :
        Boutons du clavier si ils sont appuyés

    get_mouse_move_x :
        Fonction pour récupérer la quantité de mouvement
        de la souris

    config :
        Données de configuration du jeu

    Retourne
    --------
    float:
        Position x du joueur mise à jour

    float:
        Position y du joueur mise à jour

    float:
        Angle du joueur mise à jour

    float:
        Valeur d'endurance du joueur mise à jour

    float:
        Valeur maximale d'endurance du joueur mise à jour

    int:
        Nombre qui indique si le joueur a touché
        un mur particulier

    """
    sprintcoef = 1
    touch = 0
    if keyboard["k_sf"] == 1 and (keyboard["k_up"] == 1 or keyboard["k_dw"] == 1):
        sprintcoef = 2
        if sprint_level > 0:
            sprint_level -= 1*delta_time*30
        elif max_sprint_level > 0:
            max_sprint_level -= 2*delta_time*30
        else:
            sprintcoef = 1
    else:
        if sprint_level < max_sprint_level:
            sprint_level += 0.25*delta_time*30

    pdir = (math.cos(math.radians(angle)), math.sin(math.radians(angle)))
    rdir = (math.cos(math.radians(angle+90)), math.sin(math.radians(angle+90)))

    if config["mouse_mode"] == 1:
        mouse_move_x = get_mouse_move_x()
        angle -= mouse_move_x*0.025*config["sensibility"]
    else:
        if keyboard["k_rg"] == 1:
            angle -= 90*delta_time*config["sensibility"]
        if keyboard["k_le"] == 1:
            angle += 90*delta_time*config["sensibility"]

    add_x, add_y = 0, 0

    if keyboard["k_dw"] == 1:
        add_x -= pdir[0]
        add_y -= pdir[1]
    if keyboard["k_up"] == 1:
        add_x += pdir[0]
        add_y += pdir[1]
    if keyboard["k_rg"] == 1 and config["mouse_mode"] == 1:
        add_x -= rdir[0]
        add_y -= rdir[1]
    if keyboard["k_le"] == 1 and config["mouse_mode"] == 1:
        add_x += rdir[0]
        add_y += rdir[1]

    add_x, add_y = h_ut.normalize((add_x, add_y))
    add_x *= 2.6*delta_time*sprintcoef
    add_y *= 2.6*delta_time*sprintcoef

    pos_x += add_x
    pos_y += add_y

    if map_data[int(pos_y)][int(pos_x)] == 10:
        touch = 1
    elif map_data[int(pos_y)][int(pos_x)] == 19:
        touch = 2
    if map_data[int(pos_y)][int(pos_x)] > 0:
        pos_x -= add_x
        pos_y -= add_y

    angle = angle % 360

    return pos_x, pos_y, angle, sprint_level, max_sprint_level, touch


def follow_path(path, pos_x, pos_y, distance):
    """
    Fait suivre un chemin à un point.

    Paramètres
    ----------
    path :
        Chemin à suivre

    pos_x :
        Position x du point

    pos_y :
        Position y du point

    distance :
        Distance à parcourir

    Retourne
    --------
    int:
        Position x du point mise à jour

    int:
        Position y du point mise à jour

    bool:
        Si le point est à une distance de moins de
        1 unité de son objectif.

    """
    delta_x = path[1][0]-pos_x
    delta_y = path[1][1]-pos_y
    distance_to_first = math.sqrt(delta_x**2 + delta_y**2)
    if distance_to_first >= distance:
        dir_vector_x, dir_vector_y = h_ut.normalize((delta_x, delta_y))
        dir_vector_x *= distance
        dir_vector_y *= distance
        return pos_x+dir_vector_x, pos_y+dir_vector_y, False

    distance -= distance_to_first
    try:
        delta_x = path[2][0]-path[1][0]
        delta_y = path[2][1]-path[1][1]

        dir_vector_x, dir_vector_y = h_ut.normalize((delta_x, delta_y))
        dir_vector_x *= distance
        dir_vector_y *= distance
        return path[1][0]+dir_vector_x, path[1][1]+dir_vector_y, False
    except IndexError:
        return pos_x, pos_y, True


def monster(mon_x, mon_y, pos_x, pos_y, path_map, monster_speed, anim_num, spr_list, delta_time):
    """
    Fonction pour mettre à jour le monstre.

    Paramètres
    ----------

    mon_x :
        Position x du monstre

    mon_y :
        Position y du monstre

    pos_x :
        Position x du joueur

    pos_y :
        Position y du joueur

    path_map :
        Map sous format adapté à la librairie Pathfinding

    monster_speed :
        Vitesse du monstre

    anim_num :
        Index de l'animation du monstre

    spr_list :
        Liste des sprites

    delta_time :
        Temps écoulé depuis la dernière frame

    Retourne
    --------

    float:
        Position x du monstre mise à jour

    float:
        Position y du monstre mise à jour

    int:
        Index de l'animation du monstre mise à jour

    bool:
        Si le monstre à atteint le joueur

    """
    end_game = False
    grid = Grid(matrix=path_map)
    start = grid.node(int(mon_x), int(mon_y))
    end = grid.node(int(pos_x), int(pos_y))

    finder = AStarFinder()
    paths, _ = finder.find_path(start, end, grid)

    mon_x, mon_y, end_game = follow_path(paths, mon_x, mon_y, (1/monster_speed)*26*delta_time)

    spr_list[0][0] = mon_x+0.5
    spr_list[0][1] = mon_y+0.5
    anim_num += 1
    anim_num = anim_num % 16
    if anim_num > 11:
        spr_list[0][5] = 1
    elif anim_num > 7:
        spr_list[0][5] = 2
    elif anim_num > 3:
        spr_list[0][5] = 0
    else:
        spr_list[0][5] = 2


    if mon_x+1 > pos_x > mon_x-1:
        if mon_y+1 > pos_y > mon_y-1:
            end_game = True


    return mon_x, mon_y, anim_num, end_game


def key(key_pool, spr_list, key_number, pos_x, pos_y, timer_value, monster_speed, play_sound):
    """
    Fonction pour mettre à jour les clés.

    Paramètres
    ----------
    key_pool :
        Liste des clés de la map

    spr_list :
        Liste des sprites

    key_number :
        Nombre de clés

    pos_x :
        Position x du joueur

    pos_y :
        Position y du joueur

    timer_value :
        Valeur du timer

    monster_speed :
        Vitesse du monstre

    play_sound :
        Joue un effet sonore

    Retourne
    --------
    int:
        Nombre de clés mise à jour

    int:
        Valeur du temps mise à jour

    int:
        Vitesse du monstre mise à jour

    """
    for i in range(len(key_pool)):
        if spr_list[i+1][5] == -1:
            continue
        if spr_list[i+1][0]+0.5 > pos_x > spr_list[i+1][0]-0.5:
            if spr_list[i+1][1]+0.5 > pos_y > spr_list[i+1][1]-0.5:
                play_sound("snd/cle.wav")
                spr_list[i+1][5] = -1
                key_number -= 1
                if key_number == 0:
                    timer_value = 0
                else:
                    timer_value = timer_value/2
                monster_speed -= 1
    return key_number, timer_value, monster_speed
