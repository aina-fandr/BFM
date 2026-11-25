# Lire le projet AGV bancaire BFM V4

## En une phrase

Le projet étudie un véhicule mobile qui transporterait des sacs dans quatre casiers, puis les remettrait à un poste fixe. Les modèles BFM_V4 montrent une implantation CAO ; ils ne sont ni une machine prête à l’emploi ni des plans approuvés pour fabrication.

## Repères visuels et fichiers

| Repère | Modèle | Ce qu’il représente |
|---|---|---|
| A01 | Roue assemblée | Bandage, jante, moyeu, axe et pièces de liaison |
| A03 | Châssis | Longerons, traverses et platines d’implantation |
| A04 | Motorisation | Deux motoréducteurs et leurs interfaces de positionnement |
| A07 | Coffre 2 × 2 | Enveloppe et organisation des quatre casiers |
| A08 | Quatre tiroirs | Plateaux et rails proposés |
| A11 | Électronique | Volumes d’implantation des équipements |
| A12 | Station de dépôt | Ébauche du poste fixe |
| A13 | Robot complet | Enveloppe du robot fermé |
| A14 | Robot + station | Implantation côte à côte |
| A15 | Vue éclatée | Répartition verticale des sous-ensembles |

Les modèles 3D sont dans `../models/` et `../models/assemblies/`. Leur unité source est le millimètre.

Les rendus JPEG de `../images/` sont des vues calculées depuis ces géométries. Leur code couleur aide à séparer les familles de pièces et ne définit pas la couleur, le matériau ou la finition d’un futur équipement.

## Enveloppes mesurées sur les exports GLB

Les bornes ci-dessous sont calculées sur les sommets transformés de chaque modèle, selon X × Y × Z. Elles ne décrivent ni les jeux fonctionnels, ni les tolérances, ni la masse ou la capacité de charge.

| Export | X × Y × Z | Interprétation |
|---|---:|---|
| A13 · robot complet | 1 112 × 767,5 × 1 070 mm | Bornes maximales du robot fermé |
| A03 · châssis | 1 050 × 639 × 106 mm | Enveloppe de l’assemblage de châssis exporté |
| A07 · coffre | 1 007,5 × 501 × 749 mm | Enveloppe de l’assemblage de coffre |
| A08 · quatre tiroirs | 899 × 494 × 495 mm | Enveloppe du groupe de plateaux exporté |
| A12 · station | 610 × 500 × 1 050 mm | Enveloppe de l’ébauche de station |
| A15 · éclaté | 1 261,5 × 767,5 × 2 260 mm | Enveloppe de la vue éclatée ; pas le gabarit en circulation |

La fiche vectorielle `../plans/enveloppe-mesuree-v4.svg` montre le gabarit A13. Elle ne contient pas de détails de fabrication.

## Composants et statut des chiffres

### Mécanique

- **Mobilité :** deux roues motrices différentielles sont prévues, avec roues porteuses de soutien. La référence, la charge admissible, le freinage et la stabilité restent à dimensionner.
- **Roues :** la nomenclature propose un bandage Ø200 mm, largeur 44 mm. Les roues, roulements et axes ne sont pas encore une sélection complète validée.
- **Motorisation :** le dossier source positionne deux motoréducteurs F6B250-24GU-30S. L’enveloppe nominale inscrite est 237 × 172,5 × 104 mm par unité. La présence d’une fiche fabricant ou d’un STEP ne valide pas les performances ni les interfaces de montage.
- **Casiers :** disposition 2 × 2. La charge de 40 kg par casier et les 160 kg cumulés sont des propositions à vérifier par calcul, choix des rails, essais de stabilité et validation des sacs réels.
- **Tiroirs et déchargement :** rails, verrouillages, actionneurs, butées et transfert vers la station sont schématiques. L’ouverture d’un tiroir chargé présente des risques de basculement et de pincement.

### Électronique

E01–E07 représentent des volumes réservés, pas des références sélectionnées. La nomenclature propose notamment une enveloppe batterie 310 × 210 × 140 mm, un contrôleur 160 × 120 × 42 mm, un driver 130 × 85 × 45 mm et un volume de scanner Ø104 × 62 mm. Tension réelle, chimie, puissance, câblage, protections, capteurs et sécurité restent à définir.

### Logiciel

La page web de ce dossier est une présentation statique avec navigation dans les GLB. Elle ne contient pas de pilote. Le prototype logiciel décrit dans les travaux précédents utilise un état simulé local ; aucune télémétrie, commande de moteurs ou connexion au robot n’est fournie ici.

## Cycle d’usage envisagé

1. Un opérateur affecte un sac à un casier libre après contrôle de ses dimensions.
2. Le robot suit une mission interne jusqu’à la destination prévue.
3. Il s’immobilise face à une station fixe et confirme son positionnement.
4. Un mécanisme conçu et sécurisé transférerait le sac, puis fermerait le casier.

Seuls les modèles CAO et une présentation de ce scénario sont livrés. Aucune de ces étapes n’est validée pour exécution réelle.

## Ce qu’il faut obtenir avant de fabriquer

1. Mesurer les sacs chargés, leurs poignées, le bâtiment, les portes, les seuils et l’ascenseur.
2. Choisir les composants auprès de fournisseurs et remplacer les volumes schématiques par leurs modèles fabricants.
3. Calculer structure, charge utile, centre de gravité, efforts, freinage, stabilité, rails, verrous et actionneurs.
4. Concevoir les fonctions de sécurité, le câblage et les interfaces de commande.
5. Faire valider les risques et les procédures par les responsables compétents, puis réaliser les essais encadrés.

## Origine et dates

Les exports A13, A14 et A15 proviennent du lot `BFM_V4/.../BFM_AGV_CAO_V02/10_ROBOT_COMPLET/GLB/` ; leurs dates de modification sont respectivement le 18/11/2026 à 17:12:32, 17:12:56 et 17:13:28. La nomenclature et le rapport mécanique sont issus du même lot et datés du 18/11/2026 à 17:14. Les rendus présents dans `../images/` sont générés depuis ces GLB.
