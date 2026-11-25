# BFM V4 — dossier visuel AGV

Ce dossier contient une page de présentation autonome et ses ressources locales. **`index.html` est le point d’entrée** ; aucun outil de compilation ni serveur applicatif n’est requis.

## Consulter la page

- Pour une expérience complète, publier ce dossier avec GitHub Pages ou le servir en HTTP local.
- L’ouverture directe en `file://` peut empêcher le navigateur de lire la nomenclature CSV. Les modèles et images restent présents, mais la liste filtrable doit être servie en HTTP.
- La visionneuse 3D est chargée depuis `model-viewer` sur Google CDN. Une connexion Internet est donc requise pour manipuler les GLB ; les rendus JPEG et les plans SVG locaux servent de prévisualisation de secours.

## Publier sur GitHub Pages

1. Copier **tout le contenu** de `BFM_V4_GITHUB` dans la racine du dépôt, ou conserver le dossier et sélectionner ce sous-dossier comme source Pages.
2. Vérifier que `index.html` et `assets/` restent au même niveau.
3. Dans GitHub, ouvrir **Settings → Pages**, choisir la branche et le dossier qui contiennent `index.html`, puis enregistrer.
4. Attendre la publication et ouvrir l’URL fournie par GitHub Pages.

## Contenu

- `index.html` : présentation, visionneuse 3D, cotes, scénario conceptuel et nomenclature filtrable.
- `assets/models/` : 15 exports GLB au total — A13, A14 et A15, ainsi que 12 assemblages issus du lot BFM_V4.
- `assets/images/` : nouveaux rendus hors ligne, calculés depuis les GLB BFM_V4.
- `assets/plans/enveloppe-mesuree-v4.svg` : gabarit vectoriel des enveloppes mesurées du robot A13.
- `assets/documents/` : guide de lecture V4, nomenclature, rapport, réserves CAO, notes de conception et documents de référence.

Les modèles exportés sont en millimètres ; la visionneuse applique l’échelle 0,001 pour les présenter en mètres. L’enveloppe maximale du robot fermé A13 est de **1 112 × 767,5 × 1 070 mm** (X × Y × Z). Il s’agit des bornes du GLB, pas d’une tolérance ni d’une cote de fabrication.

Les rendus JPEG sont calculés hors ligne depuis les géométries BFM_V4 et recolorisés par sous-ensemble pour faciliter leur lecture. Ces couleurs ne spécifient pas les matériaux ou les finitions du projet.

## Limites d’usage

Ce dossier présente un avant-projet. Les volumes, charges, matériaux, équipements électroniques, interfaces, station et cycle de transfert restent à valider. La capacité de 40 kg par casier est une proposition, pas une charge utile certifiée. La page n’est connectée à aucun robot et n’envoie aucune commande.
