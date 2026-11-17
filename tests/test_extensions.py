
from defauts import lire_defaut
from extensions import (
    calculer_extensions,
    consequence_credulous,
    consequence_sceptique
)


def test_no_defaults():
    extensions = calculer_extensions(["p"], [])

    assert len(extensions) == 1


def test_empty_theory():
    extensions = calculer_extensions([], [])

    assert len(extensions) == 1


def test_default_without_prerequisite():
    defauts = [lire_defaut(": p / q")]

    extensions = calculer_extensions([], defauts)

    assert len(extensions) == 1
    assert consequence_sceptique(extensions, "q")


def test_default_with_false_prerequisite():
    defauts = [lire_defaut("p : q / r")]

    extensions = calculer_extensions(["~p"], defauts)

    assert len(extensions) == 1
    assert not consequence_credulous(extensions, "r")


def test_default_with_inconsistent_justification():
    defauts = [lire_defaut("p : q / r")]

    extensions = calculer_extensions(["p", "~q"], defauts)

    assert len(extensions) == 1
    assert not consequence_credulous(extensions, "r")


def test_nixon_diamond_two_extensions():
    W = ["Quaker", "Republican"]

    defauts = [
        lire_defaut("Quaker : Pacifist / Pacifist"),
        lire_defaut("Republican : ~Pacifist / ~Pacifist")
    ]

    extensions = calculer_extensions(W, defauts)

    assert len(extensions) == 2


def test_credulous_consequence():
    W = ["Quaker", "Republican"]

    defauts = [
        lire_defaut("Quaker : Pacifist / Pacifist"),
        lire_defaut("Republican : ~Pacifist / ~Pacifist")
    ]

    extensions = calculer_extensions(W, defauts)

    assert consequence_credulous(extensions, "Pacifist")
    assert consequence_credulous(extensions, "~Pacifist")


def test_skeptical_consequence():
    W = ["Quaker", "Republican"]

    defauts = [
        lire_defaut("Quaker : Pacifist / Pacifist"),
        lire_defaut("Republican : ~Pacifist / ~Pacifist")
    ]

    extensions = calculer_extensions(W, defauts)

    assert consequence_sceptique(extensions, "Quaker")
    assert consequence_sceptique(extensions, "Republican")
    assert not consequence_sceptique(extensions, "Pacifist")


def test_inconsistent_world():
    extensions = calculer_extensions(["p", "~p"], [])

    assert len(extensions) == 1
    assert consequence_sceptique(extensions, "q")


def test_two_conflicting_defaults():
    defauts = [
        lire_defaut(": p / p"),
        lire_defaut(": ~p / ~p")
    ]

    extensions = calculer_extensions([], defauts)

    # Deux extensions existent
    assert len(extensions) == 2

    # p est une conséquence crédule
    assert consequence_credulous(extensions, "p")

    # ~p est aussi une conséquence crédule
    assert consequence_credulous(extensions, "~p")

    # Aucune des deux formules n'est une conséquence sceptique
    assert not consequence_sceptique(extensions, "p")
    assert not consequence_sceptique(extensions, "~p")
