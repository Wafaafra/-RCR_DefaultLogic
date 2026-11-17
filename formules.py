
import re

from sympy import Symbol, true, false
from sympy.logic.boolalg import Not, And, Or, Implies, Equivalent


# Recognizes logical operators, parentheses and atomic propositions.
# P(x) is treated as one indivisible proposition.
TOKEN_PATTERN = re.compile(
    r"\s*(<->|->|[~&|()]|[A-Za-z_][A-Za-z0-9_]*(?:\s*\([^()]*\))?)"
)


def tokeniser(texte):
    """Convert a formula into a list of tokens."""
    tokens = []
    position = 0

    while position < len(texte):
        # Ignore trailing whitespace
        if texte[position:].strip() == "":
            break

        match = TOKEN_PATTERN.match(texte, position)

        if not match:
            raise ValueError(
                f"Caractère ou élément invalide à la position {position}."
            )

        tokens.append(match.group(1).strip())
        position = match.end()

    return tokens


class Parseur:
    """Recursive-descent parser for propositional logic."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def courant(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def accepter(self, token):
        if self.courant() == token:
            self.position += 1
            return True
        return False

    def analyser(self):
        formule = self.equivalence()

        if self.courant() is not None:
            raise ValueError(
                f"Élément inattendu : {self.courant()}"
            )

        return formule

    # Lowest precedence: equivalence
    def equivalence(self):
        gauche = self.implication()

        while self.accepter("<->"):
            droite = self.implication()
            gauche = Equivalent(gauche, droite)

        return gauche

    # Implication is right-associative
    def implication(self):
        gauche = self.disjonction()

        if self.accepter("->"):
            droite = self.implication()
            return Implies(gauche, droite)

        return gauche

    # OR
    def disjonction(self):
        gauche = self.conjonction()

        while self.accepter("|"):
            droite = self.conjonction()
            gauche = Or(gauche, droite)

        return gauche

    # AND
    def conjonction(self):
        gauche = self.negation()

        while self.accepter("&"):
            droite = self.negation()
            gauche = And(gauche, droite)

        return gauche

    # NOT, parentheses and atoms
    def negation(self):
        if self.accepter("~"):
            return Not(self.negation())

        if self.accepter("("):
            formule = self.equivalence()

            if not self.accepter(")"):
                raise ValueError("Parenthèse fermante manquante.")

            return formule

        token = self.courant()

        if token is None or token in ("&", "|", "->", "<->", ")"):
            raise ValueError("Formule incomplète ou syntaxe incorrecte.")

        self.position += 1

        if token.lower() == "true":
            return true

        if token.lower() == "false":
            return false

        return Symbol(token)


def lire_formule(texte):
    """
    Transforme une formule textuelle en expression logique SymPy.

    Syntaxe :
    ~p, p & q, p | q, p -> q, p <-> q
    Parentheses and predicates such as P(x) are supported.
    """

    if not isinstance(texte, str) or not texte.strip():
        raise ValueError("La formule ne peut pas être vide.")

    tokens = tokeniser(texte)
    parseur = Parseur(tokens)

    return parseur.analyser()


def afficher_formule(formule):
    """Convert a SymPy formula back into readable logical notation."""

    if formule == true:
        return "true"

    if formule == false:
        return "false"

    if isinstance(formule, Symbol):
        return str(formule)

    if isinstance(formule, Not):
        enfant = formule.args[0]
        texte = afficher_formule(enfant)

        if isinstance(enfant, Symbol) or enfant in (true, false):
            return "~" + texte

        return "~(" + texte + ")"

    if isinstance(formule, And):
        return " & ".join(
            _parentheser(arg) for arg in formule.args
        )

    if isinstance(formule, Or):
        return " | ".join(
            _parentheser(arg) for arg in formule.args
        )

    if isinstance(formule, Implies):
        gauche, droite = formule.args
        return f"{_parentheser(gauche)} -> {_parentheser(droite)}"

    if isinstance(formule, Equivalent):
        gauche, droite = formule.args
        return f"{_parentheser(gauche)} <-> {_parentheser(droite)}"

    return str(formule)


def _parentheser(formule):
    texte = afficher_formule(formule)

    if isinstance(formule, Symbol) or formule in (true, false):
        return texte

    return f"({texte})"


def variables(formules):
    """
    Return the unique proposition names in a formula
    or in a collection of formulas.
    """

    if hasattr(formules, "free_symbols"):
        formules = [formules]

    resultat = set()

    for formule in formules:
        resultat.update(str(symbole) for symbole in formule.free_symbols)

    return sorted(resultat)
