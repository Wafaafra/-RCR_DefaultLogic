
import json
from pathlib import Path

from formules import lire_formule
from defauts import lire_defaut


def sauvegarder_theorie(fichier, monde, defauts):
    """
    Sauvegarde une théorie de défauts dans un fichier JSON.
    monde : liste de formules textuelles.
    defauts : liste de défauts (objets Defaut ou textes).
    """
    donnees = {
        "monde": [
            str(formule) for formule in monde
        ],
        "defauts": [
            str(defaut) if not isinstance(defaut, str) else defaut
            for defaut in defauts
        ]
    }

    chemin = Path(fichier)

    with chemin.open("w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)


def charger_theorie(fichier):
    """
    Charge une théorie depuis un fichier JSON.
    Retourne (monde, defauts).
    """
    chemin = Path(fichier)

    with chemin.open("r", encoding="utf-8") as f:
        donnees = json.load(f)

    if not isinstance(donnees, dict):
        raise ValueError("Le fichier doit contenir un objet JSON.")

    if "monde" not in donnees or "defauts" not in donnees:
        raise ValueError("Le fichier doit contenir 'monde' et 'defauts'.")

    monde = donnees["monde"]
    textes_defauts = donnees["defauts"]

    if not isinstance(monde, list) or not isinstance(textes_defauts, list):
        raise ValueError("'monde' et 'defauts' doivent être des listes.")

    # Vérifier les formules du monde
    for formule in monde:
        if not isinstance(formule, str):
            raise ValueError("Chaque formule du monde doit être un texte.")
        lire_formule(formule)

    # Recréer les objets Defaut
    defauts = [
        lire_defaut(texte) for texte in textes_defauts
    ]

    return monde, defauts
