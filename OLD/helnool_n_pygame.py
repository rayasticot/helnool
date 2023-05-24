import pygame
import math
import time
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import yaml
import colordata

SX = 230
SY = 120
FOV = 57.5
HALF_FOV = 28.75

WINDOW_SCALE = 6

k_up, k_dw, k_rg, k_le, k_en, k_sf = 0, 0, 0, 0, 0, 0
run = True

quality = 0
limit_fps = False
mouseMode = 0
sensibility = 1.75


def write(screen, color, y, x):
    screen[x, y] = colordata.colorlist[color]


def createimage(screen, name, y, x):
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
            write(screen, data[index-1], col+y, lin+x)
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


def saveGame(saveFile, levelId, value):
    with open(saveFile, "r") as f:
        saveData = yaml.safe_load(f)
    saveData[levelId][value] = True
    with open(saveFile, "w") as f:
        yaml.dump(saveData, f)


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
door = loadtexture("img/door.legba")
induwall = loadtexture("img/induwall.legba")
induwall_d = loadtexture("img/induwall_d.legba")
bloodwall = loadtexture("img/bloodwall.legba")
bloodwall_d = loadtexture("img/bloodwall_d.legba")
colorwall = loadtexture("img/colorwall.legba")
colorwall_d = loadtexture("img/colorwall_d.legba")
chickenwall = loadtexture("img/wallchicken.legba")
chickenwall_d = loadtexture("img/wallchicken_d.legba")
chickenpanneau = loadtexture("img/chickenpanneau.legba")
chickenpanneau_d = loadtexture("img/chickenpanneau_d.legba")
caisse = loadtexture("img/caisse.legba")
caisse_d = loadtexture("img/caisse_d.legba")
icewall = loadtexture("img/icewall.legba")
icewall_d = loadtexture("img/icewall_d.legba")
window = loadtexture("img/window.legba")
backwall = loadtexture("img/backwall.legba")
backwall_d = loadtexture("img/backwall_d.legba")
peur1 = loadtexture("img/mons1.legba")
peur2 = loadtexture("img/mons2.legba")
peur3 = loadtexture("img/mons3.legba")
peur4 = loadtexture("img/mons4.legba")
cle = loadtexture("img/cle.legba")
gun = loadtexture("img/gun.legba")
courir = loadtexture("img/courir.legba")
retour = loadtexture("img/retour.legba")
bureautest = loadtexture("img/bureautest.legba")
toilette = loadtexture("img/toilette.legba")
chickentable = loadtexture("img/chickentable.legba")
pouletpend = loadtexture("img/pouletpend.legba")
text_index = ((brique, brique_d), (toile, toile_d), (herb, herb_d), (filet, filet), (eye, eye_d), (labo, labo_d), (concrete, concrete_d), (box, box_d), (samsung, samsung_d), (keyhole, keyhole), (door, door), (induwall, induwall_d), (bloodwall, bloodwall_d), (colorwall, colorwall_d), (chickenwall, chickenwall_d), (chickenpanneau, chickenpanneau), (caisse, caisse_d), (icewall, icewall_d), (window, window), (backwall, backwall_d))
simp_index = ((160, 124), (223, 180), (238, 237), (249, 239), (70, 71), (160, 124), (223, 180), (238, 237), (249, 239), (70, 71))
sprite_tex_index = (peur1, peur2, peur3, cle, gun, peur4, courir, retour, bureautest, toilette, chickentable, pouletpend)


def refreshScreen(pixel_array, window):
    scale_and_show(pixel_array, window)
    pygame.display.flip()


def normalize(vector):
    norme = math.sqrt(vector[0]**2 + vector[1]**2)
    if norme == 0:
        return 0, 0
    return vector[0]/norme, vector[1]/norme


def frame(screen, map, posX, posY, angle):
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
        wallSize = round(int(SY*1.5)/fixdist)
        wallStart = round((SY-wallSize)/2)
        for lin in range(SY):
            if side == 0:
                color = map[int(pnty-dir[1])][int(pntx)]-1
            if side == 1:
                color = map[int(pnty)][int(pntx-dir[0])]-1
            if lin < wallStart:
                write(screen, 238, lin, col)
            elif lin > wallSize+wallStart:
                write(screen, 240, lin, col)
            else:
                in_x = 0
                in_y = 0
                pixcolor = 0
                if quality == 0:
                    if side == 0:
                        in_x = round((pnty % 1)*63)
                    else:
                        in_x = round((pntx % 1)*63)
                    in_y = round(((lin-wallStart)/wallSize)*63)
                    pixcolor = text_index[color][side][in_y][in_x]
                elif quality == 1:
                    pixcolor = simp_index[color][side]
                write(screen, pixcolor, lin, col)
    return scr_dist


def drawsprite(screen, sprite_list, posX, posY, angle, scr_dist):
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
        
        dif_angle = angle + HALF_FOV - spr_angle
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
        if sprite[2] > 400:
            continue
        for col in range(sprite[2]):
            for lin in range(sprite[2]):
                if lin+sprite[1] in range(SY) and col+sprite[0] in range(SX):
                    if sprite[3] < scr_dist[col+sprite[0]]:
                        tex_y = round((col/sprite[2])*63)
                        tex_x = round((lin/sprite[2])*63)
                        pixcolor = sprite_tex_index[sprite[4]][tex_x][tex_y]
                        if pixcolor == 201:
                            continue
                        write(screen, pixcolor, lin+sprite[1], col+sprite[0])


def player(map, posx, posy, angle, sprintlevel, maxsprintlevel, dt):
    sprintcoef = 1
    touchElevator = False
    if k_sf == 1 and (k_up == 1 or k_dw == 1):
        sprintcoef = 2
        if sprintlevel > 0:
            sprintlevel -= 1*dt*30
        elif maxsprintlevel > 0:
            maxsprintlevel -= 2*dt*30
        else:
            sprintcoef = 1
    else:
        if sprintlevel < maxsprintlevel:
            sprintlevel += 0.25*dt*30

    pdir = (math.cos(math.radians(angle)), math.sin(math.radians(angle)))
    rdir = (math.cos(math.radians(angle+90)), math.sin(math.radians(angle+90)))
    
    if mouseMode == 1:
        mouseMoveX = pygame.mouse.get_pos()[0]-((SX*WINDOW_SCALE)/2)
        pygame.mouse.set_pos((SX*WINDOW_SCALE)/2, (SY*WINDOW_SCALE)/2)
        angle -= mouseMoveX*0.2*sensibility
    else:
        if k_rg == 1:
            angle -= 90*dt*sensibility
        if k_le == 1:
            angle += 90*dt*sensibility

    addX, addY = 0, 0

    if k_dw == 1:
        addX -= pdir[0]
        addY -= pdir[1]
    if k_up == 1:
        addX += pdir[0]
        addY += pdir[1]
    if k_rg == 1 and mouseMode == 1:
        addX -= rdir[0]
        addY -= rdir[1]
    if k_le == 1 and mouseMode == 1:
        addX += rdir[0]
        addY += rdir[1]

    addX, addY = normalize((addX, addY))
    addX *= 2.6*dt*sprintcoef
    addY *= 2.6*dt*sprintcoef

    posx += addX
    posy += addY
    
    if map[int(posy)][int(posx)] == 10:
        touchElevator = True
    if map[int(posy)][int(posx)] > 0:
        posx -= addX
        posy -= addY
    
    angle = angle % 360

    return posx, posy, angle, sprintlevel, maxsprintlevel, touchElevator


def followPath(path, x, y, distance):
    deltaX = path[1][0]-x
    deltaY = path[1][1]-y
    distanceToFirst = math.sqrt(deltaX**2 + deltaY**2)
    if distanceToFirst >= distance:
        dirVectorX, dirVectorY = normalize((deltaX, deltaY))
        dirVectorX *= distance
        dirVectorY *= distance
        return x+dirVectorX, y+dirVectorY, False
    else:
        distance -= distanceToFirst
        try:
            deltaX = path[2][0]-path[1][0]
            deltaY = path[2][1]-path[1][1]

            dirVectorX, dirVectorY = normalize((deltaX, deltaY))
            dirVectorX *= distance
            dirVectorY *= distance
            return path[1][0]+dirVectorX, path[1][1]+dirVectorY, False
        except IndexError:
            return x, y, True


def monster(monx, mony, posx, posy, pathMap, monsterspeed, anim_num, spr_list, dt):
    endGame = False
    grid = Grid(matrix=pathMap)
    start = grid.node(int(monx), int(mony))
    end = grid.node(int(posx), int(posy))

    finder = AStarFinder()
    paths, runs = finder.find_path(start, end, grid)
    
    monx, mony, endGame = followPath(paths, monx, mony, (1/monsterspeed)*26*dt)
    
    spr_list[0][0] = monx+0.5
    spr_list[0][1] = mony+0.5
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
            endGame = True
    
    
    return monx, mony, anim_num, endGame


def sprintbarupdate(screen, maxsprintlevel, sprintlevel):
    for i in range(round(maxsprintlevel)):
        if sprintlevel >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            write(screen, couleur, SY-i_b-1, i)


def key(key_pool, spr_list, key_number, posx, posy, timerValue, monsterspeed):
    for i in range(len(key_pool)):
        if spr_list[i+1][5] == -1:
            continue
        if posx > spr_list[i+1][0]-0.5 and posx < spr_list[i+1][0]+0.5:
            if posy > spr_list[i+1][1]-0.5 and posy < spr_list[i+1][1]+0.5:
                key_sound = pygame.mixer.Sound("snd/cle.wav")
                pygame.mixer.Sound.play(key_sound)
                spr_list[i+1][5] = -1
                key_number -= 1
                if key_number == 0:
                    timerValue = 0
                else:
                    timerValue = timerValue/2
                monsterspeed -= 1
    return key_number, timerValue, monsterspeed


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
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                k_le = 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                k_rg = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                k_up = 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                k_dw = 1
            if event.key == pygame.K_SPACE:
                k_en = 1
            if event.key == pygame.K_LSHIFT:
                k_sf = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                k_le = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                k_rg = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                k_up = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                k_dw = 0
            if event.key == pygame.K_SPACE:
                k_en = 0
            if event.key == pygame.K_LSHIFT:
                k_sf = 0


def secondsToMinute(timeSeconds):
    leftMinutes = int(timeSeconds/60)
    leftSeconds = int(timeSeconds%60)
    return leftMinutes, leftSeconds


def createDigitSprite(screen, minutes, seconds):
    DIGIT_SIZE = 8
    FIRST_DIGIT_POS = 206
    DIGIT_POSY = 107
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
                write(screen, digitColor, col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i))
    write(screen, BLACK, DIGIT_POSY+4, FIRST_DIGIT_POS+8)
    write(screen, BLACK, DIGIT_POSY+9, FIRST_DIGIT_POS+8)


def createKeyNumbers(screen, keyNumber, totalKeys):
    DIGIT_SIZE = 8
    FIRST_DIGIT_POS = 206
    DIGIT_POSY = -2

    chiffreTexture = loadtexture("img/chiffre.legba")
    slashTexture = loadtexture("img/slash.legba")

    for i in range(3):
        if i == 0:
            digit = totalKeys-keyNumber
        elif i == 2:
            digit = totalKeys
        if i != 1:
            for col in range(12):
                for lin in range(8):
                    if chiffreTexture[col][lin+(digit*DIGIT_SIZE)] == 201:
                        continue
                    write(screen, 231, col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i))
        else:
            for col in range(13):
                for lin in range(8):
                    if slashTexture[col][lin] == 201:
                        continue
                    write(screen, 231, col+DIGIT_POSY+1, lin+FIRST_DIGIT_POS+(8*i))


def createHand(screen, monsterDistance):
    if monsterDistance > 16:
        createimage(screen, "img/handgood.legba", 0, 0)
    elif monsterDistance > 8:
        createimage(screen, "img/handmid.legba", 0, 0)
    else:
        createimage(screen, "img/handbad.legba", 0, 0)


def uiUpdate(screen, timerValue, keyNumber, totalKeys, monsterDistance):
    minutes, seconds = secondsToMinute(timerValue)
    createDigitSprite(screen, minutes, seconds)
    createKeyNumbers(screen, keyNumber, totalKeys)
    createHand(screen, monsterDistance)


def brouillage(screen, window, seconds, helnool):
    pygame.mixer.music.load("snd/brouille.wav")
    pygame.mixer.music.play(-1)
    t1 = time.time()
    while time.time()-t1 < seconds and run == True:
        checkinput()
        for col in range(SY):
            for lin in range(SX):
                pixcolor = random.randrange(231, 255)
                write(screen, pixcolor, col, lin)
        if helnool == True:
            createimage(screen, "img/helnool.legba", 0, 55)
        refreshScreen(screen, window)
    pygame.mixer.music.stop()


def menu(screen, window, keyboard):
    positionCurseur = 0
    XPOS = 82
    YPOS = (46, 67, 89)
    arrowSpriteX = XPOS
    arrowSpriteY = YPOS[0]
    
    


def createCheckElevator(screen, levels):
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)

    for i in range(len(levels)):
        if levels[i]["completed"] == True:
            createimage(screen, "img/check.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))]+73)
        if levels[i]["unlocked"] == False:
            createimage(screen, "img/warning.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))])


def elevator(screen, window):
    global k_up
    global k_dw
    global k_rg
    global k_le
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)
    arrowIndex = 1
    arrowSpriteX = XPOS[0]-20
    arrowSpriteY = YPOS[1]
    brouillage(screen, window, 0.25, False)

    with open("save.yaml", "r") as f:
        levels = yaml.safe_load(f)

    while run == True:
        createimage(screen, "img/elevatorbg.legba", 0, 0)
        createCheckElevator(screen, levels)
        checkinput()

        if k_up == 1:
            k_up = 0
            arrowIndex += 1
            arrowIndex %= len(XPOS)*len(YPOS)
        
        if k_dw == 1:
            k_dw = 0
            arrowIndex -= 1
            arrowIndex %= len(XPOS)*len(YPOS)

        if k_rg == 1:
            k_rg = 0
            arrowIndex += len(YPOS)
            arrowIndex %= len(XPOS)*len(YPOS)
        
        if k_le == 1:
            k_le = 0
            arrowIndex -= len(YPOS)
            arrowIndex %= len(XPOS)*len(YPOS)

        if k_en == 1:
            if levels[arrowIndex]["unlocked"] == True:
                brouillage(screen, window, 0.25, False)
                return levels[arrowIndex]["a_name"]

        arrowSpriteX = XPOS[int(arrowIndex/len(YPOS))]
        arrowSpriteY = YPOS[arrowIndex%len(YPOS)]

        createimage(screen, "img/arrow.legba", arrowSpriteY, arrowSpriteX-21)
        refreshScreen(screen, window)


def safeLevelUpdate(screen, window, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList):
    dt = 0
    while run == True:
        ti = time.time()
        checkinput()
        screenWallDistance = frame(screen, levelMap, playerPosX, playerPosY, playerAngle)
        drawsprite(screen, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, touchElevator = player(levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, dt)
        sprintbarupdate(screen, maxSprintLevel, sprintLevel)
        if touchElevator == True:
            return elevator(screen, window)
        refreshScreen(screen, window)
        dt = time.time()-ti
        if limit_fps == True:
            if(dt < 0.033333):
                time.sleep(0.033333-dt)


def levelUpdate(screen, window, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, keyPool, monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap, levelId):
    pygame.mixer.music.load("snd/helnoolarrive.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()

    animNum = 0

    oldPlayerPosX = playerPosX
    oldPlayerPosY = playerPosY

    dt = 0
    
    while run == True:
        ti = time.time()
        checkinput()
        screenWallDistance = frame(screen, levelMap, playerPosX, playerPosY, playerAngle)
        drawsprite(screen, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, touchElevator = player(levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, dt)
        if touchElevator == True and (keyNumber == 0):
            pygame.mixer.music.stop()
            brouillage(screen, window, 0.25, False)
            saveGame("save.yaml", levelId, "completed")
            saveGame("save.yaml", levelId+1, "unlocked")
            return elevator(screen, window)
        if monsterActivate == True and levelId != 0:
            pygame.mixer.music.unpause()
            monsterPosX, monsterPosY, animNum, endGame = monster(monsterPosX, monsterPosY, playerPosX, playerPosY, pathMap, monsterSpeed, animNum, spriteList, dt)
            if endGame == True:
                pygame.mixer.music.stop()
                brouillage(screen, window, 2, True)
                return "map/map_lobby.yaml"
        sprintbarupdate(screen, maxSprintLevel, sprintLevel)
        keyNumber, timerValue, monsterSpeed = key(keyPool, spriteList, keyNumber, playerPosX, playerPosY, timerValue, monsterSpeed)
        uiUpdate(screen, timerValue, keyNumber, len(keyPool), spriteList[0][3])
        if timerValue > 0:
            if oldPlayerPosX == playerPosX and oldPlayerPosY == playerPosY:
                pass
            else:
                timerValue -= dt
                if timerValue < 0:
                    timerValue = 0
        elif monsterActivate == False:
            monsterActivate = True
        refreshScreen(screen, window)
        pre_dt = time.time()-ti
        if limit_fps == True:
            if(pre_dt < 0.033333):
                time.sleep(0.033333-pre_dt)
        dt = time.time()-ti


def level(screen, window, levelFileName):
    mapFile = loadmap(levelFileName)
    spriteList = []
    keyList = []
    playerPosX = mapFile["player_spawn_point"]["pos_x"]
    playerPosY = mapFile["player_spawn_point"]["pos_y"]
    playerAngle = mapFile["player_spawn_point"]["angle"]
    sprintLevel = 100.0
    maxSprintLevel = 100.0
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

    for spr in mapFile["map_spr_list"]:
        spriteList.append([spr["pos_x"], spr["pos_y"], 0, 0, 0, spr["spr"]])

    if mapFile["monstre_spawn_time"] >= 0:
        return levelUpdate(screen, window, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, mapFile["key_pool"], monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap, mapFile["level_id"])
    else:
        return safeLevelUpdate(screen, window, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList)


def title(screen, window):
    pygame.mixer.music.load("snd/helpeur.wav")
    pygame.mixer.music.play(-1)
    createimage(screen, "img/title.legba", 0, 0)
    createimage(screen, "img/t0.legba", 9, 2)
    refreshScreen(screen, window)
    frameindex = 1
    while run == True:
        checkinput()
        if quality == 0:
            createimage(screen, f"img/t{frameindex}.legba", 9, 2)
            refreshScreen(screen, window)
            time.sleep(0.03333)
            frameindex += 1
            if frameindex == 5:
                frameindex = 0
        if k_en == 1:
            pygame.mixer.music.stop()
            break


def scale_and_show(pixel_array, surface):
    scaled_size = (SX * WINDOW_SCALE, SY * WINDOW_SCALE)
    
    scaled_surface = pygame.transform.scale(pixel_array.surface, scaled_size)
    
    surface.blit(scaled_surface, (0, 0))


def main():
    pygame.init()
    
    window_size = (230, 120)
    window = pygame.display.set_mode((230*WINDOW_SCALE, 120*WINDOW_SCALE))
    pixel_array = pygame.PixelArray(pygame.Surface((230, 120)))

    pygame.mouse.set_visible(False)

    createimage(pixel_array, "img/title.legba", 0, 0)

    title(pixel_array, window)
    brouillage(pixel_array, window, 0.25, False)

    newLevel = "map/map_lobby.yaml"
    
    while run == True:
        newLevel = level(pixel_array, window, newLevel)


if __name__ == "__main__":
    main()