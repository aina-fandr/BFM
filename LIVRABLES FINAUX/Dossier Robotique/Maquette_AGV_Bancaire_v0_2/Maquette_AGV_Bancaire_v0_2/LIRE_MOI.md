# Maquette 3D du bâtiment - AGV bancaire V0.2

Cette maquette reprend le plan 2D retenu le 20 octobre 2026. Les deux niveaux
utilisent le même repère, en mètres, avec le même emplacement pour l'ascenseur.
L'écart d'altitude de 3 m, les hauteurs et les dimensions signalées H restent
des hypothèses de conception.

## Ouvrir la vue 3D

Ouvrir **Maquette_AGV_Batiment_3D.html** dans Chrome, Edge ou Firefox.
Ce fichier fonctionne hors ligne, sans installation ni serveur. WebGL doit être
disponible dans le navigateur.

- Choisir le niveau de départ, le rez-de-chaussée, les deux niveaux ou la vue éclatée.
- Faire glisser la souris pour pivoter ; utiliser la molette ou les boutons pour zoomer.
- Sur écran tactile : glisser pour pivoter et pincer pour zoomer.
- Activer la coupe pour lire les pièces ; la désactiver pour voir les murs à leur hauteur prévue.
- Les cases permettent d'afficher les parcours, les noms et le gabarit AGV.
- Le clavier fonctionne lorsque la vue est sélectionnée : flèches, puis + ou -.

La vue éclatée ajoute uniquement une séparation visuelle. Les fichiers de modèles
conservent les altitudes proposées 0 m et +3 m.

## Contenu du bâtiment

- Salle de collecte : 8 x 6 m ; pièce A : 4 x 3 m.
- Pièce B, bureaux et comptoir, placés selon le plan de principe.
- Sortie sud-ouest, couloir de 6 m et ascenseur A.
- Au RDC : parcours de 2 m, 6 m et 10 m, hall et trois dépôts.
- Dépôt 3 prioritaire avec zones C1, C2 et C3 ; dépôt 1 en repli autorisé.
- Portes coulissantes représentées ouvertes, avec cadres et linteaux.
- Cabine de l'ascenseur fixe pour cette étape.
- Emplacement d'attente après livraison.

Le robot reprend un châssis de 1,10 x 0,70 m, un coffre de 1,00 x 0,50 x
0,75 m et quatre tiroirs indépendants en disposition 2 x 2. La charge nominale
proposée est de 40 kg par tiroir, soit 160 kg au total. Le volume intérieur
indicatif d'un tiroir est de 0,46 x 0,44 x 0,30 m ; les sacs réels doivent être
mesurés pour confirmer qu'ils y entrent. Les glissières, butées, verrous et
l'extension de service de 0,35 m sont des hypothèses, pas des composants
dimensionnés. Le robot reste un modèle statique et ses roues sont fixes.
La simulation React présente séparément un cycle automatique en cinq étapes :
accostage, alignement d'une station élévatrice, extraction du tiroir, transfert
vers la zone C1/C2/C3 et reverrouillage. Ce cycle animé ne représente pas un
mécanisme testé et n'envoie aucune commande réelle.

## Dossier visuel du robot

L'atlas mécanique imprimable se trouve dans `../../docs/atlas_mecanique_robot_agv_bfm_v2.pdf`.
Il réunit les vues 2D cotées, les rendus assemblé/éclaté, le détail d'un tiroir
et l'ordre d'assemblage proposé. La source imprimable est
`../../docs/atlas_mecanique_robot_agv_bfm_v2.html`; le plan 2D vectoriel est
`../../docs/plan_2d_robot_agv_bfm_v2.svg`, et les rendus PNG se trouvent dans
`../../docs/images/`.

## Fichiers 3D

Dans `modeles/` :

| Fichier | Usage |
| --- | --- |
| `robot_agv.glb` | Robot seul, quatre tiroirs et châssis, importable dans un éditeur glTF 2.0 |
| `robot_agv_eclate.glb` | Vue éclatée avec sous-ensembles séparés et pièces nommées pour l'inspection |
| `catalogue_robot.json` | Index des fichiers individuels et des étapes, avec noms, sous-ensembles et dimensions |
| `pieces/*.glb` | Un fichier GLB indépendant par objet 3D modélisé, placé à l'origine pour l'inspection |
| `sous_ensembles/*.glb` | Roue motrice assemblée et la même roue éclatée en composants |
| `assemblage/*.glb` | Douze modèles cumulés, du châssis nu au robot terminé |
| `batiment_complet.glb` | Bâtiment complet, importable dans un éditeur 3D prenant en charge glTF 2.0 |
| `niveau_depart.glb` | Niveau de départ et gabarit AGV |
| `rez_de_chaussee.glb` | Rez-de-chaussée |
| `batiment_complet.sdf` | Monde Gazebo des deux niveaux, murs entiers |
| `niveau_depart.sdf` | Monde Gazebo du niveau de départ, murs entiers |
| `rez_de_chaussee.sdf` | Monde Gazebo du RDC, murs entiers |
| `niveau_depart_coupe.sdf` | Monde Gazebo du niveau de départ, murs réduits pour la lecture |
| `rez_de_chaussee_coupe.sdf` | Monde Gazebo du RDC, murs réduits pour la lecture |

Les fichiers SDF n'utilisent aucun modèle ni texture à télécharger. Leur cible
est Gazebo Harmonic. Les dalles, murs, meubles, réceptions et gabarit possèdent
des collisions statiques. Les éléments décoratifs et les vantaux ouverts sont
visuels. Les mondes isolés présentent la cabine à leur niveau ; le monde complet
conserve une seule cabine, au niveau de départ.

Les modèles AGV incluent une représentation conceptuelle du châssis, des roues,
du coffre, des quatre tiroirs, de leurs glissières, des verrouillages et de
l'électronique. Dans `robot_agv_eclate.glb`, les groupes sont décalés pour rendre
les sous-ensembles lisibles ; les petites fixations sont des repères graphiques.
Ces volumes ne définissent ni références commerciales ni plans de fabrication.

Le dossier `pieces/` fournit chaque objet affiché dans le modèle robot comme un
GLB séparé, y compris les exemplaires distincts des éléments répétés. Le
`catalogue_robot.json` permet de retrouver un fichier par son nom et son
sous-ensemble. `sous_ensembles/roue_motrice_assemblee.glb` et
`roue_motrice_eclatee.glb` montrent une roue seule, puis ses composants
séparés. Les étapes de `assemblage/` sont des vues cumulatives dans l'ordre
proposé : châssis, roues, batterie, coffre, séparateurs, glissières, tiroirs
S1 à S4, commandes/électronique, puis toit. Chaque étape conserve les
coordonnées finales des pièces montées ; elle n'anime pas leur insertion et ne
décrit pas les fixations réelles. Les pièces et les étapes restent des modèles
conceptuels, pas des plans de fabrication validés.

## Ouvrir dans Gazebo Harmonic

Depuis le dossier extrait, choisir l'une des commandes :

```bash
bash lancer_gazebo.sh depart
```

```bash
bash lancer_gazebo.sh rdc
```

```bash
bash lancer_gazebo.sh complet
```

Le script appelle simplement `gz sim` sur le monde choisi. Gazebo Harmonic doit
déjà être installé. Les deux premières commandes ouvrent les versions en coupe.

## Modifier et régénérer

`data/geometrie_plan_retenu.json` contient les coordonnées du plan, les murs,
les trajets et les catégories de billets. Les rectangles utilisent la forme
`[x_min, y_min, x_max, y_max]`, avec x vers l'est, y vers le nord et z vers le haut.
L'origine est l'angle intérieur sud-ouest de la salle de collecte.

Dans `data/parametres_3d.json`, les réglages suivants sont utilisés à la génération :

- `wall_height_m` : hauteur des murs ;
- `door_clear_height_m` : hauteur libre des portes ;
- `slab_thickness_m` : épaisseur des dalles ;
- `floor_elevation_m` : altitude du niveau de départ.

Les autres valeurs du fichier décrivent le gabarit et les hypothèses de cette
version. La disposition des tiroirs se modifie dans `generer_maquette.py`.
`visualiseur_template.html` contient l'interface et le rendu 3D.

Pour régénérer, installer les deux dépendances puis exécuter le générateur :

```bash
python3 -m pip install -r requirements.txt
python3 generer_maquette.py
```

Le générateur réécrit les modèles, le visualiseur et l'aperçu. Il conserve les
réglages déjà présents dans `data/parametres_3d.json`.

## Vérifications et portée

`verification_maquette.json` contient les contrôles de structure GLB/SDF, des
fichiers individuels et des douze étapes d'assemblage, ainsi que la
correspondance des murs avec le plan retenu. `verification_affichage.json`
résume les essais de la vue 3D sur écran large et sur écran étroit.
Le GLB `robot_agv.glb` est vérifié pour son format, sa charge nominale et ses
quatre façades de tiroir ; ce contrôle n'est pas un essai mécanique.

Les modèles GLB/SDF du bâtiment restent statiques. La navigation ROS 2 / Nav2,
le calcul des masses et de stabilité, les capteurs, la commande des portes,
l'ascenseur et le transfert physique des sacs restent à développer ou valider.
Voir `../../docs/conception_mecanique_robot.md` pour le cycle automatique
proposé et les validations à réaliser avant fabrication.

Les SDF ont été contrôlés comme fichiers XML et sur leur géométrie. **Gazebo
n'est pas installé dans l'environnement de génération : leur exécution dans
Gazebo n'a pas été vérifiée.**

Références de format :

- https://gazebosim.org/docs/harmonic/sdf_worlds/
- https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
