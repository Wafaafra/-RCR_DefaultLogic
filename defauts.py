
from dataclasses import dataclass
from formules import lire_formule, afficher_formule
from raisonnement import est_satisfiable


@dataclass
class Defaut:
    prerequis: object
    justifications: list
    conclusion: object

    def __str__(self):
        prerequis = (
            afficher_formule(self.prerequis)
            if self.prerequis is not None
            else ""
        )

        justifications = ", ".join(
            afficher_formule(j) for j in self.justifications
        )

        conclusion = afficher_formule(self.conclusion)

        return f"{prerequis} : {justifications} / {conclusion}"


def _separer_justifications(texte):
    """Sépare les justifications par virgule, sans couper les parenthèses."""
    morceaux = []
    debut = 0
    profondeur = 0

    for i, caractere in enumerate(texte):
        if caractere == "(":
            profondeur += 1
        elif caractere == ")":
            profondeur -= 1
            if profondeur < 0:
                raise ValueError("Parenthèses incorrectes dans les justifications.")
        elif caractere == "," and profondeur == 0:
            morceaux.append(texte[debut:i].strip())
            debut = i + 1

    if profondeur != 0:
        raise ValueError("Parenthèses incorrectes dans les justifications.")

    morceaux.append(texte[debut:].strip())

    if any(not morceau for morceau in morceaux):
        raise ValueError("Une justification ne peut pas être vide.")

    return morceaux


def lire_defaut(texte):
    """
    Lit un défaut sous la forme :
    prerequis : justification1, justification2 / conclusion

    Le prérequis peut être vide.
    """
    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("Le défaut ne peut pas être vide.")

    parties = texte.split("/")

    if len(parties) != 2:
        raise ValueError("Le défaut doit contenir un seul '/'.")

    partie_gauche = parties[0].strip()
    partie_droite = parties[1].strip()

    if not partie_droite:
        raise ValueError("La conclusion ne peut pas être vide.")

    if ":" in partie_gauche:
        prerequis_texte, justifications_texte = partie_gauche.split(":", 1)
        prerequis_texte = prerequis_texte.strip()
    else:
        # Sans deux-points, on considère le prérequis comme vide.
        prerequis_texte = ""
        justifications_texte = partie_gauche

    if not justifications_texte.strip():
        raise ValueError("Le défaut doit contenir au moins une justification.")

    prerequis = (
        lire_formule(prerequis_texte)
        if prerequis_texte
        else None
    )

    justifications = [
        lire_formule(j)
        for j in _separer_justifications(justifications_texte)
    ]

    conclusion = lire_formule(partie_droite)

    return Defaut(prerequis, justifications, conclusion)


def verifier_justifications(defaut):
    """
    Retourne les justifications qui sont individuellement insatisfaisables.
    """
    invalides = []

    for justification in defaut.justifications:
        if not est_satisfiable(justification):
            invalides.append(justification)

    return invalides


def lire_defauts(lignes):
    """Lit plusieurs défauts et retourne les défauts valides."""
    defauts = []

    for numero, ligne in enumerate(lignes, start=1):
        if not ligne.strip():
            continue

        try:
            defaut = lire_defaut(ligne)
            defauts.append(defaut)

            invalides = verifier_justifications(defaut)

            if invalides:
                noms = ", ".join(
                    afficher_formule(j) for j in invalides
                )
                print(
                    f"Avertissement (ligne {numero}) : "
                    f"justification(s) incohérente(s) : {noms}"
                )

        except ValueError as erreur:
            raise ValueError(
                f"Erreur dans le défaut à la ligne {numero} : {erreur}"
            )

    return defauts
