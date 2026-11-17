
from dataclasses import dataclass
from itertools import combinations

from formules import lire_formule, afficher_formule
from raisonnement import consequence_logique, est_consistant
from defauts import Defaut


@dataclass
class Extension:
    # Base finie qui engendre l'extension : E = Th(base)
    base: list
    defauts_appliques: list

    def __str__(self):
        formules = ", ".join(
            afficher_formule(f) for f in self.base
        )
        noms = ", ".join(
            str(d) for d in self.defauts_appliques
        )

        return (
            f"Base de l'extension : {{{formules}}}\n"
            f"Défauts appliqués : {{{noms}}}"
        )


def _preparer_base(base):
    """Convertit une base textuelle ou symbolique en liste de formules."""
    if isinstance(base, str):
        base = [base]

    resultat = []
    for formule in base:
        if isinstance(formule, str):
            formule = lire_formule(formule)
        resultat.append(formule)

    return resultat


def _est_applicable(defaut, base):
    """
    Vérifie si un défaut est applicable dans une base T.

    Conditions :
    - le prérequis est une conséquence logique de T ;
    - chaque justification est individuellement cohérente
      avec T.
    """
    if defaut.prerequis is not None:
        if not consequence_logique(base, defaut.prerequis):
            return False

    for justification in defaut.justifications:
        if not est_consistant(base + [justification]):
            return False

    return True


def _bases_equivalentes(base1, base2):
    """Vérifie si deux bases engendrent la même clôture logique."""
    for formule in base1:
        if not consequence_logique(base2, formule):
            return False

    for formule in base2:
        if not consequence_logique(base1, formule):
            return False

    return True


def calculer_extensions(base_mondiale, defauts):
    """
    Calcule les extensions d'une théorie de défauts (W, D).

    On examine chaque sous-ensemble S de défauts.
    T_S = W + conclusions des défauts de S.

    S est accepté si les défauts applicables dans T_S
    sont exactement ceux qui appartiennent à S.
    """
    W = _preparer_base(base_mondiale)
    nombre = len(defauts)

    extensions = []

    # Énumération de tous les sous-ensembles de défauts
    for taille in range(nombre + 1):
        for indices in combinations(range(nombre), taille):

            # Défauts supposés appliqués dans ce candidat
            selection = [defauts[i] for i in indices]

            # Construction de T_S
            base_candidate = W + [
                defaut.conclusion for defaut in selection
            ]

            # Calcul des défauts réellement applicables
            applicables = [
                i for i, defaut in enumerate(defauts)
                if _est_applicable(defaut, base_candidate)
            ]

            # Vérification du point fixe : S = applicables
            if set(indices) != set(applicables):
                continue

            # Élimination des extensions équivalentes
            deja_presente = any(
                _bases_equivalentes(
                    base_candidate, extension.base
                )
                for extension in extensions
            )

            if not deja_presente:
                extensions.append(
                    Extension(
                        base=base_candidate,
                        defauts_appliques=selection
                    )
                )

    return extensions


def consequence_credulous(extensions, formule):
    """
    Vrai si la formule est conséquence logique
    d'au moins une extension.
    """
    formule = lire_formule(formule) if isinstance(formule, str) else formule

    return any(
        consequence_logique(extension.base, formule)
        for extension in extensions
    )


def consequence_sceptique(extensions, formule):
    """
    Vrai si la formule est conséquence logique
    de toutes les extensions.

    Par convention, retourne False si aucune extension n'existe.
    """
    if not extensions:
        return False

    formule = lire_formule(formule) if isinstance(formule, str) else formule

    return all(
        consequence_logique(extension.base, formule)
        for extension in extensions
    )
