
from formules import lire_formule, afficher_formule, variables


def test_simple_formula():
    f = lire_formule("p")
    assert str(f) == "p"


def test_negation():
    f = lire_formule("~p")
    assert "p" in afficher_formule(f)


def test_conjunction():
    f = lire_formule("p & q")
    assert len(f.args) == 2


def test_implication():
    f = lire_formule("p -> q")
    assert f is not None


def test_equivalence():
    f = lire_formule("p <-> q")
    assert f is not None


def test_variables():
    f = lire_formule("p & q")
    assert variables([f]) == ["p", "q"]
