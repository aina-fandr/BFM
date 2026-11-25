"""BFM AGV - lot CAO 01, module de roue motrice conceptuel, dimensions en mm.
Les composants industriels restent des gabarits a remplacer par les STEP fabricants.
"""
from pathlib import Path
import json
import math
import cadquery as cq
import trimesh
import numpy as np

ROOT=Path(__file__).resolve().parent
PART=ROOT/'01_pieces_step'
STL=ROOT/'02_pieces_stl'
ASS=ROOT/'03_assemblages_step'
GLB=ROOT/'04_visualisation_glb'
for directory in (PART,STL,ASS,GLB):
    directory.mkdir(exist_ok=True)

WHEEL_OD=200
WHEEL_WIDTH=55
WHEEL_CENTRES=515
GROSS_MASS_TARGET=230
MAX_EMPTY_MASS=70

COLORS={
    'rubber':(38,43,48,255),
    'aluminium':(181,193,201,255),
    'steel':(111,128,141,255),
    'stainless':(190,199,205,255),
    'motor':(42,91,135,255),
    'frame':(73,98,116,255),
    'deck':(152,165,171,255),
    'fastener':(207,213,218,255),
}

def box(x,y,z):
    return cq.Workplane('XY').box(x,y,z).val()

def at(shape,x=0,y=0,z=0):
    return shape.translate((x,y,z))

def cyl_y(radius,length):
    return cq.Workplane('XY').circle(radius).extrude(length/2,both=True).rotate((0,0,0),(1,0,0),90).val()

def cyl_z(radius,length):
    return cq.Workplane('XY').circle(radius).extrude(length/2,both=True).val()

def ring_y(outside,inside,length):
    return cq.Workplane('XY').circle(outside).circle(inside).extrude(length/2,both=True).rotate((0,0,0),(1,0,0),90).val()

def hex_y(diameter,length):
    return cq.Workplane('XY').polygon(6,diameter).extrude(length/2,both=True).rotate((0,0,0),(1,0,0),90).val()

def hex_z(diameter,length):
    return cq.Workplane('XY').polygon(6,diameter).extrude(length/2,both=True).val()

def bolt_y_m8():
    shank=cyl_y(4,30)
    head=at(hex_y(15,5.3),y=-17.65)
    return shank.fuse(head)

def nut_y_m8():
    return hex_y(15,7).cut(cyl_y(4.2,9))

def washer_y_m8():
    return ring_y(8,4.2,1.6)

def bolt_z_m6():
    shank=cyl_z(3,50)
    head=at(hex_z(11.5,5.3),z=27.65)
    return shank.fuse(head)

def nut_z_m6():
    return hex_z(11.5,5).cut(cyl_z(3.2,8))

def washer_z_m6():
    return cq.Workplane('XY').circle(6).circle(3.2).extrude(.8,both=True).val()

def screw_z_m6():
    return cyl_z(3,12).fuse(at(hex_z(7,3),z=7.5))

def screw_z_m5():
    return cyl_z(2.5,18).fuse(at(hex_z(6,2.5),z=10.25))

def bearing_6204():
    outer=ring_y(23.5,19.5,14)
    inner=ring_y(14.5,10,14)
    balls=[]
    for index in range(8):
        angle=math.tau*index/8
        point=cq.Vector(17*math.cos(angle),0,17*math.sin(angle))
        balls.append(cq.Solid.makeSphere(3,point,angleDegrees1=-90,angleDegrees2=90))
    return cq.Compound.makeCompound([outer,inner]+balls)

def hollow_beam(length_x,length_y,outer=40,wall=3):
    outside=box(length_x,length_y,outer)
    inside=box(length_x+2,length_y-2*wall,outer-2*wall)
    return outside.cut(inside)

def write_glb(name,items):
    scene=trimesh.Scene()
    for label,shape,color in items:
        vertices,faces=shape.tessellate(.35,.25)
        if not faces:
            continue
        mesh=trimesh.Trimesh(
            vertices=np.asarray([[v.x,v.y,v.z] for v in vertices]),
            faces=np.asarray(faces,dtype=int),
            process=False,
        )
        mesh.visual.vertex_colors=np.tile(np.asarray(color,dtype=np.uint8),(len(vertices),1))
        scene.add_geometry(mesh,geom_name=label,node_name=label)
    (GLB/(name+'.glb')).write_bytes(scene.export(file_type='glb'))

def write_assembly(name,items):
    assembly=cq.Assembly(name=name)
    for label,shape,color in items:
        rgba=tuple(channel/255 for channel in color)
        assembly.add(shape,name=label,color=cq.Color(*rgba))
    assembly.save(str(ASS/(name+'.step')))
    write_glb(name,items)

parts={}
parts['R01_pneu_bande_roulement']=ring_y(100,80,WHEEL_WIDTH)

rim=ring_y(80,72,51).fuse(ring_y(72,27.3,12))
bolt_circle=40
bolt_angles=[math.tau*i/6 for i in range(6)]
for angle in bolt_angles:
    rim=rim.cut(at(cyl_y(4.25,18),bolt_circle*math.cos(angle),0,bolt_circle*math.sin(angle)))
parts['R02_jante_avec_trous_M8_PCD80']=rim

hub=ring_y(27,10,42)
hub=at(hub,y=9).fuse(at(ring_y(50,10,8),y=-10))
for angle in bolt_angles:
    hub=hub.cut(at(cyl_y(4.25,14),bolt_circle*math.cos(angle),-10,bolt_circle*math.sin(angle)))
hub=hub.cut(at(box(6,32,3),y=9,z=11.5))
parts['R03_moyeu_a_bride_et_rainure_clavette']=hub
parts['R04_roulement_6204_gabarit_20x47x14']=bearing_6204()
parts['R05_entretoise_axiale']=ring_y(19,10.2,6)

shaft=cyl_y(10,185)
shaft=at(shaft,y=37.5).cut(at(box(6,32,3),y=9,z=8.5))
parts['R06_arbre_D20_avec_rainure_clavette']=shaft
parts['R07_rondelle_M8']=washer_y_m8()
parts['R08_clavette_6x6x30']=box(6,30,6)

support=box(82,52,70)
for bearing_y in [-15,15]:
    support=support.cut(at(cyl_y(23.5,14.4),y=bearing_y))
support=support.cut(cyl_y(10.2,54))
parts['R09_support_double_paliers_siege_6204']=support
collar=ring_y(17,10.1,8).cut(at(cyl_z(2.5,12),z=16))
parts['R10_collier_arret_arbre_D20']=collar

coupling=at(ring_y(25,10,20),y=120).fuse(at(ring_y(25,8,20),y=140))
for coupling_y in [120,140]:
    coupling=coupling.cut(at(cyl_z(2.5,14),y=coupling_y,z=24))
parts['M03_accouplement_flexible_20x16_gabarit']=coupling
parts['M04_vis_M5_accouplement']=screw_z_m5()
parts['R11_vis_M6_collier_arret']=screw_z_m6()

motor=at(box(128,94,70),y=154+47)
for x in [-48,48]:
    for z in [-25,25]:
        motor=motor.fuse(at(box(18,8,18),x=x,y=154,z=z))
        motor=motor.cut(at(cyl_y(4.25,14),x=x,y=154,z=z))
motor=motor.fuse(at(cyl_y(8,24),y=142))
parts['M01_motor_reducteur_gabarit_128x94x70']=motor

motor_plate=box(150,8,100)
motor_plate=at(motor_plate,y=151)
motor_plate=motor_plate.cut(at(cyl_y(27.5,12),y=151))
for x in [-48,48]:
    for z in [-25,25]:
        motor_plate=motor_plate.cut(at(cyl_y(4.25,12),x=x,y=151,z=z))
parts['M02_platine_moteur_percee_et_soudable']=motor_plate

left_rail=hollow_beam(1100,40)
right_rail=hollow_beam(1100,40)
for x in [-450,450]:
    left_rail=left_rail.cut(at(cyl_z(3.2,42),x=x))
    right_rail=right_rail.cut(at(cyl_z(3.2,42),x=x))
parts['C01_longeron_gauche_40x40x3']=left_rail
parts['C02_longeron_droit_40x40x3']=right_rail
for position,label in [(-530,'avant'),(0,'central'),(530,'arriere')]:
    beam=hollow_beam(40,360)
    if label=='central':
        for y in [-150,150]:
            beam=beam.cut(at(cyl_z(3.2,42),y=y))
    parts[f'C0{3+[-530,0,530].index(position)}_traverse_{label}_40x40x3']=beam

deck=box(970,420,3)
deck_fixings=[(-450,-200),(-450,200),(450,-200),(450,200),(0,-150),(0,150)]
for x,y in deck_fixings:
    deck=deck.cut(at(cyl_z(3.2,6),x=x,y=y))
parts['C06_plancher_3mm_perce_6xM6']=deck

parts['F01_vis_M8x30_hexagonale']=bolt_y_m8()
parts['F02_ecrou_M8']=nut_y_m8()
parts['F04_vis_M6x50_hexagonale']=bolt_z_m6()
parts['F05_ecrou_M6']=nut_z_m6()
parts['F06_rondelle_plate_M6']=washer_z_m6()

frame_and_deck_names=[
    'C01_longeron_gauche_40x40x3',
    'C02_longeron_droit_40x40x3',
    'C03_traverse_avant_40x40x3',
    'C04_traverse_central_40x40x3',
    'C05_traverse_arriere_40x40x3',
    'C06_plancher_3mm_perce_6xM6',
]
frame_and_deck_mass_kg=sum(parts[name].Volume() for name in frame_and_deck_names)*7.85e-6

PART_INFO={}
for name in parts:
    if name.startswith('R01'):
        info=('achete_a_remplacer_par_STEP_fabricant','Pneu caoutchouc industriel; reference et charge a choisir.','Elastomere')
    elif name.startswith('R04'):
        info=('achete_gabarit_standard','Roulement 6204, dimensions normalisees 20x47x14; fabricant non selectionne.','Acier de roulement')
    elif name.startswith('M01'):
        info=('achete_gabarit_non_dimensionne','Enveloppe indicative du motor reducteur; modele, arbre et puissance a selectionner.','Aluminium/acier selon fabricant')
    elif name.startswith('M03'):
        info=('achete_gabarit_non_dimensionne','Accouplement indicatif 20x16; type et couple admissible a valider.','Aluminium/acier selon fabricant')
    elif name.startswith(('F01','F02','F04','F05','F06')) or name.startswith('R07'):
        info=('achete_standard','Visserie ISO representative; classe, longueur et protection a valider.','Acier zingue a confirmer')
    elif name.startswith(('M04','R11')):
        info=('achete_standard','Vis de serrage representative; filetage et classe a confirmer.','Acier zingue a confirmer')
    elif name.startswith(('C01','C02','C03','C04','C05','C06')):
        info=('fabrique_localement','Profil creux acier S235 40x40x3 ou tôle acier 3 mm; soudage/perçages a confirmer.','Acier S235')
    elif name.startswith(('R02','R03','R05','R06','R07','R08','R09','R10','M02')):
        info=('fabrique_localement','Piece usinee/soudee a partir des interfaces indiquees; tolerances a valider.','Acier S235 ou aluminium a confirmer')
    else:
        info=('a_confirmer','Role et materiau a confirmer.','A confirmer')
    PART_INFO[name]={'supply_type':info[0],'role':info[1],'material':info[2]}

def placed(label,shape,color,x=0,y=0,z=0):
    return (label,at(shape,x,y,z),color)

def build_wheel_module():
    items=[
        placed('R01_pneu',parts['R01_pneu_bande_roulement'],COLORS['rubber']),
        placed('R02_jante',parts['R02_jante_avec_trous_M8_PCD80'],COLORS['aluminium']),
        placed('R03_moyeu',parts['R03_moyeu_a_bride_et_rainure_clavette'],COLORS['steel']),
        placed('R06_arbre',parts['R06_arbre_D20_avec_rainure_clavette'],COLORS['stainless']),
        placed('R08_clavette',parts['R08_clavette_6x6x30'],COLORS['steel'],y=9,z=10),
        placed('R09_support_paliers',parts['R09_support_double_paliers_siege_6204'],COLORS['frame'],y=59),
        placed('R04_6204_exterieur',parts['R04_roulement_6204_gabarit_20x47x14'],COLORS['stainless'],y=44),
        placed('R04_6204_interieur',parts['R04_roulement_6204_gabarit_20x47x14'],COLORS['stainless'],y=74),
        placed('R05_entretoise',parts['R05_entretoise_axiale'],COLORS['steel'],y=34),
        placed('R10_collier_exterieur',parts['R10_collier_arret_arbre_D20'],COLORS['steel'],y=29),
        placed('R10_collier_interieur',parts['R10_collier_arret_arbre_D20'],COLORS['steel'],y=88),
        placed('M03_accouplement',parts['M03_accouplement_flexible_20x16_gabarit'],COLORS['aluminium']),
        placed('M02_platine_moteur',parts['M02_platine_moteur_percee_et_soudable'],COLORS['frame'],y=151),
        placed('M01_motor_reducteur',parts['M01_motor_reducteur_gabarit_128x94x70'],COLORS['motor']),
    ]
    for index,angle in enumerate(bolt_angles,1):
        x=bolt_circle*math.cos(angle);z=bolt_circle*math.sin(angle)
        items.append(placed(f'F01_vis_jante_{index:02d}',parts['F01_vis_M8x30_hexagonale'],COLORS['fastener'],x=x,y=1,z=z))
        items.append(placed(f'R07_rondelle_jante_{index:02d}',parts['R07_rondelle_M8'],COLORS['fastener'],x=x,y=6.8,z=z))
        items.append(placed(f'F02_ecrou_jante_{index:02d}',parts['F02_ecrou_M8'],COLORS['fastener'],x=x,y=11.5,z=z))
    for index,(x,z) in enumerate([(x,z) for x in [-48,48] for z in [-25,25]],1):
        items.append(placed(f'F01_vis_moteur_{index:02d}',parts['F01_vis_M8x30_hexagonale'],COLORS['fastener'],x=x,y=162,z=z))
        items.append(placed(f'R07_rondelle_moteur_{index:02d}',parts['R07_rondelle_M8'],COLORS['fastener'],x=x,y=147.8,z=z))
        items.append(placed(f'F02_ecrou_moteur_{index:02d}',parts['F02_ecrou_M8'],COLORS['fastener'],x=x,y=173.5,z=z))
    for index,collar_y in enumerate([29,88],1):
        items.append(placed(f'R11_vis_collier_{index:02d}',parts['R11_vis_M6_collier_arret'],COLORS['fastener'],y=collar_y,z=11))
    for index,coupling_y in enumerate([120,140],1):
        items.append(placed(f'M04_vis_accouplement_{index:02d}',parts['M04_vis_M5_accouplement'],COLORS['fastener'],y=coupling_y,z=16))
    return items

wheel=build_wheel_module()
shaft_bounds=parts['R06_arbre_D20_avec_rainure_clavette'].BoundingBox()
motor_bounds=parts['M01_motor_reducteur_gabarit_128x94x70'].BoundingBox()
coupling_bounds=parts['M03_accouplement_flexible_20x16_gabarit'].BoundingBox()
assert abs(shaft_bounds.ymax-130)<1e-6
assert abs(motor_bounds.ymin-130)<1e-6
assert abs(coupling_bounds.ymin-110)<1e-6 and abs(coupling_bounds.ymax-150)<1e-6
write_assembly('A01_roue_assemblee',wheel)

explode_delta={
    'R01_':0,'R02_':110,'R03_':220,'F01_vis_jante':300,'F02_ecrou_jante':340,
    'R07_rondelle_jante':380,'R08_':450,'R06_':520,'R04_':650,'R09_':740,
    'R05_':820,'R10_':900,'M03_':1000,'M02_':1120,'M01_':1240,
    'F01_vis_moteur':1360,'F02_ecrou_moteur':1400,    'R07_rondelle_moteur':1440,
}
exploded=[]
for label,shape,color in wheel:
    delta=next((value for prefix,value in explode_delta.items() if label.startswith(prefix)),0)
    exploded.append((label,at(shape,y=delta),color))
write_assembly('A02_roue_eclatee',exploded)

frame=[
    ('C01_longeron_gauche',parts['C01_longeron_gauche_40x40x3'],COLORS['frame'],0,-200,155),
    ('C02_longeron_droit',parts['C02_longeron_droit_40x40x3'],COLORS['frame'],0,200,155),
    ('C03_traverse_avant',parts['C03_traverse_avant_40x40x3'],COLORS['frame'],-530,0,155),
    ('C04_traverse_centrale',parts['C04_traverse_central_40x40x3'],COLORS['frame'],0,0,155),
    ('C05_traverse_arriere',parts['C05_traverse_arriere_40x40x3'],COLORS['frame'],530,0,155),
]
base=[(label,at(shape,x,y,z),color) for label,shape,color,x,y,z in frame]
base.append(placed('C06_plancher',parts['C06_plancher_3mm_perce_6xM6'],COLORS['deck'],z=176.5))
for index,(x,y) in enumerate(deck_fixings,1):
    base.append(placed(f'F04_vis_plancher_{index:02d}',parts['F04_vis_M6x50_hexagonale'],COLORS['fastener'],x=x,y=y,z=154.6))
    base.append(placed(f'F05_ecrou_plancher_{index:02d}',parts['F05_ecrou_M6'],COLORS['fastener'],x=x,y=y,z=132.5))
    base.append(placed(f'F06_rondelle_plancher_{index:02d}',parts['F06_rondelle_plate_M6'],COLORS['fastener'],x=x,y=y,z=178.8))
for side in [-1,1]:
    side_id='G' if side<0 else 'D'
    for label,shape,color in wheel:
        installed=shape if side==-1 else shape.mirror('XZ')
        base.append((f'{side_id}_{label}',at(installed,y=side*WHEEL_CENTRES/2,z=100),color))
write_assembly('A03_roues_sur_chassis',base)

interfaces={
    'status':'Concept; positions/interfaces explicites, assemblages STEP composes de solides sans contraintes cinematiques.',
    'units':'mm',
    'design_load':{'payload_kg':160,'empty_robot_target_max_kg':MAX_EMPTY_MASS,'gross_mass_target_kg':GROSS_MASS_TARGET,
                   'structural_validation':'NOT_DONE'},
    'connections':[
        {'id':'rim_to_hub','components':['R02_jante','R03_moyeu'],'type':'6x M8x30, ecrous et rondelles','pattern':'PCD 80 mm, 60 degres','holes':'D8.5 mm traversants dans la jante et la bride'},
        {'id':'hub_to_axle','components':['R03_moyeu','R06_arbre','R08_clavette'],'type':'arbre D20 avec clavette parallele 6x6x30','fit':'jeu/serrage a calculer; rainures a valider'},
        {'id':'axle_support','components':['R04_roulement_6204_gabarit_20x47x14','R09_support_double_paliers_siege_6204'],'type':'2 roulements 6204, alesages de logement D47','retention':'montage ajuste provisoire; epaulements/circlips a finaliser'},
        {'id':'bearing_support_to_frame','components':['R09_support_double_paliers_siege_6204','C01_longeron_gauche_40x40x3','C02_longeron_droit_40x40x3'],'type':'soudure du support sur le longeron, cordon a dimensionner'},
        {'id':'motor_to_plate','components':['M01_motor_reducteur_gabarit_128x94x70','M02_platine_moteur_percee_et_soudable'],'type':'4x M8, entraxe provisoire 96x50 mm'},
        {'id':'motor_to_axle','components':['M01_motor_reducteur_gabarit_128x94x70','M03_accouplement_flexible_20x16_gabarit','R06_arbre_D20_avec_rainure_clavette'],'type':'accouplement indicatif 20x16 mm; couple et longueur d arbre a verifier'},
        {'id':'motor_plate_to_crossmember','components':['M02_platine_moteur_percee_et_soudable','C04_traverse_central_40x40x3'],'type':'soudure; cordons et renforts a dimensionner'},
        {'id':        'deck_to_frame','components':['C06_plancher_3mm_perce_6xM6','C01_longeron_gauche_40x40x3','C02_longeron_droit_40x40x3','C04_traverse_central_40x40x3'],'type':'6x M6, rondelles et ecrous, trous alignes dans la tole et les profils'},
        {'id':'frame_welds','components':['C01_longeron_gauche_40x40x3','C02_longeron_droit_40x40x3','C03_traverse_avant_40x40x3','C04_traverse_central_40x40x3','C05_traverse_arriere_40x40x3'],'type':'assemblage soude; cordons et procedure a valider'},
    ],
}
(ROOT/'interfaces_assemblage.json').write_text(json.dumps(interfaces,ensure_ascii=False,indent=2),encoding='utf-8')

def robot_quantity(name):
    if name.startswith(('C01','C02','C03','C04','C05','C06')):
        return 1
    quantities={
        'R01':2,'R02':2,'R03':2,'R04':4,'R05':2,'R06':2,'R07':20,'R08':2,
        'R09':2,'R10':4,'R11':4,'M01':2,'M02':2,'M03':2,'M04':4,
        'F01':20,'F02':20,'F04':6,'F05':6,'F06':6,
    }
    return next((quantity for prefix,quantity in quantities.items() if name.startswith(prefix)),0)

catalog={
    'title':'BFM AGV - CAO conceptuelle du module de roue motrice',
    'units':'mm',
    'wheel':{'outer_diameter':WHEEL_OD,'width':WHEEL_WIDTH,'track_between_wheel_centres':WHEEL_CENTRES},
    'mass_targets':{
        'empty_robot_max_kg':MAX_EMPTY_MASS,
        'payload_kg':160,
        'gross_robot_kg':GROSS_MASS_TARGET,
        'interpretation':'230 kg est la masse brute minimale avec 160 kg de charge et 70 kg a vide. La masse reelle peut etre superieure.',
        'mass_budget_kg':{'chassis_plancher_supports':25,'roues_motorisation':18,
                         'roues_porteuses_suspension':5,'coffre_et_4_tiroirs':15,
                         'batterie_electronique_cablage':7},
        'mass_budget_status':'PROVISIONAL_NOT_MEASURED',
        'frame_and_deck_geometry_estimate_kg':round(frame_and_deck_mass_kg,2),
        'remaining_mass_under_70kg_cap_kg':round(MAX_EMPTY_MASS-frame_and_deck_mass_kg,2),
        'mass_estimate_basis':'Steel S235 density 7850 kg/m3 applied to the generated solid volume; excludes supports, wheel modules, fasteners, cabinet, drawers, battery and electronics.',
        'structural_validation':'NOT_DONE'
    },
    'parts':[{'name':name,'quantity_per_robot':robot_quantity(name),**PART_INFO[name]} for name in parts],
    'assemblies':['A01_roue_assemblee','A02_roue_eclatee','A03_roues_sur_chassis'],
    'interfaces_file':'interfaces_assemblage.json',
    'limitations':['Les references industrielles ne sont pas selectionnees; les gabarits ne sont pas des STEP fabricants.',
                   'La puissance moteur, les charges roulement/arbre, les soudures et le seuil de 70 kg restent a valider.']
}
(ROOT/'nomenclature.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')

for name,shape in parts.items():
    cq.exporters.export(shape,str(PART/(name+'.step')))
    cq.exporters.export(shape,str(STL/(name+'.stl')),tolerance=.12,angularTolerance=.15)

invalid=[name for name,shape in parts.items() if not shape.isValid()]
assert not invalid,invalid
assert len(parts)==26
assert len(wheel)==48
assert len(base)==120
assert WHEEL_CENTRES+WHEEL_WIDTH==570
checks={
    'individual_parts_valid':len(parts),
    'wheel_assembly_components':len(wheel),
    'chassis_assembly_components':len(base),
    'rim_bolts_each_wheel':6,
    'motor_mount_bolts_each_wheel':4,
    'deck_bolts':len(deck_fixings),
    'wheel_centres_mm':WHEEL_CENTRES,
    'outer_width_mm':WHEEL_CENTRES+WHEEL_WIDTH,
    'gross_mass_target_kg':GROSS_MASS_TARGET,
    'empty_mass_cap_kg':MAX_EMPTY_MASS,
    'frame_and_deck_geometry_estimate_kg':round(frame_and_deck_mass_kg,2),
    'mass_budget_status':'PROVISIONAL_NOT_MEASURED',
    'geometry_validation':'PASS',
    'load_validation':'NOT_DONE',
}
(ROOT/'validation_cao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

print(json.dumps({'pieces':len(parts),'assemblages':3,'fixations_jante':18,'fixations_moteur':12,
                  'fixations_plancher':18,'gross_mass_target_kg':GROSS_MASS_TARGET,
                  'outputs':str(ROOT)},ensure_ascii=False,indent=2))
