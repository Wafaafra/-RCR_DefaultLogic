
from sympy import And, Not, Symbol, true, false
from sympy.logic.inference import satisfiable

from formules import lire_formule


def _preparer_formules(formules):
    """
    Convertit les formules textuelles en expressions SymPy.
    Accepte une formule seule ou une collection de formules.
    """
    if isinstance(formules, (list, tuple, set)):
        liste = list(formules)
    else:
        liste = [formules]

    resultat = []

    for formule in liste:
        if isinstance(formule, str):
            formule = lire_formule(formule)

        resultat.append(formule)

    return resultat


def est_satisfiable(formule):
    """
    Vérifie si une formule possède au moins une interprétation vraie.

    Retourne True si elle est satisfiable, False sinon.
    """
    formule = _preparer_formules(formule)[0]

    return satisfiable(formule) is not False


def est_tautologie(formule):
    """
    Vérifie si une formule est toujours vraie.

    Une formule est une tautologie si sa négation est insatisfiable.
    """
    formule = _preparer_formules(formule)[0]

    return satisfiable(Not(formule)) is False


def est_consistant(formules):
    """
    Vérifie si un ensemble de formules est cohérent.

    Un ensemble est consistant s'il existe au moins
    une interprétation qui rend toutes les formules vraies.
    """
    formules = _preparer_formules(formules)

    base = And(*formules)

    return satisfiable(base) is not False


def consequence_logique(base, formule):
    """
    Vérifie si une formule est une conséquence logique
    d'une base de connaissances.

    KB |= formule si KB ET NON(formule) est insatisfiable.
    """
    base = _preparer_formules(base)
    formule = _preparer_formules(formule)[0]

    ensemble = And(*(base + [Not(formule)]))

    return satisfiable(ensemble) is False


def trouver_modele(formules):
    """
    Cherche une interprétation qui satisfait toutes les formules.

    Retourne :
    - Un dictionnaire contenant une interprétation si elle existe.
    - None si l'ensemble est inconsistant.
    """
    formules = _preparer_formules(formules)

    base = And(*formules)

    resultat = satisfiable(base)

    if resultat is False:
        return None

    modele = {}

    for variable, valeur in resultat.items():
        modele[str(variable)] = bool(valeur)

    return modele
