"""
Remet la sauvegarde à sa valeur par défaut.
"""

import yaml

if __name__ == "__main__":
    with open("settings_default.yaml", encoding="utf8") as fichier:
        default_settings = yaml.safe_load(fichier)
    with open("settings.yaml", "w", encoding="utf8") as fichier:
        yaml.dump(default_settings, fichier)