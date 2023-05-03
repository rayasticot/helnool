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


def level(levelFileName):
    loadmap