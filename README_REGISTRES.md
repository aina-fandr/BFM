# Registres du projet — guide de remplissage

## Utilisation

Les fichiers `.csv` restent les sources simples à échanger et à importer. Leur
classeur `.xlsx` associé est une vue de travail mise en forme : filtres,
en-têtes contrastés, volets figés et repères de statut. Après modification du
CSV, régénérer les classeurs depuis le dossier projet :

```powershell
python -m pip install -r .\outils\requirements.txt
python .\outils\generer_registres.py
```

Les registres ont été préremplis à partir des sources du projet. Pour
reconstruire ces données après mise à jour des nomenclatures, lancer
explicitement :

```powershell
python .\outils\generer_registres.py --remplir-donnees
```

Cette option régénère les huit CSV à partir des sources connues et remplace
leurs contenus actuels. Sans cette option, le script conserve les CSV tels
qu'ils sont et ne fait que recréer les classeurs.

Le format couleur facilite la lecture, mais ne constitue ni une approbation,
ni une preuve de conformité. Les cellules vides ou marquées « à définir » ne
sont pas des valeurs zéro.

## Ouverture dans VS Code

L'espace de travail fixe l'éditeur XLSX `csv-excel-viewer-excel-editor` dans
`.vscode/settings.json`, pour éviter que plusieurs extensions concurrentes se
remplacent comme éditeur par défaut après une mise à jour. Fermer puis rouvrir
les anciens onglets XLSX après changement de l'association.

Les générateurs utilisent un filtre de feuille standard plutôt que des tableaux
structurés Excel et normalisent les liens OOXML internes en chemins relatifs.
Cette combinaison contourne les erreurs de lecture signalées par les éditeurs
XLSX de VS Code. Après avoir remplacé ou modifié un CSV source, régénérer ses
classeurs avec `python .\outils\generer_registres.py`.

## Registre par registre

| Domaine | Fichier de travail | Ce qui est déjà renseigné | À compléter par |
|---|---|---|---|
| Budget et stock | `APPROVISIONNEMENT/Budget Et Stock/MODELE_BUDGET_STOCK.xlsx` | Quantités CAO A13, quantité d'achat calculée sous hypothèse de stock nul, prix unitaires et totaux de planification | Inventaire physique et devis locaux |
| Commandes | `APPROVISIONNEMENT/Commandes et achats/MODELE_SUIVI_COMMANDES.xlsx` | Prévisions chiffrées par référence ; aucune commande, offre reçue ou réception n'est attestée | Achats / approvisionneur |
| Câblage | `ELECTRONIQUE/Cablage et Integration/REGISTRE_CABLAGE_A_COMPLETER.xlsx` | Huit liaisons fonctionnelles, limites et vérifications à définir | Responsable électrique, concepteur et sécurité |
| Interfaces | `INFORMATIQUE/Communication/INTERFACES_A_DEFINIR.xlsx` | Simulation locale et frontières backend, robot, ascenseur et caméras synthétiques | Intégrateur AGV, équipe informatique et responsable du site |
| Firmware | `INFORMATIQUE/Firmware et Microcontroleurs/INVENTAIRE_FIRMWARE_A_COMPLETER.xlsx` | Repères E01–E07 issus des volumes de la nomenclature | Équipe électronique, après sélection des matériels |
| ROS 2 | `ROBOTIQUE/Architecture ROS2/INVENTAIRE_ROS2_A_COMPLETER.xlsx` | Constat détaillé de l'absence de paquet et d'interface ROS 2 dans les sources examinées | Intégrateur de l'AGV, après confirmation de son API |
| Risques | `QUALITE ET SECURITE/Analyse des risques/REGISTRE_RISQUES_A_COMPLETER.xlsx` | Huit dangers, situations et mesures initiales ; aucune cotation inventée | Équipe compétente en sécurité et responsables concernés |
| Normes | `QUALITE ET SECURITE/Normes et Reglementations/REGISTRE_NORMES_A_DETERMINER.xlsx` | Références candidates et contexte Madagascar/Fianarantsoa, non déclarés applicables | Responsable HSE/juridique et organisme malgache compétent |

## Légende de décision

- **Existant / fourni** : constat limité aux fichiers ou données cités.
- **Conceptuel / candidat** : piste tirée de la CAO ou des documents, à vérifier.
- **À confirmer / à définir** : décision ou mesure qui manque ; ne pas la
  remplacer par une valeur inventée.
- **Validé** : à utiliser seulement lorsqu'une personne responsable a signé ou
  fourni une preuve datée.

Les 130 placements de composants dans l'assemblage CAO A13 ont été comptés par
référence. Ces quantités sont des repères de conception, pas des quantités
achetées. La colonne de stock reste « Non inventorié »; le calcul des quantités
d'achat utilise seulement une hypothèse de stock nul, qui doit être remplacée
après inventaire physique. Les références hors A13 sont à zéro dans le budget
du robot et ne sont pas déclarées inutiles pour d'autres sous-ensembles.

## Estimations de budget (23 novembre 2026)

Les montants des fichiers Budget et Commandes sont maintenant renseignés en
ariary. Ce sont des **estimations de planification**, pas des prix de marché
confirmés, offres, commandes ou engagements de dépense.

- Pour les deux motoréducteurs M01/M01_D, la page StepperOnline affichait
  **107,02 USD par unité** pour 1 à 4 unités. Le taux de référence publié par
  ExchangeRate-API le 23 novembre 2026 était **1 USD = 4 598,727 MGA**; le
  registre calcule donc 492 156 MGA par moteur. Le montant exclut transport,
  douane et taxes locales. Références :
  [prix du moteur](https://www.omc-stepperonline.com/24v-250w-60rpm-geared-bldc-motor-26-43nm-3742-10oz-in-50-1-right-angle-gearbox-f6b250-24gu-30s-6gu50rt)
  et [taux USD/MGA](https://open.er-api.com/v6/latest/USD).
- Les autres composants ont une provision de planification saisie manuellement
  par pièce, à partir de la famille et des dimensions conceptuelles. Ce n'est
  pas une grille de prix calculée ni un prix fournisseur : aucune grille locale
  n'a été fournie ou vérifiée. L'incertitude est importante (±50 % ou davantage);
  ces montants ne doivent pas servir à passer commande sans devis.
- La colonne **Nature du montant** distingue explicitement le prix public en
  ligne converti des provisions de planification. R05 est classé comme provision,
  car le roulement affiché en comparaison n'est pas compatible avec sa géométrie.
- La provision de R05 est provisoire : le SKF 6204-2RSH repéré en ligne coûte
  5,68 EUR, mais ses dimensions (20 × 47 × 14 mm) ne correspondent pas au volume
  CAO R05 (24 × 62 × 18 mm). Ce roulement n'est donc pas déclaré compatible.
  La pièce exacte doit être sélectionnée avant achat.
- Le registre Commandes utilise des références `PREVISION-2026-*` uniquement
  pour organiser le budget. Les champs devis, commande et réception indiquent
  explicitement qu'aucune opération réelle n'est enregistrée.
- Le total du classeur reprend la nomenclature A13 et l'hypothèse de stock nul.
  Il n'inclut ni les coûts d'importation, ni les taxes, ni les modifications
  de conception, ni les articles hors A13.

Les montants de câblage, les versions firmware, les interfaces matérielles,
les API réelles et les risques résiduels ne sont pas déductibles des maquettes.
Ils restent distincts des estimations budgétaires et ne sont pas inventés.

## Électronique industrielle — chiffrage préliminaire

Le classeur
`APPROVISIONNEMENT/Budget Et Stock/BOM_ELECTRONIQUE_INDUSTRIELLE_PRELIMINAIRE.xlsx`
présente une architecture candidate séparant calcul/navigation, commande moteur,
sécurité et alimentation. Il n'est pas fusionné au total de
16 269 312 MGA : la référence exacte du calculateur, le scanner et contrôleur de
sécurité, la batterie, les protections et le câblage exigent encore une
conception ou des devis. Le seul sous-total public indiqué concerne un
contrôleur BLDC candidat et un accessoire Hall, hors transport, taxes, douane
et intégration; il ne constitue pas un budget industriel complet.

Pour le régénérer après modification de ses hypothèses, exécuter :

```powershell
python .\outils\generer_bom_electronique_industrielle.py
```

Le document ne propose pas de microcontrôleur nu ni de PCB de puissance/sécurité
faite maison. Une éventuelle carte d'interface non liée à la sécurité devra
être conçue après définition des E/S. Les valeurs et quantités de résistances,
condensateurs, connecteurs et protections seront extraites du schéma validé,
pas déduites des volumes CAO.

## Contexte réglementaire et sécurité

Le lieu fourni pour le projet est **Fianarantsoa, Madagascar**. Les normes ISO
et IEC inscrites au registre sont des pistes à examiner, pas des obligations
légales présumées. Confirmer l'édition courante, l'adoption éventuelle comme
norme malgache, l'applicabilité à la classe réelle de l'AGV et les textes
nationaux en vigueur avec un responsable compétent avant tout essai réel.

La fiche officielle du [catalogue ISO pour ISO 12100:2010](https://www.iso.org/standard/51528.html)
indique une publication confirmée en 2022 et une révision en préparation au
moment de la consultation. Les autres éditions indiquées dans le registre
doivent être vérifiées directement auprès des éditeurs avant d'être figées.

Le prototype logiciel et les maquettes sont des démonstrateurs. Les risques
doivent être cotés par l'équipe compétente ; ce guide ne constitue pas une
analyse de risques approuvée ni une autorisation d'exploitation.
