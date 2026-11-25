# Structure complete - MECANIQUE

**Dossier :** `MECANIQUE/`

Arborescence des dossiers et fichiers du perimetre ci-dessous. Les dependances generees (`node_modules`, `dist`, `.vite`, `__pycache__` et `.git`) sont exclues.

```text
MECANIQUE/
├── Calculs et Dimensionnements/
│   └── BFM_V4/
│       ├── enveloppe-mesuree-v4.svg
│       └── validation_mecanique.json
├── Etude et Conception/
│   └── BFM_V4/
│       ├── Avant_projet_mecanique.md
│       ├── Exigences_initiales.md
│       ├── GUIDE_TECHNIQUE_V4.md
│       └── LIMITES_CAO_BFM_V4.md
├── Fabrication mécanique/
│   ├── Avant_projet_mecanique.md
│   ├── ETAT_FABRICATION.md
│   └── LIMITES_CAO_BFM_V4.md
├── Modelisation 3D et Plans/
│   ├── Sources_BFM_V4/
│   │   ├── 01_ROUES/
│   │   │   ├── STEP/
│   │   │   │   ├── R01.step
│   │   │   │   ├── R02.step
│   │   │   │   ├── R03.step
│   │   │   │   ├── R04.step
│   │   │   │   ├── R05.step
│   │   │   │   ├── R06.step
│   │   │   │   └── R07.step
│   │   │   └── STL/
│   │   │       ├── R01.stl
│   │   │       ├── R02.stl
│   │   │       ├── R03.stl
│   │   │       ├── R04.stl
│   │   │       ├── R05.stl
│   │   │       ├── R06.stl
│   │   │       └── R07.stl
│   │   ├── 02_MOTORISATION/
│   │   │   ├── STEP/
│   │   │   │   ├── M01.step
│   │   │   │   ├── M01_D.step
│   │   │   │   ├── M02.step
│   │   │   │   ├── M03.step
│   │   │   │   ├── M04.step
│   │   │   │   └── M05.step
│   │   │   └── STL/
│   │   │       ├── M01.stl
│   │   │       ├── M01_D.stl
│   │   │       ├── M02.stl
│   │   │       ├── M03.stl
│   │   │       ├── M04.stl
│   │   │       └── M05.stl
│   │   ├── 03_CHASSIS/
│   │   │   ├── STEP/
│   │   │   │   ├── C01.step
│   │   │   │   ├── C02.step
│   │   │   │   ├── C03.step
│   │   │   │   ├── C04.step
│   │   │   │   ├── C05.step
│   │   │   │   └── C06.step
│   │   │   └── STL/
│   │   │       ├── C01.stl
│   │   │       ├── C02.stl
│   │   │       ├── C03.stl
│   │   │       ├── C04.stl
│   │   │       ├── C05.stl
│   │   │       └── C06.stl
│   │   ├── 04_SUSPENSION/
│   │   │   ├── STEP/
│   │   │   │   ├── S01.step
│   │   │   │   ├── S02.step
│   │   │   │   ├── S03.step
│   │   │   │   └── S04.step
│   │   │   └── STL/
│   │   │       ├── S01.stl
│   │   │       ├── S02.stl
│   │   │       ├── S03.stl
│   │   │       └── S04.stl
│   │   ├── 05_COFFRE_2X2/
│   │   │   ├── STEP/
│   │   │   │   ├── K01.step
│   │   │   │   ├── K02.step
│   │   │   │   ├── K03.step
│   │   │   │   ├── K04.step
│   │   │   │   ├── K05.step
│   │   │   │   ├── K06.step
│   │   │   │   ├── K07.step
│   │   │   │   └── K08.step
│   │   │   └── STL/
│   │   │       ├── K01.stl
│   │   │       ├── K02.stl
│   │   │       ├── K03.stl
│   │   │       ├── K04.stl
│   │   │       ├── K05.stl
│   │   │       ├── K06.stl
│   │   │       ├── K07.stl
│   │   │       └── K08.stl
│   │   ├── 06_TIROIRS/
│   │   │   ├── STEP/
│   │   │   │   ├── T01.step
│   │   │   │   ├── T02.step
│   │   │   │   ├── T03.step
│   │   │   │   ├── T04.step
│   │   │   │   ├── T05.step
│   │   │   │   ├── T06.step
│   │   │   │   └── T07.step
│   │   │   └── STL/
│   │   │       ├── T01.stl
│   │   │       ├── T02.stl
│   │   │       ├── T03.stl
│   │   │       ├── T04.stl
│   │   │       ├── T05.stl
│   │   │       ├── T06.stl
│   │   │       └── T07.stl
│   │   ├── 07_DECHARGEMENT/
│   │   │   ├── STEP/
│   │   │   │   ├── D01.step
│   │   │   │   ├── D02.step
│   │   │   │   ├── D03.step
│   │   │   │   ├── D04.step
│   │   │   │   ├── D05.step
│   │   │   │   ├── D06.step
│   │   │   │   ├── D07.step
│   │   │   │   └── D08.step
│   │   │   └── STL/
│   │   │       ├── D01.stl
│   │   │       ├── D02.stl
│   │   │       ├── D03.stl
│   │   │       ├── D04.stl
│   │   │       ├── D05.stl
│   │   │       ├── D06.stl
│   │   │       ├── D07.stl
│   │   │       └── D08.stl
│   │   ├── 08_ELECTRONIQUE/
│   │   │   ├── STEP/
│   │   │   │   ├── E01.step
│   │   │   │   ├── E02.step
│   │   │   │   ├── E03.step
│   │   │   │   ├── E04.step
│   │   │   │   ├── E05.step
│   │   │   │   ├── E06.step
│   │   │   │   └── E07.step
│   │   │   └── STL/
│   │   │       ├── E01.stl
│   │   │       ├── E02.stl
│   │   │       ├── E03.stl
│   │   │       ├── E04.stl
│   │   │       ├── E05.stl
│   │   │       ├── E06.stl
│   │   │       └── E07.stl
│   │   ├── 09_ASSEMBLAGES/
│   │   │   ├── GLB/
│   │   │   │   ├── A01_ROUE_ASSEMBLEE.glb
│   │   │   │   ├── A02_ROUE_ECLATEE.glb
│   │   │   │   ├── A03_CHASSIS.glb
│   │   │   │   ├── A04_MOTORISATION.glb
│   │   │   │   ├── A05_ROUES_MOTRICES.glb
│   │   │   │   ├── A06_ROULETTES.glb
│   │   │   │   ├── A07_COFFRE_2X2.glb
│   │   │   │   ├── A08_QUATRE_TIROIRS.glb
│   │   │   │   ├── A09_MECANISMES_EXTRACTION.glb
│   │   │   │   ├── A10_BASE_ROULANTE.glb
│   │   │   │   ├── A11_ELECTRONIQUE.glb
│   │   │   │   └── A12_STATION_DEPOT.glb
│   │   │   └── STEP/
│   │   │       ├── A01_ROUE_ASSEMBLEE.step
│   │   │       ├── A02_ROUE_ECLATEE.step
│   │   │       ├── A03_CHASSIS.step
│   │   │       ├── A04_MOTORISATION.step
│   │   │       ├── A05_ROUES_MOTRICES.step
│   │   │       ├── A06_ROULETTES.step
│   │   │       ├── A07_COFFRE_2X2.step
│   │   │       ├── A08_QUATRE_TIROIRS.step
│   │   │       ├── A09_MECANISMES_EXTRACTION.step
│   │   │       ├── A10_BASE_ROULANTE.step
│   │   │       ├── A11_ELECTRONIQUE.step
│   │   │       └── A12_STATION_DEPOT.step
│   │   ├── 10_ROBOT_COMPLET/
│   │   │   ├── GLB/
│   │   │   │   ├── A13_ROBOT_COMPLET.glb
│   │   │   │   ├── A14_ROBOT_ET_STATION.glb
│   │   │   │   └── A15_VUE_ECLATEE_GLOBALE.glb
│   │   │   └── STEP/
│   │   │       ├── A13_ROBOT_COMPLET.step
│   │   │       ├── A14_ROBOT_ET_STATION.step
│   │   │       └── A15_VUE_ECLATEE_GLOBALE.step
│   │   ├── generer_cao.py
│   │   ├── LISEZ_MOI.md
│   │   ├── NOMENCLATURE_ASSEMBLAGES.csv
│   │   ├── NOMENCLATURE_PIECES.csv
│   │   └── validation_mecanique.json
│   └── Sources_Plan_AGV_v0_1/
│       ├── build_agv_plans.py
│       ├── geometrie_AGV_v0_1.json
│       ├── LIRE_MOI.txt
│       ├── plan_01.svg
│       ├── plan_02.svg
│       └── plan_03.svg
├── README.md
└── STRUCTURE_COMPLETE.md
```
