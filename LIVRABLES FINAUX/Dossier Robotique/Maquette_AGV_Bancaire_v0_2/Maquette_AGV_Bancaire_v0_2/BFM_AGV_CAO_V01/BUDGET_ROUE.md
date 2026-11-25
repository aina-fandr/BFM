# Pistes d'achat et prix observes — roue motrice

Releve de prix en ligne du 15 novembre 2026. Les prix sont indicatifs, en devises d'origine, hors transport, taxes d'importation et disponibilite a Fianarantsoa. Une page fournisseur peut changer de prix ou de reference.

| Composant | Piste / caracteristiques annoncees | Prix observe | Quantite indicative | Statut pour le CAO |
|---|---|---:|---:|---|
| Roulement | [SKF 6204-2RSH, 20 x 47 x 14 mm — 123Roulement](https://www.123roulement.com/roulement-palier/roulement-bille/simple-rangee/6204-2rsh-skf) | 5,68 EUR TTC / unite | 4 | Correspond aux dimensions nominales du gabarit. Charge, ajustement et duree de vie a verifier. |
| Roue industrielle alternative | [Blickle ALTH 200/20K — Heiz24](https://www.heiz24.de/fr/blickle-roue-pour-charges-lourdes-polyurethane-aluminium-alth-200-20k-capacite-de-charge-800kg-la-200mm-du-trou-essieu-20mm) | 91,99 EUR / unite affiche dans le resultat indexe | 2 | Alternative a etudier, pas compatible sans adaptation : roue polyurethanne/aluminium Ø200, alesage 20 mm et capacite annoncee 800 kg, mais le modele CAO emploie une bande de 55 mm et une jante boulonnee. La page vendeur a renvoye un blocage Cloudflare lors de la verification directe du prix. |
| Motorisation de comparaison | [StepperOnline F6B250-24GU-30S/6GU50RT, BLDC 24 V, 250 W, 60 tr/min, reducteur 50:1, 26,43 Nm, arbre claveté, carcasse 104 x 104 mm](https://www.omc-stepperonline.com/24v-250w-60rpm-geared-bldc-motor-26-43nm-3742-10oz-in-50-1-right-angle-gearbox-f6b250-24gu-30s-6gu50rt) | 103,98 USD / unite dans un palier annonce a partir de 5 pieces | 2 a verifier | Piste de comparaison uniquement : pas selectionnee, prix de gros non confirme pour 2 pieces, frein et diametre d'arbre a confirmer. La page indique un STEP accessible apres connexion. Le couple requis depend de la vitesse, pente, acceleration, cycle et masse totale. |
| Accouplement flexible | Lovejoy L090, alesages a confirmer (20 et 16 mm) | Devis requis | 2 | Le couple nominal et les diametres doivent etre confirmes avant selection. Le modele CAO reste un gabarit. |
| Visserie, pneu 200 x 55, jante/moyeu et pieces fabriquees | References et vendeurs a choisir | Devis requis / cout de fabrication local a chiffrer | Selon nomenclature | Aucune reference exacte ni prix fiable n'a ete confirme pour cette geometrie et cette application. |

## Decision de conception

Aucune ligne de ce tableau n'est encore un choix d'achat definitif. Le roulement SKF est une piste dimensionnelle raisonnable pour remplacer le gabarit; la roue et le moteur ne sont pas declares compatibles ni dimensionnes pour le robot. Le prix tres bas d'une annonce generique de moteur 24 V/250 W n'est pas retenu comme reference industrielle.

Avant validation du module, il faut obtenir les fiches STEP des references retenues et les donnees de charge, vitesse, pente, acceleration, freinage et regime de service. Les couples d'assemblage, ajustements, interfaces et charges des roues doivent ensuite etre verifies. Le budget final doit ajouter transport, douane, taxes, fixations, fabrication locale et composants non listes.
