
import json
import pytest

from theories import sauvegarder_theorie, charger_theorie
from defauts import lire_defaut


def test_save_and_load(tmp_path):
    monde = ["p", "q -> r"]

    defauts = [
        lire_defaut("p : q / r")
    ]

    fichier = tmp_path / "theorie.json"

    sauvegarder_theorie(fichier, monde, defauts)

    monde_charge, defauts_charges = charger_theorie(fichier)

    assert monde_charge == monde
    assert len(defauts_charges) == 1
    assert str(defauts_charges[0]) == "p : q / r"


def test_save_empty_theory(tmp_path):
    fichier = tmp_path / "vide.json"

    sauvegarder_theorie(fichier, [], [])

    monde, defauts = charger_theorie(fichier)

    assert monde == []
    assert defauts == []


def test_invalid_json_structure(tmp_path):
    fichier = tmp_path / "incorrect.json"

    fichier.write_text(
        json.dumps({"formules": ["p"]}),
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        charger_theorie(fichier)


def test_invalid_formula_in_file(tmp_path):
    fichier = tmp_path / "incorrect.json"

    fichier.write_text(
        json.dumps({
            "monde": ["p &"],
            "defauts": []
        }),
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        charger_theorie(fichier)
