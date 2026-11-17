
from raisonnement import (
    est_satisfiable,
    est_tautologie,
    est_consistant,
    consequence_logique,
    trouver_modele
)


def test_satisfiable():
    assert est_satisfiable("p | q") is True


def test_unsatisfiable():
    assert est_satisfiable("p & ~p") is False


def test_tautologie():
    assert est_tautologie("p | ~p") is True


def test_not_tautologie():
    assert est_tautologie("p & q") is False


def test_consistent():
    assert est_consistant(["p", "p -> q"]) is True


def test_inconsistent():
    assert est_consistant(["p", "~p"]) is False


def test_logical_consequence():
    base = ["p", "p -> q"]

    assert consequence_logique(base, "q") is True


def test_not_logical_consequence():
    base = ["p | q"]

    assert consequence_logique(base, "p") is False


def test_find_model():
    modele = trouver_modele(["p", "p -> q"])

    assert modele is not None
    assert modele["p"] is True
    assert modele["q"] is True


def test_no_model():
    modele = trouver_modele(["p", "~p"])

    assert modele is None
