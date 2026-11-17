
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QGroupBox
)

from formules import lire_formule, afficher_formule
from defauts import lire_defaut, verifier_justifications
from extensions import (
    calculer_extensions,
    consequence_credulous,
    consequence_sceptique
)
from theories import sauvegarder_theorie, charger_theorie


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logique des défauts - Reiter")
        self.setMinimumSize(850, 700)

        self.extensions = []

        self.creer_interface()

    def creer_interface(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Titre
        titre = QLabel("Système de logique des défauts")
        titre.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2457A6;"
        )
        layout.addWidget(titre)

        description = QLabel(
            "Entrez votre base de connaissances et vos défauts "
            "pour calculer les extensions de Reiter."
        )
        layout.addWidget(description)

        # Base de connaissances W
        groupe_monde = QGroupBox("1. Base de connaissances (W)")
        monde_layout = QVBoxLayout()

        self.zone_monde = QTextEdit()
        self.zone_monde.setPlaceholderText(
            "Entrez une formule par ligne.\n"
            "Exemple :\n"
            "Sportif(Pierre)\n"
            "Homme(Pascal)\n"
            "Sportif(Pierre) -> Homme(Pierre)"
        )

        monde_layout.addWidget(self.zone_monde)
        groupe_monde.setLayout(monde_layout)
        layout.addWidget(groupe_monde)

        # Ensemble des défauts D
        groupe_defauts = QGroupBox("2. Ensemble des défauts (D)")
        defauts_layout = QVBoxLayout()

        self.zone_defauts = QTextEdit()
        self.zone_defauts.setPlaceholderText(
            "Entrez un défaut par ligne.\n"
            "Format : prerequis : justification / conclusion\n"
            "Exemple :\n"
            "p : q / r\n"
            ": q / r"
        )

        defauts_layout.addWidget(self.zone_defauts)
        groupe_defauts.setLayout(defauts_layout)
        layout.addWidget(groupe_defauts)

        # Boutons principaux
        boutons_layout = QHBoxLayout()

        self.btn_calculer = QPushButton("Calculer les extensions")
        self.btn_calculer.clicked.connect(self.calculer)
        boutons_layout.addWidget(self.btn_calculer)

        self.btn_sauvegarder = QPushButton("Sauvegarder")
        self.btn_sauvegarder.clicked.connect(self.sauvegarder)
        boutons_layout.addWidget(self.btn_sauvegarder)

        self.btn_charger = QPushButton("Charger")
        self.btn_charger.clicked.connect(self.charger)
        boutons_layout.addWidget(self.btn_charger)

        layout.addLayout(boutons_layout)

        # Résultats
        groupe_resultats = QGroupBox("3. Extensions obtenues")
        resultats_layout = QVBoxLayout()

        self.zone_resultats = QTextEdit()
        self.zone_resultats.setReadOnly(True)
        self.zone_resultats.setPlaceholderText(
            "Les extensions calculées apparaîtront ici."
        )

        resultats_layout.addWidget(self.zone_resultats)
        groupe_resultats.setLayout(resultats_layout)
        layout.addWidget(groupe_resultats)

        # Test de conséquence
        groupe_requete = QGroupBox(
            "4. Tester une conséquence (crédule / sceptique)"
        )
        requete_layout = QVBoxLayout()

        self.champ_requete = QLineEdit()
        self.champ_requete.setPlaceholderText(
            "Entrez une formule, par exemple : p"
        )
        requete_layout.addWidget(self.champ_requete)

        self.btn_tester = QPushButton("Tester la conséquence")
        self.btn_tester.clicked.connect(self.tester_consequence)
        requete_layout.addWidget(self.btn_tester)

        self.zone_requete_resultat = QLabel(
            "Le résultat du test apparaîtra ici."
        )
        self.zone_requete_resultat.setWordWrap(True)
        requete_layout.addWidget(self.zone_requete_resultat)

        groupe_requete.setLayout(requete_layout)
        layout.addWidget(groupe_requete)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F4F6FA;
            }

            QLabel {
                color: #263445;
            }

            QGroupBox {
                color: #263445;
                font-weight: bold;
                border: 1px solid #C8D1E0;
                border-radius: 8px;
                margin-top: 14px;
                padding: 12px;
                background-color: white;
            }

            QGroupBox::title {
                color: #2457A6;
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }

            QTextEdit, QLineEdit {
                color: #263445;
                border: 1px solid #C8D1E0;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                selection-background-color: #2457A6;
            }

            QPushButton {
                background-color: #2457A6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 11px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #17427F;
            }

            QPushButton:pressed {
                background-color: #123563;
            }
        """)



    def lire_entrees(self):
        """Récupère et valide les données saisies."""

        monde = [
            ligne.strip()
            for ligne in self.zone_monde.toPlainText().splitlines()
            if ligne.strip()
        ]

        textes_defauts = [
            ligne.strip()
            for ligne in self.zone_defauts.toPlainText().splitlines()
            if ligne.strip()
        ]

        # Vérifier les formules du monde
        for formule in monde:
            lire_formule(formule)

        # Lire les défauts
        defauts = [
            lire_defaut(texte)
            for texte in textes_defauts
        ]

        return monde, defauts

    def calculer(self):
        try:
            monde, defauts = self.lire_entrees()

            # Calcul des extensions par le module logique
            self.extensions = calculer_extensions(monde, defauts)

            self.zone_resultats.clear()

            if not self.extensions:
                self.zone_resultats.setPlainText(
                    "Aucune extension trouvée."
                )
            else:
                texte = (
                    f"Nombre d'extensions trouvées : "
                    f"{len(self.extensions)}\n\n"
                )

                for i, extension in enumerate(self.extensions, start=1):
                    texte += f"EXTENSION {i}\n"
                    texte += str(extension)
                    texte += "\n\n" + "-" * 50 + "\n\n"

                self.zone_resultats.setPlainText(texte)

            # Vérifier les justifications incohérentes
            avertissements = []

            for numero, defaut in enumerate(defauts, start=1):
                invalides = verifier_justifications(defaut)

                for justification in invalides:
                    avertissements.append(
                        f"Défaut {numero} : "
                        f"{afficher_formule(justification)}"
                    )

            if avertissements:
                QMessageBox.warning(
                    self,
                    "Justifications incohérentes",
                    "Les justifications suivantes sont "
                    "individuellement insatisfaisables :\n\n"
                    + "\n".join(avertissements)
                )

            self.zone_requete_resultat.setText(
                "Extensions calculées. Vous pouvez tester une formule."
            )

        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur",
                str(erreur)
            )

    def tester_consequence(self):
        try:
            if not self.extensions:
                QMessageBox.warning(
                    self,
                    "Attention",
                    "Calculez d'abord les extensions."
                )
                return

            formule = self.champ_requete.text().strip()

            if not formule:
                QMessageBox.warning(
                    self,
                    "Attention",
                    "Entrez une formule à tester."
                )
                return

            # Les fonctions de conséquence effectuent le raisonnement
            credulous = consequence_credulous(
                self.extensions, formule
            )

            skeptical = consequence_sceptique(
                self.extensions, formule
            )

            resultat = (
                f"Formule testée : {formule}\n\n"
                f"Conséquence crédule : "
                f"{'OUI' if credulous else 'NON'}\n"
                f"Conséquence sceptique : "
                f"{'OUI' if skeptical else 'NON'}"
            )

            self.zone_requete_resultat.setText(resultat)

        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur",
                str(erreur)
            )

    def sauvegarder(self):
        try:
            monde, defauts = self.lire_entrees()

            fichier, _ = QFileDialog.getSaveFileName(
                self,
                "Sauvegarder la théorie",
                "",
                "Fichiers JSON (*.json)"
            )

            if not fichier:
                return

            if not fichier.lower().endswith(".json"):
                fichier += ".json"

            sauvegarder_theorie(fichier, monde, defauts)

            QMessageBox.information(
                self,
                "Succès",
                "La théorie a été sauvegardée."
            )

        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur",
                str(erreur)
            )

    def charger(self):
        fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Charger une théorie",
            "",
            "Fichiers JSON (*.json)"
        )

        if not fichier:
            return

        try:
            monde, defauts = charger_theorie(fichier)

            self.zone_monde.setPlainText(
                "\n".join(monde)
            )

            self.zone_defauts.setPlainText(
                "\n".join(str(d) for d in defauts)
            )

            self.extensions = []
            self.zone_resultats.clear()
            self.zone_requete_resultat.setText(
                "Théorie chargée. Cliquez sur "
                "'Calculer les extensions'."
            )

            QMessageBox.information(
                self,
                "Succès",
                "La théorie a été chargée."
            )

        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur",
                str(erreur)
            )


def lancer_application():
    app = QApplication(sys.argv)

    fenetre = MainWindow()
    fenetre.show()

    sys.exit(app.exec())
