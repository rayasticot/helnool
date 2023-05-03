import pygame
import math
import time
import random
import colordata
import yaml

MAP_FILE = "map/map_default.yaml"

SX = 230
SY = 120
FOV = 57.5
HALF_FOV = 28.75

run = True
posx = 32.5
posy = 8.5
angle = 0
k_up, k_dw, k_rg, k_le, k_en, k_sf = 0, 0, 0, 0, 0, 0
scr_dist = [0] * SX
spr_list = [[229, 229, 0, 0, 0, 0], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3]]
cleliste = []
dt = 0

quality = 0
limit_fps = False


def writepixel(screen, color, y, x):
    screen[x, y] = colordata.colorlist[color]


def loadtexture(name):
    f = open(name, "rb")
    data = f.read()
    index = 3
    textu = []
    for col in range(data[1]):
        x_textu = []
        for lin in range(data[0]):
            x_textu.append(data[index-1])
            index += 1
        textu.append(x_textu)
    f.close()
    return tuple(textu)


def loadmap(mapfile):
    with open(mapfile, "r") as f:
        mapfiledata = yaml.safe_load(f)
    return mapfiledata


def update_spr_list(spr_list, mapfile):
    for spri in mapfile["map_spr_list"]:
        spr_list.append([spri["pos_x"], spri["pos_y"], 0, 0, 0, spri["spr"]])


mapfile = loadmap(MAP_FILE)
map = loadtexture(mapfile["map_data_file"])
key_pool = mapfile["key_pool"]
posx = mapfile["player_spawn_point"]["pos_x"]
posy = mapfile["player_spawn_point"]["pos_y"]
monsx = mapfile["monstre_spawn_point"]["pos_x"]
monsy = mapfile["monstre_spawn_point"]["pos_y"]
update_spr_list(spr_list, mapfile)

brique = loadtexture("img/brak.legba")
brique_d = loadtexture("img/brakd.legba")
toile = loadtexture("img/toile.legba")
toile_d = loadtexture("img/toile_d.legba")
labo = loadtexture("img/labo.legba")
labo_d = loadtexture("img/labo_d.legba")
herb = loadtexture("img/herb.legba")
herb_d = loadtexture("img/herb_d.legba")
filet = loadtexture("img/filet.legba")
eye = loadtexture("img/eye.legba")
eye_d = loadtexture("img/eye_d.legba")
keyhole = loadtexture("img/keyhole.legba")
samsung = loadtexture("img/samsung.legba")
samsung_d = loadtexture("img/samsung_d.legba")
concrete = loadtexture("img/concrete.legba")
concrete_d = loadtexture("img/concrete_d.legba")
box = loadtexture("img/box.legba")
box_d = loadtexture("img/box_d.legba")
peur1 = loadtexture("img/mons1.legba")
peur2 = loadtexture("img/mons2.legba")
peur3 = loadtexture("img/mons3.legba")
peur4 = loadtexture("img/mons4.legba")
cle = loadtexture("img/cle.legba")
gun = loadtexture("img/gun.legba")
test = loadtexture("img/test.legba")
text_index = ((brique, brique_d), (toile, toile_d), (herb, herb_d), (filet, filet), (eye, eye_d), (labo, labo_d), (concrete, concrete_d), (box, box_d), (samsung, samsung_d), (keyhole, keyhole))
simp_index = ((160, 124), (223, 180), (238, 237), (249, 239), (70, 71), (160, 124), (223, 180), (238, 237), (249, 239), (70, 71))
sprite_tex_index = (peur1, peur2, peur3, cle, gun, peur4, test)


def frame(screen):
    t1 = time.time()
    global screenpx
    global scr_dist
    linang = (angle+(FOV/2))+0.25
    linang = linang % 360
    for col in range(SX):
        linang -= 0.25
        linang = linang % 360
        dir = [math.cos(math.radians(linang)), math.sin(math.radians(linang))]
        pntx = posx
        pnty = posy
        dist = 0
        side = 0
        while 1:
            pntx += dir[0]
            pnty += dir[1]
            dist += 1
            if map[int(pnty)][int(pntx-dir[0])] != 0:
                break
            if map[int(pnty-dir[1])][int(pntx)] != 0:
                break
            if map[int(pnty)][int(pntx)] != 0:
                break
        dist -= 1
        pntx -= dir[0]
        pnty -= dir[1]
        dir[0] = dir[0]*0.015625
        dir[1] = dir[1]*0.015625
        while 1:
            pntx += dir[0]
            pnty += dir[1]
            dist += 0.015625
            if map[int(pnty)][int(pntx-dir[0])] != 0:
                side = 1
                break
            if map[int(pnty-dir[1])][int(pntx)] != 0:
                side = 0
                break
        fixdist = dist*math.cos(math.radians(linang-angle))
        scr_dist[col] = fixdist
        numrat = round(int(SY*1.5)/fixdist)
        caca = round((SY-numrat)/2)
        if caca == 0:
            caca = 0
        for lin in range(SY):
            if side == 0:
                color = map[int(pnty-dir[1])][int(pntx)]-1
            if side == 1:
                color = map[int(pnty)][int(pntx-dir[0])]-1
            if lin < caca:
                writepixel(screen, 238, lin, col)
                #screen[12].append([lin, col])
            #elif lin == caca:
            #    console.addstr(lin, col, " ", curses.color_pair(0))
            elif lin > numrat+caca:
                writepixel(screen, 240, lin, col)
                #screen[8].append([lin, col])
            #elif lin == numrat+caca:
            #    console.addstr(lin, col, " ", curses.color_pair(0))
            else:
                in_x = 0
                in_y = 0
                pixcolor = 0
                if side == 0:
                    if quality == 0:
                        in_x = round((pnty % 1)*63)
                        in_y = round(((lin-caca)/numrat)*63)
                        pixcolor = text_index[color][0][in_y][in_x]
                    elif quality == 1:
                        pixcolor = simp_index[color][0]
                else:
                    if quality == 0:
                        in_x = round((pntx % 1)*63)
                        in_y = round(((lin-caca)/numrat)*63)
                        pixcolor = text_index[color][1][in_y][in_x]
                    elif quality == 1:
                        pixcolor = simp_index[color][1]
                writepixel(screen, pixcolor, lin, col)
                #screen[pixcolor].append([lin, col])
    t2 = time.time()
    return t2-t1


def drawsprite(screen):
    t1 = time.time()
    sprite_loc_list = spr_list.copy()
    screen_spr_list = []

    for i in range(len(sprite_loc_list)):
        sprite_loc_list[i][3] = (math.sqrt(((sprite_loc_list[i][0]-posx)**2) + ((sprite_loc_list[i][1]-posy)**2)))
    sprite_loc_list = sorted(sprite_loc_list, key=lambda x: - x[3])

    for i in range(len(sprite_loc_list)):
        if sprite_loc_list[i][5] == -1:
            continue
        dify = sprite_loc_list[i][1]-posy
        difx = sprite_loc_list[i][0]-posx
        spr_angle = math.degrees(math.atan(dify/difx))
        if difx < 0:
            spr_angle += 180
        
        dif_angle = angle + 28.75 - spr_angle
        if spr_angle > 270 and angle < 90:
            dif_angle += 360
        if angle > 270 and spr_angle < 90:
            dif_angle -= 360
        sprite_loc_list[i][4] = dif_angle
        
        scale = round(256/sprite_loc_list[i][3])
        #(sprite_dir - player.a)*(fb.w/2)/(player.fov) + (fb.w/2)/2 - sprite_screen_size/2;
        #scr_x = round(((spr_list[i][4]*115)/FOV) + 57.5 - scale/2)
        scr_x = round((sprite_loc_list[i][4] * 4) - scale/2)
        scr_y = round((SY/2) - (scale/2))
        screen_spr_list.append([scr_x, scr_y, scale, sprite_loc_list[i][3], sprite_loc_list[i][5]])
    
    for sprite in screen_spr_list:
        for col in range(sprite[2]):
            for lin in range(sprite[2]):
                if lin+sprite[1] in range(SY) and col+sprite[0] in range(SX):
                    if sprite[3] < scr_dist[col+sprite[0]]:
                        tex_y = round((col/sprite[2])*63)
                        tex_x = round((lin/sprite[2])*63)
                        pixcolor = sprite_tex_index[sprite[4]][tex_x][tex_y]
                        if pixcolor == 201:
                            continue
                        writepixel(screen, pixcolor, lin+sprite[1], col+sprite[0])
    t2 = time.time()
    return t2-t1


def init_keys():
    global cleliste
    for i in range(len(key_pool)):
        cle = random.randrange(0, len(key_pool[i]))
        cleliste.append(cle)
        spr_list[i+1][0] = key_pool[i][cle][0]
        spr_list[i+1][1] = key_pool[i][cle][1]


def player(screen):
    t1 = time.time()
    global angle
    global posx
    global posy
    global spr_list
    
    sprintcoef = 1
    if k_sf == 1:
        sprintcoef = 2
    pdir = (math.cos(math.radians(angle))*3*dt*sprintcoef, math.sin(math.radians(angle))*3*dt*sprintcoef)
    if k_le == 1:
        angle += 90*dt
    if k_rg == 1:
        angle -= 90*dt
    if k_dw == 1:
        posx -= pdir[0]
        posy -= pdir[1]
        if map[int(posy)][int(posx)] > 0:
            posx += pdir[0]
            posy += pdir[1]
    if k_up == 1:
        posx += pdir[0]
        posy += pdir[1]
        if map[int(posy)][int(posx)] > 0:
            posx -= pdir[0]
            posy -= pdir[1]
    angle = angle % 360
    t2 = time.time()
    return t2-t1


def checkinput():
    global run
    global k_up
    global k_dw
    global k_rg
    global k_le
    global k_en
    global k_sf
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                k_le = 1
            if event.key == pygame.K_RIGHT:
                k_rg = 1
            if event.key == pygame.K_UP:
                k_up = 1
            if event.key == pygame.K_DOWN:
                k_dw = 1
            if event.key == pygame.K_SPACE:
                k_en = 1
            if event.key == pygame.K_LSHIFT:
                k_sf = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                k_le = 0
            if event.key == pygame.K_RIGHT:
                k_rg = 0
            if event.key == pygame.K_UP:
                k_up = 0
            if event.key == pygame.K_DOWN:
                k_dw = 0
            if event.key == pygame.K_SPACE:
                k_en = 0
            if event.key == pygame.K_LSHIFT:
                k_sf = 0


def main():
    global dt
    global k_en
    pygame.init()
    window = pygame.display.set_mode((SX, SY))

    rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
    pixel_array = pygame.PixelArray(window)
    window.fill(0)

    init_keys()

    """
    low = 100
    high = 0
    tot = 0
    avg_c = 0
    """

    while run == True:
        ti = time.time()
        t = 0
        checkinput()
        t += frame(pixel_array)
        t += drawsprite(pixel_array)
        #drawscreen(console)
        t += player(pixel_array)
        
        if k_en == 1:
            print("")
            print("Pos x : "+str(posx))
            print("Pos y : "+str(posy))
            print("Angle : "+str(angle))
            k_en = 0

        pygame.display.flip()
        if limit_fps == True:
            if(t < 0.033333):
                time.sleep(0.033333-t)
        dt = time.time()-ti


if __name__ == "__main__":
    main()