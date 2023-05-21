import curses
import math
import time
import random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pynput.keyboard
from pynput.mouse import Button, Controller
import simpleaudio as sa
import yaml

SX = 230
SY = 120
FOV = 57.5
HALF_FOV = 28.75

mouse = Controller()
mouse.position = (800, 800)

quality = 0
limit_fps = False
mouseMode = 1
sensibility = 1.75


def createOnPress(keyboard):
    def on_press(key):
        try:
            if key.char == "w" or key.char == "W":
                keyboard["k_up"] = 1
            elif key.char == "s" or key.char == "S":
                keyboard["k_dw"] = 1
            elif key.char == "d" or key.char == "D":
                keyboard["k_rg"] = 1
            elif key.char == "a" or key.char == "A":
                keyboard["k_le"] = 1
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                keyboard["k_en"] = 1
            elif key == pynput.keyboard.Key.shift:
                keyboard["k_sf"] = 1
            elif key == pynput.keyboard.Key.up:
                keyboard["k_up"] = 1
            elif key == pynput.keyboard.Key.down:
                keyboard["k_dw"] = 1
            elif key == pynput.keyboard.Key.right:
                keyboard["k_rg"] = 1
            elif key == pynput.keyboard.Key.left:
                keyboard["k_le"] = 1
    return on_press

 
def createOnRelease(keyboard):
    def on_release(key):
        try:
            if key.char == "w" or key.char == "W":
                keyboard["k_up"] = 0
            elif key.char == "s" or key.char == "S":
                keyboard["k_dw"] = 0
            elif key.char == "d" or key.char == "D":
                keyboard["k_rg"] = 0
            elif key.char == "a" or key.char == "A":
                keyboard["k_le"] = 0
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                keyboard["k_en"] = 0
            elif key == pynput.keyboard.Key.shift:
                keyboard["k_sf"] = 0
            elif key == pynput.keyboard.Key.up:
                keyboard["k_up"] = 0
            elif key == pynput.keyboard.Key.down:
                keyboard["k_dw"] = 0
            elif key == pynput.keyboard.Key.right:
                keyboard["k_rg"] = 0
            elif key == pynput.keyboard.Key.left:
                keyboard["k_le"] = 0
    return on_release


def createimage(console, name, y, x):
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
boxdark = loadtexture("img/boxdark.legba")
boxdark_d = loadtexture("img/boxdark_d.legba")
boxlight = loadtexture("img/boxlight.legba")
boxlight_d = loadtexture("img/boxlight_d.legba")
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
toyota = loadtexture("img/toyota.legba")
zakfront0 = loadtexture("img/zakfront0.legba")
zakfront1 = loadtexture("img/zakfront1.legba")
zakfront2 = loadtexture("img/zakfront2.legba")
zakback0 = loadtexture("img/zakback0.legba")
zaktoc0 = loadtexture("img/zaktoc0.legba")
zaktoc1 = loadtexture("img/zaktoc1.legba")
text_index = ((brique, brique_d), (toile, toile_d), (herb, herb_d), (filet, filet), (eye, eye_d), (labo, labo_d), (concrete, concrete_d), (box, box_d), (samsung, samsung_d), (keyhole, keyhole), (door, door), (induwall, induwall_d), (bloodwall, bloodwall_d), (colorwall, colorwall_d), (chickenwall, chickenwall_d), (chickenpanneau, chickenpanneau), (caisse, caisse_d), (icewall, icewall_d), (window, window), (backwall, backwall_d), (boxdark, boxdark_d), (boxlight, boxlight_d))
simp_index = ((160, 124), (223, 180), (238, 237), (249, 239), (70, 71), (160, 124), (223, 180), (238, 237), (249, 239), (70, 71))
sprite_tex_index = (peur1, peur2, peur3, cle, gun, peur4, courir, retour, bureautest, toilette, chickentable, pouletpend, toyota, zakfront0, zakfront1, zakfront2, zakback0, zaktoc0, zaktoc1)

"""
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
"""


def normalize(vector):
    norme = math.sqrt(vector[0]**2 + vector[1]**2)
    if norme == 0:
        return 0, 0
    return vector[0]/norme, vector[1]/norme


def rayCast(mapData, rayAngle, startpointX, startpointY):
    INITIAL_TRAVEL = 1
    PRECISION = 20
    direction = (math.cos(math.radians(rayAngle)), math.sin(math.radians(rayAngle)))
    positionX = startpointX
    positionY = startpointY
    distance = 0
    side = 0
    for i in range(0, PRECISION):
        travelDistance = INITIAL_TRAVEL/(2**i)
        while 1:
            positionX += direction[0]*travelDistance
            positionY += direction[1]*travelDistance
            distance += travelDistance
            if mapData[int(positionY)][int(positionX-(direction[0]*travelDistance))] != 0:
                side = 1
                break
            if mapData[int(positionY-(direction[1]*travelDistance))][int(positionX)] != 0:
                side = 0
                break
            if i != PRECISION-1:
                if mapData[int(positionY)][int(positionX)] != 0:
                    break
        distance -= travelDistance
        positionX -= direction[0]*travelDistance
        positionY -= direction[1]*travelDistance

    distance += travelDistance
    if side == 0:
        positionX += direction[0]*travelDistance
    else:
        positionY += direction[1]*travelDistance
    
    textureHit = mapData[int(positionY)][int(positionX)]-1
    
    return distance, side, positionX, positionY, textureHit


def findPixelColor(mapData, pixelHeight, hitPositionX, hitPositionY, side, texture, wallStart, wallSize, totalWall, heightMultiplier, floorColor):
    if pixelHeight < wallStart:
        return floorColor[0]
    elif pixelHeight > totalWall:
        return floorColor[1]
    else:
        textureX = 0
        textureY = 0
        pixelColor = 0
        if quality == 0:
            if side == 0:
                textureX = round((hitPositionY % 1)*63)
            else:
                textureX = round((hitPositionX % 1)*63)

            textureY = round(((pixelHeight-wallStart)/wallSize)*(63*heightMultiplier))%64

            if texture == 10 and (((pixelHeight-wallStart)/wallSize)*(63*heightMultiplier))/64 <= 10 and heightMultiplier != 1: # À chier
                pixelColor = text_index[0][side][textureY][textureX]
            else:
                pixelColor = text_index[texture][side][textureY][textureX]
                
        elif quality == 1:
            pixelColor = simp_index[texture][side]
        
        return pixelColor


def frame(console, mapData, posX, posY, angle, floorColor):
    scr_dist = []
    linang = (angle+(FOV/2))+0.25
    linang = linang % 360
    for col in range(SX):
        linang -= 0.25
        linang %= 360
        distance, side, hitPositionX, hitPositionY, textureHit = rayCast(mapData, linang, posX, posY)

        fixDistance = distance*math.cos(math.radians(linang-angle))
        scr_dist.append(fixDistance)
        wallSize = round(int(SY*1.5)/fixDistance)
        wallStart = round((SY-wallSize)/2)
        
        for lin in range(SY):
            pixelColor = findPixelColor(mapData, lin, hitPositionX, hitPositionY, side, textureHit, wallStart, wallSize, wallStart+wallSize, 1, floorColor)
            console.addstr(lin, col, " ", curses.color_pair(pixelColor))
    return scr_dist


def frameWithHeight(console, mapData, heightmap, posX, posY, angle, floorColor):
    scr_dist = []
    linang = (angle+(FOV/2))+0.25
    linang = linang % 360
    for col in range(SX):
        linang -= 0.25
        linang = linang % 360
        distance, side, hitPositionX, hitPositionY, textureHit = rayCast(mapData, linang, posX, posY)

        fixDistance = distance*math.cos(math.radians(linang-angle))
        scr_dist.append(fixDistance)

        if side == 0:
            heightMultiplier = heightmap[int(hitPositionY)][int(hitPositionX)]
        if side == 1:
            heightMultiplier = heightmap[int(hitPositionY)][int(hitPositionX)]
        if heightMultiplier == 0:
            heightMultiplier = 1

        wallSize = round(int(SY*1.5*heightMultiplier)/fixDistance)
        groundWallSize = round(int(SY*1.5)/fixDistance)
        wallStart = round((SY-wallSize)/2)
        groundWallStart = round((SY-groundWallSize)/2)

        for lin in range(SY):
            pixelColor = findPixelColor(mapData, lin, hitPositionX, hitPositionY, side, textureHit, wallStart, wallSize, groundWallStart+groundWallSize, heightMultiplier, floorColor)
            console.addstr(lin, col, " ", curses.color_pair(pixelColor))
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
                        console.addstr(lin+sprite[1], col+sprite[0], " ", curses.color_pair(pixcolor))


def player(map, posx, posy, angle, sprintlevel, maxsprintlevel, dt, keyboard):
    sprintcoef = 1
    touch = 0
    if keyboard["k_sf"] == 1 and (keyboard["k_up"] == 1 or keyboard["k_dw"] == 1):
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
        mouseMoveX = mouse.position[0]-800
        mouse.position = (800, 400)
        angle -= mouseMoveX*0.025*sensibility
    else:
        if keyboard["k_rg"] == 1:
            angle -= 90*dt*sensibility
        if keyboard["k_le"] == 1:
            angle += 90*dt*sensibility

    addX, addY = 0, 0

    if keyboard["k_dw"] == 1:
        addX -= pdir[0]
        addY -= pdir[1]
    if keyboard["k_up"] == 1:
        addX += pdir[0]
        addY += pdir[1]
    if keyboard["k_rg"] == 1 and mouseMode == 1:
        addX -= rdir[0]
        addY -= rdir[1]
    if keyboard["k_le"] == 1 and mouseMode == 1:
        addX += rdir[0]
        addY += rdir[1]

    addX, addY = normalize((addX, addY))
    addX *= 2.6*dt*sprintcoef
    addY *= 2.6*dt*sprintcoef

    posx += addX
    posy += addY
    
    if map[int(posy)][int(posx)] == 10:
        touch = 1
    elif map[int(posy)][int(posx)] == 19:
        touch = 2
    if map[int(posy)][int(posx)] > 0:
        posx -= addX
        posy -= addY
    
    angle = angle % 360

    return posx, posy, angle, sprintlevel, maxsprintlevel, touch


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


def engineCinematic(console, fileName):
    with open(fileName) as f:
        cinematicInfo = yaml.safe_load(f)
    
    with open(cinematicInfo["map_file_name"]) as f:
        mapFile = yaml.safe_load(f)

    sprList = []
    for sprite in mapFile["map_spr_list"]:
        sprList.append([sprite["pos_x"], sprite["pos_y"], 0, 0, 0, sprite["spr"]])
    actorIndex = len(sprList)
    actorDir = []
    for actor in cinematicInfo["actors"]:
        sprList.append([actor[0]["pos_x"], actor[0]["pos_y"], 0, 0, 0, actor[0]["spr"]])
        deltaPosX = actor[1]["pos_x"]-actor[0]["pos_x"]
        deltaPosY = actor[1]["pos_y"]-actor[0]["pos_y"]
        actorDir.append((deltaPosX, deltaPosY))
    actorDir = tuple(actorDir)

    mapData = loadtexture(mapFile["map_data_file"])
    if cinematicInfo["height"] == True:
        heightMap = loadtexture("map/height.legba")

    camX = cinematicInfo["cam"][0]["pos_x"]
    camY = cinematicInfo["cam"][0]["pos_y"]
    camAngle = cinematicInfo["cam"][0]["angle"]
    camDir = (
        cinematicInfo["cam"][1]["pos_x"]-cinematicInfo["cam"][0]["pos_x"],
        cinematicInfo["cam"][1]["pos_y"]-cinematicInfo["cam"][0]["pos_y"],
    )
    elapsedTime = 0
    dt = 0

    while 1:
        t1 = time.time()
        if cinematicInfo["height"] == True:
            screenDist = frameWithHeight(console, mapData, heightMap, camX, camY, camAngle, (81, 28))
        else:
            screenDist = frame(console, mapData, camX, camY, camAngle, (238, 240))

        drawsprite(console, sprList, camX, camY, camAngle, screenDist)

        for i in range(len(cinematicInfo["actors"])):
            initialPosX = cinematicInfo["actors"][i][0]["pos_x"]
            initialPosY = cinematicInfo["actors"][i][0]["pos_y"]
            sprList[actorIndex+i][0] = initialPosX + actorDir[i][0]*(elapsedTime/cinematicInfo["time"])
            sprList[actorIndex+i][1] = initialPosY + actorDir[i][1]*(elapsedTime/cinematicInfo["time"])
            
            sprList[actorIndex+i][5] =  cinematicInfo["actors_frame"][i+1][int(elapsedTime/cinematicInfo["actors_frame"][0]["frequency"])%len(cinematicInfo["actors_frame"][i+1])]

        camX = cinematicInfo["cam"][0]["pos_x"] + camDir[0]*(elapsedTime/cinematicInfo["time"])
        camY = cinematicInfo["cam"][0]["pos_y"] + camDir[1]*(elapsedTime/cinematicInfo["time"])

        console.refresh()
        dt = time.time()-t1
        elapsedTime += dt
        if elapsedTime >= cinematicInfo["time"]:
            break


def ending(console, hard, keyboard):
    if hard == False:
        saveGame("save.yaml", 9, "completed")
        createimage(console, "img/endgame.legba", 0, 0)
    else:
        saveGame("save.yaml", 9, "h_completed")
        createimage(console, "img/endgamehard.legba", 0, 0)
    console.refresh()

    while 1:
        if keyboard["k_en"] == 1:
            brouillage(console, 0.25, False)
            return "map/map_lobby.yaml", hard
    

def sprintbarupdate(console, maxsprintlevel, sprintlevel):
    for i in range(round(maxsprintlevel)):
        if sprintlevel >= i:
            couleur = 1
        else:
            couleur = 0
        for i_b in range(4):
            console.addch(SY-i_b-1, i, " ", curses.color_pair(couleur))


def key(key_pool, spr_list, key_number, posx, posy, timerValue, monsterspeed):
    cle = sa.WaveObject.from_wave_file("snd/cle.wav")
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
    return key_number, timerValue, monsterspeed


def secondsToMinute(timeSeconds):
    leftMinutes = int(timeSeconds/60)
    leftSeconds = int(timeSeconds%60)
    return leftMinutes, leftSeconds


def createDigitSprite(console, minutes, seconds):
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
                console.addch(col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i), " ", curses.color_pair(digitColor))
    console.addch(DIGIT_POSY+4, FIRST_DIGIT_POS+8, " ", curses.color_pair(BLACK))
    console.addch(DIGIT_POSY+9, FIRST_DIGIT_POS+8, " ", curses.color_pair(BLACK))


def createKeyNumbers(console, keyNumber, totalKeys):
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
                    console.addch(col+DIGIT_POSY, lin+FIRST_DIGIT_POS+(8*i), " ", curses.color_pair(231))
        else:
            for col in range(13):
                for lin in range(8):
                    if slashTexture[col][lin] == 201:
                        continue
                    console.addch(col+DIGIT_POSY+1, lin+FIRST_DIGIT_POS+(8*i), " ", curses.color_pair(231))


def createHand(console, monsterDistance):
    if monsterDistance > 16:
        createimage(console, "img/handgood.legba", 0, 0)
    elif monsterDistance > 8:
        createimage(console, "img/handmid.legba", 0, 0)
    else:
        createimage(console, "img/handbad.legba", 0, 0)


def uiUpdate(console, timerValue, keyNumber, totalKeys, monsterDistance):
    minutes, seconds = secondsToMinute(timerValue)
    createDigitSprite(console, minutes, seconds)
    createKeyNumbers(console, keyNumber, totalKeys)
    createHand(console, monsterDistance)


def brouillage(console, seconds, helnool):
    musique = sa.WaveObject.from_wave_file("snd/brouille.wav")
    play = musique.play()
    t1 = time.time()
    while time.time()-t1 < seconds:
        for col in range(SY):
            for lin in range(SX):
                pixcolor = random.randrange(231, 255)
                console.addch(col, lin, " ", curses.color_pair(pixcolor))
        if helnool == True:
            createimage(console, "img/helnool.legba", 0, 55)
        console.refresh()
    if play.is_playing():
        play.stop()


def gunCheckCollision(gunx, guny, posx, posy):
    deltaX = gunx-posx
    deltaY = guny-posy
    if math.sqrt(deltaX**2 + deltaY**2) <= 1:
        return True
    else:
        return False


def shootBullet(levelMap, posx, posy, angle, monx, mony):
    dir = (math.cos(math.radians(angle))*0.25, math.sin(math.radians(angle))*0.25)
    pntx = posx
    pnty = posy
    while 1:
        pntx += dir[0]
        pnty += dir[1]
        if levelMap[int(pnty)][int(pntx)] != 0:
            return 0
        deltaX = pntx-monx-0.5
        deltaY = pnty-mony-0.5
        if math.sqrt(deltaX**2 + deltaY**2) <= 5:
            return 1


def gun(console, levelMap, spr_list, posx, posy, angle, monx, mony, gunsoundplay, gunsound, keyboard):
    createimage(console, "img/aim.legba", 60, 75)
    if keyboard["k_en"] == 1 and gunsoundplay.is_playing() == False:
        keyboard["k_en"] = 0
        gunsoundplay = gunsound.play()
    
        return shootBullet(levelMap, posx, posy, angle, monx, mony), gunsoundplay
    return 0, gunsoundplay

def menu(console, keyboard):
    positionCurseur = 0
    XPOS = 82
    YPOS = (46, 67, 89)
    arrowSpriteX = XPOS
    arrowSpriteY = YPOS[0]
    while 1:
        createimage(console, "img/pause.legba", 0, 0)
        if keyboard["k_up"] == 1:
            positionCurseur -= 1
        if keyboard["k_dw"] == 1:
            positionCurseur += 1
        if keyboard["k_en"] == 1:
            if positionCurseur == 0:
                # Reprendre la partie
                pass
            if positionCurseur == 1:
                # Ouvrir les options
                pass
            if positionCurseur == 2:
                exit()
        
        positionCurseur %= 3
        arrowSpriteY = YPOS[positionCurseur%len(YPOS)]

        createimage(console, "img/arrow.legba", arrowSpriteY, arrowSpriteX)
        console.refresh()

def createCheckElevator(console, sauvegarde, hard):
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)

    for i in range(len(sauvegarde)):
        if hard == True:
            complete = sauvegarde[i]["h_completed"]
            unlocked = sauvegarde[i]["h_unlocked"]
        else:
            complete = sauvegarde[i]["completed"]
            unlocked = sauvegarde[i]["unlocked"]
        if complete == True:
            createimage(console, "img/check.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))]+73)

        if unlocked == False:
            createimage(console, "img/warning.legba", YPOS[i%len(YPOS)], XPOS[int(i/len(YPOS))])

    if sauvegarde[9]["completed"] == False:
        createimage(console, "img/heltape.legba", 98, XPOS[0])


def elevator(console, keyboard):
    XPOS = (26, 136)
    YPOS = (80, 63, 46, 29, 12)
    arrowIndex = 1
    arrowSpriteX = XPOS[0]-20
    arrowSpriteY = YPOS[1]
    brouillage(console, 0.25, False)

    with open("save.yaml", "r") as f:
        sauvegarde = yaml.safe_load(f)
    with open("levels.yaml", "r") as f:
        levels = yaml.safe_load(f)
    with open("levels_hard.yaml", "r") as f:
        levels_hard = yaml.safe_load(f)

    musique = sa.WaveObject.from_wave_file("snd/ascenseur.wav")
    play = musique.play()

    hard = False

    while 1:
        if play.is_playing() == False:
            play = musique.play()
        if hard == False:
            createimage(console, "img/elevatorbg.legba", 0, 0)
            createCheckElevator(console, sauvegarde, hard)
        else:
            createimage(console, "img/elevatorburnbg.legba", 0, 0)
            createCheckElevator(console, sauvegarde, hard)

        if keyboard["k_up"] == 1:
            keyboard["k_up"] = 0
            arrowIndex += 1
        
        if keyboard["k_dw"] == 1:
            keyboard["k_dw"] = 0
            arrowIndex -= 1

        if keyboard["k_rg"] == 1:
            keyboard["k_rg"] = 0
            arrowIndex += len(YPOS)
        
        if keyboard["k_le"] == 1:
            keyboard["k_le"] = 0
            arrowIndex -= len(YPOS)

        if sauvegarde[9]["completed"] == True:
            arrowIndex %= len(XPOS)*len(YPOS)+1
        else:
            arrowIndex %= len(XPOS)*len(YPOS)

        if keyboard["k_en"] == 1:
            brouillage(console, 0.25, False)
            if arrowIndex == 10:
                if play.is_playing() == True:
                    play.stop()
                hard = not(hard)
                if hard == True:
                    musique = sa.WaveObject.from_wave_file("snd/ascenseurfeu.wav")
                    play = musique.play()
                else:
                    musique = sa.WaveObject.from_wave_file("snd/ascenseur.wav")
                    play = musique.play()
            elif hard == False and sauvegarde[arrowIndex]["unlocked"] == True:
                if play.is_playing() == True:
                    play.stop()
                return levels[arrowIndex], False
            elif hard == True and sauvegarde[arrowIndex]["h_unlocked"] == True:
                if play.is_playing() == True:
                    play.stop()
                return levels_hard[arrowIndex], True

        if arrowIndex == 10:
            arrowSpriteX = XPOS[0]
            arrowSpriteY = 93
        else:
            arrowSpriteX = XPOS[int(arrowIndex/len(YPOS))]
            arrowSpriteY = YPOS[arrowIndex%len(YPOS)]

        createimage(console, "img/arrow.legba", arrowSpriteY, arrowSpriteX-21)
        console.refresh()


def safeLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, keyboard):
    dt = 0
    while 1:
        ti = time.time()
        screenWallDistance = frame(console, levelMap, playerPosX, playerPosY, playerAngle, (238, 240))
        drawsprite(console, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, touchElevator = player(levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, dt, keyboard)
        sprintbarupdate(console, maxSprintLevel, sprintLevel)
        if touchElevator == 1:
            return elevator(console, keyboard)
        console.refresh()
        dt = time.time()-ti
        if limit_fps == True:
            if(dt < 0.033333):
                time.sleep(0.033333-dt)


def levelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, keyPool, monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap, levelId, hard, keyboard):
    arrive = sa.WaveObject.from_wave_file("snd/helnoolarrive.wav")
    arrive_play = arrive.play()
    arrive_play.stop()
    animNum = 0

    oldPlayerPosX = playerPosX
    oldPlayerPosY = playerPosY

    dt = 0
    
    while 1:
        ti = time.time()
        screenWallDistance = frame(console, levelMap, playerPosX, playerPosY, playerAngle, (238, 240))
        drawsprite(console, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, touch = player(levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, dt, keyboard)
        if touch == 1 and (keyNumber == 0) and levelId != 9:
            if arrive_play.is_playing() == True:
                arrive_play.stop()
            brouillage(console, 0.25, False)
            if hard == False:
                saveGame("save.yaml", levelId, "completed")
                saveGame("save.yaml", levelId+1, "unlocked")
            else:
                saveGame("save.yaml", levelId, "h_completed")
                saveGame("save.yaml", levelId+1, "h_unlocked")
            return elevator(console), hard
        elif touch == 2:
            if arrive_play.is_playing() == True:
                arrive_play.stop()
            brise = sa.WaveObject.from_wave_file("snd/brise.wav")
            brise_play = brise.play()
            return "map/map_dehors.yaml", hard
        if monsterActivate == True and levelId != 0:
            if arrive_play.is_playing() == False:
                arrive_play = arrive.play()
            monsterPosX, monsterPosY, animNum, endGame = monster(monsterPosX, monsterPosY, playerPosX, playerPosY, pathMap, monsterSpeed, animNum, spriteList, dt)
            if endGame == True:
                if arrive_play.is_playing() == True:
                    arrive_play.stop()
                brouillage(console, 2, True)
                return "map/map_lobby.yaml", hard
        sprintbarupdate(console, maxSprintLevel, sprintLevel)
        keyNumber, timerValue, monsterSpeed = key(keyPool, spriteList, keyNumber, playerPosX, playerPosY, timerValue, monsterSpeed)
        uiUpdate(console, timerValue, keyNumber, len(keyPool), spriteList[0][3])
        if timerValue > 0:
            if oldPlayerPosX == playerPosX and oldPlayerPosY == playerPosY:
                pass
            else:
                timerValue -= dt
                if timerValue < 0:
                    timerValue = 0
        elif monsterActivate == False:
            monsterActivate = True
        console.refresh()
        pre_dt = time.time()-ti
        if limit_fps == True:
            if(pre_dt < 0.033333):
                time.sleep(0.033333-pre_dt)
        dt = time.time()-ti


def outsideLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, monsterPosX, monsterPosY, monsterSpeed, pathMap, levelId, hard, keyboard):
    dt = 0
    monsterActivate = False
    monsterLife = 1
    animNum = 0

    shot = sa.WaveObject.from_wave_file("snd/shot.wav")
    shot_play = shot.play()
    shot_play.stop()
    music = sa.WaveObject.from_wave_file("snd/mince.wav")
    music_play = music.play()
    music_play.stop()

    heightMap = loadtexture("map/height.legba")
    while 1:
        ti = time.time()
        screenWallDistance = frameWithHeight(console, levelMap, heightMap, playerPosX, playerPosY, playerAngle, (232, 28))
        drawsprite(console, spriteList, playerPosX, playerPosY, playerAngle, screenWallDistance)
        playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, touchElevator = player(levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, dt, keyboard)
        sprintbarupdate(console, maxSprintLevel, sprintLevel)
        if monsterActivate == False and gunCheckCollision(spriteList[1][0], spriteList[1][1], playerPosX, playerPosY) == True:
            spriteList[1][5] = -1
            music_play = music.play()
            monsterActivate = True
        if monsterActivate == True:
            hit, shot_play = gun(console, levelMap, spriteList, playerPosX, playerPosY, playerAngle, monsterPosX, monsterPosX, shot_play, shot, keyboard)
            monsterLife -= hit
            if monsterLife <= 0:
                spriteList[0][5] = 5
                music_play.stop()
                if playerPosX >= spriteList[2][0]-0.5 and playerPosX <= spriteList[2][0]+0.5:
                    if playerPosY >= spriteList[2][1]-0.5 and playerPosY <= spriteList[2][1]+0.5:
                        return ending(console, hard, keyboard)
        if monsterActivate == True and monsterLife > 0:
            if music_play.is_playing() == False:
                music_play = music.play()
            monsterPosX, monsterPosY, animNum, endGame = monster(monsterPosX, monsterPosY, playerPosX, playerPosY, pathMap, monsterSpeed, animNum, spriteList, dt)
            if endGame == True:
                brouillage(console, 2, True)
                return "map/map_dehors.yaml", hard
        console.addstr(123, 30, str(monsterPosX))
        console.refresh()
        dt = time.time()-ti
        if limit_fps == True:
            if(dt < 0.033333):
                time.sleep(0.033333-dt)


def level(console, levelFileName, hard, keyboard):
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
    
    if mapFile["monstre_spawn_time"] == -2:
        monsterSpeed = mapFile["monster_speed_init"]
        levelPathMap = map2pathmap(mapFile["map_data_file"])
        spriteList.append([229, 229, 0, 0, 0, 0])

    elif mapFile["monstre_spawn_time"] >= 0:
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
        return levelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, timerValue, keyNumber, mapFile["key_pool"], monsterActivate, monsterPosX, monsterPosY, monsterSpeed, pathMap, mapFile["level_id"], hard, keyboard)
    elif mapFile["monstre_spawn_time"] == -2:
        return outsideLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, monsterPosX, monsterPosY, monsterSpeed, pathMap, mapFile["level_id"], hard, keyboard)
    else:
        return safeLevelUpdate(console, levelMap, playerPosX, playerPosY, playerAngle, sprintLevel, maxSprintLevel, spriteList, keyboard)


def title(console, keyboard):
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
        if keyboard["k_en"] == 1:
            play.stop()
            console.clear()
            break
        console.addch(SY+1, SX+1, " ")


def playSmallCinematic(console):
    engineCinematic(console, "cine/cine_lobby5.yaml")
    engineCinematic(console, "cine/cine_lobby6.yaml")


def playFullCinematic(console):
    for i in range(5):
        engineCinematic(console, "cine/cine_outside" + str(i+1) + ".yaml")
    for i in range(4):
        engineCinematic(console, "cine/cine_lobby" + str(i+1) + ".yaml")

    playSmallCinematic(console)


def main(console):
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

    keyboard = {
        "k_up": 0,
        "k_dw": 0,
        "k_le": 0,
        "k_rg": 0,
        "k_en": 0,
        "k_sf": 0
    }

    listener = pynput.keyboard.Listener(on_press=createOnPress(keyboard), on_release=createOnRelease(keyboard))
    listener.start()

    title(console, keyboard)
    brouillage(console, 0.25, False)
    
    with open("save.yaml") as f:
        savedata = yaml.safe_load(f)
        if savedata[0]["completed"] == True or savedata[2]["completed"] == True:
            playSmallCinematic(console)
        else:
            playFullCinematic(console)

    newLevel = "map/map_lobby.yaml"
    hard = False
    
    while 1:
        newLevel, hard = level(console, newLevel, hard, keyboard)


if __name__ == "__main__":
    curses.wrapper(main)