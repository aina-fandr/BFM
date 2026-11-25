# Avant-projet mécanique du robot AGV

## Statut

Cette version fixe une **architecture de travail pour la maquette 3D**, pas un
plan de fabrication ni une validation de sécurité. Les dimensions du bâtiment
restent partiellement hypothétiques et les sacs réels n'ont pas encore été
mesurés. Les dimensions marquées ci-dessous doivent donc être confirmées sur
site et par des essais avant tout achat de pièces ou fabrication.

## Architecture proposée

- Châssis bas d'environ **1,10 × 0,70 m**, dans l'enveloppe d'essai retenue.
- Coffre d'environ **1,00 × 0,50 × 0,75 m** posé sur le châssis.
- Hauteur totale visée d'environ **1,12 m**, arrêt d'urgence compris.
- Quatre tiroirs distincts en disposition **2 colonnes × 2 niveaux** ; charge
  nominale proposée de **40 kg par tiroir**, soit **160 kg au total**.
- Gabarit intérieur indicatif de chaque tiroir : **0,46 × 0,44 × 0,30 m**
  (environ 61 litres). Ce volume ne garantit pas que les sacs existants y
  entreront : mesurer les sacs pleins, avec leurs poignées et leur fermeture.
- Deux roues motrices différentielles et deux roues porteuses orientables
  constituent l'option de mobilité la plus simple à prototyper. La géométrie
  3D montre quatre roues, mais ne spécifie pas encore leurs références.
- Pour limiter les coûts, partir d'un châssis mécano-soudé en profilés acier
  disponibles localement et de tôles pliées pour le coffre ; sections,
  épaisseurs, assemblages et protection anticorrosion restent à calculer et
  tester avant d'en faire un plan de fabrication.

Les tiroirs sont orientés vers une même face pour rendre leur accès visible et
faciliter une interface de réception commune. Chaque tiroir doit recevoir une
glissière à extension complète, une butée mécanique, une retenue de sac et un
verrouillage indépendant. Une seule ouverture à la fois est autorisée.
La capacité nominale des glissières doit être sélectionnée pour la masse du
tiroir chargé, avec la marge dynamique définie après mesure et calcul ; une
simple valeur de charge statique catalogue ne suffit pas pour l'extension.

## Cycle automatique illustré

La conception de travail retient désormais un **déchargement automatique sur
une station fixe**. Le modèle React propose une animation détaillée du cycle ;
les pièces, charges, temps et courses qu'elle représente restent des valeurs
conceptuelles, pas des spécifications validées.

1. **Arrivée et immobilisation** : le robot s'arrête dans la zone dédiée. La
   simulation indique la traction inhibée et attend la confirmation
   d'accostage.
2. **Mise à hauteur** : le plateau récepteur se déplace verticalement pour
   s'aligner sur le compartiment choisi : environ 0,878 m pour S1/S2 ou 0,513 m
   pour S3/S4 au-dessus du sol du robot (cotes H).
3. **Extraction** : un actionneur propre au compartiment sélectionné libère
   son verrou et sort le plateau sur une course indicative de 0,35 m, guidé
   par deux rails. Les trois autres casiers restent fermés.
4. **Transfert et tri** : un support continu guide le sac vers le plateau
   récepteur. La station s'abaisse vers une hauteur de réception indicative
   de 0,39 m, puis dirige le sac vers la zone C1, C2 ou C3 fournie par la
   commande. Le sac n'est pas lâché en chute libre. Le transfert final reste
   à choisir entre poussoir et convoyeur/rouleaux.
5. **Retour et verrouillage** : le tiroir vide rentre en butée, le verrou est
   confirmé fermé et la traction n'est réautorisée qu'après cette confirmation.

L'interface de démonstration permet de sélectionner S1 à S4, de lancer le cycle
isolément ou de le déclencher à l'arrivée d'une mission, puis de recharger les
casiers simulés. Elle visualise la hauteur du plateau, la course indicative,
la zone de catégorie, l'état du verrou et l'inhibition de traction. La
simulation navigateur ne pilote aucun moteur ni capteur.

## Sous-ensembles à concevoir

- quatre tiroirs et quatre actionneurs linéaires indépendants, avec rails,
  butées, retenue du sac et verrouillage à état surveillé ;
- un capteur de position du robot par rapport à la station et des références
  mécaniques d'accostage ;
- un plateau élévateur guidé, un actionneur dimensionné pour la charge et des
  positions haut/bas surveillées ;
- un pont de transfert à support continu entre le tiroir et le plateau ;
- un mécanisme de distribution vers trois réceptions C1/C2/C3 ;
- commande basse tension et interverrouillages : aucune traction pendant une
  ouverture, un défaut ou une perte de confirmation de verrou.

Les fins de course, détection de sac présent/absent, surcharge, obstacle et
anti-pincement doivent être définis avec l'encadrement et le responsable du
site. Aucune valeur de vitesse, force, puissance ou capacité d'actionneur
n'est fixée avant de mesurer les sacs et de calculer les cas de charge.

Une extension indicative de **0,35 m** est inscrite dans les paramètres. Elle
porte l'encombrement de service à environ 1,05 m sur l'axe d'ouverture : le
robot ne doit extraire un tiroir qu'à un poste dont la zone libre et
l'interface avec l'élévateur auront été mesurées. Cette extension n'est pas
incluse dans l'enveloppe de circulation fermée de 1,30 × 0,90 m.

## Compatibilité géométrique provisoire

L'enveloppe de commande fermée retenue est de **1,30 × 0,90 m**, incluant une
marge de 0,10 m autour du châssis d'essai de 1,10 × 0,70 m. Elle est compatible
en dimension avec une cabine hypothétique de 2,20 × 2,20 m et une porte
hypothétique de 1,20 m, mais les marges sont faibles : orientation, seuil,
portes, tolérances, garde au sol et dégagements doivent être relevés sur place.
Les virages annoncés à 1,80 × 1,80 m doivent aussi être vérifiés avec le robot
chargé et sa trajectoire réelle.

## Points de validation mécanique

Avant de figer les plans de fabrication :

- mesurer les quatre sacs pleins et vérifier l'accès au coffre ;
- définir le poids à vide, le centre de gravité et les charges admissibles du
  châssis, de chaque glissière et de chaque roue ;
- vérifier stabilité au freinage, dans les virages, sur les seuils et avec un
  tiroir en extension ; les deux tiroirs supérieurs peuvent représenter 80 kg
  placés en hauteur ; limiter à un seul tiroir ouvert ;
- vérifier frein de maintien, distance d'arrêt, vitesse maximale et retenue des
  sacs en cas de coupure d'alimentation ;
- réaliser un gabarit à l'échelle 1 et essayer les couloirs, portes et ascenseur
  avec les jeux mesurés ;
- choisir les composants disponibles localement et chiffrer avant de figer
  moteurs, batterie, glissières et verrouillages ;
- faire valider les risques et les procédures par l'encadrement du laboratoire
  et le responsable du site.

La maquette GLB/SDF montre maintenant le châssis, le coffre et les quatre
tiroirs ; l'animation web ajoute l'extraction, le transfert guidé et la station
élévatrice. Ni la maquette ni l'animation ne constituent un calcul de
structure, un essai de charge, une étude d'anti-pincement ou une preuve qu'un
sac de 40 kg peut être transféré sans risque.

## Fichiers de référence

- Atlas mécanique illustré (plans 2D, assemblage général, éclaté, détail d'un
  tiroir et ordre de montage) : `docs/atlas_mecanique_robot_agv_bfm_v2.pdf`.
- Plan 2D vectoriel : `docs/plan_2d_robot_agv_bfm_v2.svg`.
- Rendus PNG assemblé, éclaté et détail : `docs/images/`.
- Modèles glTF assemblé et éclaté : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/modeles/robot_agv.glb` et `robot_agv_eclate.glb`.
- Pièces 3D autonomes et ordre d'assemblage progressif : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/modeles/catalogue_robot.json`, avec un GLB par objet dans `modeles/pieces/` et douze modèles cumulés dans `modeles/assemblage/`.
- Lot CAO détaillé de la roue motrice et de ses liaisons (visserie, paliers, arbre, accouplement, supports et raccords au châssis) : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/BFM_AGV_CAO_V01/`.
- Source HTML imprimable de l'atlas :
  `docs/atlas_mecanique_robot_agv_bfm_v2.html`.
- Guide de procédure conceptuel, avec les actions, résultats attendus, arrêts
  et contrôles avant fabrication : `docs/manuel_operatoire_conceptuel_agv_bfm_v2.pdf`.
- Source HTML imprimable et modifiable du guide :
  `docs/manuel_operatoire_conceptuel_agv_bfm_v2.html`.
- Paramètres et dimensions provisoires : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/data/parametres_3d.json`.
- Génération des objets robot et des exports : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/generer_maquette.py`.
- Présentation et limites de la maquette : `Maquette_AGV_Bancaire_v0_2/Maquette_AGV_Bancaire_v0_2/LIRE_MOI.md`.
