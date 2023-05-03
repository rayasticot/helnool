import curses
import math
import time
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pynput import keyboard
import simpleaudio as sa

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
    ((40.5, 34.5), (40.5, 34.5), (14.5, 8.5), (14.5, 34.5))
)
key_number = 0
dt = 0
sprintlevel = 100
maxsprintlevel = 100
anim_num = 0
monsterspeed = 8
monsteractivate = False
cleliste = []
isgun = False
endingstart = False
endingtime = 0

quality = 0
limit_fps = True
difficulty = 1
MONSTER_SPEEDS = (10, 8, 7)


def on_press(key):
    global k_up
    global k_dw
    global k_rg
    global k_le
    global k_en
    global k_sf
    if key == keyboard.Key.up:
        k_up = 1
    elif key == keyboard.Key.down:
        k_dw = 1
    elif key == keyboard.Key.right:
        k_rg = 1
    elif key == keyboard.Key.left:
        k_le = 1
    elif key == keyboard.Key.space:
        k_en = 1
    elif key == keyboard.Key.shift:
        k_sf = 1

 
def on_release(key):
    global k_up
    global k_dw
    global k_rg
    global k_le
    global k_en
    global k_sf
    if key == keyboard.Key.up or key == "w":
        k_up = 0
    elif key == keyboard.Key.down or key == "s":
        k_dw = 0
    elif key == keyboard.Key.right:
        k_rg = 0
    elif key == keyboard.Key.left:
        k_le = 0
    elif key == keyboard.Key.space:
        k_en = 0
    elif key == keyboard.Key.shift:
        k_sf = 0


def createimage(console, name, y, x):
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
            console.addch(col+y, lin+x, " ", curses.color_pair(data[index-1]))
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

ganiouproche = sa.WaveObject.from_wave_file("snd/ganiou_proche.wav")
ganiou = sa.WaveObject.from_wave_file("snd/ganiou.wav")
ganiouend = sa.WaveObject.from_wave_file("snd/ganiou_end.wav")
cle = sa.WaveObject.from_wave_file("snd/cle.wav")
shot = sa.WaveObject.from_wave_file("snd/shot.wav")
ganiouproche_play = ganiouproche.play()
ganiouproche_play.stop()
ganiou_play = ganiou.play()
ganiou_play.stop()
ganiouend_play = ganiouend.play()
ganiouend_play.stop()
shot_play = shot.play()
shot_play.stop()


def frame(console):
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
                console.addstr(lin, col, " ", curses.color_pair(238))
                #screen[12].append([lin, col])
            #elif lin == caca:
            #    console.addstr(lin, col, " ", curses.color_pair(0))
            elif lin > numrat+caca:
                console.addstr(lin, col, " ", curses.color_pair(240))
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
                console.addstr(lin, col, " ", curses.color_pair(pixcolor))
                #screen[pixcolor].append([lin, col])
    t2 = time.time()
    return t2-t1


def drawsprite(console):
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
                        console.addstr(lin+sprite[1], col+sprite[0], " ", curses.color_pair(pixcolor))
    t2 = time.time()
    return t2-t1


def init_keys():
    global cleliste
    for i in range(len(key_pool)):
        cle = random.randrange(0, len(key_pool[i]))
        cleliste.append(cle)
        spr_list[i+1][0] = key_pool[i][cle][0]
        spr_list[i+1][1] = key_pool[i][cle][1]


def player(console):
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
        monsteractivate = False
        monx = 49.5
        mony = 40.5
        spr_list[0][0] = monx
        spr_list[0][1] = mony
        spr_list[0][5] = 2
        if ganiou_play.is_playing() == True:
            ganiou_play.stop()
        if ganiouproche_play.is_playing() == True:
            ganiouproche_play.stop()
    t2 = time.time()
    return t2-t1


def sprintbarupdate(console):
    t1 = time.time()
    for i in range(round(maxsprintlevel)):
        if sprintlevel >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            console.addch(SY-i_b-1, i, " ", curses.color_pair(couleur))
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
                playcle = cle.play()
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


def gameover(console):
    if ganiou_play.is_playing() == True:
        ganiou_play.stop()
    if ganiouproche_play.is_playing() == True:
        ganiouproche_play.stop()
    createimage(console, "img/dead.legba", 0, 0)
    console.refresh()
    while 1:
        if k_en == 1:
            resetvalues()
            break


def monster(console):
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
        if ganiou_play.is_playing() == True:
            ganiou_play.stop()
        if ganiouproche_play.is_playing() != True:
            ganiouproche_play = ganiouproche.play()
    elif spr_list[0][3] < 16 and spr_list[0][3] >= 8:
        if ganiouproche_play.is_playing() == True:
            ganiouproche_play.stop()
        if ganiou_play.is_playing() != True:
            ganiou_play = ganiou.play()
    else:
        if ganiou_play.is_playing() == True:
            ganiou_play.stop()
        if ganiouproche_play.is_playing() == True:
            ganiouproche_play.stop()
    
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
            gameover(console)

    t2 = time.time()
    return t2-t1


def gun(console):
    global isgun
    global k_en
    global shot
    global shot_play
    global ganiouend_play
    global spr_list
    global endingstart
    global endingtime
    if isgun == False:
        if posx > spr_list[5][0]-1 and posx < spr_list[5][0]+1:
            if posy > spr_list[5][1]-1 and posy < spr_list[5][1]+1:
                isgun = True
                spr_list[5][5] = -1
    if isgun == True:
        createimage(console, "img/aim.legba", 60, 75)
        if ganiouend_play.is_playing() == False:
            ganiouend_play = ganiouend.play()
        if endingstart == True:
            if time.time()-endingtime >= 5:
                if ganiouend_play.is_playing() == True:
                    ganiouend_play.stop()
                return True
        
        if k_en == 1 and shot_play.is_playing() == False:
            k_en = 0
            shot_play = shot.play()

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


def title(console):
    musique = sa.WaveObject.from_wave_file("snd/helpeur.wav")
    play = musique.play()
    createimage(console, "img/title.legba", 0, 0)
    createimage(console, "img/t0.legba", 9, 2)
    console.refresh()
    frameindex = 1
    while 1:
        if quality == 0:
            createimage(console, f"img/t{frameindex}.legba", 9, 2)
            console.refresh()
            time.sleep(0.03333)
            frameindex += 1
            if frameindex == 5:
                frameindex = 0
        if play.is_playing() != True:
            play = musique.play()
        if k_en == 1:
            play.stop()
            console.clear()
            break
        console.addch(SY+1, SX+1, " ")


def intro(console):
    global k_en
    musique = sa.WaveObject.from_wave_file("snd/lettre.wav")
    play = musique.play()
    createimage(console, "img/h0.legba", 0, 0)
    console.refresh()
    k_en = 0
    while 1:
        if play.is_playing() != True:
            play = musique.play()
        if k_en == 1:
            break
    createimage(console, "img/h1.legba", 0, 0)
    console.refresh()
    k_en = 0
    while 1:
        if play.is_playing() != True:
            play = musique.play()
        if k_en == 1:
            play.stop()
            console.clear()
            break


def brouillage(console):
    musique = sa.WaveObject.from_wave_file("snd/brouille.wav")
    play = musique.play()
    t1 = time.time()
    while time.time()-t1 < 6:
        for col in range(SY):
            for lin in range(SX):
                pixcolor = random.randrange(231, 255)
                console.addch(col, lin, " ", curses.color_pair(pixcolor))
        console.refresh()


def ecranfin(console):
    createimage(console, "img/victoire.legba", 0, 0)
    console.refresh()
    k_en = 0
    while k_en == 0:
        pass


def main(console):
    global dt
    global monsterspeed
    scr_size = console.getmaxyx()
    if scr_size[0] < SY or scr_size[1] < SX:
        curses.endwin()
        print(f"Votre terminal doit avoir une résolution d'au moins {SX} de largeur par {SY} de hauteur.")
        print(f"Votre résolution actuelle est de {scr_size[1]} de largeur par {scr_size[0]} de hauteur.")
        exit()
    
    console.clear()
    console.nodelay(True)
    curses.noecho()
    curses.curs_set(0)

    for i in range(255):
        curses.init_pair(i+1, 0, i+1)

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    monsterspeed = MONSTER_SPEEDS[difficulty]
    
    title(console)
    intro(console)
    init_keys()

    """
    low = 100
    high = 0
    tot = 0
    avg_c = 0
    """

    while 1:
        ti = time.time()
        t = 0
        t += frame(console)
        t += drawsprite(console)
        #drawscreen(console)
        t += player(console)
        if isgun == False:
            t += sprintbarupdate(console)
        t += key()
        if monsteractivate == True:
            t += monster(console)
        if gun(console) == True:
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
        console.refresh()
        if limit_fps == True:
            if(t < 0.033333):
                time.sleep(0.033333-t)
        dt = time.time()-ti
    
    brouillage(console)
    ecranfin(console)


curses.wrapper(main)