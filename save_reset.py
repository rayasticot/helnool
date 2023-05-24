"""
Remet la sauvegarde à sa valeur par défaut.
"""

import yaml

if __name__ == "__main__":
    with open("save_default.yaml", encoding="utf8") as fichier:
        default_save = yaml.safe_load(fichier)
    with open("save.yaml", "w", encoding="utf8") as fichier:
        yaml.dump(default_save, fichier)