# Exigences initiales — AGV bancaire

Cette première liste traduit le descriptif « AGV BANCAIRE - AVANT-PROJET 2D V0.1 » en exigences vérifiables. Elle décrit un prototype de démonstration, pas un système de convoyage bancaire prêt à exploiter.

## Statuts

- **Fourni** : information explicitement présente dans le descriptif.
- **Hypothèse** : choix géométrique ou comportement provisoire, à confirmer.
- **À valider** : vérification dépendant du site, du robot, de son intégrateur ou des règles de l'agence.
- **Prototype** : comportement simulé dans le frontend ; aucune commande réelle n'est envoyée.

## Exigences fonctionnelles

| ID | Exigence | Vérification | Statut |
|---|---|---|---|
| EF-01 | L'application présente le niveau de départ, le rez-de-chaussée, la salle de collecte, les couloirs, l'ascenseur A et les dépôts 1, 2 et 3. | Comparer les noms, les dimensions affichées et les liaisons au plan v0.1. | Prototype ; cotes D et H signalées |
| EF-02 | Une mission de transfert associe une catégorie de sacs C1, C2 ou C3 à une destination. Le dépôt 3 est le dépôt prioritaire et le dépôt 1 est le repli autorisé provisoire. | Créer une mission pour chaque catégorie ; vérifier la destination et le statut de priorité/repli. | Dépôt 3 fourni ; dépôt 1 à autoriser |
| EF-03 | Les missions en attente sont conservées dans une file et lancées dans leur ordre d'arrivée. | Créer plusieurs missions puis vérifier que la plus ancienne démarre en premier. | Prototype |
| EF-04 | Le trajet nominal suit collecte, passage ouest, sortie P1, ascenseur A, rez-de-chaussée, segments de 2 m, 6 m et 10 m, puis dépôt 3 et attente. | Comparer les étapes et les repères du trajet affichés au descriptif. | Séquence fournie ; coordonnées de détail à confirmer |
| EF-05 | L'ascenseur A conserve les mêmes coordonnées X/Y entre les niveaux ; l'altitude du niveau de départ est représentée comme une hypothèse de +3 m. | Comparer sa position sur les deux niveaux ; vérifier que +3 m est marqué comme hypothèse. | Position commune fournie ; altitude H |
| EF-06 | L'application affiche l'état de connexion, la mission, la destination, la progression et la batterie lorsqu'ils sont disponibles. | Vérifier les valeurs simulées et distinguer visuellement les données absentes des données reçues. | Prototype local ; télémétrie réelle à définir |
| EF-07 | Une batterie à 20 % ou moins déclenche une alerte et empêche de démarrer une nouvelle mission dans la démonstration. | Tester 21 %, 20 % et une valeur basse ; contrôler l'alerte et le blocage. | Seuil fourni ; comportement d'exploitation à valider |
| EF-08 | L'opérateur peut créer une mission, démarrer la prochaine mission, suspendre et reprendre une mission simulée, puis réinitialiser le scénario. | Exécuter chaque action et vérifier l'état affiché dans la file. | Prototype local |
| EF-09 | La simulation 3D représente les deux niveaux, le robot, la salle de collecte, les locaux, l'ascenseur et les dépôts ; la destination peut être le dépôt 3 ou le dépôt 1. | Changer de destination et observer le trajet et l'arrivée du robot dans la scène. | Prototype géométrique ; certaines dimensions H |
| EF-10 | La scène fournit deux vues de caméra synthétiques depuis des poses conceptuelles et permet d'afficher les faisceaux de capteurs simulés. | Démarrer le trajet et vérifier que les vues POV suivent le robot. | Prototype ; pas de vidéo réelle |
| EF-11 | Les contrôles géométriques sont présentés avec une enveloppe orientée de 1,30 × 0,90 m, issue d'un châssis d'essai de 1,10 × 0,70 m et d'une marge de 0,10 m par face ; pas de translation ≤ 0,025 m et pas angulaire ≤ 2°. | Comparer les paramètres affichés au descriptif et au JSON de validation lorsqu'il sera disponible. | Paramètres fournis ; résultats non importés |
| EF-12 | Les portes sont supposées ouvertes ; les virages RDC 5 et 6 sont prévus avec une zone de 1,80 × 1,80 m. | Vérifier les hypothèses affichées et les cotes dans la géométrie finale. | Portes fournies ; virages H |
| EF-13 | L'application ne présente pas une simulation locale comme une liaison réelle, une validation de sécurité ou un flux capteur en direct. | Vérifier les avertissements, les badges de connexion et les libellés de caméras/capteurs. | Prototype local |
| EF-14 | Le concept 3D représente quatre compartiments indépendants, chacun prévu pour un sac de 40 kg, dans un coffre de 1,00 × 0,50 × 0,75 m et un châssis de 1,10 × 0,70 m. | Compter les tiroirs dans les exports GLB/SDF et confronter les dimensions aux paramètres mécaniques. | Avant-projet ; charge et cotes à valider |
| EF-15 | À la station, le cycle simulé immobilise l'AGV, aligne le plateau, extrait un seul tiroir, transfère le sac vers C1/C2/C3, puis referme et reverrouille avant de réautoriser la traction. | Exécuter les cinq étapes pour S1 à S4, contrôler les hauteurs/courses animées et l'état de chaque interverrouillage. | Animation du concept ; matériel non implémenté |

## Limites et décisions à confirmer

- Les coordonnées proviennent du descriptif et d'une interprétation de l'aperçu ; le fichier `geometrie_AGV_v0_1.json` n'est pas présent dans le dépôt. Les résultats SAT et d'inclusion de sol ne sont donc pas reproduits par le frontend.
- Les dépôts C1/C2/C3 dans le dépôt 3, l'autorisation de repli vers le dépôt 1, l'altitude +3 m, les pièces et les dégagements marqués H sont des hypothèses à valider avec le responsable du site.
- La simulation n'évalue pas les masses, la stabilité, le freinage, les personnes, les tolérances de construction, les portes ni le mécanisme de prise/dépose des sacs.
- L'architecture mécanique proposée, les dimensions intérieures des tiroirs, leur charge de 40 kg, l'extension et les verrous doivent être vérifiés par mesure, calcul et essais avant fabrication.
- L'animation du cycle de cinq étapes est illustrative. Elle ne modélise pas les efforts, la déformation du sac, les tolérances, les défauts de capteurs, le temps réel ni une validation de sécurité.
- L'identité de l'AGV bancaire, sa charge utile, son système de navigation, ses capteurs, ses interfaces logicielles et son comportement en perte de connexion restent à confirmer.
- Une mise en production nécessitera une authentification des opérateurs, des droits d'accès, une journalisation durable, une passerelle sécurisée et des procédures de sécurité validées avec l'intégrateur. Le frontend actuel ne fournit pas ces garanties.
- Les topics ROS 2 documentés dans les travaux PARC antérieurs ne sont pas présumés disponibles sur l'AGV bancaire ; ils doivent être vérifiés avant toute intégration.
