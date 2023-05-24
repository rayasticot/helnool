"""
Fonctions pour gérer la partie graphique du jeu.
"""
import math
import helnool_constants as h_co
import helnool_texture as h_tex

def ray_cast(map_data, ray_angle, startpoint_x, startpoint_y):
    """
    Trace un rayon sur une map à partir d'une position et d'un angle.

    Paramètres
    ----------
    map_data :
        Données de la map sur lequel tracer le rayon

    ray_angle :
        Angle du rayon en degrées

    startpoint_x :
        Position X de départ du rayon

    startpoint_y :
        Position Y de départ du rayon

    Retourne
    --------
    float :
        Longueur du rayon

    int :
        Coté sur du mur sur lequel le rayon a touché

    float :
        Position X où le rayon a touché

    float :
        Position Y où le rayon a touché

    int :
        Index de la texture du mur touché par le rayon

    """
    INITIAL_TRAVEL = 1
    PRECISION = 20
    direction = (math.cos(math.radians(ray_angle)), math.sin(math.radians(ray_angle)))
    position_x = startpoint_x
    position_y = startpoint_y
    distance = 0
    side = 0
    for i in range(0, PRECISION):
        travel_distance = INITIAL_TRAVEL/(2**i)
        while 1:
            position_x += direction[0]*travel_distance
            position_y += direction[1]*travel_distance
            distance += travel_distance
            if map_data[int(position_y)][int(position_x-(direction[0]*travel_distance))] != 0:
                side = 1
                break
            if map_data[int(position_y-(direction[1]*travel_distance))][int(position_x)] != 0:
                side = 0
                break
            if i != PRECISION-1:
                if map_data[int(position_y)][int(position_x)] != 0:
                    break
        distance -= travel_distance
        position_x -= direction[0]*travel_distance
        position_y -= direction[1]*travel_distance

    distance += travel_distance
    if side == 0:
        position_x += direction[0]*travel_distance
    else:
        position_y += direction[1]*travel_distance

    texture_hit = map_data[int(position_y)][int(position_x)]-1

    return distance, side, position_x, position_y, texture_hit


def find_pixel_color(pixel_height, hit_position_x, hit_position_y, side, texture, wall_start, wall_size, total_wall, height_multiplier, floor_color):
    """
    Détermine la couleur d'un pixel à l'écran.

    Paramètres
    ----------
    pixel_height :
        Hauteur du pixel à déterminer

    hit_position_x :
        Position X où le rayon a touché

    hit_position_y :
        Position Y où le rayon a touché

    side :
        Côté du mur que le rayon a touché

    texture :
        Texture du mur que le rayon a touché

    wall_start :
        Hauteur où le mur doit commencer à être dessiné

    wall_size :
        Taille du mur à dessiner

    total_wall :
        Hauteur où le mur arrête d'être dessiné

    height_multiplier :
        Nombre de mur en hauteur à dessiner

    floor_color :
        Couleur du sol et du plafond

    Retourne
    --------
    int:
        couleur du pixel à dessiner

    """
    if pixel_height < wall_start:
        return floor_color[0]
    if pixel_height > total_wall:
        return floor_color[1]

    texture_x = 0
    texture_y = 0
    pixel_color = 0
    if side == 0:
        texture_x = round((hit_position_y % 1)*63)
    else:
        texture_x = round((hit_position_x % 1)*63)

    texture_y = round(((pixel_height-wall_start)/wall_size)*(63*height_multiplier))%64

    if texture == 10 and height_multiplier != 1:
        if (((pixel_height-wall_start)/wall_size)*(63*height_multiplier))/64 <= 10:
            pixel_color = h_tex.text_index[0][side][texture_y][texture_x]
    if pixel_color == 0:
        pixel_color = h_tex.text_index[texture][side][texture_y][texture_x]

    return pixel_color


def frame(console, write_pixel, map_data, pos_x, pos_y, angle, floor_color):
    """
    Dessine une frame sans différence de hauteur des murs

    Paramètres
    ----------
    console :
        Écran sur lequel dessiner la frame

    write_pixel :
        Fonction pour dessiner des pixels

    map_data :
        Données de la map

    pos_x :
        Position X de la camera

    pos_y :
        Position Y de la camera

    angle :
        Angle de la caméra

    floor_color :
        Couleur du sol et du plafond

    Retourne
    --------
    tuple :
        Distance du mur à chaque colonne de l'écran

    """
    scr_dist = []
    linang = (angle+(h_co.FOV/2))+0.25
    linang = linang % 360
    for col in range(h_co.SX):
        linang -= 0.25
        linang %= 360
        distance, side, hit_position_x, hit_position_y, texture_hit = ray_cast(map_data, linang, pos_x, pos_y)

        fix_distance = distance*math.cos(math.radians(linang-angle))
        scr_dist.append(fix_distance)
        wall_size = round(int(h_co.SY*1.5)/fix_distance)
        wall_start = round((h_co.SY-wall_size)/2)

        for lin in range(h_co.SY):
            pixel_color = find_pixel_color(lin, hit_position_x, hit_position_y, side, texture_hit, wall_start, wall_size, wall_start+wall_size, 1, floor_color)
            write_pixel(console, pixel_color, lin, col)
    return tuple(scr_dist)


def frame_with_height(console, write_pixel, map_data, height_map, pos_x, pos_y, angle, floor_color):
    """
    Dessine une frame avec différence de hauteur des murs

    Paramètres
    ----------
    console :
        Écran sur lequel dessiner la frame

    write_pixel :
        Fonction pour dessiner des pixels

    map_data :
        Données de la map

    height_map :
        Données de hauteur de la map

    pos_x :
        Position X de la camera

    pos_y :
        Position Y de la camera

    angle :
        Angle de la caméra

    floor_color :
        Couleur du sol et du plafond

    Retourne
    --------
    tuple :
        Distance du mur à chaque colonne de l'écran

    """
    scr_dist = []
    linang = (angle+(h_co.FOV/2))+0.25
    linang = linang % 360
    for col in range(h_co.SX):
        linang -= 0.25
        linang = linang % 360
        distance, side, hit_position_x, hit_position_y, texture_hit = ray_cast(map_data, linang, pos_x, pos_y)

        fix_distance = distance*math.cos(math.radians(linang-angle))
        scr_dist.append(fix_distance)

        if side == 0:
            height_multiplier = height_map[int(hit_position_y)][int(hit_position_x)]
        if side == 1:
            height_multiplier = height_map[int(hit_position_y)][int(hit_position_x)]
        if height_multiplier == 0:
            height_multiplier = 1

        wall_size = round(int(h_co.SY*1.5*height_multiplier)/fix_distance)
        ground_wall_size = round(int(h_co.SY*1.5)/fix_distance)
        wall_start = round((h_co.SY-wall_size)/2)
        ground_wall_start = round((h_co.SY-ground_wall_size)/2)

        for lin in range(h_co.SY):
            pixel_color = find_pixel_color(lin, hit_position_x, hit_position_y, side, texture_hit, wall_start, wall_size, ground_wall_start+ground_wall_size, height_multiplier, floor_color)
            write_pixel(console, pixel_color, lin, col)
    return tuple(scr_dist)


def drawsprite(console, write_pixel, sprite_list, pos_x, pos_y, angle, scr_dist):
    """
    Dessine les sprites présents sur la map à l'écran

    Paramètres
    ----------
        console :
            Écran sur lequel dessiner les sprites

        write_pixel :
            Fonction pour dessiner des pixels

        sprite_list :
            Liste des sprites à dessiner

        pos_x :
            Position X de la caméra

        pos_y :
            Position Y de la caméra

        angle :
            Angle de la caméra

        scr_dist :
            Distance du mur à chaque colonne de l'écran

    """
    sprite_loc_list = sprite_list.copy()
    screen_spr_list = []

    for i, _ in enumerate(sprite_loc_list):
        sprite_loc_list[i][3] = (math.sqrt(((sprite_loc_list[i][0]-pos_x)**2) + ((sprite_loc_list[i][1]-pos_y)**2)))
    sprite_loc_list = sorted(sprite_loc_list, key=lambda x: - x[3])

    for i, _ in enumerate(sprite_loc_list):
        if sprite_loc_list[i][5] == -1:
            continue
        dify = sprite_loc_list[i][1]-pos_y
        difx = sprite_loc_list[i][0]-pos_x
        spr_angle = math.degrees(math.atan(dify/difx))
        if difx < 0:
            spr_angle += 180

        dif_angle = angle + h_co.HALF_FOV - spr_angle
        if spr_angle > 270 and angle < 90:
            dif_angle += 360
        if angle > 270 and spr_angle < 90:
            dif_angle -= 360
        sprite_loc_list[i][4] = dif_angle

        scale = round(256/sprite_loc_list[i][3])
        #(sprite_dir - player.a)*(fb.w/2)/(player.fov) + (fb.w/2)/2 - sprite_screen_size/2;
        #scr_x = round(((spr_list[i][4]*115)/FOV) + 57.5 - scale/2)
        scr_x = round((sprite_loc_list[i][4] * 4) - scale/2)
        scr_y = round((h_co.SY/2) - (scale/2))
        screen_spr_list.append([scr_x, scr_y, scale, sprite_loc_list[i][3], sprite_loc_list[i][5]])

    for sprite in screen_spr_list:
        if sprite[2] > 400:
            continue
        for col in range(sprite[2]):
            for lin in range(sprite[2]):
                if lin+sprite[1] in range(h_co.SY) and col+sprite[0] in range(h_co.SX):
                    if sprite[3] < scr_dist[col+sprite[0]]:
                        tex_y = round((col/sprite[2])*63)
                        tex_x = round((lin/sprite[2])*63)
                        pixcolor = h_tex.sprite_tex_index[sprite[4]][tex_x][tex_y]
                        if pixcolor == 201:
                            continue
                        write_pixel(console, pixcolor, lin+sprite[1], col+sprite[0])
