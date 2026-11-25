# Projet Banque Centrale — dossier consolidé

Mis à jour le 23 novembre 2026. Ce dossier regroupe les sources et livrables actuellement disponibles. Les huit rubriques existantes ont été conservées ; les fichiers de coordination présents avant l’ajout n’ont pas été modifiés ni remplacés. Les sous-dossiers spécialisés contiennent les ressources disponibles ou, lorsqu’une donnée réelle manque, une estimation explicitement marquée ou un constat précis de l’information non documentée.

## Où trouver les ressources

- **Registres de suivi lisibles et modifiables :** [guide des registres](README_REGISTRES.md). Les CSV contiennent les données de travail ; leurs classeurs Excel associés ajoutent filtres, couleurs et consignes de lecture. Les montants budgétaires sont des estimations de planification, pas des devis ni des achats réels.

- **Page visuelle prête pour GitHub Pages :** [index.html](<LIVRABLES FINAUX/Dossier de Conception Final/BFM_V4_GITHUB/index.html>). Le dossier [BFM_V4_GITHUB](<LIVRABLES FINAUX/Dossier de Conception Final/BFM_V4_GITHUB>) contient ses images, ses plans, ses documents et ses 15 fichiers GLB. Publier ensemble `index.html` et `assets/`. La nomenclature se charge en HTTP ; la visionneuse 3D nécessite une connexion au CDN `model-viewer`.
- **CAO BFM_V4 complète :** `MECANIQUE/Modelisation 3D et Plans/Sources_BFM_V4/` contient les fichiers sources STEP, STL et GLB, les scripts, nomenclatures et réserves CAO du lot le plus récent.
- **Plans et implantation :** `MECANIQUE/Modelisation 3D et Plans/Sources_Plan_AGV_v0_1/`.
- **Étude mécanique :** `MECANIQUE/Etude et Conception/BFM_V4/`. Les cotes d’enveloppe et leurs réserves sont aussi dans `MECANIQUE/Calculs et Dimensionnements/BFM_V4/`.
- **Nomenclature et moteur :** `APPROVISIONNEMENT/Nomenclature des Matériels/BFM_V4/` et `APPROVISIONNEMENT/Fournisseurs et Devis/F6B250-24GU-30S/`. Les fichiers moteur disponibles sont une fiche technique et un STEP, pas un devis fournisseur.
- **Électronique conceptuelle :** `ELECTRONIQUE/Conception éléctronique/BFM_V4/` contient les volumes CAO E01–E07 et l’assemblage A11.
- **Prototype logiciel :** `INFORMATIQUE/Architecture Logicielle/Prototype_Supervision/`. Copie destinée au livrable informatique : `LIVRABLES FINAUX/Dossier Informatique/Prototype_Supervision/`.
- **Maquette du bâtiment et modèles :** `ROBOTIQUE/Modelisation du Robot/Maquette_AGV_Bancaire_v0_2/`. Une copie est incluse dans le livrable robotique.
- **Documentation et diagramme UML :** `LIVRABLES FINAUX/Rapport Final du Projet/Documentation_Projet/` et `INFORMATIQUE/Architecture Logicielle/UML/`.
- **Sources de validation et exigences :** rubriques `QUALITE ET SECURITE/` et `LIVRABLES FINAUX/`. L’état de chaque dossier final est détaillé dans [ETAT_DES_DOSSIERS.md](<LIVRABLES FINAUX/ETAT_DES_DOSSIERS.md>).

## Ouvrir les prototypes

Pour lancer l’application React/Vite depuis la racine de ce dossier :

```powershell
Set-Location '.\INFORMATIQUE\Architecture Logicielle\Prototype_Supervision'
npm ci
npm run dev
```

Le prototype web simule localement les missions, mesures et déplacements ; il ne se connecte ni à un robot, ni à ROS 2, ni à un backend. La maquette HTML hors ligne peut être ouverte dans un navigateur compatible WebGL à `ROBOTIQUE/Modelisation du Robot/Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Batiment_3D.html`.

## Portée et limites

Les modèles BFM_V4 et les maquettes de bâtiment sont des supports de conception, pas des plans approuvés pour fabrication. Les cotes sont des enveloppes relevées sur des exports ; matériaux, composants, interfaces, capacité de charge, câblage, sécurité et transfert des sacs restent à valider. Les contrôles JSON portent sur les fichiers et la géométrie, pas sur des essais physiques. Aucun dossier électrique final, devis, analyse de risques approuvée ou plan de fabrication certifié n’a été inventé pour remplir les rubriques correspondantes.

## Documentation de suivi

- Avancement général du projet, priorités et remarques : [AVANCEMENT_PROJET.md](AVANCEMENT_PROJET.md)
- Structure complète des dossiers et fichiers : [STRUCTURE_COMPLETE.md](STRUCTURE_COMPLETE.md)
- Structure générale du dossier principal : [README.md](README_PROJET.md)
- État détaillé des dossiers livrables : [LIVRABLES FINAUX/ETAT_DES_DOSSIERS.md](<LIVRABLES FINAUX/ETAT_DES_DOSSIERS.md>)

## Documentation des grands dossiers

Chaque grand dossier possède son README de présentation et son inventaire exhaustif `STRUCTURE_COMPLETE.md`.

| Domaine | README | Structure détaillée |
|---|---|---|
| Approvisionnement | [README](<APPROVISIONNEMENT/README.md>) | [Structure complète](<APPROVISIONNEMENT/STRUCTURE_COMPLETE.md>) |
| Coordination du projet | [README](<COORDINATION DU PROJET/README.md>) | [Structure complète](<COORDINATION DU PROJET/STRUCTURE_COMPLETE.md>) |
| Électronique | [README](<ELECTRONIQUE/README.md>) | [Structure complète](<ELECTRONIQUE/STRUCTURE_COMPLETE.md>) |
| Informatique | [README](<INFORMATIQUE/README.md>) | [Structure complète](<INFORMATIQUE/STRUCTURE_COMPLETE.md>) |
| Livrables finaux | [README](<LIVRABLES FINAUX/README.md>) | [Structure complète](<LIVRABLES FINAUX/STRUCTURE_COMPLETE.md>) |
| Mécanique | [README](<MECANIQUE/README.md>) | [Structure complète](<MECANIQUE/STRUCTURE_COMPLETE.md>) |
| Outils | [README](<outils/README.md>) | [Structure complète](<outils/STRUCTURE_COMPLETE.md>) |
| Qualité et sécurité | [README](<QUALITE ET SECURITE/README.md>) | [Structure complète](<QUALITE ET SECURITE/STRUCTURE_COMPLETE.md>) |
| Robotique | [README](<ROBOTIQUE/README.md>) | [Structure complète](<ROBOTIQUE/STRUCTURE_COMPLETE.md>) |

## Règle de stockage

Tous les fichiers utiles doivent être conservés à l’intérieur de ce dossier `PROJET BANQUE CENTRALE/`. Les nouvelles sources, images, exports, modèles, classeurs, résultats de tests et livrables doivent être placés dans une rubrique cohérente de ce dossier. Aucun nouveau travail principal ne doit être créé dans les dossiers historiques situés à la racine de `STAGE_L3/`.

