# Pistes d'achat et prix observes — roue motrice

Releve de prix en ligne du 23 novembre 2026. Les prix sont indicatifs, hors transport, taxes d'importation et disponibilite a Fianarantsoa. Une page fournisseur peut changer de prix ou de reference.

| Composant | Piste / caracteristiques annoncees | Prix observe | Quantite indicative | Statut pour le CAO |
|---|---|---:|---:|---|
| Roulement | [SKF 6204-2RSH, 20 x 47 x 14 mm — 123Roulement](https://www.123roulement.com/roulement-palier/roulement-bille/simple-rangee/6204-2rsh-skf) | 5,68 EUR TTC / unite | 4 en CAO | Prix comparatif seulement : le gabarit R05 est Ø24 / Ø62 / 18 mm, donc ce SKF n'est pas compatible sans reconception. |
| Roue industrielle alternative | [Blickle ALTH 200/20K — Heiz24](https://www.heiz24.de/fr/blickle-roue-pour-charges-lourdes-polyurethane-aluminium-alth-200-20k-capacite-de-charge-800kg-la-200mm-du-trou-essieu-20mm) | 91,99 EUR / unite affiche dans le resultat indexe | 2 | Alternative a etudier, pas compatible sans adaptation : roue polyurethanne/aluminium Ø200, alesage 20 mm et capacite annoncee 800 kg, mais le modele CAO emploie une bande de 55 mm et une jante boulonnee. La page vendeur a renvoye un blocage Cloudflare lors de la verification directe du prix. |
| Motoréducteur M01 / M01_D | [StepperOnline F6B250-24GU-30S/6GU50RT, BLDC 24 V, 250 W, 60 tr/min, réducteur 50:1, 26,43 Nm](https://www.omc-stepperonline.com/24v-250w-60rpm-geared-bldc-motor-26-43nm-3742-10oz-in-50-1-right-angle-gearbox-f6b250-24gu-30s-6gu50rt) | 107,02 USD / unite pour 1-4 pieces; 103,98 USD a partir de 5 | 2 dans A13 | La même référence figure dans la nomenclature CAO. Prix public indicatif, pas un devis ni un achat; frein, interfaces, dimensionnement au cycle et compatibilité mécanique restent à valider. |
| Accouplement flexible | Lovejoy L090, alesages a confirmer (20 et 16 mm) | Devis requis | 2 | Le couple nominal et les diametres doivent etre confirmes avant selection. Le modele CAO reste un gabarit. |
| Visserie, pneu 200 x 55, jante/moyeu et pieces fabriquees | References et vendeurs a choisir | Devis requis / cout de fabrication local a chiffrer | Selon nomenclature | Aucune reference exacte ni prix fiable n'a ete confirme pour cette geometrie et cette application. |

## Decision de conception

Aucune ligne de ce tableau ne constitue un achat. Le motoréducteur est référencé dans la CAO, mais son dimensionnement d'application reste à valider. Le roulement SKF affiché est un repère de prix uniquement : ses dimensions ne correspondent pas au volume R05.

Pour le budget de planification, le taux de conversion consulté le 23 novembre 2026 était de 1 USD = 4 598,727 MGA ([ExchangeRate-API](https://open.er-api.com/v6/latest/USD)). Le montant converti exclut transport, douane et taxes locales. Il faut relever un devis livré à Fianarantsoa avant tout achat.

Avant validation du module, il faut obtenir les fiches STEP des references retenues et les donnees de charge, vitesse, pente, acceleration, freinage et regime de service. Les couples d'assemblage, ajustements, interfaces et charges des roues doivent ensuite etre verifies. Le budget final doit ajouter transport, douane, taxes, fixations, fabrication locale et composants non listes.
