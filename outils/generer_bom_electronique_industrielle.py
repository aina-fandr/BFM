from __future__ import annotations

import re
from pathlib import Path
from zipfile import ZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from xlsx_compat import save_workbook_compatible


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "APPROVISIONNEMENT"
    / "Budget Et Stock"
    / "BOM_ELECTRONIQUE_INDUSTRIELLE_PRELIMINAIRE.xlsx"
)
USD_TO_MGA = 4598.727
PRICE_DATE = "23/11/2026"

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

ROBOTEQ_URL = (
    "https://www.roboteq.com/products/products-brushless-dc-motor-controllers/"
    "fblg2360t-detail"
)
ROBOTEQ_DATASHEET_URL = (
    "https://www.roboteq.com/docman-list/motor-controllers-documents-and-files/"
    "documentation/datasheets/robog4/1044-fblg23xx-datasheet/file"
)
JLCPCB_URL = "https://jlcpcb.com/help/article/pcb-assembly-price"
JLCPCB_CAPABILITIES_URL = "https://jlcpcb.com/capabilities/pcb-assembly-capabilities"
ONLOGIC_K410_URL = "https://www.onlogic.com/store/k410/"
SICK_NANOSCAN_URL = (
    "https://www.sick.com/us/en/catalog/products/safety/"
    "safety-laser-scanners/nanoscan3/c/g550621"
)


def style_title(ws, end_column: int, title: str, subtitle: str) -> None:
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end_column)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=end_column)
    title_cell = ws.cell(1, 1, title)
    title_cell.fill = PatternFill("solid", fgColor=NAVY)
    title_cell.font = Font(name="Aptos Display", size=16, bold=True, color=WHITE)
    title_cell.alignment = Alignment(vertical="center")
    subtitle_cell = ws.cell(2, 1, subtitle)
    subtitle_cell.fill = PatternFill("solid", fgColor=PALE_BLUE)
    subtitle_cell.font = Font(name="Aptos", size=10, italic=True, color=GRAY)
    subtitle_cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 34


def style_header(ws, row: int, start_column: int, end_column: int) -> None:
    for column in range(start_column, end_column + 1):
        cell = ws.cell(row, column)
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.font = Font(name="Aptos", size=10, bold=True, color=WHITE)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=Side(style="thin", color=LINE))
    ws.row_dimensions[row].height = 34


def style_body(ws, start_row: int, end_row: int, start_column: int, end_column: int) -> None:
    for row in ws.iter_rows(
        min_row=start_row,
        max_row=end_row,
        min_col=start_column,
        max_col=end_column,
    ):
        for cell in row:
            cell.font = Font(name="Aptos", size=10, color="243746")
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=Side(style="thin", color=LINE))
            if cell.row % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7FAFC")
    for row_number in range(start_row, end_row + 1):
        ws.row_dimensions[row_number].height = 56


def add_hyperlink(cell, url: str) -> None:
    cell.hyperlink = url
    cell.style = "Hyperlink"
    cell.alignment = Alignment(wrap_text=True, vertical="top")


def build_summary(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "Synthèse"
    ws.sheet_view.showGridLines = False
    style_title(
        ws,
        4,
        "Architecture électronique industrielle — proposition préliminaire",
        "Document de cadrage et de chiffrage partiel. Les lignes sont des candidats ou des besoins à définir, jamais des achats, commandes ou réceptions.",
    )
    ws.append([])
    summary_rows = [
        ["Indicateur", "Valeur / décision", "Statut", "Commentaire"],
        [
            "Budget détaillé existant",
            "16 269 312 MGA",
            "Base inchangée",
            "Budget antérieur de nomenclature et provisions; il ne représente pas un système industriel complet.",
        ],
        [
            "Sous-total des composants industriels à prix public identifié",
            round(915 * USD_TO_MGA) + round(28 * USD_TO_MGA),
            "Partiel seulement",
            "Roboteq FBLG2360T (915 USD) + câble Hall ABC (28 USD, accessoire candidat); hors transport, taxes, douane et intégration.",
        ],
        [
            "Total d'une électronique industrielle complète",
            "Non déterminable à ce stade",
            "Devis et conception requis",
            "Ordinateur industriel exact, sécurité, batterie, protections, câblage et interfaces ne sont pas encore sélectionnés/chiffrés.",
        ],
        [
            "Approche recommandée",
            "Ordinateur industriel + contrôleur BLDC industriel + chaîne de sécurité indépendante",
            "À concevoir / valider",
            "Ne pas confier les fonctions de sécurité à une carte MCU/PCB maison ni au logiciel de navigation.",
        ],
    ]
    for row in summary_rows:
        ws.append(row)
    style_header(ws, 4, 1, 4)
    style_body(ws, 5, 8, 1, 4)
    for cell in ws[6]:
        if cell.column <= 4:
            cell.fill = PatternFill("solid", fgColor=PALE_AMBER)
    ws["B6"].number_format = '#,##0" MGA"'
    ws.merge_cells("A10:D10")
    ws["A10"] = "Architecture recommandée"
    ws["A10"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A10"].font = Font(name="Aptos", size=12, bold=True, color=WHITE)
    ws.append(["Sous-système", "Proposition", "État", "Critère / vérification avant achat"])
    style_header(ws, 11, 1, 4)

    architecture_rows = [
        [
            "Calcul / navigation",
            "Ordinateur industriel fanless compatible avec le logiciel réellement retenu (ROS 2 si confirmé), CAN et interfaces réseau nécessaires.",
            "Modèle et prix à obtenir",
            "Définir charge CPU/GPU, OS, température, vibrations, alimentation, E/S et disponibilité du modèle. Un ancien Karbon 410 n'est pas retenu : le fabricant le marque discontinué.",
        ],
        [
            "Commande des 2 moteurs BLDC",
            "Roboteq FBLG2360T, candidat double canal; 2 × 40 A continus, 2 × 60 A en pointe (30 s), Hall, CAN/USB et STO annoncée.",
            "Prix public candidat; compatibilité à confirmer",
            "Vérifier plage de tension minimale à 24 V, courant moteur réel, compatibilité Hall, refroidissement, dimensions, câblage et intégration STO avec le système complet.",
        ],
        [
            "Sécurité fonctionnelle",
            "Scanner de sécurité et relais/automate de sécurité distincts du calculateur de navigation; bouton d'arrêt d'urgence adapté.",
            "Références et prix à obtenir",
            "D'abord réaliser l'analyse de risques et fixer PLr/SIL, distances/champs de protection, temps d'arrêt, interfaces et comportement en défaut; faire valider par une personne compétente.",
        ],
        [
            "Batterie et distribution",
            "Batterie 24 V à choisir avec BMS/chargeur compatibles, alimentation DC/DC, coupure, protections et distribution dimensionnées.",
            "Données insuffisantes",
            "Capacité, chimie, courant de pointe, autonomie et protections ne sont pas déductibles du seul volume CAO E01.",
        ],
        [
            "MCU, PCB et passifs",
            "Ne pas ajouter un microcontrôleur nu ni une PCB de puissance/sécurité par défaut. Utiliser les contrôleurs industriels; PCB d'interface non-sécurité seulement si l'analyse des E/S le justifie.",
            "Schéma et nomenclature requis",
            "Les valeurs/quantités de résistances, condensateurs, connecteurs et protections se déterminent depuis les fiches des interfaces et le schéma validé; elles ne sont pas inventées ici.",
        ],
    ]
    for row in architecture_rows:
        ws.append(row)
    style_body(ws, 12, 16, 1, 4)

    ws.merge_cells("A18:D18")
    ws["A18"] = "Règles de lecture et limites"
    ws["A18"].fill = PatternFill("solid", fgColor=NAVY)
    ws["A18"].font = Font(name="Aptos", size=12, bold=True, color=WHITE)
    notes = [
        "Le sous-total de 4 336 600 MGA est une conversion indicative au taux déjà utilisé dans le budget (1 USD = 4 598,727 MGA); il comprend le contrôleur et le câble Hall candidat. Ce n'est pas le total du robot.",
        "Le prix Roboteq et celui du câble sont des prix publics fabricant relevés dans la recherche du projet; revalider disponibilité, révision, options et prix avant achat.",
        "La page fabricant OnLogic consultée indique que le Karbon 410 est discontinué; le montant de recherche associé ne doit pas servir de prix pour un ordinateur disponible.",
        "Le scanner lidar E04 de la maquette n'est pas un scanner de sécurité sélectionné ou certifié. Aucun prix exact de scanner de sécurité ni de contrôleur de sécurité n'est confirmé dans cette proposition.",
        "Aucune ligne ne constate une commande, une réception, un devis reçu ou un stock physique. Les montants/quantités sont des candidats de planification.",
    ]
    for index, note in enumerate(notes, start=19):
        ws.merge_cells(start_row=index, start_column=1, end_row=index, end_column=4)
        cell = ws.cell(index, 1, note)
        cell.fill = PatternFill("solid", fgColor=PALE_AMBER if index < 23 else PALE_RED)
        cell.font = Font(name="Aptos", size=10, color="243746")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=Side(style="thin", color=LINE))
        ws.row_dimensions[index].height = 38

    ws.freeze_panes = "A5"
    for column, width in {"A": 34, "B": 58, "C": 27, "D": 72}.items():
        ws.column_dimensions[column].width = width
    ws.sheet_properties.tabColor = TEAL


def build_bom(wb: Workbook) -> None:
    ws = wb.create_sheet("BOM industriel")
    ws.sheet_view.showGridLines = False
    headers = [
        "Référence",
        "Sous-système",
        "Besoin / composant",
        "Modèle / candidat",
        "Quantité indicative",
        "Prix unitaire (USD)",
        "Prix unitaire (MGA)",
        "Total ligne (MGA)",
        "Nature du montant",
        "Statut d'achat",
        "Dimensionnement / vérifications",
        "Source / justificatif",
    ]
    style_title(
        ws,
        len(headers),
        "Nomenclature électronique industrielle candidate",
        f"Prix publics candidats consultés dans la recherche projet; conversion USD/MGA = {USD_TO_MGA:,.3f} (référence du budget, {PRICE_DATE}). Cellules vides = prix non confirmé, pas zéro.",
    )
    ws.append([])
    ws.append(headers)

    rows = [
        [
            "IPC-01",
            "Calcul / navigation",
            "Ordinateur industriel fanless",
            "Référence exacte à sélectionner",
            1,
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Charge de calcul, OS/ROS 2, CAN, Ethernet, alimentation, température, vibrations, montage et disponibilité à fixer.",
            "L'ancien OnLogic Karbon 410 est discontinué selon la page fabricant; choisir un SKU courant et demander un devis.",
        ],
        [
            "MOT-01",
            "Commande moteur",
            "Contrôleur double canal BLDC",
            "Roboteq FBLG2360T",
            1,
            915,
            round(915 * USD_TO_MGA),
            round(915 * USD_TO_MGA),
            "Prix public fabricant",
            "Candidat; non commandé",
            "2 × 40 A continus; 2 × 60 A crête/30 s; Hall, CAN/USB, STO annoncé. Confirmer tension minimale compatible avec bus 24 V, moteur, limites thermiques et application de sécurité.",
            "Prix/candidat : " + ROBOTEQ_URL + " | Fiche technique : " + ROBOTEQ_DATASHEET_URL,
        ],
        [
            "MOT-02",
            "Commande moteur",
            "Câble Hall double canal (accessoire candidat)",
            "Roboteq ABC Dual Hall Cable",
            1,
            28,
            round(28 * USD_TO_MGA),
            round(28 * USD_TO_MGA),
            "Prix public fabricant",
            "Option à vérifier; non commandée",
            "Vérifier si nécessaire, inclus ou adapté aux connecteurs et capteurs Hall des moteurs retenus.",
            ROBOTEQ_URL,
        ],
        [
            "SEC-01",
            "Détection de sécurité",
            "Scanner laser de sécurité",
            "SICK nanoScan3 — référence exacte à définir",
            1,
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Champ protecteur, portée, résolution, temps de réponse, montage et interface à déterminer par analyse des risques; la référence exacte et le prix ne sont pas confirmés.",
            SICK_NANOSCAN_URL,
        ],
        [
            "SEC-02",
            "Logique de sécurité",
            "Relais ou automate de sécurité",
            "Modèle à choisir après détermination du PLr/SIL",
            1,
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Définir nombre de zones/entrées, EDM, reset, sorties sûres, arrêt moteurs et preuves de validation.",
            "Choix après analyse de risques; aucun modèle/prix exact confirmé.",
        ],
        [
            "SEC-03",
            "Arrêt d'urgence",
            "Bouton(s), contacts et intégration à la chaîne de sécurité",
            "Référence certifiée à choisir",
            "À déterminer",
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Position, nombre, contacts, catégorie d'arrêt et architecture à définir selon l'évaluation de risques.",
            "Le volume E05 de la CAO n'identifie aucun composant réel.",
        ],
        [
            "PWR-01",
            "Alimentation traction",
            "Batterie 24 V avec BMS adapté",
            "Chimie, capacité et référence à choisir",
            1,
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionnée",
            "Capacité, courant continu/de pointe, autonomie, masse, charge et BMS impossibles à dimensionner sans profil de mission et mesures moteur.",
            "Le volume E01 ne fixe que l'enveloppe et une proposition de tension 24 V.",
        ],
        [
            "PWR-02",
            "Alimentation",
            "Chargeur compatible batterie/BMS",
            "Référence à choisir avec le pack",
            1,
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Choisir avec chimie, tension de charge, courant, connectique et procédure de charge.",
            "Aucune chimie, capacité ou chargeur définis.",
        ],
        [
            "PWR-03",
            "Alimentation logique",
            "Convertisseur(s) DC/DC industriel(s) vers tensions logiques",
            "Tensions et références à définir",
            "À déterminer",
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Lister les charges et courants (ordinateur, scanner, I/O, écran), transitoires, isolation et tenue CEM avant choix.",
            "Pas de schéma ni de charges détaillées.",
        ],
        [
            "PWR-04",
            "Distribution / protection",
            "Fusibles, contacteur, sectionneur, distribution et câblage",
            "À dimensionner sur courant de défaut et architecture",
            "À déterminer",
            None,
            None,
            None,
            "Devis requis",
            "Non sélectionné",
            "Calibres, courants de coupure, sections, connecteurs, cheminement, protections et longueurs à calculer/documenter.",
            "Aucun schéma, calibre ni connecteur n'est défini.",
        ],
        [
            "IO-01",
            "Entrées/sorties non-sécurité",
            "Carte d'interface / microcontrôleur éventuel",
            "Pas de MCU autonome retenu à ce stade",
            "À déterminer",
            None,
            None,
            None,
            "Non chiffré",
            "Non requis avant définition des E/S",
            "À envisager seulement si les interfaces de l'ordinateur et des modules industriels sont insuffisantes; jamais comme contrôleur de sécurité.",
            "Niveaux logiques, capteurs, bus, connecteurs et fonctions non définis.",
        ],
        [
            "PCB-01",
            "PCB personnalisée",
            "PCB d'interface non-sécurité, si nécessaire",
            "Pas de conception validée",
            "À déterminer",
            None,
            None,
            None,
            "Provision non chiffrée",
            "Non commandée",
            "Ne pas concevoir avant architecture d'E/S, schéma, règles CEM, isolation, connecteurs et revue. Exclure toute fonction de sécurité/puissance critique d'une PCB improvisée.",
            "Frais d'assemblage indicatifs uniquement dans l'onglet « PCB & passifs »; fabrication complète non cotée.",
        ],
        [
            "PCB-02",
            "Passifs et connectique",
            "Résistances, condensateurs, protections de signal, connecteurs",
            "Valeurs, boîtiers et quantités non définis",
            "À déterminer",
            None,
            None,
            None,
            "Non chiffré",
            "À définir depuis le schéma",
            "Ne pas acheter une liste générique : choisir valeurs/tolérances/puissances et composants après sélection des capteurs, entrées, alimentation et schéma.",
            "Les passifs internes aux modules industriels sont déjà intégrés; seuls les composants externes seront listés dans une BOM issue du schéma validé.",
        ],
    ]
    for row in rows:
        ws.append(row)
    style_header(ws, 4, 1, len(headers))
    style_body(ws, 5, 4 + len(rows), 1, len(headers))
    for row_number in range(5, 5 + len(rows)):
        status = str(ws.cell(row_number, 10).value or "").casefold()
        if "non command" in status or "non sélection" in status or "à vérifier" in status:
            ws.cell(row_number, 10).fill = PatternFill("solid", fgColor=PALE_AMBER)
        if ws.cell(row_number, 1).value in {"MOT-01", "MOT-02"}:
            ws.cell(row_number, 10).fill = PatternFill("solid", fgColor=PALE_GREEN)
        for column in (6, 7, 8):
            ws.cell(row_number, column).number_format = '#,##0.00;[Red]-#,##0.00;–'
        source_cell = ws.cell(row_number, 12)
        if ws.cell(row_number, 1).value == "MOT-01":
            add_hyperlink(source_cell, ROBOTEQ_URL)
    ws.auto_filter.ref = f"A4:L{4 + len(rows)}"
    ws.freeze_panes = "A5"
    widths = [14, 22, 38, 40, 18, 18, 20, 19, 24, 27, 68, 66]
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.sheet_properties.tabColor = TEAL


def build_pcb(wb: Workbook) -> None:
    ws = wb.create_sheet("PCB & passifs")
    ws.sheet_view.showGridLines = False
    headers = ["Élément", "Prix/service publié", "Ce que le montant couvre", "Ce qui reste hors prix", "Décision projet", "Source"]
    style_title(
        ws,
        len(headers),
        "PCB, microcontrôleur et composants passifs",
        "Aucun schéma électronique n'étant fourni, les valeurs et quantités de composants ne peuvent pas être renseignées sans les inventer.",
    )
    ws.append([])
    ws.append(headers)
    rows = [
        [
            "JLCPCB — frais de mise en place PCBA économique",
            "8,18 USD",
            "Frais de service publiés pour le niveau de montage économique.",
            "PCB, composants, stencil/options, quantité, transport, taxes et douane; le total dépend des fichiers de conception.",
            "Repère de service uniquement; pas un prix total de carte.",
            JLCPCB_URL,
        ],
        [
            "JLCPCB — montage standard simple face",
            "25,56 USD",
            "Frais de service PCBA standard simple face publiés.",
            "PCB, BOM, options, expédition et autres frais.",
            "À chiffrer seulement après conception.",
            JLCPCB_URL,
        ],
        [
            "JLCPCB — montage standard double face",
            "51,12 USD",
            "Frais de service PCBA standard double face publiés.",
            "PCB, BOM, options, expédition et autres frais.",
            "À chiffrer seulement après conception.",
            JLCPCB_URL,
        ],
        [
            "JLCPCB — assemblage SMT par joint",
            "0,0016 USD / joint",
            "Tarif unitaire de service indiqué pour les paliers concernés.",
            "Nombre de joints, PCB, composants, options, stencil, transport et taxes.",
            "Ne pas extrapoler sans BOM/fichiers de fabrication; vérifier le tarif courant.",
            JLCPCB_URL,
        ],
        [
            "Microcontrôleur nu",
            "Non chiffré",
            "Aucun composant MCU particulier retenu.",
            "Référence, quantité, tension, E/S, communications, température, support et logiciel.",
            "Non recommandé comme contrôleur central ou dispositif de sécurité sans architecture et validation.",
            "Séparer navigation (ordinateur industriel), traction (drive industriel) et sécurité (contrôleur de sécurité).",
        ],
        [
            "Résistances et condensateurs",
            "Non chiffrés",
            "Aucune valeur ni quantité ne peut être tirée des volumes CAO.",
            "Schéma, capteurs, interfaces, tolérance, puissance, tension, CEM, boîtier et conditions thermiques.",
            "À intégrer dans une nomenclature générée depuis le schéma validé; ne pas inventer de valeurs.",
            "Les composants internes aux cartes/contrôleurs achetés ne sont pas à compter comme pièces séparées.",
        ],
        [
            "PCB d'interface non-sécurité",
            "Non chiffrée",
            "Éventuellement une interface de signaux après définition des E/S.",
            "Schéma, routage, vérification CEM, choix composants, BOM, fabrication et essais.",
            "Optionnelle; aucun besoin établi. Ne pas héberger la fonction de sécurité ou la commande de puissance.",
            JLCPCB_CAPABILITIES_URL,
        ],
    ]
    for row in rows:
        ws.append(row)
    style_header(ws, 4, 1, len(headers))
    style_body(ws, 5, 4 + len(rows), 1, len(headers))
    ws.auto_filter.ref = f"A4:F{4 + len(rows)}"
    for row_number in range(5, 5 + len(rows)):
        status = str(ws.cell(row_number, 5).value or "").casefold()
        ws.cell(row_number, 5).fill = PatternFill(
            "solid",
            fgColor=PALE_AMBER if "à " in status or "option" in status else PALE_BLUE,
        )
        if row_number <= 8:
            ws.cell(row_number, 2).fill = PatternFill("solid", fgColor=PALE_GREEN)
        source_cell = ws.cell(row_number, 6)
        source_value = str(source_cell.value or "")
        if source_value.startswith("https://"):
            add_hyperlink(source_cell, source_value)
    ws.freeze_panes = "A5"
    for index, width in enumerate([42, 25, 45, 62, 54, 68], start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.sheet_properties.tabColor = "70AD47"


def build_decisions(wb: Workbook) -> None:
    ws = wb.create_sheet("Données à confirmer")
    ws.sheet_view.showGridLines = False
    headers = ["Priorité", "Donnée requise", "État connu", "Valeur à obtenir / décision", "Débloque"]
    style_title(
        ws,
        len(headers),
        "Données nécessaires avant BOM complète et budget d'achat",
        "Compléter ces points avec l'équipe mécanique, électronique, robotique et sécurité; les valeurs manquantes empêchent un chiffrage fiable.",
    )
    ws.append([])
    ws.append(headers)
    rows = [
        ["1", "Moteurs exacts et courants", "Deux motoréducteurs BLDC annoncés 24 V / 250 W / 13 A dans la base de projet.", "Fiche de référence exacte; préciser si 13 A est le courant d'entrée nominal, phase ou autre; courant de démarrage/blocage; Hall/encodeur et frein.", "Validation driver, câbles, connecteurs, protections et autonomie."],
        ["2", "Batterie et mission", "24 V proposés; chimie, capacité et autonomie inconnues.", "Profil mission, charge utile, durée, cycles, vitesse, pente, courant de pointe, température et recharge.", "Pack, BMS, chargeur, convertisseurs et protections."],
        ["3", "Fonctions de sécurité", "Scanner E04 et arrêt E05 sont des volumes conceptuels; aucun composant réel.", "Analyse de risques, PLr/SIL requis, vitesse, distance d'arrêt, champ protecteur, reset, zones et états sûrs.", "Scanner exact, contrôleur de sécurité, E-stop, architecture STO et validation."],
        ["4", "Calculateur et logiciel", "Aucun calculateur sélectionné; ROS 2/API réelle non confirmés.", "Logiciel/middleware, charge CPU/GPU, stockage, ports, CAN/Ethernet, OS, température, montage et support.", "SKU d'ordinateur industriel et accessoires."],
        ["5", "Capteurs et E/S", "Types de capteurs de casier, écran et connectique non spécifiés.", "Liste des capteurs, niveaux électriques, sorties, longueurs, fréquence, connecteurs et environnement.", "Besoin réel ou non de MCU/PCB, valeurs de passifs et câblage."],
        ["6", "Environnement d'exploitation", "Site de projet mentionné à Fianarantsoa; exigences terrain détaillées non fournies.", "Température, poussière/eau, vibrations, EMC, nettoyage, disponibilité maintenance et exigences réglementaires locales.", "IP, température, composants, connecteurs et validation."],
        ["7", "Règles d'approvisionnement", "Aucun devis, commande ou stock attesté.", "Fournisseurs autorisés, coût transport/douane/taxes, devise, délais et pièces de rechange.", "Budget complet et planning d'achat réels."],
    ]
    for row in rows:
        ws.append(row)
    style_header(ws, 4, 1, len(headers))
    style_body(ws, 5, 4 + len(rows), 1, len(headers))
    ws.auto_filter.ref = f"A4:E{4 + len(rows)}"
    for row_number in range(5, 5 + len(rows)):
        ws.cell(row_number, 1).fill = PatternFill("solid", fgColor=PALE_RED if row_number <= 7 else PALE_AMBER)
    ws.freeze_panes = "A5"
    for index, width in enumerate([13, 32, 54, 78, 56], start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.sheet_properties.tabColor = "C00000"


def main() -> None:
    wb = Workbook()
    wb.properties.title = "BOM électronique industrielle préliminaire"
    wb.properties.subject = "Architecture candidate, BOM partielle et prix sourcés"
    wb.properties.creator = "Projet robot"
    build_summary(wb)
    build_bom(wb)
    build_pcb(wb)
    build_decisions(wb)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    save_workbook_compatible(wb, OUTPUT)

    check = load_workbook(OUTPUT, data_only=False, read_only=False)
    expected_sheets = {"Synthèse", "BOM industriel", "PCB & passifs", "Données à confirmer"}
    if set(check.sheetnames) != expected_sheets:
        raise ValueError(f"Onglets inattendus dans le classeur : {check.sheetnames}")
    if check["BOM industriel"].max_row != 17:
        raise ValueError("Nombre de lignes inattendu dans la BOM industrielle")
    if any(sheet.tables for sheet in check.worksheets):
        raise ValueError("Les classeurs de compatibilité ne doivent pas contenir de tableaux structurés")
    if check["Synthèse"]["B6"].value != round(915 * USD_TO_MGA) + round(28 * USD_TO_MGA):
        raise ValueError("Le sous-total des prix publics ne correspond pas au calcul")
    check.close()
    with ZipFile(OUTPUT) as package:
        for name in package.namelist():
            if not name.endswith(".rels"):
                continue
            relationship_xml = package.read(name)
            if re.search(rb'Target="/(?!/)', relationship_xml):
                raise ValueError(f"Cible OOXML absolue non normalisée dans {name}")
    print(f"Classeur créé et relu : {OUTPUT}")


if __name__ == "__main__":
    main()
