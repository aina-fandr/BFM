import os, math, csv, json, zipfile, shutil
from pathlib import Path
import cadquery as cq
import trimesh
import numpy as np
from collections import defaultdict
ROOT=str(Path(__file__).resolve().parent)
PROJECT_ROOT=str(Path(__file__).resolve().parents[2])
os.makedirs(ROOT,exist_ok=True)
FOLDERS=['01_ROUES','02_MOTORISATION','03_CHASSIS','04_SUSPENSION','05_COFFRE_2X2','06_TIROIRS','07_DECHARGEMENT','08_ELECTRONIQUE','09_ASSEMBLAGES','10_ROBOT_COMPLET']
for f in FOLDERS:
 for sub in (['STEP','STL'] if f[:2] in ['01','02','03','04','05','06','07','08'] else ['STEP','GLB']): os.makedirs(os.path.join(ROOT,f,sub),exist_ok=True)
parts={}; group=defaultdict(list); entries=[]
COL={'acier': [105,128,148,255], 'alu':[177,188,198,255],'caoutchouc':[43,50,61,255], 'polymere':[206,218,226,255], 'electronique':[43,122,100,255], 'sac':[176,148,104,255], 'moteur':[65,108,154,255], 'securite':[211,166,77,255]}
def box(a,b,c): return cq.Workplane('XY').box(a,b,c).val()
def cyl(r,h,axis='z'):
 return cq.Workplane('XY' if axis=='z' else 'XZ' if axis=='y' else 'YZ').circle(r).extrude(h/2,both=True).val()
def hollow(ro,ri,h,axis='z'):
 return cq.Workplane('XY' if axis=='z' else 'XZ' if axis=='y' else 'YZ').circle(ro).circle(ri).extrude(h/2,both=True).val()
def move(sh,x=0,y=0,z=0):return sh.translate((x,y,z))
def part(groupid,code,name,shape,material,role,dim,note='Concept non valide'):
 parts[code]=(shape,material,name)
 group[groupid].append(code)
 folder=FOLDERS[groupid-1]
 cq.exporters.export(shape,os.path.join(ROOT,folder,'STEP',code+'.step'))
 cq.exporters.export(shape,os.path.join(ROOT,folder,'STL',code+'.stl'),tolerance=0.7,angularTolerance=0.25)
 entries.append([code,folder,name,material,dim,role,note])
def inst(code,x=0,y=0,z=0):return (code,(x,y,z))
# Wheel axis Y, origin at center
part(1,'R01','Bandage elastomere',hollow(100,77,44,'y'),'caoutchouc','Adherence et roulement','Ø200 ext / Ø154 int / 44 mm','Durete/charge fournisseur a choisir')
part(1,'R02','Jante',hollow(79,22,40,'y'),'alu','Support du bandage et connexion moyeu','Ø158 / alésage Ø44 / 40 mm')
part(1,'R03','Moyeu',hollow(31,12,64,'y'),'acier','Connexion de la jante a l axe','Ø62 / alésage Ø24 / 64 mm')
part(1,'R04','Axe',cyl(12,120,'y'),'acier','Transmission du couple','Ø24 / 120 mm')
part(1,'R05','Roulement schématique',hollow(31,12,18,'y'),'acier','Guidage en rotation, volume enveloppe','Ø62 / Ø24 / 18 mm','Remplacer par reference fabricant')
part(1,'R06','Entretoise',hollow(18,12.5,22,'y'),'acier','Maintien axial','Ø36 / Ø25 / 22 mm')
part(1,'R07','Rondelle',hollow(20,12.5,3,'y'),'acier','Appui de fixation','Ø40 / Ø25 / 3 mm')
# Motors
motor_step=os.path.join(PROJECT_ROOT,'F6B250-24GU-30S_6GUXXRT.STEP')
if os.path.exists(motor_step):
 motor_import=cq.importers.importStep(motor_step)
 motor_real=motor_import.val()
 motor_box=motor_real.BoundingBox()
 motor_center=(motor_box.center.x,motor_box.center.y,motor_box.center.z)
 motor_real=motor_real.translate((-motor_center[0],-motor_center[1],-motor_center[2]))
 motor_real=motor_real.clean()
 motor_dim='237 × 172.5 × 104 mm; arbre de sortie orienté selon Y'
 motor_note='STEP fabricant F6B250-24GU-30S/6GU50RT; positionné avec l arbre de sortie coaxial à la roue'
else:
 motor_real=cyl(51,155,'y')
 motor_dim='Ø102 / 155 mm'
 motor_note='STEP fabricant absent: gabarit simplifié'
motor_real=motor_real.rotate((0,0,0),(1,0,0),0)
part(2,'M01','Motoréducteur réel F6B250-24GU-30S',motor_real,'moteur','Motorisation roue motrice',motor_dim,motor_note)
motor_real_right=motor_real.mirror('XZ')
part(2,'M01_D','Motoréducteur droit réel F6B250-24GU-30S',motor_real_right,'moteur','Motorisation roue motrice droite',motor_dim,motor_note)
part(2,'M02','Bride moteur',box(136,10,128),'acier','Fixation motorisation au chassis','136 × 10 × 128 mm','Perpendiculaire à l axe Y')
part(2,'M03','Accouplement axial roue-moteur',hollow(23,12,36,'y'),'acier','Liaison réducteur-moyeu','Ø46 / Ø24 / 36 mm','Arbre de sortie et moyeu à vérifier avec pièces réelles')
part(2,'M05','Frein de maintien simplifié',hollow(45,12,22,'y'),'securite','Maintien statique en absence alimentation','Ø90 / Ø24 / 22 mm','Frein certifie et mecanisme reel a choisir')
# chassis parts shape origins local, placements later
part(3,'C01','Longeron longitudinal',box(1050,40,40),'acier','Element porteur principal','1050 × 40 × 40 mm; tube conceptuel','Remplacer par profile creux et assemblage soude')
part(3,'C02','Traverse',box(40,520,40),'acier','Rigidification transversale','40 × 520 × 40 mm')
part(3,'C03','Platine de fond',box(1040,520,5),'acier','Support équipements bas','1040 × 520 × 5 mm')
part(3,'C04','Platine coffre',box(1030,530,8),'acier','Support et liaison coffret','1030 × 530 × 8 mm')
part(3,'C05','Renfort diagonal schématique',box(310,35,30),'acier','Renfort local','310 × 35 × 30 mm','Orientation finale a calculer')
part(3,'C06','Support moteur',box(190,95,10),'acier','Interface chassis motorisation','190 × 95 × 10 mm')
# caster
part(4,'S01','Roue libre de support',cyl(40,30,'y'),'caoutchouc','Support vertical et roulement','Ø80 / 30 mm')
part(4,'S02','Fourche roulette',box(70,12,90),'acier','Support roulette','70 × 12 × 90 mm','Modélisation volumique simplifiee')
part(4,'S03','Pivot vertical',cyl(13,80,'z'),'acier','Orientation roue folle','Ø26 / 80 mm')
part(4,'S04','Platines pivot',box(80,80,8),'acier','Fixation roulette au chassis','80 × 80 × 8 mm')
# cabinet (top from 245 to 995; walls). horizontal X direction storage / front +X
part(5,'K01','Panneau dessus',box(1000,500,3),'acier','Fermeture superieure','1000 × 500 × 3 mm')
part(5,'K02','Panneau latéral',box(1000,3,744),'acier','Enveloppe laterale','1000 × 3 × 744 mm')
part(5,'K03','Panneau arrière',box(3,494,744),'acier','Enveloppe arrière','3 × 494 × 744 mm')
part(5,'K04','Plancher coffre',box(1000,500,5),'acier','Base coffre','1000 × 500 × 5 mm')
part(5,'K05','Cloison verticale',box(980,3,735),'acier','Separation gauche/droite','980 × 3 × 735 mm')
part(5,'K06','Cloison horizontale',box(980,487,5),'acier','Separation haut/bas','980 × 487 × 5 mm')
part(5,'K07','Porte frontale casier',box(4,235,340),'acier','Fermeture indépendante','4 × 235 × 340 mm','Charniere / serrure a definir')
part(5,'K08','Charnière schématique',cyl(7,50,'z'),'acier','Axe articulation porte','Ø14 / 50 mm')
# drawer local x front +X, y centered, z local
part(6,'T01','Fond plateau coulissant',box(860,214,4),'acier','Support sac 40 kg','860 × 214 × 4 mm','Conception subordonnée aux dimensions du sac')
part(6,'T02','Joue latérale du plateau',box(860,4,100),'acier','Retenue laterale sac','860 × 4 × 100 mm')
part(6,'T03','Butée avant',box(4,204,90),'acier','Retenir sac en transport','4 × 204 × 90 mm')
part(6,'T04','Rail fixe schématique',box(880,16,20),'acier','Guidage support tiroir','880 × 16 × 20 mm','Charge reelle rails a selectionner')
part(6,'T05','Rail mobile schématique',box(865,12,12),'alu','Partie coulissante du guidage','865 × 12 × 12 mm')
part(6,'T06','Verrou de transport',box(48,25,28),'securite','Retenir tiroir ferme','48 × 25 × 28 mm','Schématique non anti-effraction')
part(6,'T07','Support capteur fin de course',box(35,25,3),'alu','Support capteur tiroir','35 × 25 × 3 mm')
# transfer mechanism (simplified conceptual)
part(7,'D01','Vis de translation',cyl(9,820,'x'),'acier','Motoriser extraction du plateau','Ø18 / 820 mm','Pas, flambement et guidage a dimensionner')
part(7,'D02','Ecrou entrainement',box(45,42,38),'alu','Liaison entre vis et plateau','45 × 42 × 38 mm','Filetage non modele')
part(7,'D03','Moteur extracteur volume',box(75,58,58),'moteur','Entrainement vis de tiroir','75 × 58 × 58 mm')
part(7,'D04','Plaque poussoir',box(5,195,140),'acier','Transfert vers station après arrimage','5 × 195 × 140 mm','N est pas un mécanisme de transfert validé')
part(7,'D05','Guide poussoir',box(720,15,15),'acier','Guidage translation poussoir','720 × 15 × 15 mm')
part(7,'D06','Butée d arrimage station',box(45,75,90),'securite','Appui de centrage a la station','45 × 75 × 90 mm')
part(7,'D07','Plateau de réception station',box(500,500,8),'acier','Station externe, accueil sac','500 × 500 × 8 mm','Station non embarquee')
part(7,'D08','Colonne station fixe',box(65,65,1050),'acier','Guidage élévation station','65 × 65 × 1050 mm','Station non embarquee')
# electronics placeholders
part(8,'E01','Batterie volume enveloppe',box(310,210,140),'electronique','Masse basse alimentation 24V','310 × 210 × 140 mm','Chimie et capacite non fixees')
part(8,'E02','Controleur central volume enveloppe',box(160,120,42),'electronique','Pilotage des mouvements','160 × 120 × 42 mm')
part(8,'E03','Driver moteur volume enveloppe',box(130,85,45),'electronique','Commande propulsion','130 × 85 × 45 mm')
part(8,'E04','Scanner lidar volume enveloppe',cyl(52,62),'electronique','Localisation et obstacles','Ø104 × 62 mm','Pas capteur de securite certifie')
part(8,'E05','Arrêt d urgence volume',cyl(23,32),'securite','Arret d urgence','Ø46 × 32 mm','Composant certifié à choisir')
part(8,'E06','Capteur presence casier volume',box(22,16,12),'electronique','Detection présence ou position','22 × 16 × 12 mm')
part(8,'E07','Ecran interface volume',box(8,145,90),'electronique','Interface personnel','8 × 145 × 90 mm')
# build assemblies represented as (code,xyz); trimesh scene by tessellation
assemblies={}
assemblies['A01_ROUE_ASSEMBLEE']=[inst('R01'),inst('R02'),inst('R03'),inst('R04'),inst('R05',0,30,0),inst('R05',0,-30,0),inst('R06',0,48,0),inst('R07',0,62,0)]
assemblies['A02_ROUE_ECLATEE']=[inst('R01',0,0,0),inst('R02',0,90,0),inst('R03',0,170,0),inst('R04',0,280,0),inst('R05',0,380,0),inst('R05',0,430,0),inst('R06',0,490,0),inst('R07',0,540,0)]
chassis=[]
for y in [-270,270]: chassis.append(inst('C01',0,y,155))
for x in [-495,0,495]:chassis.append(inst('C02',x,0,155))
chassis += [inst('C03',0,0,175),inst('C04',0,0,237)]
for y in [-272,272]:chassis.append(inst('C06',0,y,178))
assemblies['A03_CHASSIS']=chassis
motors=[]; wheels=[]
for wheel_y,side in [(-322,'G'),(322,'D')]:
 motor_code='M01' if side=='G' else 'M01_D'
 motor_x=-103.5
 motor_y=-241.25 if side=='G' else 241.25
 motor_output_y=-322.0 if side=='G' else 322.0
 coupling_y=-304.0 if side=='G' else 304.0
 plate_y=-291.0 if side=='G' else 291.0
 brake_y=-289.0 if side=='G' else 289.0
 motors += [
  inst(motor_code,motor_x,motor_y,105),
  inst('M02',motor_x,plate_y,105),
  inst('M03',0,coupling_y,105),
  inst('M05',0,brake_y,105),
 ]
 wheels += [(c,(x,wheel_y+yy,z+105)) for c,(x,yy,z) in assemblies['A01_ROUE_ASSEMBLEE']]
assert motor_output_y == 322 or motor_output_y == -322
assemblies['A04_MOTORISATION']=motors
assemblies['A05_ROUES_MOTRICES']=wheels
casters=[]
for x in [-420,420]:
 for y in [-185,185]:casters += [inst('S01',x,y,49),inst('S02',x,y+23,65),inst('S03',x,y,107),inst('S04',x,y,138)]
assemblies['A06_ROULETTES']=casters
# cabinet origin base z=247, roof z=992
cab=[inst('K01',0,0,992),inst('K04',0,0,247),inst('K03',-499,0,620),inst('K05',0,0,620),inst('K06',0,0,620)]
for y in [-249,249]:cab.append(inst('K02',0,y,620))
for y in [-125,125]:
 for z in [433,808]:cab += [inst('K07',500,y,z),inst('K08',500,y-113,z+125)]
assemblies['A07_COFFRE_2X2']=cab
# 4 instances trays
trays=[]; act=[]; sensors=[]
for y in [-125,125]:
 for z in [426,801]:
  trays += [inst('T01',0,y,z),inst('T02',0,y-104,z+52),inst('T02',0,y+104,z+52),inst('T03',433,y,z+45),inst('T04',0,y-114,z-8),inst('T04',0,y+114,z-8),inst('T05',0,y-114,z),inst('T05',0,y+114,z),inst('T06',435,y-100,z+32)]
  act += [inst('D01',0,y,z-30),inst('D02',-230,y,z-30),inst('D03',-465,y,z-30),inst('D04',-420,y,z+85),inst('D05',0,y+65,z+25)]
  sensors += [inst('E06',445,y-88,z+58)]
assemblies['A08_QUATRE_TIROIRS']=trays
assemblies['A09_MECANISMES_EXTRACTION']=act
base=chassis+motors+wheels+casters
assemblies['A10_BASE_ROULANTE']=base
el=[inst('E01',-220,0,65),inst('E02',260,-70,194),inst('E03',275,95,194),inst('E04',535,0,170),inst('E05',430,130,1015),inst('E07',350,-160,1020)]+sensors
assemblies['A11_ELECTRONIQUE']=el
station=[inst('D07',900,0,530),inst('D08',1150,-205,545),inst('D08',1150,205,545),inst('D06',595,-180,465),inst('D06',595,180,465)]
assemblies['A12_STATION_DEPOT']=station
full=base+cab+trays+act+el
assemblies['A13_ROBOT_COMPLET']=full
assemblies['A14_ROBOT_ET_STATION']=full+station
# exploded global arrange principal layers separated, act etc translate
assemblies['A15_VUE_ECLATEE_GLOBALE']=base+[(code,(x,y,z+290)) for code,(x,y,z) in cab]+[(code,(x+150,y,z+620)) for code,(x,y,z) in trays]+[(code,(x-150,y,z+940)) for code,(x,y,z) in act]+[(code,(x,y,z+1200)) for code,(x,y,z) in el]
# export assembly STEP compound and GLB scene, OBJ meshes allow color and positions
from cadquery import exporters
# GLB remesh with mild tolerance, per reusable solid cached
mesh_cache={}
def asmesh(code):
 if code not in mesh_cache:
  sh=parts[code][0]
  v,faces=sh.tessellate(1.8,0.25)
  vs=np.array([[x.x,x.y,x.z] for x in v]); fs=np.asarray(faces,dtype=int)
  mesh_cache[code]=trimesh.Trimesh(vertices=vs,faces=fs,process=False)
 return mesh_cache[code]
def export_ass(name,items,dest):
 scene=trimesh.Scene(); solids=[]
 for i,(code,(x,y,z)) in enumerate(items):
  try:
   m=asmesh(code).copy();m.apply_translation([x,y,z]);m.visual.face_colors=COL[parts[code][1]]
   scene.add_geometry(m,node_name=f'{code}_{i}',geom_name=f'{code}_{i}')
   solids.append(move(parts[code][0],x,y,z))
  except Exception as e:print('ERROR',name,code,str(e))
 scene.export(os.path.join(ROOT,dest,'GLB',name+'.glb'))
 # STEP compound - can be expensive
 cq.exporters.export(cq.Compound.makeCompound(solids),os.path.join(ROOT,dest,'STEP',name+'.step'))
for name,items in assemblies.items():
 dest='09_ASSEMBLAGES' if name not in ['A13_ROBOT_COMPLET','A14_ROBOT_ET_STATION','A15_VUE_ECLATEE_GLOBALE'] else '10_ROBOT_COMPLET'
 print('ASSEMBLY',name,len(items),flush=True)
 export_ass(name,items,dest)
with open(os.path.join(ROOT,'NOMENCLATURE_PIECES.csv'),'w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Reference','Famille','Piece','Matiere envisagee','Enveloppe / dimensions conceptuelles','Fonction','Etat']);w.writerows(entries)
with open(os.path.join(ROOT,'NOMENCLATURE_ASSEMBLAGES.csv'),'w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Assemblage','Nombre instances','Pieces uniques','Components / coordinates mm']);
 for n,items in assemblies.items():w.writerow([n,len(items),len(set(c for c,_ in items)),json.dumps(items,ensure_ascii=False)])
readme='''# BFM AGV — DOSSIER CAO V02 — CONCEPT NON VALIDÉ

## Contenu
- 8 familles de pièces, avec fichiers STEP (solides B-Rep) et STL individuels.
- 09_ASSEMBLAGES: sous-ensembles, dont roue assemblée ET éclatée, motorisation, base roulante, coffre et tiroirs.
- 10_ROBOT_COMPLET: robot global, robot + station de dépôt, vue éclatée globale.
- Pour chaque assemblage : STEP (géométries), GLB (aperçu 3D coloré).
- NOMENCLATURE_PIECES.csv : fonctions, matériaux et dimensions préliminaires.
- NOMENCLATURE_ASSEMBLAGES.csv : instances et positions en millimètres.
- generer_cao.py : script source pour modifier et régénérer.

## Référentiel et dimensions
Unité de modélisation : millimètre. X avant/arrière; Y gauche/droite; Z hauteur.
Châssis nominal 1100 x 600 mm, coffre nominal 1000 x 500 x 750 mm.
Deux roues motrices Ø200 mm, quatre roulettes de soutien symboliques.
Coffre 2x2, compartiments indépendants; tiroirs à extraction sur rails.
Déchargement: vis d'extraction et plaque poussoir simplifiés; station fixe élévatrice est une ÉBAUCHE géométrique, pas une machine fonctionnelle.

## Statut IMPORTANT
Tous les modèles sont des propositions dimensionnelles pour étude et prototypage, PAS des plans constructibles validés.
- Les roues, roulements, motoréducteurs, capteurs, serrures, actionneurs et composants électroniques sont des VOLUMES CONCEPTUELS. Remplacer par STEP fabricant une fois les références sélectionnées.
- Les perçages, les liaisons cinématiques, la visserie réelle, soudures, réglages, butées détaillées et câblage ne sont pas définis.
- L'export STEP d'assemblage est un composé de solides positionnés, sans contraintes paramétriques natives, et non un assemblage SolidWorks/FreeCAD déjà contraint.
- Les casiers et tiroirs ne sont pas dimensionnés sur la géométrie réelle d'un sac de 40 kg: étudier les interférences avant fabrication.
- Risques majeurs : stabilité des tiroirs ouverts, pente/sol, transfert de 40 kg, passage des portes, charge admissible de l'ascenseur, collisions entre volumes et accessibilité humaine.
- Les sous-ensembles comprennent certains chevauchements volumétriques; ce dossier est une base d'organisation et de visualisation, pas un assemblage sans collision.
- Ne pas utiliser le système de déchargement avec une charge réelle avant analyse des risques, calculs, essais et supervision.

## Utilisation
Ouvrir les fichiers STEP dans FreeCAD ou autre logiciel de CAO. Ouvrir les GLB dans Blender ou un visualiseur 3D. Le script nécessite cadquery, trimesh et numpy.
'''
open(os.path.join(ROOT,'LISEZ_MOI.md'),'w',encoding='utf8').write(readme)
generated_script=os.path.join(ROOT,'generer_cao.py')
if os.path.abspath(__file__) != os.path.abspath(generated_script):
 shutil.copy(__file__,generated_script)
validation={
 'axis':'Y',
 'wheel_centers_mm':{'left':[0,-322,105],'right':[0,322,105]},
 'motor_output_centers_mm':{'left':[0,-286,105],'right':[0,286,105]},
 'coupling_centers_mm':{'left':[0,-304,105],'right':[0,304,105]},
 'chain_left':['M01 output Y-286','M03 Y-304','R04 wheel shaft Y-322'],
 'chain_right':['M01_D output Y+286','M03 Y+304','R04 wheel shaft Y+322'],
 'motor_file':'F6B250-24GU-30S_6GUXXRT.STEP',
 'rotation_check':'No arbitrary Z-rotation; STEP output-shaft axis aligned with Y',
 'status':'KINEMATIC_LAYOUT_CORRECTED_NOT_LOAD_VALIDATED'
}
with open(os.path.join(ROOT,'validation_mecanique.json'),'w',encoding='utf-8') as f:
 json.dump(validation,f,ensure_ascii=False,indent=2)
zip_path=os.path.join(str(Path(ROOT).parent),'BFM_AGV_CAO_V02_Complet.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as zf:
 for dirpath, dirs, files in os.walk(ROOT):
  for filename in files:
   p=os.path.join(dirpath,filename);zf.write(p,os.path.relpath(p,'/mnt/data'))
print('RESULT',len(parts),'unique pieces',len(assemblies),'assemblies',round(os.path.getsize(zip_path)/1e6,1),'MB',flush=True)
