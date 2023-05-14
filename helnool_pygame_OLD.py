import pygame
import math
import time
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import colordata

SX = 230
SY = 120
FOV = 57.5
HALF_FOV = 28.75
DEFAULT_posx = 32.5
DEFAULT_posy = 8.5
DEFAULT_monx = 42
DEFAULT_mony = 10
DEFAULT_angle = 0
DEFAULT_sprintlevel = 100
DEFAULT_maxsprintlevel = 100
DEFAULT_monsterspeed = 7
DEFAULT_monsteractivate = False
DEFAULT_key_number = 0
DEFAULT_cleliste = []
DEFAULT_isgun = False

currentmusic = 0
run = True
posx = 32.5
posy = 8.5
monx = 42
mony = 10
oldpx = 229
oldpy = 229
chemin = []
mon_index = 0
angle = 0
k_up, k_dw, k_rg, k_le, k_en, k_sf = 0, 0, 0, 0, 0, 0
scr_dist = [0] * SX
spr_list = [[monx, mony, 0, 0, 0, 0], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3], [229, 229, 0, 0, 0, 3], [59.5, 44.5, 0, 0, 0, 4]]
key_pool = (
    ((50.5, 35.5), (50.5, 5.5)),
    ((27.5, 6.5),),
    ((5.5, 20.5), (6.5, 17.5), (4.5, 11.5), (10.5, 29.5)),
    ((23.5, 24.5), (22.5, 12.5), (35.5, 24.5), (30.5, 17.5))
    )
monstre_spawn = (
    ((60.5, 2.5), (60.5, 2.5)),
    ((37.5, 31.5),),
    ((14.5, 23.5), (14.5, 23.5), (14.5, 23.5), (14.5, 23.5)),
    ((23.5, 24.5), (40.5, 34.5), (14.5, 8.5), (14.5, 34.5))
)
key_number = 0
dt = 0
sprintlevel = 100
maxsprintlevel = 100
anim_num = 0
monsterspeed = 7
monsteractivate = False
cleliste = []
isgun = False
endingstart = False
endingtime = 0
guntimer = 0

quality = 0
limit_fps = True
difficulty = 1
MONSTER_SPEEDS = (10, 8, 7)


def writepixel(screen, color, y, x):
    screen[x, y] = colordata.colorlist[color]


def createimage(screen, name, y, x):
    global screenpx
    f = open(name, "rb")
    data = f.read()
    index = 3
    for col in range(data[1]):
        if col+y >= SY:
            break
        for lin in range(data[0]):
            index += 1
            if lin+x >= SX:
                continue
            if data[index-1] == 201:
                continue
            writepixel(screen, data[index-1], col+y, lin+x)
    f.close()


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


def map2pathmap(name):
    pathmap = list(loadtexture(name))
    for i in range(len(pathmap)):
        for j in range(len(pathmap[i])):
            if pathmap[i][j] > 0:
                pathmap[i][j] = 0
            else:
                pathmap[i][j] = 1
    return tuple(pathmap)


map = loadtexture("img/map.legba")
path = map2pathmap("img/map.legba")
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
text_index = ((brique, brique_d), (toile, toile_d), (herb, herb_d), (filet, filet), (eye, eye_d), (labo, labo_d), (concrete, concrete_d), (box, box_d), (samsung, samsung_d), (keyhole, keyhole))
simp_index = ((160, 124), (223, 180), (238, 237), (249, 239), (70, 71), (160, 124), (223, 180), (238, 237), (249, 239), (70, 71))
sprite_tex_index = (peur1, peur2, peur3, cle, gun, peur4)

pygame.mixer.init()
key_sound = pygame.mixer.Sound("snd/cle.wav")
shot_sound = pygame.mixer.Sound("snd/shot.wav")


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
    global sprintlevel
    global maxsprintlevel
    global monsteractivate
    global monx
    global mony
    global spr_list
    global ganiou_play
    global ganiouproche_play
    
    sprintcoef = 1
    if k_sf == 1:
        sprintcoef = 2
        if sprintlevel > 0:
            sprintlevel -= 1
        elif maxsprintlevel > 0:
            maxsprintlevel -= 2
        else:
            sprintcoef = 1
    else:
        if sprintlevel < maxsprintlevel:
            sprintlevel += 0.25
    pdir = (math.cos(math.radians(angle))*3*dt*sprintcoef, math.sin(math.radians(angle))*3*dt*sprintcoef)
    if k_le == 1:
        angle += 90*dt
    if k_rg == 1:
        angle -= 90*dt
    if k_dw == 1:
        posx -= pdir[0]
        posy -= pdir[1]
        if map[int(posy)][int(posx)] > 0 and (map[int(posy)][int(posx)] < 10 or key_number < 4):
            posx += pdir[0]
            posy += pdir[1]
    if k_up == 1:
        posx += pdir[0]
        posy += pdir[1]
        if map[int(posy)][int(posx)] > 0 and (map[int(posy)][int(posx)] < 10  or key_number < 4):
            posx -= pdir[0]
            posy -= pdir[1]
    angle = angle % 360
    if int(posx) == 54 and int(posy) == 40 and spr_list[0][5] != 5:
        if monsteractivate == True:
            pygame.mixer.music.stop()
        monsteractivate = False
        monx = 49.5
        mony = 40.5
        spr_list[0][0] = monx
        spr_list[0][1] = mony
        spr_list[0][5] = 2
    t2 = time.time()
    return t2-t1


def sprintbarupdate(screen):
    t1 = time.time()
    for i in range(round(maxsprintlevel)):
        if sprintlevel >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            writepixel(screen, couleur, SY-i_b-1, i)
    t2 = time.time()
    return t2-t1


def key():
    global key_number
    global monsteractivate
    global monsterspeed
    global monx
    global mony
    t1 = time.time()
    for i in range(len(key_pool)):
        if spr_list[i+1][5] == -1:
            continue
        if posx > spr_list[i+1][0]-0.5 and posx < spr_list[i+1][0]+0.5:
            if posy > spr_list[i+1][1]-0.5 and posy < spr_list[i+1][1]+0.5:
                pygame.mixer.Sound.play(key_sound)
                spr_list[i+1][5] = -1
                key_number += 1
                if monsteractivate == False:
                    monx = monstre_spawn[i][cleliste[i]][0]
                    mony = monstre_spawn[i][cleliste[i]][1]
                    monsteractivate = True
                monsterspeed -= 1
    t2 = time.time()
    return t2-t1


def resetvalues():
    global posx
    global posy
    global monx
    global mony
    global angle
    global sprintlevel
    global maxsprintlevel
    global monsterspeed
    global monsteractivate
    global key_number
    global cleliste
    global spr_list
    global isgun
    for i in range(len(key_pool)):
        spr_list[i+1][5] = 3
    posx = DEFAULT_posx
    posy = DEFAULT_posy
    monx = DEFAULT_monx
    mony = DEFAULT_mony
    angle = DEFAULT_angle
    sprintlevel = DEFAULT_sprintlevel
    maxsprintlevel = DEFAULT_maxsprintlevel
    monsterspeed = DEFAULT_monsterspeed
    monsteractivate = DEFAULT_monsteractivate
    key_number = DEFAULT_key_number
    cleliste = DEFAULT_cleliste
    spr_list[0][0] = DEFAULT_monx
    spr_list[0][1] = DEFAULT_mony
    isgun = DEFAULT_isgun
    init_keys()


def gameover(screen):
    pygame.mixer.music.stop()
    createimage(screen, "img/dead.legba", 0, 0)
    pygame.display.flip()
    while run == True:
        checkinput()
        if k_en == 1:
            resetvalues()
            break


def monster(screen):
    t1 = time.time()
    global monx
    global mony
    global mon_index
    global chemin
    global path
    global oldpx
    global oldpy
    global ganiou_play
    global ganiouproche_play
    global anim_num
    global currentmusic

    if int(oldpx) != int(posx) or int(oldpy) != int(posy):
        oldpx = posx
        oldpy = posy
        grid = Grid(matrix=path)
        start = grid.node(int(monx), int(mony))
        end = grid.node(int(posx), int(posy))

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        paths, runs = finder.find_path(start, end, grid)
        chemin = paths
        mon_index = 1
    
    if spr_list[0][3] < 8:
        if currentmusic == 1:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("snd/ganiou_proche.wav")
            pygame.mixer.music.play(-1)
            currentmusic = 0
    elif spr_list[0][3] < 16 and spr_list[0][3] >= 8:
        if currentmusic == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("snd/ganiou.wav")
            pygame.mixer.music.play(-1)
            currentmusic = 1
    else:
        pygame.mixer.music.stop()
    
    mondir = ((chemin[int(mon_index/monsterspeed)][0]+0.5)-monx, (chemin[int(mon_index/monsterspeed)][1]+0.5)-mony)
    monx += mondir[0]/monsterspeed
    mony += mondir[1]/monsterspeed
    
    spr_list[0][0] = monx
    spr_list[0][1] = mony
    mon_index += 1
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

    if posx > monx-1 and posx < monx+1:
        if posy > mony-1 and posy < mony+1:
            gameover(screen)

    t2 = time.time()
    return t2-t1


def gun(screen):
    global isgun
    global k_en
    global shot
    global shot_play
    global ganiouend_play
    global spr_list
    global endingstart
    global endingtime
    global guntimer
    if isgun == False:
        if posx > spr_list[5][0]-1 and posx < spr_list[5][0]+1:
            if posy > spr_list[5][1]-1 and posy < spr_list[5][1]+1:
                isgun = True
                spr_list[5][5] = -1
                pygame.mixer.music.load("snd/ganiou_end.wav")
                pygame.mixer.music.play(-1)
    if isgun == True:
        createimage(screen, "img/aim.legba", 60, 75)
        if endingstart == True:
            if time.time()-endingtime >= 5:
                pygame.mixer.music.stop()
                return True
        if guntimer > 0:
            guntimer -= 1
        if k_en == 1 and guntimer == 0:
            k_en = 0
            pygame.mixer.Sound.play(shot_sound)
            guntimer = 20

            dir = [math.cos(math.radians(angle)), math.sin(math.radians(angle))]
            pntx = posx
            pnty = posy
            dist = 0
            side = 0
            hit = False
            while 1:
                pntx += dir[0]
                pnty += dir[1]
                dist += 0.25
                if map[int(pnty)][int(pntx)] != 0:
                    break
                if pntx > monx-0.5 and pntx < monx+0.5:
                    if pnty > mony-0.5 and pnty < mony+0.5:
                        hit = True
                        break
        
            if hit == True:
                spr_list[0][5] = 5
                endingstart = True
                endingtime = time.time()
    return False


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


def title(screen):
    pygame.mixer.music.load("snd/helpeur.wav")
    pygame.mixer.music.play(-1)
    createimage(screen, "img/title.legba", 0, 0)
    createimage(screen, "img/t0.legba", 9, 2)
    pygame.display.flip()
    frameindex = 1
    while run == True:
        if quality == 0:
            createimage(screen, f"img/t{frameindex}.legba", 9, 2)
            pygame.display.flip()
            time.sleep(0.03333)
            checkinput()
            frameindex += 1
            if frameindex == 5:
                frameindex = 0
        if k_en == 1:
            pygame.mixer.music.stop()
            break


def intro(screen):
    global k_en
    pygame.mixer.music.load("snd/lettre.wav")
    pygame.mixer.music.play(-1)
    createimage(screen, "img/h0.legba", 0, 0)
    pygame.display.flip()
    k_en = 0
    while run == True:
        checkinput()
        if k_en == 1:
            break
    createimage(screen, "img/h1.legba", 0, 0)
    pygame.display.flip()
    k_en = 0
    while run == True:
        checkinput()
        if k_en == 1:
            pygame.mixer.music.stop()
            break


def brouillage(screen):
    pygame.mixer.music.load("snd/brouille.wav")
    pygame.mixer.music.play()
    t1 = time.time()
    while time.time()-t1 < 6 and run == True:
        checkinput()
        for col in range(SY):
            for lin in range(SX):
                pixcolor = random.randrange(231, 255)
                writepixel(screen, pixcolor, col, lin)
        pygame.display.flip()


def ecranfin(screen):
    createimage(screen, "img/victoire.legba", 0, 0)
    pygame.display.flip()
    k_en = 0
    while k_en == 0 and run == True:
        checkinput()


def main():
    global dt
    global monsterspeed
    pygame.init()
    window = pygame.display.set_mode((SX, SY))

    rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))
    pixel_array = pygame.PixelArray(window)
    window.fill(0)

    monsterspeed = MONSTER_SPEEDS[difficulty]
    
    title(pixel_array)
    intro(pixel_array)
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
        if isgun == False:
            t += sprintbarupdate(pixel_array)
        t += key()
        if monsteractivate == True:
            t += monster(pixel_array)
        if gun(pixel_array) == True:
            break
        """
        if t > high:
            high = t
        if t < low:
            low = t
        tot += t
        avg_c += 1
        console.addstr(121, 0, str(round(1/t, 3))+" FPS")
        console.addstr(122, 0, "MAX "+str(round(1/low, 3))+" FPS")
        console.addstr(123, 0, "MIN "+str(round(1/high, 3))+" FPS")
        console.addstr(124, 0, "AVG "+str(round(1/(tot/avg_c), 3))+" FPS")
        """
        pygame.display.flip()
        if limit_fps == True:
            if(t < 0.033333):
                time.sleep(0.033333-t)
        dt = time.time()-ti
    
    if run == True:
        brouillage(pixel_array)
        ecranfin(pixel_array)


if __name__ == "__main__":
    main()