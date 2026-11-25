# BFM AGV — lot CAO 01, module de roue motrice

**Version conceptuelle de travail. Aucune piece ne doit etre fabriquee pour porter la charge avant choix des composants, calculs et validation.**

## Contenu genere

- `01_pieces_step/` et `02_pieces_stl/` : 26 fichiers individuels, dont profils creux, roue, moyeu, arbre rainure, clavette, deux paliers 6204, motorisation-gabarit, accouplement et visserie.
- `03_assemblages_step/` et `04_visualisation_glb/` :
  - `A01_roue_assemblee` : module motopropulseur, avec paliers, moteur et fixations visibles ;
  - `A02_roue_eclatee` : les memes pieces separees pour lecture des interfaces ;
  - `A03_roues_sur_chassis` : deux modules integres a un chassis soude, avec plancher boulonne.
- `nomenclature.json` : role, materiau envisage et fabrication locale / achat recommande pour chaque type de piece.
- `interfaces_assemblage.json` : positions et methodes de fixation provisoires, cotes en mm.
- `generer_cao.py` : source parametrique CadQuery.

## Logique mecanique representee

1. Le pneu de 200 x 55 mm est monte sur une jante.
2. La jante et la bride du moyeu sont alignees sur un cercle de percage de 80 mm et reunies par six vis M8, rondelles et ecrous.
3. Le moyeu est solidarise a l'arbre de 20 mm par une clavette 6 x 6 x 30 mm.
4. L'arbre tourne dans deux roulements de geometrie nominale 6204 (20 x 47 x 14 mm). Leurs bagues exterieures prennent place dans les deux sieges du support double ; deux colliers limitent le deplacement axial.
5. Le support de paliers est positionne contre le longeron. Sa liaison au chassis est indiquee comme soudee ; les cordons et renforts sont a calculer.
6. Le motor reducteur est un gabarit dont l'arbre de sortie de 16 mm et l'arbre de roue de 20 mm entrent chacun dans une moitie de l'accouplement indicatif 20 x 16 mm. Quatre vis M8 traversent la platine et les pattes de montage du gabarit.
7. Le chassis est constitue de profils creux 40 x 40 x 3 mm soudes. Le plancher de 3 mm est aligne sur les longerons et la traverse centrale puis boulonne en six points M6.

Les perçages representes correspondent aux vis et aux interfaces listees. Les assemblages restent des solides positionnes, sans contraintes cinematiques CAO. Les soudures sont une methode d'assemblage indiquee, pas des cordons calcules.

## Dimensions et masse cible

- Charge utile nominale annoncee : **160 kg**.
- Masse cible du robot a vide : **70 kg maximum**.
- Masse brute cible minimale correspondante : **230 kg** ; la masse reelle sera superieure si des equipements ou marges s'ajoutent.
- Entraxe des centres des roues motrices : **515 mm** ; largeur exterieure indicative : **570 mm**.

Le modele ne valide pas le plafond de 70 kg. Le JSON fournit une estimation de masse issue du volume CAO du chassis et du plancher en acier S235 (densite 7 850 kg/m3), mais elle exclut les autres sous-ensembles. Le budget des familles est une allocation provisoire a verifier par pesage. Une nomenclature complete pesee est requise. A 230 kg brut, la repartition par roue n'est pas necessairement egale : roues porteuses, position du centre de gravite, acceleration, freinage et seuils doivent etre pris en compte.

## Fabrication locale et achats

**A fabriquer localement (hypotheses)** : longerons et traverses en acier S235, plancher, platine moteur, support double de paliers, jante, moyeu, arbre et entretoises. L'epaisseur, les ajustements, la soudure et la protection anticorrosion restent a confirmer.

**A acheter, sans reference fournisseur choisie** : pneus/roues, roulements, motor reducteur, accouplement et visserie. Le 6204 du modele est un gabarit aux dimensions nominales, pas un STEP d'un fabricant particulier. Le motor reducteur et l'accouplement sont uniquement des volumes de reference. Le choix du moteur depend encore de la vitesse, de la pente, de l'acceleration, du cycle de service et du freinage.

Les pistes de composants et les prix observes en ligne sont documentes dans `BUDGET_ROUE.md`. Aucune reference d'achat n'est encore validee; les tarifs ne comprennent pas necessairement transport, douane ni disponibilite a Fianarantsoa.

## Regenerer

Avec Python 3.10+ :

```powershell
python -m pip install -r requirements.txt
python generer_cao.py
```

Le script regenere les pieces STEP/STL, les trois assemblages STEP/GLB et les deux catalogues JSON. Il ne fait ni calcul de resistance, ni calcul moteur, ni simulation de mouvement.
