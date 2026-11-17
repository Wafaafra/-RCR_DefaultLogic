
from defauts import lire_defaut
from extensions import (
    calculer_extensions,
    consequence_credulous,
    consequence_sceptique
)


def test_exercice_hommes_sportifs_chant():
    W = [
        "Sportif(Pierre)",
        "Homme(Pascal)",
        "Sportif(Pierre) -> Homme(Pierre)"
    ]

    D = [
        lire_defaut("Homme(Pierre) : Chanter(Pierre) / Chanter(Pierre)"),
        lire_defaut("Homme(Pascal) : Chanter(Pascal) / Chanter(Pascal)"),
        lire_defaut("Sportif(Pierre) : ~Chanter(Pierre) / ~Chanter(Pierre)")
    ]

    extensions = calculer_extensions(W, D)

    assert len(extensions) == 2

    # Pierre peut aimer chanter ou ne pas aimer chanter.
    assert consequence_credulous(extensions, "Chanter(Pierre)")
    assert consequence_credulous(extensions, "~Chanter(Pierre)")

    # Aucune conclusion sur Pierre n'est sceptique.
    assert not consequence_sceptique(extensions, "Chanter(Pierre)")
    assert not consequence_sceptique(extensions, "~Chanter(Pierre)")

    # Pascal est un homme : le défaut général s'applique.
    assert consequence_sceptique(extensions, "Chanter(Pascal)")
