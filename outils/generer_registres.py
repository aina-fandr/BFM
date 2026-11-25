from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from xlsx_compat import save_workbook_compatible


ROOT = Path(__file__).resolve().parents[1]
ESTIMATE_DATE = "2026-11-23"
USD_TO_MGA = 4598.727
UNIT_ESTIMATES_MGA = {
    "R01": 180_000,
    "R02": 160_000,
    "R03": 65_000,
    "R04": 45_000,
    "R05": 35_000,
    "R06": 10_000,
    "R07": 5_000,
    "M01": round(107.02 * USD_TO_MGA),
    "M01_D": round(107.02 * USD_TO_MGA),
    "M02": 45_000,
    "M03": 60_000,
    "M05": 250_000,
    "C01": 90_000,
    "C02": 45_000,
    "C03": 300_000,
    "C04": 450_000,
    "C05": 30_000,
    "C06": 55_000,
    "S01": 75_000,
    "S02": 35_000,
    "S03": 20_000,
    "S04": 30_000,
    "K01": 300_000,
    "K02": 280_000,
    "K03": 150_000,
    "K04": 450_000,
    "K05": 250_000,
    "K06": 280_000,
    "K07": 45_000,
    "K08": 15_000,
    "T01": 200_000,
    "T02": 35_000,
    "T03": 15_000,
    "T04": 90_000,
    "T05": 65_000,
    "T06": 40_000,
    "T07": 12_000,
    "D01": 120_000,
    "D02": 60_000,
    "D03": 300_000,
    "D04": 35_000,
    "D05": 50_000,
    "D06": 45_000,
    "D07": 400_000,
    "D08": 300_000,
    "E01": 1_200_000,
    "E02": 350_000,
    "E03": 850_000,
    "E04": 1_800_000,
    "E05": 60_000,
    "E06": 25_000,
    "E07": 300_000,
}
REGISTERS = [
    {
        "csv": Path("APPROVISIONNEMENT/Budget Et Stock/MODELE_BUDGET_STOCK.csv"),
        "title": "Budget et stock",
        "purpose": "Suivre les coûts et le stock réel à partir de devis et d'un inventaire datés.",
        "source": "Quantités CAO A13 ; prix web moteur et provisions de planification documentées dans README_REGISTRES.md.",
        "caution": "Montants estimatifs, non devis. Stock réel non inventorié; une hypothèse de stock nul sert seulement au calcul du budget.",
    },
    {
        "csv": Path("APPROVISIONNEMENT/Commandes et achats/MODELE_SUIVI_COMMANDES.csv"),
        "title": "Suivi des commandes",
        "purpose": "Suivre chaque demande de devis, commande, réception et justificatif.",
        "source": "Nomenclature A13 et estimation budgétaire associée.",
        "caution": "Toutes les lignes sont des prévisions; aucune commande, offre signée ni réception n'est attestée.",
    },
    {
        "csv": Path("ELECTRONIQUE/Cablage et Integration/REGISTRE_CABLAGE_A_COMPLETER.csv"),
        "title": "Registre de câblage",
        "purpose": "Documenter les liaisons électriques une fois les composants sélectionnés.",
        "source": "Architecture électrique conceptuelle et nomenclature des volumes E01–E07.",
        "caution": "Liaisons candidates seulement : aucun schéma, calibre, brochage ou protection n'est validé.",
    },
    {
        "csv": Path("INFORMATIQUE/Communication/INTERFACES_A_DEFINIR.csv"),
        "title": "Registre des interfaces",
        "purpose": "Décrire les échanges réels, leurs responsabilités et leurs comportements en défaut.",
        "source": "Prototype React/Vite et état de communication du projet.",
        "caution": "Le prototype est local et simulé ; aucune API de robot, ROS 2 ou backend n'est fournie.",
    },
    {
        "csv": Path("INFORMATIQUE/Firmware et Microcontroleurs/INVENTAIRE_FIRMWARE_A_COMPLETER.csv"),
        "title": "Inventaire firmware",
        "purpose": "Tracer les cartes, versions logicielles embarquées, tests et preuves de configuration.",
        "source": "Nomenclature électronique conceptuelle E01–E07.",
        "caution": "Aucune carte électronique ni version de firmware n'est sélectionnée ou fournie.",
    },
    {
        "csv": Path("ROBOTIQUE/Architecture ROS2/INVENTAIRE_ROS2_A_COMPLETER.csv"),
        "title": "Inventaire ROS 2",
        "purpose": "Inventorier uniquement les paquets et interfaces observés sur la plateforme réelle.",
        "source": "État ROS 2 du projet et inspection des sources présentes.",
        "caution": "Aucun paquet, nœud, topic, service ou fichier de lancement ROS 2 n'a été trouvé ; ne pas inventer d'API.",
    },
    {
        "csv": Path("QUALITE ET SECURITE/Analyse des risques/REGISTRE_RISQUES_A_COMPLETER.csv"),
        "title": "Registre des risques",
        "purpose": "Faire évaluer les dangers et consigner les décisions, mesures et preuves.",
        "source": "Avant-projet mécanique, exigences et notes préliminaires de risques.",
        "caution": "Les cotations sont volontairement laissées à l'équipe compétente ; ce fichier n'est pas une analyse approuvée.",
    },
    {
        "csv": Path("QUALITE ET SECURITE/Normes et Reglementations/REGISTRE_NORMES_A_DETERMINER.csv"),
        "title": "Registre des normes",
        "purpose": "Vérifier l'édition, le champ, l'adoption locale et l'applicabilité de chaque référence.",
        "source": "Catalogue ISO pour ISO 12100:2010 ; autres références à revérifier auprès des éditeurs.",
        "caution": "Fianarantsoa, Madagascar. Les normes candidates ne sont pas présentées comme des obligations légales.",
    },
]

NAVY = "17324D"
TEAL = "087E8B"
PALE_BLUE = "EAF2F8"
PALE_TEAL = "E4F3F2"
PALE_AMBER = "FFF2CC"
PALE_RED = "FCE4D6"
PALE_GREEN = "E2F0D9"
GRAY = "5B6573"
WHITE = "FFFFFF"
LINE = "D7E0E8"


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.reader(stream, delimiter=";"))
    if not rows:
        raise ValueError(f"CSV vide, en-tête manquant : {path}")
    width = len(rows[0])
    if any(len(row) != width for row in rows[1:]):
        raise ValueError(f"Nombre de colonnes incohérent : {path}")
    return rows[0], rows[1:]


def status_fill(value: str) -> str:
    lowered = value.casefold()
    if any(word in lowered for word in ("validé", "existant", "fourni", "reçu")):
        return PALE_GREEN
    if any(word in lowered for word in ("prioritaire", "non disponible", "aucun")):
        return PALE_RED
    if any(word in lowered for word in ("à ", "a ", "confirmer", "concept", "définir", "definir", "sélection", "selection", "requise", "requis", "estimation", "prévision")):
        return PALE_AMBER
    return PALE_BLUE


def write_source_register(
    csv_path: Path,
    records: list[list[str]],
    headers: list[str] | None = None,
) -> None:
    if headers is None:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
            headers = next(csv.reader(stream, delimiter=";"), None)
    if headers is None:
        raise ValueError(f"En-tête CSV manquant : {csv_path}")
    if any(len(record) != len(headers) for record in records):
        raise ValueError(f"Colonnes incompatibles avec le modèle : {csv_path}")
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";", lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(records)


def build_bom_records() -> tuple[list[dict[str, str]], dict[str, int]]:
    piece_files = [
        path
        for path in ROOT.rglob("NOMENCLATURE_PIECES.csv")
        if path.parent.name == "Sources_BFM_V4"
    ]
    assembly_files = [
        path
        for path in ROOT.rglob("NOMENCLATURE_ASSEMBLAGES.csv")
        if path.parent.name == "BFM_V4"
        and path.parent.parent.name.endswith("Matériels")
    ]
    if not piece_files or not assembly_files:
        raise FileNotFoundError("Nomenclatures BFM_V4 requises introuvables")

    with piece_files[0].open("r", encoding="utf-8-sig", newline="") as stream:
        pieces = list(csv.DictReader(stream, delimiter=";"))
    with assembly_files[0].open("r", encoding="utf-8-sig", newline="") as stream:
        assemblies = list(csv.DictReader(stream, delimiter=";"))
    full_robot = next(
        (row for row in assemblies if row.get("Assemblage") == "A13_ROBOT_COMPLET"),
        None,
    )
    if full_robot is None:
        raise ValueError("L'assemblage CAO A13_ROBOT_COMPLET est absent")

    placements = json.loads(full_robot["Components / coordinates mm"])
    quantities: dict[str, int] = {}
    for placement in placements:
        reference = placement[0]
        quantities[reference] = quantities.get(reference, 0) + 1
    return pieces, quantities


def initialise_source_data() -> None:
    pieces, quantities = build_bom_records()
    budget_rows: list[list[str]] = []
    order_rows: list[list[str]] = []
    budget_headers = [
        "Reference",
        "Piece",
        "Quantite CAO A13",
        "Quantite achat estimee (stock suppose nul)",
        "Stock constate",
        "Prix unitaire estime (MGA)",
        "Nature du montant",
        "Budget estime (MGA)",
        "Fournisseur ou canal estime",
        "Delai estime",
        "Date estimation",
        "Base de calcul et limites",
        "Statut",
    ]
    order_headers = [
        "Reference de prevision (pas une commande)",
        "Reference et piece",
        "Canal fournisseur estime",
        "Numero de devis reel",
        "Date de commande reelle",
        "Quantite d'achat estimee",
        "Prix estime (MGA)",
        "Nature du montant",
        "Delai estime apres commande",
        "Date de reception reelle",
        "Statut",
        "Base et justificatif",
    ]

    for piece in pieces:
        reference = piece["Reference"]
        count = quantities.get(reference)
        quantity = count or 0
        description = " | ".join(
            value
            for value in (
                reference,
                piece["Piece"],
                piece["Matiere envisagee"],
                piece["Enveloppe / dimensions conceptuelles"],
                piece["Fonction"],
            )
            if value
        )
        estimate = UNIT_ESTIMATES_MGA.get(reference)
        if estimate is None:
            raise ValueError(f"Estimation unitaire absente pour {reference}")
        if reference in {"M01", "M01_D"}:
            supplier = "StepperOnline (prix web public; aucun achat effectué)"
            lead_time = "30 à 60 jours après commande (import, estimation)"
            amount_type = "Prix public en ligne converti"
            basis = (
                "StepperOnline: 107,02 USD (tranche 1-4); taux USD/MGA "
                f"{USD_TO_MGA:,.3f} au {ESTIMATE_DATE}; arrondi à l'ariary. "
                "Hors transport, douane et taxes; modèle et dimensionnement à valider."
            )
        elif reference == "R05":
            supplier = "Importateur de roulements à identifier"
            lead_time = "30 à 60 jours après commande (import, estimation)"
            amount_type = "Provision; prix comparatif non compatible"
            basis = (
                "Provision 35 000 MGA. Repère web SKF 6204-2RSH à 5,68 EUR "
                "(123Roulement), mais ses dimensions 20x47x14 mm ne correspondent "
                "pas au volume CAO R05 24x62x18 mm; référence compatible à choisir."
            )
        elif reference.startswith("E"):
            supplier = "Distributeur électronique / importateur à identifier"
            lead_time = "30 à 60 jours après commande (import, estimation)"
            amount_type = "Provision de planification"
            basis = (
                "Provision manuelle de planification pour cette famille, sans modèle "
                "électronique sélectionné ni tarif fournisseur; incertitude indicative ±50 %."
            )
        else:
            supplier = "Atelier de fabrication local à identifier (Fianarantsoa)"
            lead_time = "10 à 20 jours ouvrés après commande (estimation)"
            amount_type = "Provision de planification"
            basis = (
                "Provision manuelle de planification pour cette pièce, selon sa famille "
                "et ses dimensions conceptuelles; aucun tarif local vérifié; incertitude indicative ±50 %."
            )
        if reference in {"M01", "M01_D"}:
            basis += (
                " Source prix: https://www.omc-stepperonline.com/24v-250w-60rpm-geared-bldc-motor-26-43nm-3742-10oz-in-50-1-right-angle-gearbox-f6b250-24gu-30s-6gu50rt ; "
                "taux: https://open.er-api.com/v6/latest/USD"
            )
        elif reference == "R05":
            basis += (
                " Source comparative: https://www.123roulement.com/roulement-palier/roulement-bille/simple-rangee/6204-2rsh-skf"
            )
        budget_total = estimate * quantity
        status = (
            "ESTIMATION de planification; achat et stock non confirmés"
            if quantity
            else "Hors assemblage A13; aucune quantité incluse dans ce budget"
        )
        budget_rows.append(
            [
                reference,
                description,
                str(quantity),
                str(quantity),
                "Non inventorié",
                str(estimate),
                amount_type,
                str(budget_total),
                supplier,
                lead_time,
                ESTIMATE_DATE,
                basis,
                status,
            ]
        )
        order_rows.append(
            [
                f"PREVISION-2026-{reference}",
                f"{reference} — {piece['Piece']} ({piece['Enveloppe / dimensions conceptuelles']})",
                supplier,
                "Aucun devis reçu",
                "Non commandée",
                str(quantity),
                str(budget_total),
                amount_type,
                lead_time,
                "Non réceptionnée",
                "ESTIMATION; non commandée",
                f"Nomenclature BFM_V4; {basis}",
            ]
        )

    write_source_register(
        ROOT / "APPROVISIONNEMENT/Budget Et Stock/MODELE_BUDGET_STOCK.csv",
        budget_rows,
        budget_headers,
    )
    write_source_register(
        ROOT / "APPROVISIONNEMENT/Commandes et achats/MODELE_SUIVI_COMMANDES.csv",
        order_rows,
        order_headers,
    )

    cable_rows = [
        ["ALIM-01", "E01 Batterie (24 V nominal proposé)", "E02 Contrôleur central", "À sélectionner selon courant, longueur et environnement", "À sélectionner sur fiches techniques", "À calculer; aucune section définie", "À dimensionner selon courant de défaut", "À dessiner et protéger mécaniquement", "Plan d'essai à définir; aucun résultat fourni", "Équipe électronique", "Architecture conceptuelle; composants non sélectionnés"],
        ["MOT-01", "E02 Contrôleur central", "E03 Driver moteur", "Signal de commande; nature électrique inconnue", "À définir avec les cartes retenues", "À définir selon interface", "À définir selon interface", "À dessiner", "Vérifier niveaux, sens et perte de signal après sélection", "Équipe électronique", "Interface non spécifiée"],
        ["MOT-02", "E03 Driver moteur", "M01 / M01_D Motoréducteurs (2 positions CAO)", "Câble moteur à choisir selon courant et flexion", "À confirmer avec le moteur et le driver", "À calculer sur le courant moteur réel", "Protection à dimensionner", "Deux branches à documenter; séparation puissance/signaux à étudier", "Continuité et essais moteur à définir; aucun résultat fourni", "Équipe électronique / mécanique", "STEP moteur disponible; caractérisation électrique manquante"],
        ["CAP-01", "E04 Scanner lidar (volume conceptuel)", "E02 Contrôleur central", "Données et alimentation à confirmer", "À confirmer avec le modèle choisi", "À définir d'après la fiche du capteur", "À définir", "À dessiner", "Vérifier communication et perte de capteur après sélection", "Équipe robotique", "Aucun capteur choisi; lidar non confirmé comme dispositif de sécurité"],
        ["SEC-01", "E05 Arrêt d'urgence (volume conceptuel)", "Chaîne de sécurité à concevoir", "Contacts / architecture à déterminer pour le composant choisi", "À spécifier avec le composant de sécurité", "À calculer selon l'architecture", "Fonction de sécurité à valider par spécialiste", "Cheminement séparé et protégé à concevoir", "Validation de la fonction d'arrêt requise avant essai réel", "Équipe sécurité / électrique", "Composant certifié non sélectionné"],
        ["CAP-02", "E06 Capteurs de casier (4 volumes)", "E02 Contrôleur central", "Type de sortie non défini", "À définir selon les capteurs choisis", "À déterminer", "À déterminer", "Quatre implantations conceptuelles; cheminement à dessiner", "Essai de détection et défaut à spécifier", "Équipe électronique", "Aucun capteur sélectionné"],
        ["IHM-01", "E02 Contrôleur central", "E07 Écran (volume conceptuel)", "Alimentation et communication inconnues", "À confirmer selon le modèle", "À calculer selon fiche fabricant", "À définir", "À dessiner", "Essai de communication à définir", "Équipe informatique / électronique", "Aucun écran sélectionné"],
        ["CHG-01", "Chargeur et batterie E01 à sélectionner", "E01 Batterie", "À définir avec le système batterie/BMS", "À choisir avec la batterie", "À calculer selon chargeur et batterie", "Protection et supervision à concevoir", "Zone de charge et connectique à définir", "Procédure et essais chargeur à faire valider", "Équipe électrique", "Chimie, capacité et chargeur inconnus"],
    ]
    write_source_register(
        ROOT / "ELECTRONIQUE/Cablage et Integration/REGISTRE_CABLAGE_A_COMPLETER.csv",
        cable_rows,
    )

    interface_rows = [
        ["UI-LOCAL", "Supervision React/Vite", "État local simulé de l'application", "Aucun réseau; état local", "Missions, progression, batterie et commandes simulées", "Événements de l'interface; fréquence réelle sans objet", "Aucune; données de démonstration", "Pas de transport distant; limites de simulation indiquées dans le README", "Vérifier l'interface en mode démonstration; aucune télémétrie réelle", "Équipe informatique", "Existant; simulation locale seulement"],
        ["IF-API", "Prototype de supervision", "Backend / API", "Non défini; aucun backend fourni", "Non défini", "Non définie", "À concevoir avant connexion réelle", "Timeout, perte de connexion et validation à spécifier", "Aucun test d'intégration disponible", "Équipe informatique", "À définir; ne pas considérer le prototype comme connecté"],
        ["IF-AGV", "Backend éventuel", "AGV bancaire / API intégrateur", "À confirmer auprès de l'intégrateur", "À obtenir de la documentation officielle du robot", "À confirmer", "À définir avec l'intégrateur", "État sûr et reprise à documenter avec le fournisseur", "Essais encadrés à définir après accès aux spécifications", "Intégrateur AGV", "Modèle et API réels non confirmés"],
        ["IF-ELEV", "AGV / passerelle éventuelle", "Ascenseur A et système du bâtiment", "À confirmer avec le responsable du site", "À définir", "À définir", "À confirmer par le site", "Priorités, panne et perte de liaison à convenir", "Essai à autoriser et planifier avec le site", "Responsable du site / intégrateur", "Aucune interface d'ascenseur documentée"],
        ["IF-CAM", "Vues POV de démonstration", "Scène simulée de la maquette", "Calcul local; aucun flux réseau", "Images synthétiques calculées depuis la scène", "Simulation locale", "Sans objet", "Sans flux capteur réel", "Vérifier que l'interface les identifie comme synthétiques", "Équipe informatique", "Pas de caméra physique connectée"],
    ]
    write_source_register(
        ROOT / "INFORMATIQUE/Communication/INTERFACES_A_DEFINIR.csv",
        interface_rows,
    )

    firmware_rows = [
        ["E01 — batterie (volume CAO)", "Non sélectionné", "Alimentation conceptuelle; 24 V nominal proposé", "Tension/courant de sortie et BMS inconnus", "Non défini", "Aucun firmware ou BMS documenté", "Inconnu; batterie à sélectionner", "Non spécifié", "Aucune fiche batterie ni preuve d'essai", "Équipe électronique", "Volume CAO seulement; chimie/capacité inconnues"],
        ["E02 — contrôleur central (volume CAO)", "Non sélectionné", "Pilotage conceptuel des mouvements", "Entrées/sorties à définir", "Non défini", "Aucun code ou numéro de version fourni", "Non spécifié", "Non spécifié", "Aucun matériel/firmware/test fourni", "Équipe électronique / logiciel", "Volume CAO seulement"],
        ["E03 — driver moteur (volume CAO)", "Non sélectionné", "Commande conceptuelle des moteurs", "Puissance, retours et défauts à définir", "Non défini", "Aucun code ou numéro de version fourni", "Non spécifié", "Non spécifié", "Aucun driver ni essai moteur fourni", "Équipe électronique", "Volume CAO seulement"],
        ["E04 — lidar (volume CAO)", "Modèle non sélectionné", "Localisation/obstacles envisagés", "Données et états de défaut à obtenir", "Non défini", "Firmware fabricant inconnu", "Géré par le fabricant; détails inconnus", "À vérifier sur la fiche du modèle", "Aucun lidar réel ni test fourni; non présumé de sécurité", "Équipe robotique / intégrateur", "Enveloppe conceptuelle uniquement"],
        ["E05 — arrêt d'urgence (volume CAO)", "Composant certifié à sélectionner", "Demande d'arrêt; circuit complet à concevoir", "Contacts et architecture à confirmer", "N/A pour un organe mécanique; chaîne de sécurité à concevoir", "N/A pour le bouton; contrôleur de sécurité non défini", "N/A pour le bouton", "Fonction de sécurité à spécifier et valider", "Aucun essai ni composant choisi", "Équipe sécurité / électrique", "Le volume CAO n'est pas un composant réel"],
        ["E06 — capteurs de casier (4 volumes CAO)", "Non sélectionnés", "Présence/position conceptuelle des casiers", "Type et nombre d'E/S à confirmer", "Non défini", "Firmware fabricant inconnu", "Non spécifié", "Non spécifié", "Aucun capteur ni test fourni", "Équipe électronique", "Quatre implantations de maquette"],
        ["E07 — écran (volume CAO)", "Non sélectionné", "Interface opérateur conceptuelle", "Commandes/affichage à définir", "Non défini", "Aucun logiciel embarqué d'écran fourni", "Non spécifié", "Non spécifié", "Aucun écran ou test fourni", "Équipe informatique / électronique", "Volume CAO seulement"],
    ]
    write_source_register(
        ROOT / "INFORMATIQUE/Firmware et Microcontroleurs/INVENTAIRE_FIRMWARE_A_COMPLETER.csv",
        firmware_rows,
    )

    ros_rows = [
        ["Non applicable — aucun paquet trouvé", "Aucun nœud ROS 2 fourni", "Aucune interface ROS 2 confirmée sur l'AGV bancaire", "Aucun topic entrant documenté", "Aucun topic sortant documenté", "Aucune action ou aucun service documenté", "Plateforme ROS 2/AGV non identifiée", "À spécifier uniquement après confirmation par l'intégrateur", "Aucun test ROS 2 fourni", "Intégrateur AGV / équipe robotique", "Sources examinées : aucun package.xml, nœud, launch ou interface ROS 2 disponible"],
    ]
    write_source_register(
        ROOT / "ROBOTIQUE/Architecture ROS2/INVENTAIRE_ROS2_A_COMPLETER.csv",
        ros_rows,
    )

    risk_rows = [
        ["R01", "Basculement avec tiroir ouvert", "Tiroir chargé extrait; centre de gravité et masse non calculés", "Blessure par basculement ou chute de charge (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Calculer stabilité et cas de charge; limiter l'ouverture à un tiroir uniquement après analyse; essai contrôlé à définir", "Non évalué", "Équipe mécanique / sécurité", "Avant-projet: tiroirs de 40 kg nominaux; masse totale et stabilité non validées", "À analyser avant essai réel"],
        ["R02", "Pincement ou chute pendant extraction", "Mouvement du tiroir ou transfert du sac; mécanisme et anti-pincement non conçus", "Pincement, écrasement ou chute du sac (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Définir retenue du sac, butées, protections, détection et séquence d'interverrouillage", "Non évalué", "Équipe mécanique / sécurité", "Cycle de déchargement conceptuel; actionneurs et protections non implémentés", "À analyser avant essai réel"],
        ["R03", "Collision ou passage impossible sur site", "Dimensions réelles des portes, couloirs, cabine ou trajectoire différentes du modèle", "Collision, dommage matériel ou blessure (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Relever les lieux à Fianarantsoa; vérifier gabarit, seuils et trajectoire avec une maquette chargée", "Non évalué", "Responsable du site / robotique", "Cotes D/H et dégagements explicitement à confirmer", "Mesures terrain requises"],
        ["R04", "Perte de freinage ou de maintien", "Perte d'alimentation ou défaillance du frein/commande", "Déplacement non maîtrisé ou charge non retenue (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Sélectionner un frein adapté; définir l'état hors tension et tester le maintien", "Non évalué", "Équipe mécanique / électrique", "Frein M05 uniquement schématique; référence réelle à choisir", "Composant non sélectionné"],
        ["R05", "Défaillance batterie ou protection électrique", "Court-circuit, surcharge, défaut de charge ou câblage inadéquat", "Échauffement, brûlure, incendie ou arrêt de système (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Définir batterie/BMS, chargeur, protections, conducteurs et essais par un responsable qualifié", "Non évalué", "Équipe électrique", "24 V est une proposition conceptuelle; chimie, capacité et protections non définies", "Architecture à concevoir"],
        ["R06", "Détection d'obstacle insuffisante", "Lidar absent, défaillant ou inadapté à la fonction de sécurité", "Collision avec une personne ou un obstacle (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Choisir les dispositifs requis avec l'intégrateur; ne pas attribuer une fonction de sécurité au lidar conceptuel", "Non évalué", "Équipe sécurité / intégrateur", "Source électrique précise que le lidar n'est pas certifié comme capteur de sécurité", "À analyser"],
        ["R07", "Départ intempestif pendant le déchargement", "Tiroir ouvert ou verrouillage non confirmé alors que la traction est demandée", "Collision, pincement ou détérioration (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Spécifier et valider l'interverrouillage traction/tiroirs et l'état sûr après défaut", "Non évalué", "Équipe commande / sécurité", "Interverrouillage décrit comme exigence de conception; non implémenté", "Concept non réalisé"],
        ["R08", "Commande logicielle ou communication interrompue", "Perte de liaison, données périmées ou commande ambiguë lors d'une future intégration", "Mouvement inadapté ou perte de supervision (à évaluer)", "Non évaluée", "Inconnue", "Non coté", "Définir limites de commande, délai, arrêt sûr, authentification et procédure de reprise avec l'intégrateur", "Non évalué", "Équipe informatique / intégrateur", "Prototype React/Vite local; aucune API ou liaison réelle fournie", "Pas de connexion réelle"],
    ]
    write_source_register(
        ROOT / "QUALITE ET SECURITE/Analyse des risques/REGISTRE_RISQUES_A_COMPLETER.csv",
        risk_rows,
    )

    standards_rows = [
        ["ISO 12100:2010", "Sécurité des machines — Principes généraux de conception — Appréciation et réduction du risque", "Édition 2010; le catalogue ISO indique confirmée en 2022 et révision en préparation (consultation 2026)", "Madagascar — Fianarantsoa", "À confirmer; vérifier adoption malgache et applicabilité", "Méthode d'identification des phénomènes dangereux et de réduction du risque", "Analyse documentée, vérifications et décisions de l'équipe compétente; catalogue: https://www.iso.org/standard/51528.html", "Responsable sécurité / concepteur", "Référence candidate; non déclarée obligatoire"],
        ["ISO 3691-4:2023", "Chariots de manutention — Exigences de sécurité et vérification — Chariots sans conducteur et leurs systèmes", "2023 indiquée dans les sources du projet; édition actuelle à vérifier au catalogue", "Madagascar — Fianarantsoa", "À confirmer selon la classification et l'utilisation réelle de l'AGV", "Exigences pour les chariots sans conducteur et leurs systèmes, si dans le champ", "Avis intégrateur, examen de l'édition et rapport d'essais selon le champ confirmé", "Intégrateur AGV / responsable sécurité", "Candidate; édition et applicabilité à vérifier"],
        ["IEC 60204-1:2016+A1:2021", "Sécurité des machines — Équipement électrique des machines — Partie 1", "2016 avec amendement A1:2021 indiqués dans les sources; édition actuelle à vérifier", "Madagascar — Fianarantsoa", "À confirmer par le responsable électrique et le conseil local", "Équipement électrique et commande des machines, selon le champ applicable", "Schémas, calculs, vérifications et essais électriques approuvés", "Responsable électrique", "Candidate; applicabilité à vérifier"],
        ["ISO 13849-1:2023", "Sécurité des machines — Parties des systèmes de commande relatives à la sécurité — Partie 1", "2023 indiquée dans les sources; édition actuelle à vérifier au catalogue", "Madagascar — Fianarantsoa", "À confirmer si des parties de commande liées à la sécurité sont conçues", "Conception et validation des parties de commande liées à la sécurité", "Spécification des fonctions, justification et validation par une personne compétente", "Responsable sécurité / automaticien", "Candidate; niveau et applicabilité non déterminés"],
        ["Textes malgaches à identifier", "Textes applicables en santé et sécurité au travail, équipements et exigences du site", "Texte et version en vigueur à rechercher auprès des autorités malgaches", "Madagascar — Fianarantsoa", "Vérification requise avant essai ou exploitation réelle", "Règles nationales, exigences de l'employeur et règles internes du site", "Références juridiques vérifiées et avis du responsable HSE / site", "Direction de projet / responsable HSE", "Aucun texte national spécifique confirmé dans les sources du projet"],
    ]
    write_source_register(
        ROOT / "QUALITE ET SECURITE/Normes et Reglementations/REGISTRE_NORMES_A_DETERMINER.csv",
        standards_rows,
    )


def make_workbook(config: dict[str, str]) -> Path:
    csv_path = ROOT / config["csv"]
    headers, records = read_csv(csv_path)
    workbook = Workbook()
    overview = workbook.active
    overview.title = "À lire"
    overview.sheet_view.showGridLines = False
    overview.merge_cells("A1:F1")
    overview["A1"] = config["title"].upper()
    overview["A1"].fill = PatternFill("solid", fgColor=NAVY)
    overview["A1"].font = Font(name="Aptos Display", size=18, bold=True, color=WHITE)
    overview["A1"].alignment = Alignment(vertical="center")
    overview.row_dimensions[1].height = 36

    overview.merge_cells("A3:F3")
    overview["A3"] = config["purpose"]
    overview["A3"].font = Font(name="Aptos", size=12, bold=True, color=NAVY)
    overview["A3"].alignment = Alignment(wrap_text=True, vertical="center")
    overview.row_dimensions[3].height = 34

    overview["A5"] = "ÉTAT DU FICHIER"
    overview["B5"] = "RÉFÉRENCE"
    for cell in overview[5][:2]:
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
        cell.alignment = Alignment(vertical="center")
    overview["A6"] = f"{len(records)} ligne(s) de suivi"
    overview["B6"] = config["source"]
    overview["A6"].fill = PatternFill("solid", fgColor=PALE_TEAL)
    overview["B6"].fill = PatternFill("solid", fgColor=PALE_BLUE)
    overview["A6"].font = Font(name="Aptos", bold=True, color=NAVY)
    overview["B6"].font = Font(name="Aptos", color=GRAY)

    total_column = next(
        (
            index
            for index, heading in enumerate(headers)
            if heading.casefold() in {"budget estime (mga)", "prix estime (mga)"}
        ),
        None,
    )
    if total_column is not None:
        estimated_total = sum(int(record[total_column]) for record in records)
        overview["A7"] = "Total estimatif (MGA)"
        overview["B7"] = estimated_total
        overview["A7"].fill = PatternFill("solid", fgColor=PALE_AMBER)
        overview["B7"].fill = PatternFill("solid", fgColor=PALE_AMBER)
        overview["A7"].font = Font(name="Aptos", bold=True, color=NAVY)
        overview["B7"].font = Font(name="Aptos", bold=True, color=NAVY)
        overview["B7"].number_format = '#,##0 "MGA"'

    overview.merge_cells("A8:F8")
    overview["A8"] = "À LIRE AVANT DE REMPLIR"
    overview["A8"].fill = PatternFill("solid", fgColor=NAVY)
    overview["A8"].font = Font(name="Aptos", bold=True, color=WHITE)
    overview.merge_cells("A9:F10")
    overview["A9"] = config["caution"]
    overview["A9"].fill = PatternFill("solid", fgColor=PALE_AMBER)
    overview["A9"].font = Font(name="Aptos", size=11, color=NAVY)
    overview["A9"].alignment = Alignment(wrap_text=True, vertical="center")
    overview.row_dimensions[9].height = 34
    overview.row_dimensions[10].height = 20

    overview.merge_cells("A12:F12")
    overview["A12"] = "LÉGENDE"
    overview["A12"].fill = PatternFill("solid", fgColor=NAVY)
    overview["A12"].font = Font(name="Aptos", bold=True, color=WHITE)
    legend = [
        ("Vert", "Information explicitement indiquée comme existante ou fournie."),
        ("Ambre", "À confirmer, à définir, conceptuel ou en attente d'une décision."),
        ("Rouge", "Point critique ou donnée indisponible : traiter avant de conclure."),
        ("Bleu clair", "Cellule à compléter ou information de contexte."),
    ]
    for row_index, (label, explanation) in enumerate(legend, 13):
        overview.cell(row_index, 1, label)
        overview.merge_cells(start_row=row_index, start_column=2, end_row=row_index, end_column=6)
        overview.cell(row_index, 2, explanation)
        fill_color = {
            "Vert": PALE_GREEN,
            "Ambre": PALE_AMBER,
            "Rouge": PALE_RED,
            "Bleu clair": PALE_BLUE,
        }[label]
        for cell in overview[row_index][:6]:
            cell.fill = PatternFill("solid", fgColor=fill_color)
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        overview.cell(row_index, 1).font = Font(name="Aptos", bold=True, color=NAVY)
        overview.cell(row_index, 2).font = Font(name="Aptos", color=GRAY)

    overview.merge_cells("A19:F19")
    overview["A19"] = "PÉRIMÈTRE"
    overview["A19"].fill = PatternFill("solid", fgColor=NAVY)
    overview["A19"].font = Font(name="Aptos", bold=True, color=WHITE)
    overview.merge_cells("A20:F21")
    overview["A20"] = (
        "Contexte de projet : Fianarantsoa, Madagascar ; devise du budget : ariary. "
        "La couleur aide à repérer les actions mais ne remplace ni une validation, "
        "ni une preuve, ni une approbation réglementaire."
    )
    overview["A20"].fill = PatternFill("solid", fgColor=PALE_BLUE)
    overview["A20"].font = Font(name="Aptos", color=NAVY)
    overview["A20"].alignment = Alignment(wrap_text=True, vertical="center")
    overview.column_dimensions["A"].width = 28
    for col in "BCDEF":
        overview.column_dimensions[col].width = 21
    overview.freeze_panes = "A5"
    overview.sheet_properties.pageSetUpPr.fitToPage = True

    sheet = workbook.create_sheet("Registre")
    sheet.sheet_view.showGridLines = False
    sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    sheet.cell(1, 1, config["title"].upper())
    sheet.cell(1, 1).fill = PatternFill("solid", fgColor=NAVY)
    sheet.cell(1, 1).font = Font(name="Aptos Display", size=16, bold=True, color=WHITE)
    sheet.cell(1, 1).alignment = Alignment(vertical="center")
    sheet.row_dimensions[1].height = 32
    sheet.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(headers))
    sheet.cell(2, 1, config["caution"])
    sheet.cell(2, 1).fill = PatternFill("solid", fgColor=PALE_AMBER)
    sheet.cell(2, 1).font = Font(name="Aptos", italic=True, color=NAVY)
    sheet.cell(2, 1).alignment = Alignment(wrap_text=True, vertical="center")
    sheet.row_dimensions[2].height = 34

    header_row = 4
    for column, heading in enumerate(headers, 1):
        cell = sheet.cell(header_row, column, heading)
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=Side(style="medium", color=NAVY))
    sheet.row_dimensions[header_row].height = 34

    for row_index, record in enumerate(records, header_row + 1):
        for column, value in enumerate(record, 1):
            heading = headers[column - 1].casefold()
            is_money = "(mga)" in heading
            is_quantity = heading.startswith("quantite ")
            cell_value = int(value) if value and (is_money or is_quantity) else value
            cell = sheet.cell(row_index, column, cell_value)
            cell.font = Font(name="Aptos", size=10, color=NAVY)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=Side(style="hair", color=LINE))
            if is_money:
                cell.number_format = '#,##0 "MGA"'
            if row_index % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7FAFC")
            if not value.strip():
                cell.fill = PatternFill("solid", fgColor=PALE_AMBER)
        status_columns = [
            index + 1
            for index, name in enumerate(headers)
            if "statut" in name.casefold()
        ]
        for column in status_columns:
            cell = sheet.cell(row_index, column)
            cell.fill = PatternFill("solid", fgColor=status_fill(str(cell.value or "")))
            cell.font = Font(name="Aptos", size=10, bold=True, color=NAVY)
        sheet.row_dimensions[row_index].height = 42

    for column, heading in enumerate(headers, 1):
        values = [str(heading)] + [str(row[column - 1]) for row in records]
        width = min(max(max((len(part) for part in value.splitlines()), default=10) for value in values) + 3, 42)
        sheet.column_dimensions[get_column_letter(column)].width = max(width, 14)

    last_row = header_row + len(records)
    for row_index in range(header_row + 1, last_row + 1):
        wrapped_lines = 1
        for column, heading in enumerate(headers, 1):
            cell_value = str(sheet.cell(row_index, column).value or "")
            column_width = max(int(sheet.column_dimensions[get_column_letter(column)].width) - 2, 1)
            line_count = sum(
                max(1, (len(line) + column_width - 1) // column_width)
                for line in cell_value.splitlines()
            )
            wrapped_lines = max(wrapped_lines, line_count)
        sheet.row_dimensions[row_index].height = min(max(42, wrapped_lines * 15), 150)

    last_column = sheet.cell(header_row, len(headers)).column_letter
    sheet.freeze_panes = "A5"
    sheet.auto_filter.ref = f"A{header_row}:{last_column}{last_row}"
    # Use a plain worksheet AutoFilter instead of a structured Excel Table;
    # several VS Code spreadsheet readers fail on structured-table relationships.
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.page_margins.left = 0.25
    sheet.page_margins.right = 0.25
    output_path = csv_path.with_suffix(".xlsx")
    save_workbook_compatible(workbook, output_path)
    return output_path


def make_detailed_budget_workbook() -> Path:
    csv_path = ROOT / "APPROVISIONNEMENT/Budget Et Stock/MODELE_BUDGET_STOCK.csv"
    headers, records = read_csv(csv_path)
    budget_rows = [dict(zip(headers, record)) for record in records]
    budget_by_reference = {row["Reference"]: row for row in budget_rows}
    pieces, _ = build_bom_records()
    pieces_by_reference = {piece["Reference"]: piece for piece in pieces}
    if set(budget_by_reference) != set(pieces_by_reference):
        raise ValueError("Le budget et la nomenclature BFM_V4 ne contiennent pas les mêmes références")

    family_labels = {
        "01_ROUES": "Roues motrices",
        "02_MOTORISATION": "Motorisation",
        "03_CHASSIS": "Châssis",
        "04_SUSPENSION": "Suspension",
        "05_COFFRE_2X2": "Coffre 2 × 2",
        "06_TIROIRS": "Tiroirs",
        "07_DECHARGEMENT": "Déchargement et station",
        "08_ELECTRONIQUE": "Électronique",
    }
    detail_headers = [
        "Famille",
        "Référence",
        "Désignation",
        "Matière envisagée",
        "Dimensions conceptuelles",
        "Fonction",
        "Quantité CAO A13",
        "Quantité à acheter estimée",
        "Prix unitaire estimé (MGA)",
        "Nature du montant",
        "Montant estimé (MGA)",
        "Fournisseur ou canal estimé",
        "Délai estimé",
        "Base de calcul et limites",
        "Statut",
    ]

    workbook = Workbook()
    detail = workbook.active
    detail.title = "Détail des dépenses"
    detail.sheet_view.showGridLines = False
    detail.merge_cells("A1:O1")
    detail["A1"] = "DÉTAIL DU BUDGET PRÉVISIONNEL — ROBOT A13"
    detail["A1"].fill = PatternFill("solid", fgColor=NAVY)
    detail["A1"].font = Font(name="Aptos Display", size=18, bold=True, color=WHITE)
    detail["A1"].alignment = Alignment(vertical="center")
    detail.row_dimensions[1].height = 36
    detail.merge_cells("A2:O2")
    detail["A2"] = (
        "Une ligne par référence CAO. Les montants sont des estimations, pas des devis; "
        "le stock réel n'est pas inventorié et le calcul suppose un stock nul."
    )
    detail["A2"].fill = PatternFill("solid", fgColor=PALE_AMBER)
    detail["A2"].font = Font(name="Aptos", bold=True, color=NAVY)
    detail["A2"].alignment = Alignment(wrap_text=True, vertical="center")
    detail.row_dimensions[2].height = 34

    header_row = 4
    for column, heading in enumerate(detail_headers, 1):
        cell = detail.cell(header_row, column, heading)
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=Side(style="medium", color=NAVY))
    detail.row_dimensions[header_row].height = 40

    family_totals: dict[str, dict[str, int]] = {}
    total_estimate = 0
    total_quantity = 0
    public_total = 0
    for row_index, piece in enumerate(pieces, header_row + 1):
        reference = piece["Reference"]
        budget = budget_by_reference[reference]
        family_key = piece["Famille"]
        family = family_labels.get(family_key)
        if family is None:
            raise ValueError(f"Famille CAO inconnue pour {reference}: {family_key}")
        quantity = int(budget["Quantite CAO A13"])
        purchase_quantity = int(budget["Quantite achat estimee (stock suppose nul)"])
        unit_price = int(budget["Prix unitaire estime (MGA)"])
        line_total = int(budget["Budget estime (MGA)"])
        family_total = family_totals.setdefault(
            family,
            {"references": 0, "quantity": 0, "amount": 0, "public": 0, "provision": 0},
        )
        family_total["references"] += 1
        family_total["quantity"] += quantity
        family_total["amount"] += line_total
        if budget["Nature du montant"] == "Prix public en ligne converti":
            family_total["public"] += line_total
            public_total += line_total
        else:
            family_total["provision"] += line_total
        total_estimate += line_total
        total_quantity += quantity

        values = [
            family,
            reference,
            piece["Piece"],
            piece["Matiere envisagee"],
            piece["Enveloppe / dimensions conceptuelles"],
            piece["Fonction"],
            quantity,
            purchase_quantity,
            unit_price,
            budget["Nature du montant"],
            line_total,
            budget["Fournisseur ou canal estime"],
            budget["Delai estime"],
            budget["Base de calcul et limites"],
            budget["Statut"],
        ]
        for column, value in enumerate(values, 1):
            cell = detail.cell(row_index, column, value)
            cell.font = Font(name="Aptos", size=10, color=NAVY)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=Side(style="hair", color=LINE))
            if row_index % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7FAFC")
            if column in {9, 11}:
                cell.number_format = '#,##0 "MGA"'
            elif column in {7, 8}:
                cell.number_format = "#,##0"
        detail.cell(row_index, 10).fill = PatternFill(
            "solid",
            fgColor=PALE_GREEN
            if budget["Nature du montant"] == "Prix public en ligne converti"
            else PALE_AMBER,
        )
        detail.cell(row_index, 10).font = Font(name="Aptos", size=10, bold=True, color=NAVY)

    last_detail_row = header_row + len(pieces)
    total_row = last_detail_row + 1
    detail.cell(total_row, 1, "TOTAL A13")
    detail.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=6)
    detail.cell(total_row, 7, total_quantity)
    detail.cell(total_row, 11, total_estimate)
    for cell in detail[total_row]:
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
    detail.cell(total_row, 11).number_format = '#,##0 "MGA"'
    detail.row_dimensions[total_row].height = 26

    widths = [26, 12, 30, 20, 34, 36, 16, 20, 20, 34, 21, 38, 38, 72, 48]
    for column, width in enumerate(widths, 1):
        detail.column_dimensions[get_column_letter(column)].width = width
    for row_index in range(header_row + 1, last_detail_row + 1):
        wrapped_lines = 1
        for column, width in enumerate(widths, 1):
            value = str(detail.cell(row_index, column).value or "")
            lines = sum(
                max(1, math.ceil(len(line) / max(width - 3, 1)))
                for line in value.splitlines()
            )
            wrapped_lines = max(wrapped_lines, lines)
        detail.row_dimensions[row_index].height = min(max(42, wrapped_lines * 15), 150)
    detail.freeze_panes = "A5"
    detail.auto_filter.ref = f"A{header_row}:O{last_detail_row}"
    detail.sheet_properties.pageSetUpPr.fitToPage = True
    detail.page_setup.orientation = "landscape"
    detail.page_setup.fitToWidth = 1
    detail.page_setup.fitToHeight = 0

    summary = workbook.create_sheet("Synthèse par famille")
    summary.sheet_view.showGridLines = False
    summary.merge_cells("A1:H1")
    summary["A1"] = "SYNTHÈSE DES DÉPENSES PAR FAMILLE"
    summary["A1"].fill = PatternFill("solid", fgColor=NAVY)
    summary["A1"].font = Font(name="Aptos Display", size=18, bold=True, color=WHITE)
    summary.row_dimensions[1].height = 36
    summary.merge_cells("A2:H2")
    summary["A2"] = "Sous-totaux calculés à partir des lignes de l'onglet « Détail des dépenses »."
    summary["A2"].fill = PatternFill("solid", fgColor=PALE_BLUE)
    summary["A2"].font = Font(name="Aptos", color=NAVY)
    summary["A2"].alignment = Alignment(wrap_text=True, vertical="center")
    summary.row_dimensions[2].height = 30
    summary_headers = [
        "Famille",
        "Références",
        "Quantité CAO A13",
        "Prix publics convertis (MGA)",
        "Provisions (MGA)",
        "Total estimé (MGA)",
        "Part du total",
        "Observation",
    ]
    for column, heading in enumerate(summary_headers, 1):
        cell = summary.cell(4, column, heading)
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    summary.row_dimensions[4].height = 36
    for row_index, (family, values) in enumerate(family_totals.items(), 5):
        observation = "Montants estimatifs; voir le détail par référence."
        row_values = [
            family,
            values["references"],
            values["quantity"],
            values["public"],
            values["provision"],
            values["amount"],
            values["amount"] / total_estimate if total_estimate else 0,
            observation,
        ]
        for column, value in enumerate(row_values, 1):
            cell = summary.cell(row_index, column, value)
            cell.font = Font(name="Aptos", size=10, color=NAVY)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if row_index % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7FAFC")
            if column in {4, 5, 6}:
                cell.number_format = '#,##0 "MGA"'
            elif column == 7:
                cell.number_format = "0.0%"

    summary_total_row = 5 + len(family_totals)
    summary.cell(summary_total_row, 1, "TOTAL A13")
    summary.merge_cells(
        start_row=summary_total_row,
        start_column=1,
        end_row=summary_total_row,
        end_column=2,
    )
    summary.cell(summary_total_row, 3, total_quantity)
    summary.cell(summary_total_row, 4, public_total)
    summary.cell(summary_total_row, 5, total_estimate - public_total)
    summary.cell(summary_total_row, 6, total_estimate)
    summary.cell(summary_total_row, 7, 1 if total_estimate else 0)
    for cell in summary[summary_total_row]:
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
    for column in (4, 5, 6):
        summary.cell(summary_total_row, column).number_format = '#,##0 "MGA"'
    summary.cell(summary_total_row, 7).number_format = "0.0%"
    for column, width in enumerate([28, 14, 18, 24, 22, 22, 16, 52], 1):
        summary.column_dimensions[get_column_letter(column)].width = width
    summary.freeze_panes = "A5"
    summary.auto_filter.ref = f"A4:H{summary_total_row - 1}"

    assumptions = workbook.create_sheet("Hypothèses et sources")
    assumptions.sheet_view.showGridLines = False
    assumptions.merge_cells("A1:C1")
    assumptions["A1"] = "HYPOTHÈSES, SOURCES ET EXCLUSIONS"
    assumptions["A1"].fill = PatternFill("solid", fgColor=NAVY)
    assumptions["A1"].font = Font(name="Aptos Display", size=18, bold=True, color=WHITE)
    assumptions.row_dimensions[1].height = 36
    assumptions.merge_cells("A2:C2")
    assumptions["A2"] = (
        "Ce classeur détaille le budget prévisionnel A13. Il ne constitue ni un devis, "
        "ni une autorisation d'achat."
    )
    assumptions["A2"].fill = PatternFill("solid", fgColor=PALE_AMBER)
    assumptions["A2"].font = Font(name="Aptos", bold=True, color=NAVY)
    assumptions["A2"].alignment = Alignment(wrap_text=True, vertical="center")
    assumption_headers = ["Élément", "Valeur", "Détail"]
    for column, heading in enumerate(assumption_headers, 1):
        cell = assumptions.cell(4, column, heading)
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", bold=True, color=WHITE)
    provisions_total = total_estimate - public_total
    assumption_rows = [
        ["Date de référence", ESTIMATE_DATE, "Date de consultation des prix publics et de préparation des provisions."],
        ["Total estimatif A13", total_estimate, "Somme des 52 lignes de détail; comprend uniquement les quantités présentes dans A13."],
        ["Quantité CAO A13", total_quantity, "130 placements comptés dans la nomenclature; ce n'est pas une quantité achetée."],
        ["Prix public des moteurs", "107,02 USD / unité; 492 156 MGA / unité", "Prix StepperOnline affiché pour 1 à 4 unités; taux de référence 4 598,727 MGA/USD."],
        ["Total des deux moteurs", 984_312, "2 × 492 156 MGA; transport, douane et taxes locales exclus."],
        ["Source prix moteur", "StepperOnline — F6B250-24GU-30S/6GU50RT", "Prix public consulté; pas de commande ni de devis obtenu."],
        ["Source taux de change", "ExchangeRate-API — USD vers MGA", "Taux consulté le 23 novembre 2026; peut varier."],
        ["Provisions des autres pièces", provisions_total, "Montants provisoires saisis par référence; aucun tarif local vérifié; incertitude indicative de ±50 % ou davantage."],
        ["Roulement R05", "Provision de 35 000 MGA / unité", "Le SKF 6204 comparé n'est pas compatible avec le gabarit CAO; sélectionner la référence correcte avant achat."],
        ["Stock réel", "Non inventorié", "La quantité d'achat estimée suppose temporairement un stock nul; faire un inventaire physique."],
        ["Lignes hors A13", "Quantité et total A13 = 0", "Certaines pièces de station ne figurent pas dans l'assemblage robot A13 et ne sont donc pas incluses dans ce total."],
        ["Exclusions", "Non chiffrées dans ce total", "Transport, droits, taxes, changements de conception, achats non inscrits dans la nomenclature et dépenses réelles non fournies."],
        ["Commandes et réceptions", "Aucune enregistrée", "Les identifiants PREVISION-2026-* sont des repères de planification, pas des numéros de commande."],
    ]
    for row_index, values in enumerate(assumption_rows, 5):
        for column, value in enumerate(values, 1):
            cell = assumptions.cell(row_index, column, value)
            cell.font = Font(name="Aptos", size=10, color=NAVY)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=Side(style="hair", color=LINE))
            if row_index % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7FAFC")
        if isinstance(values[1], int):
            assumptions.cell(row_index, 2).number_format = '#,##0 "MGA"'
    assumptions["C10"].hyperlink = (
        "https://www.omc-stepperonline.com/24v-250w-60rpm-geared-bldc-motor-26-43nm-3742-10oz-in-50-1-right-angle-gearbox-f6b250-24gu-30s-6gu50rt"
    )
    assumptions["C10"].style = "Hyperlink"
    assumptions["C11"].hyperlink = "https://open.er-api.com/v6/latest/USD"
    assumptions["C11"].style = "Hyperlink"
    assumptions.column_dimensions["A"].width = 28
    assumptions.column_dimensions["B"].width = 44
    assumptions.column_dimensions["C"].width = 92
    for row_index in range(5, 5 + len(assumption_rows)):
        text_length = max(len(str(assumptions.cell(row_index, column).value or "")) for column in range(1, 4))
        assumptions.row_dimensions[row_index].height = min(max(32, math.ceil(text_length / 90) * 18), 90)
    assumptions.freeze_panes = "A5"

    output_path = csv_path.with_name("BUDGET_DETAILLE_ESTIMATIF.xlsx")
    workbook.active = 0
    save_workbook_compatible(workbook, output_path)
    return output_path


def main() -> None:
    if "--remplir-donnees" in sys.argv:
        initialise_source_data()
        print("Registres CSV renseignés à partir des sources BFM_V4 et des documents du projet.")
    for register in REGISTERS:
        output = make_workbook(register)
        print(f"Créé : {output.relative_to(ROOT)}")
    detailed_budget = make_detailed_budget_workbook()
    print(f"Créé : {detailed_budget.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
