# BFM AGV — DOSSIER CAO V02 — CONCEPT NON VALIDÉ

## Contenu
- 8 familles de pièces, avec fichiers STEP (solides B-Rep) et STL individuels.
- 09_ASSEMBLAGES: sous-ensembles, dont roue assemblée ET éclatée, motorisation, base roulante, coffre et tiroirs.
- 10_ROBOT_COMPLET: robot global, robot + station de dépôt, vue éclatée globale.
- Pour chaque assemblage : STEP (géométries), GLB (aperçu 3D coloré).
- NOMENCLATURE_PIECES.csv : fonctions, matériaux et dimensions préliminaires.
- NOMENCLATURE_ASSEMBLAGES.csv : instances et positions en millimètres.
- generer_cao.py : script source pour modifier et régénérer.

## Référentiel et dimensions
Unité de modélisation : millimètre. X avant/arrière; Y gauche/droite; Z hauteur.
Châssis nominal 1100 x 600 mm, coffre nominal 1000 x 500 x 750 mm.
Deux roues motrices Ø200 mm, quatre roulettes de soutien symboliques.
Coffre 2x2, compartiments indépendants; tiroirs à extraction sur rails.
Déchargement: vis d'extraction et plaque poussoir simplifiés; station fixe élévatrice est une ÉBAUCHE géométrique, pas une machine fonctionnelle.

## Statut IMPORTANT
Tous les modèles sont des propositions dimensionnelles pour étude et prototypage, PAS des plans constructibles validés.
- Les roues, roulements, motoréducteurs, capteurs, serrures, actionneurs et composants électroniques sont des VOLUMES CONCEPTUELS. Remplacer par STEP fabricant une fois les références sélectionnées.
- Les perçages, les liaisons cinématiques, la visserie réelle, soudures, réglages, butées détaillées et câblage ne sont pas définis.
- L'export STEP d'assemblage est un composé de solides positionnés, sans contraintes paramétriques natives, et non un assemblage SolidWorks/FreeCAD déjà contraint.
- Les casiers et tiroirs ne sont pas dimensionnés sur la géométrie réelle d'un sac de 40 kg: étudier les interférences avant fabrication.
- Risques majeurs : stabilité des tiroirs ouverts, pente/sol, transfert de 40 kg, passage des portes, charge admissible de l'ascenseur, collisions entre volumes et accessibilité humaine.
- Les sous-ensembles comprennent certains chevauchements volumétriques; ce dossier est une base d'organisation et de visualisation, pas un assemblage sans collision.
- Ne pas utiliser le système de déchargement avec une charge réelle avant analyse des risques, calculs, essais et supervision.

## Utilisation
Ouvrir les fichiers STEP dans FreeCAD ou autre logiciel de CAO. Ouvrir les GLB dans Blender ou un visualiseur 3D. Le script nécessite cadquery, trimesh et numpy.
