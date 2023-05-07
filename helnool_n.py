import curses
import math
import time
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pynput import keyboard
import simpleaudio as sa
import yaml

SX = 230
SY = 120
FOV = 57.5
HALF_FOV = 28.75
LEVEL_LIST = ("map/map_default.yaml")

dt = 0
k_up, k_dw, k_rg, k_le, k_en, k_sf = 0, 0, 0, 0, 0, 0

quality = 0
limit_fps = True


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
    if key == keyboard.Key.up:
        k_up = 0
    elif key == keyboard.Key.down:
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
    index = 4
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


def loadmap(mapfile):
    with open(mapfile, "r") as f:
        mapfiledata = yaml.safe_load(f)
    return mapfiledata


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
keyhole = loadtexture("img/elevator.legba")
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
arrive = sa.WaveObject.from_wave_file("snd/helnoolarrive.wav")
ganiouproche_play = ganiouproche.play()
ganiouproche_play.stop()
ganiou_play = ganiou.play()
ganiou_play.stop()
ganiouend_play = ganiouend.play()
ganiouend_play.stop()
shot_play = shot.play()
shot_play.stop()
arrive_play = arrive.play()
arrive_play.stop()


def frame(console, map, posX, posY, angle):
    scr_dist = []
    linang = (angle+(FOV/2))+0.25
    linang = linang % 360
    for col in range(SX):
        linang -= 0.25
        linang = linang % 360
        dir = [math.cos(math.radians(linang)), math.sin(math.radians(linang))]
        pntx = posX
        pnty = posY
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
        scr_dist.append(fixdist)
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
    return scr_dist


def drawsprite(console, sprite_list, posX, posY, angle, scr_dist):
    sprite_loc_list = sprite_list.copy()
    screen_spr_list = []

    for i in range(len(sprite_loc_list)):
        sprite_loc_list[i][3] = (math.sqrt(((sprite_loc_list[i][0]-posX)**2) + ((sprite_loc_list[i][1]-posY)**2)))
    sprite_loc_list = sorted(sprite_loc_list, key=lambda x: - x[3])

    for i in range(len(sprite_loc_list)):
        if sprite_loc_list[i][5] == -1:
            continue
        dify = sprite_loc_list[i][1]-posY
        difx = sprite_loc_list[i][0]-posX
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


def player(console, map, posx, posy, angle, sprintlevel, maxsprintlevel):
    """
    global monsteractivate
    global monx
    global mony
    global spr_list
    global ganiou_play
    global ganiouproche_play
    """

    sprintcoef = 1
    if k_sf == 1 and (k_up == 1 or k_dw == 1):
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
    """
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
    """
    return posx, posy, angle, sprintlevel, maxsprintlevel


def monster(console, monx, mony, posx, posy, mon_index, chemin, path, oldpx, oldpy, monsterspeed, anim_num, spr_list):
    global ganiou_play
    global ganiouproche_play

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
    
    """
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
    """
    
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

    endGame = False
    if posx > monx-1 and posx < monx+1:
        if posy > mony-1 and posy < mony+1:
            endGame = True
    
    return monx, mony, mon_index, chemin, oldpx, oldpy, anim_num, endGame


def sprintbarupdate(console, maxsprintlevel, sprintlevel):
    for i in range(round(maxsprintlevel)):
        if sprintlevel >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            console.addch(SY-i_b-1, i, " ", curses.color_pair(couleur))


def key(key_pool, spr_list, key_number, posx, posy, timerValue, monsterspeed):
    """
    global monsteractivate
    global monsterspeed
    global monx
    global mony
    """
    for i in range(len(key_pool)):
        if spr_list[i+1][5] == -1:
            continue
        if posx > spr_list[i+1][0]-0.5 and posx < spr_list[i+1][0]+0.5:
            if posy > spr_list[i+1][1]-0.5 and posy < spr_list[i+1][1]+0.5:
                playcle = cle.play()
                spr_list[i+1][5] = -1
                key_number -= 1
                if key_number == 0:
                    timerValue = 0
                else:
                    timerValue = timerValue/2
                monsterspeed -= 1
                """
                if monsteractivate == False:
                    monx = monstre_spawn[i][cleliste[i]][0]
                    mony = monstre_spawn[i][cleliste[i]][1]
                    monsteractivate = True
                
                """
    return key_number, timerValue, monsterspeed


def secondsToMinute(timeSeconds):
    leftMinutes = int(timeSeconds/60)
    leftSeconds = int(timeSeconds%60)
    return leftMinutes, leftSeconds


def createDigitSprite(console, minutes, seconds):
    DIGIT_SIZE = 8
    FIRST_DIGIT_POS = 206
    DIGIT_POSY = 108
    WHITE = 231
    BLACK = 232
    YELLOW = 226
    RED = 160

    chiffreTexture = loadtexture("img/chiffre.legba")

    digitColor = WHITE
    if minutes == 0 and seconds <= 15:
        digitColor = RED
    elif minutes == 0 and seconds <= 30:
        digitColor = YELLOW

    for i in range(3):
        if i == 0:
            digit = minutes
        elif i == 2:
            digit = int(seconds%10)
        else:
            digit = int(seconds/10)
        for col in range(12):
            for lin in range(8):
                if chiffreTexture[col][lin+(digit*DIGIT_SIZE)] == 201:
                    continue
                console.addch(col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i), " ", curses.color_pair(digitColor))
    console.addch(DIGIT_POSY+4, FIRST_DIGIT_POS+8, " ", curses.color_pair(BLACK))
    console.addch(DIGIT_POSY+9, FIRST_DIGIT_POS+8, " ", curses.color_pair(BLACK))


def timerUpdate(console, timerValue):
    minutes, seconds = secondsToMinute(timerValue)
    createDigitSprite(console, minutes, seconds)


def safeLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList):
    global dt
    while 1:
        ti = time.time()
        screenWallDistance = frame(console, levelMap, playerPosX, playerPosY, playerAngle)
        drawsprite(console, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel = player(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel)
        sprintbarupdate(console, maxSprintLevel, sprintLevel)
        if k_en == 1:
            return "map/map_map1.yaml"
        console.refresh()
        dt = time.time()-ti
        if limit_fps == True:
            if(dt < 0.033333):
                time.sleep(0.033333-dt)


def levelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, keyPool, monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap):
    global dt
    global arrive_play
    oldPlayerPosX = playerPosX
    oldPlayerPosY = playerPosY
    monsterIndex = 0
    chemin = []
    animNum = 0
    
    while 1:
        ti = time.time()
        screenWallDistance = frame(console, levelMap, playerPosX, playerPosY, playerAngle)
        drawsprite(console, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel = player(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel)
        if monsterActivate == True:
            if arrive_play.is_playing() == False:
                arrive_play = arrive.play()
            monsterPosX, monsterPosY, monsterIndex, chemin, oldPlayerPosX, oldPlayerPosY, animNum, endGame = \
            monster(console, monsterPosX, monsterPosY, playerPosX, playerPosY, monsterIndex, chemin, pathMap, oldPlayerPosX, oldPlayerPosY, monsterSpeed, animNum, spriteList)
            if endGame == True:
                return "map/map_lobby.yaml"
        sprintbarupdate(console, maxSprintLevel, sprintLevel)
        keyNumber, timerValue, monsterSpeed = key(keyPool, spriteList, keyNumber, playerPosX, playerPosY, timerValue, monsterSpeed)
        timerUpdate(console, timerValue)
        if timerValue > 0:
            if oldPlayerPosX == playerPosX and oldPlayerPosY == playerPosY:
                pass
            else:
                timerValue -= dt
                if timerValue < 0:
                    timerValue = 0
        elif monsterActivate == False:
            monsterActivate = True
        if k_en == 1:
            return "map/map_map1.yaml"
        console.refresh()
        dt = time.time()-ti
        if limit_fps == True:
            if(dt < 0.033333):
                time.sleep(0.033333-dt)


def level(console, levelFileName):
    global dt
    mapFile = loadmap(levelFileName)
    spriteList = []
    keyList = []
    playerPosX = mapFile["player_spawn_point"]["pos_x"]
    playerPosY = mapFile["player_spawn_point"]["pos_y"]
    playerAngle = 0
    sprintLevel = 100
    maxSprintLevel = 100
    keyNumber = -1
    monsterActivate = False
    monsterSpeed = 0
    monsterPosX = mapFile["monstre_spawn_point"]["pos_x"]
    monsterPosY = mapFile["monstre_spawn_point"]["pos_y"]
    levelMap = loadtexture(mapFile["map_data_file"])
    pathMap = map2pathmap(mapFile["map_data_file"])
    timerValue = mapFile["monstre_spawn_time"]
    
    if mapFile["monstre_spawn_time"] >= 0:
        keyNumber = len(mapFile["key_pool"])
        monsterSpeed = mapFile["monster_speed_init"]
        levelPathMap = map2pathmap(mapFile["map_data_file"])
        spriteList.append([229, 229, 0, 0, 0, 0])
        for keys in mapFile["key_pool"]:
            key = random.randrange(0, len(keys))
            keyList.append(key)
            spriteList.append([keys[key][0], keys[key][1], 0, 0, 0, 3])

    if mapFile["monstre_spawn_time"] >= 0:
        return levelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, mapFile["key_pool"], monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap)
    else:
        return safeLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList)


def main(console):
    global dt
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

    newLevel = "map/map_map1.yaml"
    
    while 1:
        newLevel = level(console, newLevel)


curses.wrapper(main)