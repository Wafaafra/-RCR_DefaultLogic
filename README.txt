# Mini-projet 1 : Logique des défauts

Module : Représentation de Connaissances et Raisonnement  
Niveau : 4-ING-IA  
Établissement : USTHB

## 1. Présentation

Ce projet consiste à développer une application Python permettant de représenter et de raisonner sur des connaissances à l'aide de la logique des défauts de Reiter.

L'application permet de définir une théorie composée d'un ensemble de formules mondiales W et d'un ensemble de défauts D, de calculer ses extensions et de tester les conséquences crédules et sceptiques.

## 2. Fonctionnalités

- Saisie des formules de l'ensemble W.
- Saisie des défauts de l'ensemble D.
- Analyse syntaxique et validation des formules.
- Vérification de la cohérence des justifications.
- Calcul des extensions de la théorie.
- Vérification des conséquences crédules et sceptiques.
- Sauvegarde et chargement des théories au format JSON.
- Interface graphique avec PyQt6.

## 3. Technologies utilisées

- Python 3
- PyQt6 : interface graphique.
- SymPy : manipulation logique et vérification de satisfiabilité.
- Pytest : tests automatisés.

## 4. Installation

Créer un environnement virtuel :

    python -m venv .venv

Activer l'environnement sous Windows :

    .venv\Scripts\activate

Installer les dépendances :

    pip install -r requirements.txt

## 5. Exécution

Lancer l'application avec :

    python main.py

## 6. Syntaxe des formules

Les opérateurs logiques acceptés sont :

- ~ : négation
- & : conjonction
- | : disjonction
- -> : implication
- <-> : équivalence

Les constantes logiques sont :

- true : vrai
- false : faux

Exemples :

    Homme(Pierre)
    Sportif(Pierre) -> Homme(Pierre)
    Chanter(Pierre) & ~Danser(Pierre)

## 7. Syntaxe des défauts

Un défaut est écrit sous la forme :

    Prérequis : Justification1, Justification2 / Conclusion

Exemple :

    Homme(Pierre) : Chanter(Pierre) / Chanter(Pierre)

Le prérequis peut être vide :

    : Voler(oiseau) / Voler(oiseau)

## 8. Tests

Pour exécuter les tests automatisés :

    pytest -v

Les tests couvrent les différents modules du projet, notamment l'analyse des formules, le raisonnement, les défauts, le calcul des extensions et la sauvegarde des théories.

## 9. Architecture du projet

- formules.py : analyse syntaxique des formules logiques.
- raisonnement.py : opérations de raisonnement et vérification logique.
- defauts.py : représentation et analyse des défauts.
- extensions.py : calcul des extensions et conséquences.
- theories.py : sauvegarde et chargement des théories.
- interface.py : interface graphique.
- main.py : point d'entrée de l'application.
- tests/ : tests automatisés.

## 10. Limites

L'application traite les formules comme des propositions atomiques. Les expressions de type prédicat, par exemple Homme(Pierre), sont considérées comme des atomes propositionnels. La logique du premier ordre complète, notamment les quantificateurs, n'est pas prise en charge.

Le calcul des extensions repose sur l'exploration des combinaisons de défauts. Le temps de calcul peut donc augmenter avec le nombre de défauts.
