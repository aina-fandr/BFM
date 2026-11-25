# Structure complete - ROBOTIQUE

**Dossier :** `ROBOTIQUE/`

Arborescence des dossiers et fichiers du perimetre ci-dessous. Les dependances generees (`node_modules`, `dist`, `.vite`, `__pycache__` et `.git`) sont exclues.

```text
ROBOTIQUE/
├── Architecture ROS2/
│   ├── ETAT_ROS2.md
│   ├── INVENTAIRE_ROS2_A_COMPLETER.csv
│   └── INVENTAIRE_ROS2_A_COMPLETER.xlsx
├── Cartographie et Localisation/
│   ├── Sources_maquette_v0_2/
│   │   ├── geometrie_plan_retenu.json
│   │   ├── parametres_3d.json
│   │   ├── plan_01.svg
│   │   └── scene_3d.json
│   └── ETAT_CARTOGRAPHIE.md
├── Modelisation du Robot/
│   └── Maquette_AGV_Bancaire_v0_2/
│       └── Maquette_AGV_Bancaire_v0_2/
│           ├── BFM_AGV_CAO_V01/
│           │   ├── 01_pieces_step/
│           │   │   ├── C01_longeron_gauche_40x40x3.step
│           │   │   ├── C02_longeron_droit_40x40x3.step
│           │   │   ├── C03_traverse_avant_40x40x3.step
│           │   │   ├── C04_traverse_central_40x40x3.step
│           │   │   ├── C05_traverse_arriere_40x40x3.step
│           │   │   ├── C06_plancher_3mm_perce_6xM6.step
│           │   │   ├── F01_vis_M8x30_hexagonale.step
│           │   │   ├── F02_ecrou_M8.step
│           │   │   ├── F04_vis_M6x50_hexagonale.step
│           │   │   ├── F05_ecrou_M6.step
│           │   │   ├── F06_rondelle_plate_M6.step
│           │   │   ├── M01_motor_reducteur_gabarit_128x94x70.step
│           │   │   ├── M02_platine_moteur_percee_et_soudable.step
│           │   │   ├── M03_accouplement_flexible_20x16_gabarit.step
│           │   │   ├── M04_vis_M5_accouplement.step
│           │   │   ├── R01_pneu_bande_roulement.step
│           │   │   ├── R02_jante_avec_trous_M8_PCD80.step
│           │   │   ├── R03_moyeu_a_bride_et_rainure_clavette.step
│           │   │   ├── R04_roulement_6204_gabarit_20x47x14.step
│           │   │   ├── R05_entretoise_axiale.step
│           │   │   ├── R06_arbre_D20_avec_rainure_clavette.step
│           │   │   ├── R07_rondelle_M8.step
│           │   │   ├── R08_clavette_6x6x30.step
│           │   │   ├── R09_support_double_paliers_siege_6204.step
│           │   │   ├── R10_collier_arret_arbre_D20.step
│           │   │   └── R11_vis_M6_collier_arret.step
│           │   ├── 02_pieces_stl/
│           │   │   ├── C01_longeron_gauche_40x40x3.stl
│           │   │   ├── C02_longeron_droit_40x40x3.stl
│           │   │   ├── C03_traverse_avant_40x40x3.stl
│           │   │   ├── C04_traverse_central_40x40x3.stl
│           │   │   ├── C05_traverse_arriere_40x40x3.stl
│           │   │   ├── C06_plancher_3mm_perce_6xM6.stl
│           │   │   ├── F01_vis_M8x30_hexagonale.stl
│           │   │   ├── F02_ecrou_M8.stl
│           │   │   ├── F04_vis_M6x50_hexagonale.stl
│           │   │   ├── F05_ecrou_M6.stl
│           │   │   ├── F06_rondelle_plate_M6.stl
│           │   │   ├── M01_motor_reducteur_gabarit_128x94x70.stl
│           │   │   ├── M02_platine_moteur_percee_et_soudable.stl
│           │   │   ├── M03_accouplement_flexible_20x16_gabarit.stl
│           │   │   ├── M04_vis_M5_accouplement.stl
│           │   │   ├── R01_pneu_bande_roulement.stl
│           │   │   ├── R02_jante_avec_trous_M8_PCD80.stl
│           │   │   ├── R03_moyeu_a_bride_et_rainure_clavette.stl
│           │   │   ├── R04_roulement_6204_gabarit_20x47x14.stl
│           │   │   ├── R05_entretoise_axiale.stl
│           │   │   ├── R06_arbre_D20_avec_rainure_clavette.stl
│           │   │   ├── R07_rondelle_M8.stl
│           │   │   ├── R08_clavette_6x6x30.stl
│           │   │   ├── R09_support_double_paliers_siege_6204.stl
│           │   │   ├── R10_collier_arret_arbre_D20.stl
│           │   │   └── R11_vis_M6_collier_arret.stl
│           │   ├── 03_assemblages_step/
│           │   │   ├── A01_roue_assemblee.step
│           │   │   ├── A02_roue_eclatee.step
│           │   │   └── A03_roues_sur_chassis.step
│           │   ├── 04_visualisation_glb/
│           │   │   ├── A01_roue_assemblee.glb
│           │   │   ├── A02_roue_eclatee.glb
│           │   │   └── A03_roues_sur_chassis.glb
│           │   ├── BUDGET_ROUE.md
│           │   ├── generer_cao.py
│           │   ├── interfaces_assemblage.json
│           │   ├── LISEZ_MOI.md
│           │   ├── nomenclature.json
│           │   ├── requirements.txt
│           │   └── validation_cao.json
│           ├── data/
│           │   ├── geometrie_plan_retenu.json
│           │   ├── parametres_3d.json
│           │   └── scene_3d.json
│           ├── modeles/
│           │   ├── assemblage/
│           │   │   ├── etape_01_chassis.glb
│           │   │   ├── etape_02_roues.glb
│           │   │   ├── etape_03_batterie.glb
│           │   │   ├── etape_04_coffre.glb
│           │   │   ├── etape_05_separateurs.glb
│           │   │   ├── etape_06_glissieres.glb
│           │   │   ├── etape_07_tiroir_S1.glb
│           │   │   ├── etape_08_tiroir_S2.glb
│           │   │   ├── etape_09_tiroir_S3.glb
│           │   │   ├── etape_10_tiroir_S4.glb
│           │   │   ├── etape_11_commandes.glb
│           │   │   └── etape_12_toit.glb
│           │   ├── pieces/
│           │   │   ├── 001_plaque_superieure_chassis.glb
│           │   │   ├── 002_longeron_gauche.glb
│           │   │   ├── 003_longeron_droite.glb
│           │   │   ├── 004_traverse_chassis_1.glb
│           │   │   ├── 005_traverse_chassis_2.glb
│           │   │   ├── 006_traverse_chassis_3.glb
│           │   │   ├── 007_traverse_chassis_4.glb
│           │   │   ├── 008_moteur_reducteur_gauche.glb
│           │   │   ├── 009_roue_motrice_gauche.glb
│           │   │   ├── 010_moyeu_moteur_gauche.glb
│           │   │   ├── 011_ecrou_roue_gauche_1.glb
│           │   │   ├── 012_ecrou_roue_gauche_2.glb
│           │   │   ├── 013_ecrou_roue_gauche_3.glb
│           │   │   ├── 014_ecrou_roue_gauche_4.glb
│           │   │   ├── 015_ecrou_roue_gauche_5.glb
│           │   │   ├── 016_ecrou_roue_gauche_6.glb
│           │   │   ├── 017_moteur_reducteur_droite.glb
│           │   │   ├── 018_roue_motrice_droite.glb
│           │   │   ├── 019_moyeu_moteur_droite.glb
│           │   │   ├── 020_ecrou_roue_droite_1.glb
│           │   │   ├── 021_ecrou_roue_droite_2.glb
│           │   │   ├── 022_ecrou_roue_droite_3.glb
│           │   │   ├── 023_ecrou_roue_droite_4.glb
│           │   │   ├── 024_ecrou_roue_droite_5.glb
│           │   │   ├── 025_ecrou_roue_droite_6.glb
│           │   │   ├── 026_support_roulette_avant.glb
│           │   │   ├── 027_roulette_pivotante_avant.glb
│           │   │   ├── 028_axe_roulette_avant.glb
│           │   │   ├── 029_fourche_roulette_avant_gauche.glb
│           │   │   ├── 030_vis_axe_roulette_avant_gauche.glb
│           │   │   ├── 031_fourche_roulette_avant_droite.glb
│           │   │   ├── 032_vis_axe_roulette_avant_droite.glb
│           │   │   ├── 033_support_roulette_arriere.glb
│           │   │   ├── 034_roulette_pivotante_arriere.glb
│           │   │   ├── 035_axe_roulette_arriere.glb
│           │   │   ├── 036_fourche_roulette_arriere_gauche.glb
│           │   │   ├── 037_vis_axe_roulette_arriere_gauche.glb
│           │   │   ├── 038_fourche_roulette_arriere_droite.glb
│           │   │   ├── 039_vis_axe_roulette_arriere_droite.glb
│           │   │   ├── 040_pare_chocs_avant.glb
│           │   │   ├── 041_pare_chocs_arriere.glb
│           │   │   ├── 042_support_batterie.glb
│           │   │   ├── 043_batterie_format_a_definir.glb
│           │   │   ├── 044_coffret_controleur_hypothese.glb
│           │   │   ├── 045_support_coffret_controleur.glb
│           │   │   ├── 046_fond_coffre.glb
│           │   │   ├── 047_paroi_arriere.glb
│           │   │   ├── 048_paroi_laterale_-0_49.glb
│           │   │   ├── 049_paroi_laterale_0_49.glb
│           │   │   ├── 050_toit_coffre.glb
│           │   │   ├── 051_separateur_horizontal.glb
│           │   │   ├── 052_separateur_vertical.glb
│           │   │   ├── 053_montant_face_-0_49.glb
│           │   │   ├── 054_montant_face_0_00.glb
│           │   │   ├── 055_montant_face_0_49.glb
│           │   │   ├── 056_traverse_face_0_33.glb
│           │   │   ├── 057_traverse_face_0_70.glb
│           │   │   ├── 058_traverse_face_1_06.glb
│           │   │   ├── 059_s1_fond_tiroir.glb
│           │   │   ├── 060_s1_flanc_gauche.glb
│           │   │   ├── 061_s1_glissiere_fixe_gauche.glb
│           │   │   ├── 062_s1_glissiere_mobile_gauche.glb
│           │   │   ├── 063_s1_flanc_droite.glb
│           │   │   ├── 064_s1_glissiere_fixe_droite.glb
│           │   │   ├── 065_s1_glissiere_mobile_droite.glb
│           │   │   ├── 066_s1_fond_arriere.glb
│           │   │   ├── 067_s1_joint_peripherique.glb
│           │   │   ├── 068_s1_facade.glb
│           │   │   ├── 069_s1_poignee.glb
│           │   │   ├── 070_s1_support_poignee_-1.glb
│           │   │   ├── 071_s1_support_poignee_1.glb
│           │   │   ├── 072_s1_plaque_identification.glb
│           │   │   ├── 073_s1_marquage_0_a.glb
│           │   │   ├── 074_s1_marquage_0_f.glb
│           │   │   ├── 075_s1_marquage_0_g.glb
│           │   │   ├── 076_s1_marquage_0_c.glb
│           │   │   ├── 077_s1_marquage_0_d.glb
│           │   │   ├── 078_s1_marquage_1_b.glb
│           │   │   ├── 079_s1_marquage_1_c.glb
│           │   │   ├── 080_s1_loquet.glb
│           │   │   ├── 081_s1_actionneur_corps.glb
│           │   │   ├── 082_s1_actionneur_tige.glb
│           │   │   ├── 083_s1_butee_-0_429.glb
│           │   │   ├── 084_s1_butee_-0_071.glb
│           │   │   ├── 085_s1_vis_face_-1_-1.glb
│           │   │   ├── 086_s1_vis_face_-1_1.glb
│           │   │   ├── 087_s1_vis_face_1_-1.glb
│           │   │   ├── 088_s1_vis_face_1_1.glb
│           │   │   ├── 089_s2_fond_tiroir.glb
│           │   │   ├── 090_s2_flanc_gauche.glb
│           │   │   ├── 091_s2_glissiere_fixe_gauche.glb
│           │   │   ├── 092_s2_glissiere_mobile_gauche.glb
│           │   │   ├── 093_s2_flanc_droite.glb
│           │   │   ├── 094_s2_glissiere_fixe_droite.glb
│           │   │   ├── 095_s2_glissiere_mobile_droite.glb
│           │   │   ├── 096_s2_fond_arriere.glb
│           │   │   ├── 097_s2_joint_peripherique.glb
│           │   │   ├── 098_s2_facade.glb
│           │   │   ├── 099_s2_poignee.glb
│           │   │   ├── 100_s2_support_poignee_-1.glb
│           │   │   ├── 101_s2_support_poignee_1.glb
│           │   │   ├── 102_s2_plaque_identification.glb
│           │   │   ├── 103_s2_marquage_0_a.glb
│           │   │   ├── 104_s2_marquage_0_f.glb
│           │   │   ├── 105_s2_marquage_0_g.glb
│           │   │   ├── 106_s2_marquage_0_c.glb
│           │   │   ├── 107_s2_marquage_0_d.glb
│           │   │   ├── 108_s2_marquage_1_a.glb
│           │   │   ├── 109_s2_marquage_1_b.glb
│           │   │   ├── 110_s2_marquage_1_g.glb
│           │   │   ├── 111_s2_marquage_1_e.glb
│           │   │   ├── 112_s2_marquage_1_d.glb
│           │   │   ├── 113_s2_loquet.glb
│           │   │   ├── 114_s2_actionneur_corps.glb
│           │   │   ├── 115_s2_actionneur_tige.glb
│           │   │   ├── 116_s2_butee_0_071.glb
│           │   │   ├── 117_s2_butee_0_429.glb
│           │   │   ├── 118_s2_vis_face_-1_-1.glb
│           │   │   ├── 119_s2_vis_face_-1_1.glb
│           │   │   ├── 120_s2_vis_face_1_-1.glb
│           │   │   ├── 121_s2_vis_face_1_1.glb
│           │   │   ├── 122_s3_fond_tiroir.glb
│           │   │   ├── 123_s3_flanc_gauche.glb
│           │   │   ├── 124_s3_glissiere_fixe_gauche.glb
│           │   │   ├── 125_s3_glissiere_mobile_gauche.glb
│           │   │   ├── 126_s3_flanc_droite.glb
│           │   │   ├── 127_s3_glissiere_fixe_droite.glb
│           │   │   ├── 128_s3_glissiere_mobile_droite.glb
│           │   │   ├── 129_s3_fond_arriere.glb
│           │   │   ├── 130_s3_joint_peripherique.glb
│           │   │   ├── 131_s3_facade.glb
│           │   │   ├── 132_s3_poignee.glb
│           │   │   ├── 133_s3_support_poignee_-1.glb
│           │   │   ├── 134_s3_support_poignee_1.glb
│           │   │   ├── 135_s3_plaque_identification.glb
│           │   │   ├── 136_s3_marquage_0_a.glb
│           │   │   ├── 137_s3_marquage_0_f.glb
│           │   │   ├── 138_s3_marquage_0_g.glb
│           │   │   ├── 139_s3_marquage_0_c.glb
│           │   │   ├── 140_s3_marquage_0_d.glb
│           │   │   ├── 141_s3_marquage_1_a.glb
│           │   │   ├── 142_s3_marquage_1_b.glb
│           │   │   ├── 143_s3_marquage_1_g.glb
│           │   │   ├── 144_s3_marquage_1_c.glb
│           │   │   ├── 145_s3_marquage_1_d.glb
│           │   │   ├── 146_s3_loquet.glb
│           │   │   ├── 147_s3_actionneur_corps.glb
│           │   │   ├── 148_s3_actionneur_tige.glb
│           │   │   ├── 149_s3_butee_-0_429.glb
│           │   │   ├── 150_s3_butee_-0_071.glb
│           │   │   ├── 151_s3_vis_face_-1_-1.glb
│           │   │   ├── 152_s3_vis_face_-1_1.glb
│           │   │   ├── 153_s3_vis_face_1_-1.glb
│           │   │   ├── 154_s3_vis_face_1_1.glb
│           │   │   ├── 155_s4_fond_tiroir.glb
│           │   │   ├── 156_s4_flanc_gauche.glb
│           │   │   ├── 157_s4_glissiere_fixe_gauche.glb
│           │   │   ├── 158_s4_glissiere_mobile_gauche.glb
│           │   │   ├── 159_s4_flanc_droite.glb
│           │   │   ├── 160_s4_glissiere_fixe_droite.glb
│           │   │   ├── 161_s4_glissiere_mobile_droite.glb
│           │   │   ├── 162_s4_fond_arriere.glb
│           │   │   ├── 163_s4_joint_peripherique.glb
│           │   │   ├── 164_s4_facade.glb
│           │   │   ├── 165_s4_poignee.glb
│           │   │   ├── 166_s4_support_poignee_-1.glb
│           │   │   ├── 167_s4_support_poignee_1.glb
│           │   │   ├── 168_s4_plaque_identification.glb
│           │   │   ├── 169_s4_marquage_0_a.glb
│           │   │   ├── 170_s4_marquage_0_f.glb
│           │   │   ├── 171_s4_marquage_0_g.glb
│           │   │   ├── 172_s4_marquage_0_c.glb
│           │   │   ├── 173_s4_marquage_0_d.glb
│           │   │   ├── 174_s4_marquage_1_f.glb
│           │   │   ├── 175_s4_marquage_1_g.glb
│           │   │   ├── 176_s4_marquage_1_b.glb
│           │   │   ├── 177_s4_marquage_1_c.glb
│           │   │   ├── 178_s4_loquet.glb
│           │   │   ├── 179_s4_actionneur_corps.glb
│           │   │   ├── 180_s4_actionneur_tige.glb
│           │   │   ├── 181_s4_butee_0_071.glb
│           │   │   ├── 182_s4_butee_0_429.glb
│           │   │   ├── 183_s4_vis_face_-1_-1.glb
│           │   │   ├── 184_s4_vis_face_-1_1.glb
│           │   │   ├── 185_s4_vis_face_1_-1.glb
│           │   │   ├── 186_s4_vis_face_1_1.glb
│           │   │   ├── 187_grille_ventilation_fond.glb
│           │   │   ├── 188_ailette_grille_ventilation_1.glb
│           │   │   ├── 189_ailette_grille_ventilation_2.glb
│           │   │   ├── 190_ailette_grille_ventilation_3.glb
│           │   │   ├── 191_ailette_grille_ventilation_4.glb
│           │   │   ├── 192_ailette_grille_ventilation_5.glb
│           │   │   ├── 193_ailette_grille_ventilation_6.glb
│           │   │   ├── 194_ailette_grille_ventilation_7.glb
│           │   │   ├── 195_support_afficheur.glb
│           │   │   ├── 196_ecran_commande.glb
│           │   │   ├── 197_ecran_indicateur_1.glb
│           │   │   ├── 198_ecran_indicateur_2.glb
│           │   │   ├── 199_ecran_indicateur_3.glb
│           │   │   ├── 200_support_arret_urgence.glb
│           │   │   ├── 201_arret_urgence_rouge.glb
│           │   │   └── 202_capteur_emplacement_avant.glb
│           │   ├── sous_ensembles/
│           │   │   ├── roue_motrice_assemblee.glb
│           │   │   └── roue_motrice_eclatee.glb
│           │   ├── batiment_complet.glb
│           │   ├── batiment_complet.sdf
│           │   ├── catalogue_robot.json
│           │   ├── niveau_depart.glb
│           │   ├── niveau_depart.sdf
│           │   ├── niveau_depart_coupe.sdf
│           │   ├── rez_de_chaussee.glb
│           │   ├── rez_de_chaussee.sdf
│           │   ├── rez_de_chaussee_coupe.sdf
│           │   ├── robot_agv.glb
│           │   └── robot_agv_eclate.glb
│           ├── Apercu_Maquette_AGV_3D.png
│           ├── generer_maquette.py
│           ├── lancer_gazebo.sh
│           ├── LIRE_MOI.md
│           ├── manifest_fichiers.json
│           ├── Maquette_AGV_Batiment_3D.html
│           ├── requirements.txt
│           ├── validation_glTF.json
│           ├── verification_affichage.json
│           ├── verification_maquette.json
│           └── visualiseur_template.html
├── Navigation et Simulation/
│   ├── Maquette_AGV_Bancaire_v0_2/
│   │   └── Maquette_AGV_Bancaire_v0_2/
│   │       ├── BFM_AGV_CAO_V01/
│   │       │   ├── 01_pieces_step/
│   │       │   │   ├── C01_longeron_gauche_40x40x3.step
│   │       │   │   ├── C02_longeron_droit_40x40x3.step
│   │       │   │   ├── C03_traverse_avant_40x40x3.step
│   │       │   │   ├── C04_traverse_central_40x40x3.step
│   │       │   │   ├── C05_traverse_arriere_40x40x3.step
│   │       │   │   ├── C06_plancher_3mm_perce_6xM6.step
│   │       │   │   ├── F01_vis_M8x30_hexagonale.step
│   │       │   │   ├── F02_ecrou_M8.step
│   │       │   │   ├── F04_vis_M6x50_hexagonale.step
│   │       │   │   ├── F05_ecrou_M6.step
│   │       │   │   ├── F06_rondelle_plate_M6.step
│   │       │   │   ├── M01_motor_reducteur_gabarit_128x94x70.step
│   │       │   │   ├── M02_platine_moteur_percee_et_soudable.step
│   │       │   │   ├── M03_accouplement_flexible_20x16_gabarit.step
│   │       │   │   ├── M04_vis_M5_accouplement.step
│   │       │   │   ├── R01_pneu_bande_roulement.step
│   │       │   │   ├── R02_jante_avec_trous_M8_PCD80.step
│   │       │   │   ├── R03_moyeu_a_bride_et_rainure_clavette.step
│   │       │   │   ├── R04_roulement_6204_gabarit_20x47x14.step
│   │       │   │   ├── R05_entretoise_axiale.step
│   │       │   │   ├── R06_arbre_D20_avec_rainure_clavette.step
│   │       │   │   ├── R07_rondelle_M8.step
│   │       │   │   ├── R08_clavette_6x6x30.step
│   │       │   │   ├── R09_support_double_paliers_siege_6204.step
│   │       │   │   ├── R10_collier_arret_arbre_D20.step
│   │       │   │   └── R11_vis_M6_collier_arret.step
│   │       │   ├── 02_pieces_stl/
│   │       │   │   ├── C01_longeron_gauche_40x40x3.stl
│   │       │   │   ├── C02_longeron_droit_40x40x3.stl
│   │       │   │   ├── C03_traverse_avant_40x40x3.stl
│   │       │   │   ├── C04_traverse_central_40x40x3.stl
│   │       │   │   ├── C05_traverse_arriere_40x40x3.stl
│   │       │   │   ├── C06_plancher_3mm_perce_6xM6.stl
│   │       │   │   ├── F01_vis_M8x30_hexagonale.stl
│   │       │   │   ├── F02_ecrou_M8.stl
│   │       │   │   ├── F04_vis_M6x50_hexagonale.stl
│   │       │   │   ├── F05_ecrou_M6.stl
│   │       │   │   ├── F06_rondelle_plate_M6.stl
│   │       │   │   ├── M01_motor_reducteur_gabarit_128x94x70.stl
│   │       │   │   ├── M02_platine_moteur_percee_et_soudable.stl
│   │       │   │   ├── M03_accouplement_flexible_20x16_gabarit.stl
│   │       │   │   ├── M04_vis_M5_accouplement.stl
│   │       │   │   ├── R01_pneu_bande_roulement.stl
│   │       │   │   ├── R02_jante_avec_trous_M8_PCD80.stl
│   │       │   │   ├── R03_moyeu_a_bride_et_rainure_clavette.stl
│   │       │   │   ├── R04_roulement_6204_gabarit_20x47x14.stl
│   │       │   │   ├── R05_entretoise_axiale.stl
│   │       │   │   ├── R06_arbre_D20_avec_rainure_clavette.stl
│   │       │   │   ├── R07_rondelle_M8.stl
│   │       │   │   ├── R08_clavette_6x6x30.stl
│   │       │   │   ├── R09_support_double_paliers_siege_6204.stl
│   │       │   │   ├── R10_collier_arret_arbre_D20.stl
│   │       │   │   └── R11_vis_M6_collier_arret.stl
│   │       │   ├── 03_assemblages_step/
│   │       │   │   ├── A01_roue_assemblee.step
│   │       │   │   ├── A02_roue_eclatee.step
│   │       │   │   └── A03_roues_sur_chassis.step
│   │       │   ├── 04_visualisation_glb/
│   │       │   │   ├── A01_roue_assemblee.glb
│   │       │   │   ├── A02_roue_eclatee.glb
│   │       │   │   └── A03_roues_sur_chassis.glb
│   │       │   ├── BUDGET_ROUE.md
│   │       │   ├── generer_cao.py
│   │       │   ├── interfaces_assemblage.json
│   │       │   ├── LISEZ_MOI.md
│   │       │   ├── nomenclature.json
│   │       │   ├── requirements.txt
│   │       │   └── validation_cao.json
│   │       ├── data/
│   │       │   ├── geometrie_plan_retenu.json
│   │       │   ├── parametres_3d.json
│   │       │   └── scene_3d.json
│   │       ├── modeles/
│   │       │   ├── assemblage/
│   │       │   │   ├── etape_01_chassis.glb
│   │       │   │   ├── etape_02_roues.glb
│   │       │   │   ├── etape_03_batterie.glb
│   │       │   │   ├── etape_04_coffre.glb
│   │       │   │   ├── etape_05_separateurs.glb
│   │       │   │   ├── etape_06_glissieres.glb
│   │       │   │   ├── etape_07_tiroir_S1.glb
│   │       │   │   ├── etape_08_tiroir_S2.glb
│   │       │   │   ├── etape_09_tiroir_S3.glb
│   │       │   │   ├── etape_10_tiroir_S4.glb
│   │       │   │   ├── etape_11_commandes.glb
│   │       │   │   └── etape_12_toit.glb
│   │       │   ├── pieces/
│   │       │   │   ├── 001_plaque_superieure_chassis.glb
│   │       │   │   ├── 002_longeron_gauche.glb
│   │       │   │   ├── 003_longeron_droite.glb
│   │       │   │   ├── 004_traverse_chassis_1.glb
│   │       │   │   ├── 005_traverse_chassis_2.glb
│   │       │   │   ├── 006_traverse_chassis_3.glb
│   │       │   │   ├── 007_traverse_chassis_4.glb
│   │       │   │   ├── 008_moteur_reducteur_gauche.glb
│   │       │   │   ├── 009_roue_motrice_gauche.glb
│   │       │   │   ├── 010_moyeu_moteur_gauche.glb
│   │       │   │   ├── 011_ecrou_roue_gauche_1.glb
│   │       │   │   ├── 012_ecrou_roue_gauche_2.glb
│   │       │   │   ├── 013_ecrou_roue_gauche_3.glb
│   │       │   │   ├── 014_ecrou_roue_gauche_4.glb
│   │       │   │   ├── 015_ecrou_roue_gauche_5.glb
│   │       │   │   ├── 016_ecrou_roue_gauche_6.glb
│   │       │   │   ├── 017_moteur_reducteur_droite.glb
│   │       │   │   ├── 018_roue_motrice_droite.glb
│   │       │   │   ├── 019_moyeu_moteur_droite.glb
│   │       │   │   ├── 020_ecrou_roue_droite_1.glb
│   │       │   │   ├── 021_ecrou_roue_droite_2.glb
│   │       │   │   ├── 022_ecrou_roue_droite_3.glb
│   │       │   │   ├── 023_ecrou_roue_droite_4.glb
│   │       │   │   ├── 024_ecrou_roue_droite_5.glb
│   │       │   │   ├── 025_ecrou_roue_droite_6.glb
│   │       │   │   ├── 026_support_roulette_avant.glb
│   │       │   │   ├── 027_roulette_pivotante_avant.glb
│   │       │   │   ├── 028_axe_roulette_avant.glb
│   │       │   │   ├── 029_fourche_roulette_avant_gauche.glb
│   │       │   │   ├── 030_vis_axe_roulette_avant_gauche.glb
│   │       │   │   ├── 031_fourche_roulette_avant_droite.glb
│   │       │   │   ├── 032_vis_axe_roulette_avant_droite.glb
│   │       │   │   ├── 033_support_roulette_arriere.glb
│   │       │   │   ├── 034_roulette_pivotante_arriere.glb
│   │       │   │   ├── 035_axe_roulette_arriere.glb
│   │       │   │   ├── 036_fourche_roulette_arriere_gauche.glb
│   │       │   │   ├── 037_vis_axe_roulette_arriere_gauche.glb
│   │       │   │   ├── 038_fourche_roulette_arriere_droite.glb
│   │       │   │   ├── 039_vis_axe_roulette_arriere_droite.glb
│   │       │   │   ├── 040_pare_chocs_avant.glb
│   │       │   │   ├── 041_pare_chocs_arriere.glb
│   │       │   │   ├── 042_support_batterie.glb
│   │       │   │   ├── 043_batterie_format_a_definir.glb
│   │       │   │   ├── 044_coffret_controleur_hypothese.glb
│   │       │   │   ├── 045_support_coffret_controleur.glb
│   │       │   │   ├── 046_fond_coffre.glb
│   │       │   │   ├── 047_paroi_arriere.glb
│   │       │   │   ├── 048_paroi_laterale_-0_49.glb
│   │       │   │   ├── 049_paroi_laterale_0_49.glb
│   │       │   │   ├── 050_toit_coffre.glb
│   │       │   │   ├── 051_separateur_horizontal.glb
│   │       │   │   ├── 052_separateur_vertical.glb
│   │       │   │   ├── 053_montant_face_-0_49.glb
│   │       │   │   ├── 054_montant_face_0_00.glb
│   │       │   │   ├── 055_montant_face_0_49.glb
│   │       │   │   ├── 056_traverse_face_0_33.glb
│   │       │   │   ├── 057_traverse_face_0_70.glb
│   │       │   │   ├── 058_traverse_face_1_06.glb
│   │       │   │   ├── 059_s1_fond_tiroir.glb
│   │       │   │   ├── 060_s1_flanc_gauche.glb
│   │       │   │   ├── 061_s1_glissiere_fixe_gauche.glb
│   │       │   │   ├── 062_s1_glissiere_mobile_gauche.glb
│   │       │   │   ├── 063_s1_flanc_droite.glb
│   │       │   │   ├── 064_s1_glissiere_fixe_droite.glb
│   │       │   │   ├── 065_s1_glissiere_mobile_droite.glb
│   │       │   │   ├── 066_s1_fond_arriere.glb
│   │       │   │   ├── 067_s1_joint_peripherique.glb
│   │       │   │   ├── 068_s1_facade.glb
│   │       │   │   ├── 069_s1_poignee.glb
│   │       │   │   ├── 070_s1_support_poignee_-1.glb
│   │       │   │   ├── 071_s1_support_poignee_1.glb
│   │       │   │   ├── 072_s1_plaque_identification.glb
│   │       │   │   ├── 073_s1_marquage_0_a.glb
│   │       │   │   ├── 074_s1_marquage_0_f.glb
│   │       │   │   ├── 075_s1_marquage_0_g.glb
│   │       │   │   ├── 076_s1_marquage_0_c.glb
│   │       │   │   ├── 077_s1_marquage_0_d.glb
│   │       │   │   ├── 078_s1_marquage_1_b.glb
│   │       │   │   ├── 079_s1_marquage_1_c.glb
│   │       │   │   ├── 080_s1_loquet.glb
│   │       │   │   ├── 081_s1_actionneur_corps.glb
│   │       │   │   ├── 082_s1_actionneur_tige.glb
│   │       │   │   ├── 083_s1_butee_-0_429.glb
│   │       │   │   ├── 084_s1_butee_-0_071.glb
│   │       │   │   ├── 085_s1_vis_face_-1_-1.glb
│   │       │   │   ├── 086_s1_vis_face_-1_1.glb
│   │       │   │   ├── 087_s1_vis_face_1_-1.glb
│   │       │   │   ├── 088_s1_vis_face_1_1.glb
│   │       │   │   ├── 089_s2_fond_tiroir.glb
│   │       │   │   ├── 090_s2_flanc_gauche.glb
│   │       │   │   ├── 091_s2_glissiere_fixe_gauche.glb
│   │       │   │   ├── 092_s2_glissiere_mobile_gauche.glb
│   │       │   │   ├── 093_s2_flanc_droite.glb
│   │       │   │   ├── 094_s2_glissiere_fixe_droite.glb
│   │       │   │   ├── 095_s2_glissiere_mobile_droite.glb
│   │       │   │   ├── 096_s2_fond_arriere.glb
│   │       │   │   ├── 097_s2_joint_peripherique.glb
│   │       │   │   ├── 098_s2_facade.glb
│   │       │   │   ├── 099_s2_poignee.glb
│   │       │   │   ├── 100_s2_support_poignee_-1.glb
│   │       │   │   ├── 101_s2_support_poignee_1.glb
│   │       │   │   ├── 102_s2_plaque_identification.glb
│   │       │   │   ├── 103_s2_marquage_0_a.glb
│   │       │   │   ├── 104_s2_marquage_0_f.glb
│   │       │   │   ├── 105_s2_marquage_0_g.glb
│   │       │   │   ├── 106_s2_marquage_0_c.glb
│   │       │   │   ├── 107_s2_marquage_0_d.glb
│   │       │   │   ├── 108_s2_marquage_1_a.glb
│   │       │   │   ├── 109_s2_marquage_1_b.glb
│   │       │   │   ├── 110_s2_marquage_1_g.glb
│   │       │   │   ├── 111_s2_marquage_1_e.glb
│   │       │   │   ├── 112_s2_marquage_1_d.glb
│   │       │   │   ├── 113_s2_loquet.glb
│   │       │   │   ├── 114_s2_actionneur_corps.glb
│   │       │   │   ├── 115_s2_actionneur_tige.glb
│   │       │   │   ├── 116_s2_butee_0_071.glb
│   │       │   │   ├── 117_s2_butee_0_429.glb
│   │       │   │   ├── 118_s2_vis_face_-1_-1.glb
│   │       │   │   ├── 119_s2_vis_face_-1_1.glb
│   │       │   │   ├── 120_s2_vis_face_1_-1.glb
│   │       │   │   ├── 121_s2_vis_face_1_1.glb
│   │       │   │   ├── 122_s3_fond_tiroir.glb
│   │       │   │   ├── 123_s3_flanc_gauche.glb
│   │       │   │   ├── 124_s3_glissiere_fixe_gauche.glb
│   │       │   │   ├── 125_s3_glissiere_mobile_gauche.glb
│   │       │   │   ├── 126_s3_flanc_droite.glb
│   │       │   │   ├── 127_s3_glissiere_fixe_droite.glb
│   │       │   │   ├── 128_s3_glissiere_mobile_droite.glb
│   │       │   │   ├── 129_s3_fond_arriere.glb
│   │       │   │   ├── 130_s3_joint_peripherique.glb
│   │       │   │   ├── 131_s3_facade.glb
│   │       │   │   ├── 132_s3_poignee.glb
│   │       │   │   ├── 133_s3_support_poignee_-1.glb
│   │       │   │   ├── 134_s3_support_poignee_1.glb
│   │       │   │   ├── 135_s3_plaque_identification.glb
│   │       │   │   ├── 136_s3_marquage_0_a.glb
│   │       │   │   ├── 137_s3_marquage_0_f.glb
│   │       │   │   ├── 138_s3_marquage_0_g.glb
│   │       │   │   ├── 139_s3_marquage_0_c.glb
│   │       │   │   ├── 140_s3_marquage_0_d.glb
│   │       │   │   ├── 141_s3_marquage_1_a.glb
│   │       │   │   ├── 142_s3_marquage_1_b.glb
│   │       │   │   ├── 143_s3_marquage_1_g.glb
│   │       │   │   ├── 144_s3_marquage_1_c.glb
│   │       │   │   ├── 145_s3_marquage_1_d.glb
│   │       │   │   ├── 146_s3_loquet.glb
│   │       │   │   ├── 147_s3_actionneur_corps.glb
│   │       │   │   ├── 148_s3_actionneur_tige.glb
│   │       │   │   ├── 149_s3_butee_-0_429.glb
│   │       │   │   ├── 150_s3_butee_-0_071.glb
│   │       │   │   ├── 151_s3_vis_face_-1_-1.glb
│   │       │   │   ├── 152_s3_vis_face_-1_1.glb
│   │       │   │   ├── 153_s3_vis_face_1_-1.glb
│   │       │   │   ├── 154_s3_vis_face_1_1.glb
│   │       │   │   ├── 155_s4_fond_tiroir.glb
│   │       │   │   ├── 156_s4_flanc_gauche.glb
│   │       │   │   ├── 157_s4_glissiere_fixe_gauche.glb
│   │       │   │   ├── 158_s4_glissiere_mobile_gauche.glb
│   │       │   │   ├── 159_s4_flanc_droite.glb
│   │       │   │   ├── 160_s4_glissiere_fixe_droite.glb
│   │       │   │   ├── 161_s4_glissiere_mobile_droite.glb
│   │       │   │   ├── 162_s4_fond_arriere.glb
│   │       │   │   ├── 163_s4_joint_peripherique.glb
│   │       │   │   ├── 164_s4_facade.glb
│   │       │   │   ├── 165_s4_poignee.glb
│   │       │   │   ├── 166_s4_support_poignee_-1.glb
│   │       │   │   ├── 167_s4_support_poignee_1.glb
│   │       │   │   ├── 168_s4_plaque_identification.glb
│   │       │   │   ├── 169_s4_marquage_0_a.glb
│   │       │   │   ├── 170_s4_marquage_0_f.glb
│   │       │   │   ├── 171_s4_marquage_0_g.glb
│   │       │   │   ├── 172_s4_marquage_0_c.glb
│   │       │   │   ├── 173_s4_marquage_0_d.glb
│   │       │   │   ├── 174_s4_marquage_1_f.glb
│   │       │   │   ├── 175_s4_marquage_1_g.glb
│   │       │   │   ├── 176_s4_marquage_1_b.glb
│   │       │   │   ├── 177_s4_marquage_1_c.glb
│   │       │   │   ├── 178_s4_loquet.glb
│   │       │   │   ├── 179_s4_actionneur_corps.glb
│   │       │   │   ├── 180_s4_actionneur_tige.glb
│   │       │   │   ├── 181_s4_butee_0_071.glb
│   │       │   │   ├── 182_s4_butee_0_429.glb
│   │       │   │   ├── 183_s4_vis_face_-1_-1.glb
│   │       │   │   ├── 184_s4_vis_face_-1_1.glb
│   │       │   │   ├── 185_s4_vis_face_1_-1.glb
│   │       │   │   ├── 186_s4_vis_face_1_1.glb
│   │       │   │   ├── 187_grille_ventilation_fond.glb
│   │       │   │   ├── 188_ailette_grille_ventilation_1.glb
│   │       │   │   ├── 189_ailette_grille_ventilation_2.glb
│   │       │   │   ├── 190_ailette_grille_ventilation_3.glb
│   │       │   │   ├── 191_ailette_grille_ventilation_4.glb
│   │       │   │   ├── 192_ailette_grille_ventilation_5.glb
│   │       │   │   ├── 193_ailette_grille_ventilation_6.glb
│   │       │   │   ├── 194_ailette_grille_ventilation_7.glb
│   │       │   │   ├── 195_support_afficheur.glb
│   │       │   │   ├── 196_ecran_commande.glb
│   │       │   │   ├── 197_ecran_indicateur_1.glb
│   │       │   │   ├── 198_ecran_indicateur_2.glb
│   │       │   │   ├── 199_ecran_indicateur_3.glb
│   │       │   │   ├── 200_support_arret_urgence.glb
│   │       │   │   ├── 201_arret_urgence_rouge.glb
│   │       │   │   └── 202_capteur_emplacement_avant.glb
│   │       │   ├── sous_ensembles/
│   │       │   │   ├── roue_motrice_assemblee.glb
│   │       │   │   └── roue_motrice_eclatee.glb
│   │       │   ├── batiment_complet.glb
│   │       │   ├── batiment_complet.sdf
│   │       │   ├── catalogue_robot.json
│   │       │   ├── niveau_depart.glb
│   │       │   ├── niveau_depart.sdf
│   │       │   ├── niveau_depart_coupe.sdf
│   │       │   ├── rez_de_chaussee.glb
│   │       │   ├── rez_de_chaussee.sdf
│   │       │   ├── rez_de_chaussee_coupe.sdf
│   │       │   ├── robot_agv.glb
│   │       │   └── robot_agv_eclate.glb
│   │       ├── Apercu_Maquette_AGV_3D.png
│   │       ├── generer_maquette.py
│   │       ├── lancer_gazebo.sh
│   │       ├── LIRE_MOI.md
│   │       ├── manifest_fichiers.json
│   │       ├── Maquette_AGV_Batiment_3D.html
│   │       ├── requirements.txt
│   │       ├── validation_glTF.json
│   │       ├── verification_affichage.json
│   │       ├── verification_maquette.json
│   │       └── visualiseur_template.html
│   ├── Sources_frontend/
│   │   ├── simulation/
│   │   │   ├── scene_3d.json
│   │   │   └── world.ts
│   │   ├── Simulation3D.css
│   │   └── Simulation3D.tsx
│   └── ETAT_SIMULATION.md
├── README.md
└── STRUCTURE_COMPLETE.md
```
