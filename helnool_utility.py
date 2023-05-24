"""
Fonctions générales qui sont utilisés à plusieurs endroits
du code.
"""
import math
import yaml
import helnool_constants as h_co

def createimage(console, write_pixel, name, pos_y, pos_x):
    """
    Affiche une image à l'écran à une certaine position.

    Paramètres
    ----------
    console : 
        La fenêtre représentant l'écran avec Curses
        ou la pixel_array représentant l'écran avec Pygame

    write_pixel :
        La fonction qui dessine un pixel à l'écran
    
    name :
        Nom du fichier de l'image

    pos_y :
        Position Y de l'image à dessiner

    pos_x: 
        Position X de l'image à dessiner

    """
    with open(name, "rb") as data_file:
        data = data_file.read()
        index = 3
        for col in range(data[1]):
            if col+pos_y >= h_co.SY:
                break
            for lin in range(data[0]):
                index += 1
                if lin+pos_x >= h_co.SX:
                    continue
                if data[index-1] == 201:
                    continue
                write_pixel(console, data[index-1], col+pos_y, lin+pos_x)


def loadtexture(name):
    """
    Charge une texture.

    Paramètres
    ----------
    name :
        Le nom du fichier de la texture à charger

    Retourne
    --------
    tuple :
        Données de la texture

    """
    with open(name, "rb") as data_file:
        data = data_file.read()
        index = 4
        textu = []
        for _ in range(data[1]):
            x_textu = []
            for __ in range(data[0]):
                x_textu.append(data[index-1])
                index += 1
            textu.append(x_textu)
    return tuple(textu)


def map2pathmap(name):
    """
    Charge un fichier map et le transforme en
    tuple utilisable par la librarie Pathfinding.

    Paramètres
    ----------
    name :
        Le nom du fichier de la map à charger

    Retourne
    --------
    tuple :
        Données de la map sous format utilisable
        par la librairie Pathfinding

    """
    pathmap = list(loadtexture(name))
    for i, _ in enumerate(pathmap):
        for j in range(len(pathmap[i])):
            if pathmap[i][j] > 0:
                pathmap[i][j] = 0
            else:
                pathmap[i][j] = 1
    return tuple(pathmap)


def loadmap(mapfile):
    """
    Charge un fichier de niveau.

    Paramètres
    ----------
    mapfile :
        Le nom du fichier du niveau à charger

    Retourne
    --------
    dict :
        Données du niveau

    """
    with open(mapfile, "r", encoding="utf8") as data_file:
        mapfiledata = yaml.safe_load(data_file)
    return mapfiledata


def save_game(save_file, level_id, value):
    """
    Sauvegarde la partie sur un fichier YAML.

    Paramètres
    ----------
    save_file :
        Le nom du fichier YAML sur lequel sauvegarder

    level_id :
        Le numéro du niveau sur lequel on doit changer
        les données.

    value :
        La donnée du fichier sauvegarde à changer

    """
    with open(save_file, "r", encoding="utf8") as data_file:
        save_data = yaml.safe_load(data_file)
    save_data[level_id][value] = True
    with open(save_file, "w", encoding="utf8") as data_file:
        yaml.dump(save_data, data_file)


def normalize(vector):
    """
    Normalise un vecteur

    Paramètres
    ----------
    vector :
        Le vecteur à normaliser

    Retourne
    --------
    float :
        Composante X du vecteur normalisé

    Float :
        Composante Y du vecteur normalisé

    """
    norme = math.sqrt(vector[0]**2 + vector[1]**2)
    if norme == 0:
        return 0, 0
    return vector[0]/norme, vector[1]/norme
