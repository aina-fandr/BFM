# Glossaire — AGV bancaire

Les termes décrivent le prototype et le plan v0.1. Ils ne garantissent pas que l'AGV réel fournisse déjà ces données ou fonctions.

| Terme | Explication simple | Exemple dans le projet |
|---|---|---|
| AGV | Véhicule à guidage automatique qui transporte une charge dans un site. | Robot simulé entre la collecte et les dépôts. |
| Application de supervision | Interface qui présente les missions et l'état connu de l'AGV. | Le tableau de bord montre la batterie et la file de transferts simulées. |
| Mission de transfert | Demande de transporter une charge vers une destination définie. | Transfert de sacs C1 vers le dépôt 3. |
| File FIFO | File qui traite les demandes dans leur ordre de création (premier entré, premier sorti). | La plus ancienne mission en attente est lancée en premier. |
| C1, C2, C3 | Catégories de tri indiquées dans le plan fourni. | Les trois zones sont provisoirement implantées au dépôt 3. |
| Dépôt prioritaire | Local de destination choisi par défaut dans le scénario nominal. | Le dépôt 3 est prioritaire, avec dimensions 4 × 4 m marquées H. |
| Dépôt de repli | Destination alternative utilisée si elle est autorisée. | Le dépôt 1 est un repli à autoriser selon le descriptif. |
| Ascenseur A | Liaison verticale entre les deux niveaux du plan. | Même X/Y aux deux niveaux ; cabine supposée permettre un demi-tour. |
| D / H | « D » désigne une donnée du descriptif ; « H » une hypothèse de conception. | 8 × 6 m pour la collecte est D ; +3 m est H. |
| Enveloppe orientée | Rectangle de sécurité représentant l'espace occupé par le robot selon son orientation. | Enveloppe de contrôle 1,30 × 0,90 m. |
| Contrôle géométrique | Vérification numérique de collisions et d'inclusion dans les sols. | Le descriptif mentionne SAT, échantillonnage à 0,05 m et des pas définis. |
| Télémétrie | Informations transmises par un robot, par exemple son état ou sa batterie. | Le frontend actuel affiche seulement des valeurs de démonstration. |
| Alerte | Signalement qui requiert l'attention d'un opérateur. | Batterie simulée à 20 % ou moins. |
| Perte de connexion | Absence de données récentes du robot ou de son système de supervision. | Le prototype peut simuler la perte de liaison ; il n'est relié à aucun AGV. |
| ROS 2 | Middleware robotique qui transporte notamment des messages, services et actions. | Aucune interface ROS 2 n'est connectée à l'application bancaire. |
| Topic ROS 2 | Canal nommé sur lequel des nœuds ROS 2 publient ou reçoivent des messages. | `/scan` et `/imu` sont des références PARC antérieures, à confirmer pour l'AGV bancaire. |
| Vue POV | Image rendue depuis le point de vue d'une caméra. | Les deux vues du simulateur sont synthétiques, pas des flux caméra. |
| Simulation navigateur | Scène interactive calculée localement dans le navigateur, sans robot réel. | La scène 3D présente les deux niveaux, le trajet et l'AGV conceptuel. |
| Hypothèse de conception | Valeur choisie pour construire un premier modèle en attendant une mesure ou une validation. | L'altitude du niveau de départ est provisoirement fixée à +3 m. |
| Passerelle backend | Service intermédiaire sécurisé entre l'application web et les interfaces robotiques. | Une passerelle réelle devra être conçue après inspection des interfaces de l'AGV. |
