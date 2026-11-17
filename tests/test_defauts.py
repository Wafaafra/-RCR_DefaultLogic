
import pytest

from defauts import (
    Defaut,
    lire_defaut,
    lire_defauts,
    verifier_justifications
)
from formules import afficher_formule


def test_read_default():
    d = lire_defaut("p : q / r")

    assert afficher_formule(d.prerequis) == "p"
    assert afficher_formule(d.justifications[0]) == "q"
    assert afficher_formule(d.conclusion) == "r"


def test_default_without_prerequisite():
    d = lire_defaut(": q / r")

    assert d.prerequis is None
    assert afficher_formule(d.conclusion) == "r"


def test_multiple_justifications():
    d = lire_defaut("p : q, r / s")

    assert len(d.justifications) == 2


def test_complex_justification():
    d = lire_defaut("p : (q & r), s / t")

    assert len(d.justifications) == 2


def test_inconsistent_justification():
    d = lire_defaut("p : (q & ~q) / r")

    invalides = verifier_justifications(d)

    assert len(invalides) == 1


def test_valid_justification():
    d = lire_defaut("p : q / r")

    assert verifier_justifications(d) == []


def test_missing_conclusion():
    with pytest.raises(ValueError):
        lire_defaut("p : q / ")


def test_missing_justification():
    with pytest.raises(ValueError):
        lire_defaut("p : / r")


def test_multiple_defaults():
    lignes = [
        "p : q / r",
        "a : b / c"
    ]

    defauts = lire_defauts(lignes)

    assert len(defauts) == 2
