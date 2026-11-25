# Avancement du projet AGV bancaire

**Date de mise à jour :** 23 novembre 2026  
**Phase actuelle :** avant-projet conceptuel et démonstration

Ce document se trouve à la racine du dossier actif `PROJET BANQUE CENTRALE/`.

## Règle de stockage du projet

Tous les fichiers nécessaires au projet doivent être conservés à l’intérieur de :

```text
C:\Users\Nek's\Documents\Nekena\PROJET\STAGE_L3\PROJET BANQUE CENTRALE
```

Aucun document, modèle, image, source, outil ou livrable utile ne doit dépendre d’un emplacement extérieur à ce dossier. Les dossiers historiques situés ailleurs sous `STAGE_L3/` ne doivent plus recevoir les nouveaux travaux. Les exports temporaires doivent être déplacés dans une sous-arborescence appropriée ou supprimés lorsqu’ils ne sont plus nécessaires.

## Légende

| Statut | Signification |
|---|---|
| Terminé | Élément réalisé dans les sources disponibles |
| En cours | Élément démarré ou partiellement documenté |
| À faire | Travaux nécessaires mais non réalisés |
| À confirmer | Décision ou donnée attendue d’une personne ou d’un acteur compétent |
| Bloqué | Dépend d’une information, d’un matériel ou d’une validation externe |

## Tableau d’avancement

| Domaine | Ce qui est fait | Avancement | Ce qui reste à faire |
|---|---|---:|---|
| Analyse du besoin | Exigences initiales, cas d’usage, dépôts C1/C2/C3, trajet entre les deux niveaux | En cours | Valider les cas réels, les responsabilités, les priorités et les procédures |
| Plans du bâtiment | Plan 2D V0.1, maquette HTML V0.2, SVG, géométrie JSON et vues 3D | Partiellement terminé | Mesurer le bâtiment réel, confirmer portes, seuils, dégagements, ascenseur et altitude |
| Mécanique | GLB, STEP/STL, nomenclatures, châssis, coffre, tiroirs, roues et assemblage conceptuel | En cours | Calculs de structure, masse, charge, centre de gravité, stabilité, tolérances et plans de fabrication |
| Station de dépôt | Ébauche 3D de poste fixe | À confirmer | Définir l’alignement, les interfaces, la sécurité, les dimensions et le mécanisme de réception |
| Motorisation | Positionnement conceptuel et fiche/STEP d’un motoréducteur candidat | À confirmer | Sélection finale, couples, freinage, roues porteuses, puissance, refroidissement et montage |
| Transfert des sacs | Cycle illustratif dans la maquette : ouverture, extraction, transfert et retour | Conceptuel | Actionneurs, rails, verrouillages, butées, convoyage, capteurs et essais chargés |
| Électronique | Volumes E01–E07, assemblage conceptuel A11 et BOM préliminaire | En cours | Schémas, composants réels, batterie, protections, câblage, I/O, arrêt d’urgence et conformité |
| Approvisionnement | Nomenclature, budget provisoire, suivi des commandes et moteur candidat | En cours | Inventaire physique, devis locaux, fournisseurs, taxes, importation, commandes et réceptions |
| Logiciel | Prototype React/Vite de supervision, missions simulées, tableau de bord et maquette 3D | Démonstrateur disponible | Backend, authentification, API AGV, persistance, journalisation, erreurs et déploiement sécurisé |
| Robotique | Maquette du bâtiment, SDF, parcours illustratif et sources frontend | Conceptuel | Localisation, cartographie réelle, planification Nav2, gestion d’ascenseur, alignement et essais |
| ROS 2 / communication | Constat enregistré, frontières d’interface et registre à compléter | À faire | Confirmer les API réelles, protocoles, bus, capteurs, fréquence, latence et sécurité |
| Sécurité | Registre préliminaire des risques, réserves CAO et limites documentées | À confirmer | Analyse des risques validée, arrêt d’urgence, protections, tests, procédures et autorisations |
| Qualité | Vérifications de fichiers, affichage, GLB et géométrie | Partiellement terminé | Essais mécaniques, électriques, logiciels, endurance, reprise d’erreur et recette sur site |
| Réglementation | Pistes ISO/IEC dans un registre | À confirmer | Vérifier les éditions, leur adoption locale et leur applicabilité avec les responsables compétents |
| Livrables | Documentation, atlas, rapport sources, page GitHub Pages et prototypes | En cours | Cahier des charges signé, dossier de fabrication, dossier électrique, rapport final validé |

## Progression estimée

Cette estimation est indicative et mesure l’avancement documentaire/CAO, pas la préparation à l’exploitation.

```text
Analyse et exigences          ████████░░  80 %
Plans et maquette de bâtiment █████████░  90 %
Modèles mécaniques conceptuels ████████░░  80 %
Électronique conceptuelle     ████░░░░░░  40 %
Prototype logiciel             ██████░░░░  60 %
Simulation robotique          ██████░░░░  60 %
Approvisionnement             ██░░░░░░░░  20 %
Sécurité et conformité        ██░░░░░░░░  20 %
Fabrication réelle            ░░░░░░░░░░   0 %
Essais physiques              ░░░░░░░░░░   0 %
```

## Éléments réalisés

### Conception du bâtiment

- Plans 2D du bâtiment sur deux niveaux.
- Maquette 3D avec niveau de départ, rez-de-chaussée, ascenseur, couloirs et dépôts.
- Parcours prévu vers le dépôt 3 prioritaire et le dépôt 1 de repli.
- Données JSON, SVG, fichiers SDF/GLB et scripts de génération.

### Conception mécanique

- Assemblages conceptuels pour roue, châssis, motorisation, coffre, tiroirs, électronique et robot complet.
- Nomenclatures des pièces et assemblages.
- Vue éclatée et atlas mécanique illustré.
- Enveloppes mesurées sur les exports GLB.

### Prototype logiciel

- Interface React/Vite pour supervision et missions.
- Création, lancement, suspension et reprise de missions simulées.
- Visualisation 3D, itinéraires animés et vues synthétiques.
- Aucun flux réel n’est connecté.

### Organisation documentaire

- Dossiers par métier : mécanique, électronique, informatique, robotique, qualité, approvisionnement et coordination.
- Registres CSV/XLSX pour budget, commandes, câblage, interfaces, firmware, ROS 2, risques et normes.
- États détaillés des dossiers finaux.
- Présentation statique pour GitHub Pages.

## Travaux restant à réaliser

### Priorité 1 — validation sur site

1. Relever les dimensions réelles du bâtiment.
2. Confirmer les portes, seuils, rampes, escaliers, ascenseurs et dégagements.
3. Mesurer les sacs, leurs masses, dimensions, poignées et contraintes de transport.
4. Confirmer les emplacements C1/C2/C3, les zones d’attente et le dépôt 1 de repli.
5. Définir les règles d’affectation des missions et les procédures en cas d’urgence.

### Priorité 2 — conception mécanique validée

1. Sélectionner les composants auprès de fournisseurs.
2. Remplacer les volumes conceptuels par les modèles et interfaces réels.
3. Calculer la structure, la charge utile, le centre de gravité et la stabilité.
4. Dimensionner roues, motoréducteurs, freinage, rails, verrouillages et actionneurs.
5. Produire tolérances, plans d’atelier, nomenclature d’achat et dossier de fabrication.

### Priorité 3 — intégration électronique et sécurité

1. Définir l’alimentation, la batterie, les protections et les dissociations de puissance.
2. Produire les schémas électriques, plans de câblage et plans de masse.
3. Sélectionner calculateurs, contrôleurs, scanners, capteurs et dispositifs de sécurité.
4. Concevoir l’arrêt d’urgence, les protections contre les chutes et écrasements, et la reprise sécurisée.
5. Faire approuver une analyse de risques et le dossier de conformité.

### Priorité 4 — logiciel et robotique

1. Confirmer les interfaces API disponibles sur l’AGV réel.
2. Créer une passerelle backend authentifiée et journalisée.
3. Ajouter commandes, permissions, états, alarmes, reprises et persistance des missions.
4. Implémenter ou intégrer cartographie, localisation, planification et navigation multi-niveau.
5. Développer les procédures d’ascenseur, d’alignement, de stationnement et de déchargement.

### Priorité 5 — essais et validation

1. Réaliser des essais hors charge puis chargés dans un environnement contrôlé.
2. Vérifier freinage, stabilité, endurance, batteries, sécurité, reprise sur erreur et communications.
3. Tester les portes, l’ascenseur, les stations de dépôt et les casiers avec les sacs réels.
4. Comparer les résultats aux exigences approuvées.
5. Rédiger le rapport de recette et obtenir les autorisations nécessaires.

## Remarques importantes

- Les fichiers STEP/GLB disponibles sont des modèles de conception ; ils ne sont pas tous des modèles fonctionnels contraints ni des plans de fabrication.
- Les 11 contrôles géométriques indiqués comme PASS vérifient des scénarios documentés. Ils ne remplacent pas des essais physiques.
- La charge de 40 kg par casier est une hypothèse de conception. Elle reste à valider par les sacs réels, les calculs et les essais.
- Les moteurs, batteries, calculateurs, capteurs et protections ne sont pas tous sélectionnés ou validés.
- Les valeurs budgétaires sont des estimations de planification, pas des devis ni des achats confirmés.
- Aucun achat ou commande réelle n’est attesté dans les registres disponibles.
- Aucun paquet ROS 2, backend, firmware ou pilote réel n’est confirmé.
- Les normes ISO/IEC citées sont des pistes de vérification, pas des obligations automatiquement applicables à Madagascar.
- Les données publiées ne doivent pas être utilisées pour fabriquer ou exploiter un robot sans mesures, calculs, validation sécurité et approbations.
- Plusieurs copies du même prototype ou des mêmes maquettes existent dans les dossiers sources et les dossiers finaux. Il faut désigner une source maîtresse avant une livraison officielle.

## Sources principales à utiliser

- Synthèse du dossier : [README_PROJET.md](./README_PROJET.md)
- Structure complète : [STRUCTURE_COMPLETE.md](./STRUCTURE_COMPLETE.md)
- États des dossiers finaux : [LIVRABLES FINAUX/ETAT_DES_DOSSIERS.md](<./LIVRABLES FINAUX/ETAT_DES_DOSSIERS.md>)
- Prototype React : [INFORMATIQUE/Architecture Logicielle/Prototype_Supervision/](<./INFORMATIQUE/Architecture Logicielle/Prototype_Supervision/>)
- Plans V0.1 : [MECANIQUE/Modelisation 3D et Plans/Sources_Plan_AGV_v0_1/](<./MECANIQUE/Modelisation 3D et Plans/Sources_Plan_AGV_v0_1/>)
- Maquette V0.2 : [ROBOTIQUE/Modelisation du Robot/Maquette_AGV_Bancaire_v0_2/](<./ROBOTIQUE/Modelisation du Robot/Maquette_AGV_Bancaire_v0_2/>)
- CAO BFM : [MECANIQUE/Modelisation 3D et Plans/Sources_BFM_V4/](<./MECANIQUE/Modelisation 3D et Plans/Sources_BFM_V4/>)
- Présentation GitHub Pages : [LIVRABLES FINAUX/Dossier de Conception Final/BFM_V4_GITHUB/](<./LIVRABLES FINAUX/Dossier de Conception Final/BFM_V4_GITHUB/>)
