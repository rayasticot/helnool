"""
Données de toutes les textures utilisées à
travers le jeu.
"""
import helnool_utility as h_ut

brique = h_ut.loadtexture("img/brak.legba")
brique_d = h_ut.loadtexture("img/brakd.legba")
toile = h_ut.loadtexture("img/toile.legba")
toile_d = h_ut.loadtexture("img/toile_d.legba")
labo = h_ut.loadtexture("img/labo.legba")
labo_d = h_ut.loadtexture("img/labo_d.legba")
herb = h_ut.loadtexture("img/herb.legba")
herb_d = h_ut.loadtexture("img/herb_d.legba")
filet = h_ut.loadtexture("img/filet.legba")
eye = h_ut.loadtexture("img/eye.legba")
eye_d = h_ut.loadtexture("img/eye_d.legba")
keyhole = h_ut.loadtexture("img/elevator.legba")
samsung = h_ut.loadtexture("img/samsung.legba")
samsung_d = h_ut.loadtexture("img/samsung_d.legba")
concrete = h_ut.loadtexture("img/concrete.legba")
concrete_d = h_ut.loadtexture("img/concrete_d.legba")
box = h_ut.loadtexture("img/box.legba")
box_d = h_ut.loadtexture("img/box_d.legba")
boxdark = h_ut.loadtexture("img/boxdark.legba")
boxdark_d = h_ut.loadtexture("img/boxdark_d.legba")
boxlight = h_ut.loadtexture("img/boxlight.legba")
boxlight_d = h_ut.loadtexture("img/boxlight_d.legba")
door = h_ut.loadtexture("img/door.legba")
induwall = h_ut.loadtexture("img/induwall.legba")
induwall_d = h_ut.loadtexture("img/induwall_d.legba")
bloodwall = h_ut.loadtexture("img/bloodwall.legba")
bloodwall_d = h_ut.loadtexture("img/bloodwall_d.legba")
colorwall = h_ut.loadtexture("img/colorwall.legba")
colorwall_d = h_ut.loadtexture("img/colorwall_d.legba")
chickenwall = h_ut.loadtexture("img/wallchicken.legba")
chickenwall_d = h_ut.loadtexture("img/wallchicken_d.legba")
chickenpanneau = h_ut.loadtexture("img/chickenpanneau.legba")
chickenpanneau_d = h_ut.loadtexture("img/chickenpanneau_d.legba")
caisse = h_ut.loadtexture("img/caisse.legba")
caisse_d = h_ut.loadtexture("img/caisse_d.legba")
icewall = h_ut.loadtexture("img/icewall.legba")
icewall_d = h_ut.loadtexture("img/icewall_d.legba")
window = h_ut.loadtexture("img/window.legba")
backwall = h_ut.loadtexture("img/backwall.legba")
backwall_d = h_ut.loadtexture("img/backwall_d.legba")
peur1 = h_ut.loadtexture("img/mons1.legba")
peur2 = h_ut.loadtexture("img/mons2.legba")
peur3 = h_ut.loadtexture("img/mons3.legba")
peur4 = h_ut.loadtexture("img/mons4.legba")
cle = h_ut.loadtexture("img/cle.legba")
gun = h_ut.loadtexture("img/gun.legba")
courir = h_ut.loadtexture("img/courir.legba")
retour = h_ut.loadtexture("img/retour.legba")
bureautest = h_ut.loadtexture("img/bureautest.legba")
toilette = h_ut.loadtexture("img/toilette.legba")
chickentable = h_ut.loadtexture("img/chickentable.legba")
pouletpend = h_ut.loadtexture("img/pouletpend.legba")
toyota = h_ut.loadtexture("img/toyota.legba")
zakfront0 = h_ut.loadtexture("img/zakfront0.legba")
zakfront1 = h_ut.loadtexture("img/zakfront1.legba")
zakfront2 = h_ut.loadtexture("img/zakfront2.legba")
zakback0 = h_ut.loadtexture("img/zakback0.legba")
zaktoc0 = h_ut.loadtexture("img/zaktoc0.legba")
zaktoc1 = h_ut.loadtexture("img/zaktoc1.legba")

text_index = (
    (brique, brique_d), (toile, toile_d), (herb, herb_d),
    (filet, filet), (eye, eye_d), (labo, labo_d),
    (concrete, concrete_d), (box, box_d), (samsung, samsung_d),
    (keyhole, keyhole), (door, door), (induwall, induwall_d),
    (bloodwall, bloodwall_d), (colorwall, colorwall_d),
    (chickenwall, chickenwall_d), (chickenpanneau, chickenpanneau),
    (caisse, caisse_d), (icewall, icewall_d), (window, window),
    (backwall, backwall_d), (boxdark, boxdark_d), (boxlight, boxlight_d)
)
sprite_tex_index = (
    peur1, peur2, peur3, cle, gun, peur4, courir, retour, bureautest, toilette,
    chickentable, pouletpend, toyota, zakfront0, zakfront1, zakfront2, zakback0, zaktoc0, zaktoc1
)
