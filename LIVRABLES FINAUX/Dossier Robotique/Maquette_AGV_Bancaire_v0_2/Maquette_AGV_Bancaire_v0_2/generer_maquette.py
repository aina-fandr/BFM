"""Maquette AGV bancaire : géométrie paramétrique, GLB, SDF et visualiseur hors ligne.
Python 3 + numpy + Pillow. Aucune ressource 3D distante.
"""
from pathlib import Path
import json, math, struct, copy, hashlib, re, xml.etree.ElementTree as ET
import numpy as np

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
MODEL=ROOT/'modeles'
MODEL.mkdir(exist_ok=True)
plan=json.loads((DATA/'geometrie_plan_retenu.json').read_text(encoding='utf-8'))
P={'version':'0.2','date':'2026-10-21','wall_height_m':2.40,
   'door_clear_height_m':2.10,'slab_thickness_m':0.12,'floor_elevation_m':3.0,
   'cargo_enclosure_m':[1.0,0.5,0.75],'trial_robot_footprint_m':[1.1,0.7],
   'robot_total_height_hypothesis_m':1.12,'reception_height_hypothesis_m':0.45,
   'robot_payload_mass_kg':160,'robot_compartment_count':4,
   'robot_compartment_payload_kg':40,'robot_compartment_clear_m':[0.46,0.44,0.30],
   'robot_drawer_extension_hypothesis_m':0.35,
   'stage':'Avant-projet mécanique conceptuel. Quatre tiroirs indépendants, non validés.',
   'hypotheses':'Dimensions des sacs, structure, roues, tiroirs, stabilité, motorisation et interfaces de transfert à valider. Le modèle montre quatre compartiments à 40 kg nominaux chacun; le déchargement assisté reste un concept.'}
settings=DATA/'parametres_3d.json'
if settings.exists():P.update(json.loads(settings.read_text(encoding='utf-8')))
else:settings.write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf-8')
UP=float(P['floor_elevation_m'])
assert UP>P['wall_height_m']>P['door_clear_height_m']>0

COL={'wall':'#CED9E4','walltop':'#9BAEC0','floor':'#EDF2F6','slab':'#A8BBCD',
     'wood':'#B99B73','desk':'#EEF1F3','metal':'#586A7B','door':'#279E8D',
     'lift':'#9D8CC5','liftfloor':'#D6CEE8','route':'#216BDD',
     'return':'#8F65BB','robot':'#203A55','drawer':'#DDE7F0','accent':'#31A4E7',
     'C1':'#57B88F','C2':'#5C91DE','C3':'#AC80CA'}
ROBOT_COL={'frame':'#596469','shell':'#394348','panel':'#C2C9CA',
           'steel':'#A7B0B1','steel_dark':'#4A5458','rubber':'#202427',
           'handle':'#697276','gasket':'#252B2D','accent':'#168F90',
           'display':'#16383B','screen':'#23A79C','safety_yellow':'#E4B126',
           'safety_red':'#C72F26','label':'#30393D','label_ink':'#E9ECEB',
           'vent':'#4D585C'}

scene=[]
def box(name,level,kind,center,size,color,collision=True,yaw=0,mesh='box',status='H'):
    d={'name':name,'level':level,'kind':kind,'center':[round(float(x),6) for x in center],
       'size':[round(float(x),6) for x in size],'color':color,'collision':collision,
       'yaw':yaw,'mesh':mesh,'dimension_status':status}
    assert all(s>0 for s in d['size']),name
    scene.append(d);return d
def rectbox(name,level,kind,r,z,h,color,collision=True,status='H'):
    x0,y0,x1,y1=r
    return box(name,level,kind,[(x0+x1)/2,(y0+y1)/2,z+h/2],[x1-x0,y1-y0,h],color,collision,status=status)
def door(name,level,r,z,axis):
    # Clear opening dimensions match the retained plan. Frame and lintel lie
    # outside the clear opening; sliding leaf is parked behind the wall face.
    x0,y0,x1,y1=r; hd=P['door_clear_height_m'];hw=P['wall_height_m']
    rectbox(name+'_linteau',level,'lintel',r,z+hd,hw-hd,COL['wall'])
    if axis=='x':
        for x in (x0-.025,x1):rectbox(name+'_montant_'+str(x),level,'doorframe',[x,y0,x+.025,y1],z,hd,COL['door'],False)
        rectbox(name+'_rail',level,'doorframe',[x0,y0,x1,y1],z+hd-.035,.035,COL['door'],False)
        half=(x1-x0)/2
        for k,(a,b) in enumerate([(x0-half-.02,x0-.02),(x1+.02,x1+half+.02)]):
            rectbox(name+'_vantail_ouvert_'+str(k),level,'doorleaf',[a,(y0+y1)/2-.018,b,(y0+y1)/2+.018],z,hd-.07,COL['door'],False)
    else:
        for y in (y0-.025,y1):rectbox(name+'_montant_'+str(y),level,'doorframe',[x0,y,x1,y+.025],z,hd,COL['door'],False)
        rectbox(name+'_rail',level,'doorframe',r,z+hd-.035,.035,COL['door'],False)
        half=(y1-y0)/2
        for k,(a,b) in enumerate([(y0-half-.02,y0-.02),(y1+.02,y1+half+.02)]):
            rectbox(name+'_vantail_ouvert_'+str(k),level,'doorleaf',[(x0+x1)/2-.018,a,(x0+x1)/2+.018,b],z,hd-.07,COL['door'],False)
def strip(name,level,a,b,z,color):
    dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
    if length<1e-7:return
    box(name,level,'route',[(a[0]+b[0])/2,(a[1]+b[1])/2,z+.018],[length,.055,.018],color,False,math.atan2(dy,dx),status='D/H')
    if length>.6:
        mid=[a[0]+.57*dx,a[1]+.57*dy,z+.032]
        box(name+'_fleche',level,'route',mid,[.30,.18,.016],color,False,math.atan2(dy,dx),mesh='arrow',status='D/H')

shaft_rect=plan['levels']['N?']['walkable_rectangles'][-1]
for level,key,z in [('N1','N?',UP),('RDC','RDC',0.)]:
    source=plan['levels'][key]
    for i,r in enumerate(source['walkable_rectangles']):
        if r==shaft_rect:continue
        rectbox(f'{level}_dalle_{i:02d}',level,'floor',r,z-P['slab_thickness_m'],P['slab_thickness_m'],COL['floor'],True,'D/H')
    for i,o in enumerate(source['wall_rectangles']):
        rectbox(f'{level}_mur_{i:02d}',level,'wall',o['rect'],z,P['wall_height_m'],COL['wall'])
    path=source['route_xy']
    for i,(a,b) in enumerate(zip(path,path[1:])):strip(f'{level}_parcours_{i:02d}',level,a,b,z,COL['route'])
    door(f'{level}_ascenseur',level,[-5.72,-.25,-4.52,-.10],z,'x')
    # Cab floor is present in each isolated level view. Only the upper cab is
    # retained in combined exports: one physical cab, no duplicate lift vehicle.
    rectbox(f'{level}_cabine_plancher',level,'cabin',shaft_rect,z-.09,.09,COL['liftfloor'])
    for i,r in enumerate([[-6.20,-.08,-6.16,2.08],[-4.08,-.08,-4.04,2.08],[-6.16,2.04,-4.08,2.08]]):
        rectbox(f'{level}_cabine_paroi_{i}',level,'cabinwall',r,z,2.15,COL['lift'])

for i,obj in enumerate(plan['levels']['N?']['furniture_rectangles']):
    r=obj['rect'];x0,y0,x1,y1=r
    if 'comptoir' in obj['name']:
        rectbox('N1_comptoir_base','N1','furniture',[x0+.06,y0+.03,x1-.06,y1-.03],UP,.95,COL['metal'])
        rectbox('N1_comptoir_plateau','N1','furniture',r,UP+.95,.055,COL['wood'])
    else:
        rectbox(f'N1_bureau_{i+1}_plateau','N1','furniture',r,UP+.72,.06,COL['wood'])
        for j,(x,y) in enumerate([(x0+.06,y0+.06),(x1-.12,y0+.06),(x0+.06,y1-.12),(x1-.12,y1-.12)]):
            rectbox(f'N1_bureau_{i+1}_pied_{j}','N1','furniture',[x,y,x+.06,y+.06],UP,.72,COL['metal'])

door('N1_P0_sortie','N1',[.28,-.15,1.48,0],UP,'x')
door('N1_PB_piece_B','N1',[2.28,3,3.48,3.12],UP,'x')
door('N1_PC_piece_A','N1',[3.88,1.4,4,2.6],UP,'y')
door('RDC_P1_entree_hall','RDC',[6.73,4.2,6.88,5.4],0,'y')
for i,y in enumerate([4.8,7.92,11.54],1):door(f'RDC_depot_{i}','RDC',[9.88,y-.6,10,y+.6],0,'y')

for i,obj in enumerate(plan['levels']['RDC']['reception_rectangles'],1):
    r=obj['rect'];x0,y0,x1,y1=r
    rectbox(f'RDC_reception_C{i}_base','RDC','reception',r,0,.45,COL['C'+str(i)])
    rectbox(f'RDC_reception_C{i}_plateau','RDC','reception',[x0+.04,y0+.04,x1-.04,y1-.04],.45,.04,'#DCE6EC')
for i,(a,b) in enumerate(zip(plan['levels']['RDC']['exit_to_wait_route_xy'],plan['levels']['RDC']['exit_to_wait_route_xy'][1:])):
    strip(f'RDC_retour_attente_{i}','RDC',a,b,0,COL['return'])
rectbox('RDC_emplacement_attente','RDC','marking',[7.3,9.7,8.3,11.1],.002,.008,'#DFD1EC',False)

# Structural connections at the lift use the very same shaft x/y as the plan.
for i,r in enumerate([[-6.37,-.25,-6.22,2.25],[-4.02,-.25,-3.87,2.25],[-6.22,2.1,-4.02,2.25]]):
    rectbox(f'liaison_gaine_{i}','COMMON','shaft',r,P['wall_height_m'],UP-P['wall_height_m'],COL['lift'])
rectbox('fond_gaine','COMMON','shaft',shaft_rect,-.15,.06,COL['slab'])

# Mechanical concept: a low chassis carries a 1 x .5 x .75 m cabinet with
# four separately latched drawers in a 2 x 2 arrangement.
robot=[]
def rb(name,c,s,col,mesh='box',assembly='chassis'):
    if mesh=='box':mesh='rounded_box'
    robot.append({'name':name,'center':c,'size':s,'color':col,'mesh':mesh,'assembly':assembly})
case_x,case_y,case_h=P['cargo_enclosure_m']
chassis_x,chassis_y=P['trial_robot_footprint_m']
chassis_h=.30
case_bottom=chassis_h+.02
case_top=case_bottom+case_h
panel=.02
wheel_z=.11
rb('plaque_superieure_chassis',[0,0,.205],[chassis_x-.08,chassis_y-.08,.018],ROBOT_COL['frame'],'box','chassis')
for side,y in [('gauche',-chassis_y/2+.055),('droite',chassis_y/2-.055)]:
    rb('longeron_'+side,[0,y,.105],[chassis_x-.07,.055,.075],ROBOT_COL['shell'],'box','chassis')
for i,x in enumerate([-.48,-.16,.16,.48]):
    rb(f'traverse_chassis_{i+1}',[x,0,.105],[.055,chassis_y-.12,.075],ROBOT_COL['shell'],'box','chassis')
for side,y in [('gauche',-chassis_y/2+.045),('droite',chassis_y/2-.045)]:
    rb('moteur_reducteur_'+side,[0,y*.72,wheel_z],[.16,.12,.12],ROBOT_COL['steel_dark'],'box','roues')
    rb('roue_motrice_'+side,[0,y,wheel_z],[.22,.075,.22],ROBOT_COL['rubber'],'tire','roues')
    rb('moyeu_moteur_'+side,[0,y,wheel_z],[.105,.078,.105],ROBOT_COL['steel'],'cylinder','roues')
    face_y=y+(-1 if y<0 else 1)*.043
    for lug in range(6):
        angle=math.tau*lug/6
        rb(f'ecrou_roue_{side}_{lug+1}',
           [.041*math.cos(angle),face_y,wheel_z+.041*math.sin(angle)],
           [.012,.008,.012],ROBOT_COL['steel_dark'],'cylinder','roues')
for axle,x in [('avant',.43),('arriere',-.43)]:
    rb('support_roulette_'+axle,[x,0,.17],[.105,.105,.08],ROBOT_COL['steel_dark'],'box','roues')
    rb('roulette_pivotante_'+axle,[x,0,.075],[.14,.06,.14],ROBOT_COL['rubber'],'tire','roues')
    rb('axe_roulette_'+axle,[x,0,.075],[.05,.07,.05],ROBOT_COL['steel'],'cylinder','roues')
    for side,y in [('gauche',-.040),('droite',.040)]:
        rb(f'fourche_roulette_{axle}_{side}',[x-.012,y,.108],[.075,.012,.075],ROBOT_COL['steel_dark'],'box','roues')
        rb(f'vis_axe_roulette_{axle}_{side}',[x,y+(-.006 if y<0 else .006),.075],
           [.018,.012,.018],ROBOT_COL['steel'],'cylinder','roues')
rb('pare_chocs_avant',[0,-chassis_y/2+.005,.14],[chassis_x-.14,.035,.075],ROBOT_COL['steel_dark'],'box','chassis')
rb('pare_chocs_arriere',[0,chassis_y/2-.005,.14],[chassis_x-.14,.035,.075],ROBOT_COL['steel_dark'],'box','chassis')
rb('support_batterie',[0,.015,.227],[.43,.31,.025],ROBOT_COL['steel_dark'],'box','batterie')
rb('batterie_format_a_definir',[0,.015,.27],[.36,.25,.07],ROBOT_COL['shell'],'box','batterie')
rb('coffret_controleur_hypothese',[.27,.17,.255],[.17,.16,.075],ROBOT_COL['shell'],'box','commandes')
rb('support_coffret_controleur',[.27,.17,.205],[.20,.19,.018],ROBOT_COL['steel_dark'],'box','commandes')
case_mid=case_bottom+case_h/2
rb('fond_coffre',[0,0,case_bottom+panel/2],[case_x-2*panel,case_y-2*panel,panel],ROBOT_COL['frame'],'box','coffre')
rb('paroi_arriere',[0,case_y/2-panel/2,case_mid],[case_x,panel,case_h],ROBOT_COL['shell'],'box','coffre')
for x in [-case_x/2+panel/2,case_x/2-panel/2]:
    rb('paroi_laterale_'+str(x),[x,0,case_mid],[panel,case_y-2*panel,case_h],ROBOT_COL['shell'],'box','coffre')
rb('toit_coffre',[0,0,case_top-panel/2],[case_x,case_y,panel],ROBOT_COL['shell'],'box','toit')
rb('separateur_horizontal',[0,0,case_mid],[case_x-2*panel,case_y-2*panel,panel],ROBOT_COL['frame'],'box','separateurs')
rb('separateur_vertical',[0,0,case_mid],[panel,case_y-2*panel,case_h-2*panel],ROBOT_COL['frame'],'box','separateurs')
for x in [-case_x/2+panel/2,0,case_x/2-panel/2]:
    rb(f'montant_face_{x:.2f}',[x,-case_y/2+panel/2,case_mid],[panel,panel,case_h],ROBOT_COL['frame'],'box','coffre')
for z in [case_bottom+panel/2,case_mid,case_top-panel/2]:
    rb(f'traverse_face_{z:.2f}',[0,-case_y/2+panel/2,z],[case_x-2*panel,panel,panel],ROBOT_COL['frame'],'box','coffre')
drawer_x=(case_x-3*panel)/2
drawer_z=(case_h-3*panel)/2
for row,z in enumerate([case_bottom+2*panel+drawer_z+drawer_z/2,case_bottom+panel+drawer_z/2]):
    for column,x in enumerate([-case_x/4,case_x/4]):
        n=column+1+2*row
        assembly=f'tiroir_S{n}'
        tray_depth=case_y-panel*2-.02
        tray_height=drawer_z-.015
        rb(f'S{n}_fond_tiroir',[x,-.035,z-tray_height*.45],[drawer_x-.01,tray_depth-.02,.014],ROBOT_COL['frame'],'box',assembly)
        for side,dx in [('gauche',-1),('droite',1)]:
            rb(f'S{n}_flanc_{side}',[x+dx*(drawer_x/2-.012),-.035,z],[.014,tray_depth,tray_height*.88],ROBOT_COL['frame'],'box',assembly)
            rb(f'S{n}_glissiere_fixe_{side}',[x+dx*drawer_x*.53,.015,z-drawer_z*.38],[.018,.34,.024],ROBOT_COL['steel'],'box','glissieres')
            rb(f'S{n}_glissiere_mobile_{side}',[x+dx*drawer_x*.40,-.045,z-drawer_z*.38],[.014,.32,.018],ROBOT_COL['steel'],'box',assembly)
        rb(f'S{n}_fond_arriere',[x,case_y/2-panel-.015,z],[drawer_x-.02,.014,tray_height*.88],ROBOT_COL['frame'],'box',assembly)
        front_y=-case_y/2-panel/2
        rb(f'S{n}_joint_peripherique',[x,front_y+.010,z],[drawer_x+.004,.006,drawer_z-.008],ROBOT_COL['gasket'],'box',assembly)
        rb(f'S{n}_facade',[x,front_y,z],[drawer_x-.01,panel*.8,drawer_z-.015],ROBOT_COL['panel'],'box',assembly)
        rb(f'S{n}_poignee',[x,front_y-panel*.64,z+drawer_z*.20],[.13,.022,.025],ROBOT_COL['handle'],'box',assembly)
        for handle_side in [-1,1]:
            rb(f'S{n}_support_poignee_{handle_side}',
               [x+handle_side*.052,front_y-panel*.51,z+drawer_z*.20],
               [.014,.013,.024],ROBOT_COL['steel_dark'],'box',assembly)
        rb(f'S{n}_plaque_identification',
           [x-drawer_x*.32,front_y-panel*.64,z+drawer_z*.24],
           [.078,.004,.045],ROBOT_COL['label'],'box',assembly)
        glyph_y=front_y-panel*.64-.003
        glyph_x=x-drawer_x*.32
        glyph_z=z+drawer_z*.24
        segment_w=.013
        segment_h=.013
        segment_thickness=.0022
        glyphs={'S':['a','f','g','c','d'],'1':['b','c'],
                '2':['a','b','g','e','d'],'3':['a','b','g','c','d'],
                '4':['f','g','b','c']}
        for character_index,character in enumerate('S'+str(n)):
            gx=glyph_x+(-.012 if character_index==0 else .012)
            segments=glyphs[character]
            for segment in segments:
                if segment in ['a','g','d']:
                    offset_x=0
                    offset_z={'a':.015,'g':0,'d':-.015}[segment]
                    segment_size=[segment_w,.002,segment_thickness]
                else:
                    offset_x=-.006 if segment in ['f','e'] else .006
                    offset_z=.0075 if segment in ['f','b'] else -.0075
                    segment_size=[segment_thickness,.002,segment_h]
                rb(f'S{n}_marquage_{character_index}_{segment}',
                   [gx+offset_x,glyph_y,glyph_z+offset_z],
                   segment_size,ROBOT_COL['label_ink'],'box',assembly)
        rb(f'S{n}_loquet',[x+drawer_x*.32,front_y-panel*.62,z+drawer_z*.20],[.032,.018,.032],ROBOT_COL['accent'],'box',assembly)
        rb(f'S{n}_actionneur_corps',[x,.13,z-drawer_z*.27],[.045,.20,.045],ROBOT_COL['steel_dark'],'box',assembly)
        rb(f'S{n}_actionneur_tige',[x,-.01,z-drawer_z*.27],[.018,.11,.018],ROBOT_COL['steel'],'box',assembly)
        for rail_x in [x-drawer_x*.38,x+drawer_x*.38]:
            rb(f'S{n}_butée_{rail_x:.3f}',[rail_x,case_y/2-panel-.025,z-drawer_z*.38],[.025,.035,.045],ROBOT_COL['safety_yellow'],'box',assembly)
        for dx in [-1,1]:
            for dz in [-1,1]:
                rb(f'S{n}_vis_face_{dx}_{dz}',[x+dx*(drawer_x/2-.045),-case_y/2-panel*.92,z+dz*(drawer_z/2-.045)],[.012,.008,.012],ROBOT_COL['steel'],'cylinder',assembly)
rb('grille_ventilation_fond',[case_x/2+.003,.055,case_mid],[.008,.19,.20],ROBOT_COL['vent'],'box','coffre')
for slot in range(7):
    rb(f'ailette_grille_ventilation_{slot+1}',
       [case_x/2+.008,.055,case_mid-.075+slot*.025],
       [.004,.155,.006],ROBOT_COL['steel_dark'],'box','coffre')
rb('support_afficheur',[case_x/2+.003,-.12,case_mid+.015],[.018,.22,.14],ROBOT_COL['steel_dark'],'box','commandes')
rb('ecran_commande',[case_x/2+.014,-.12,case_mid+.015],[.006,.17,.095],ROBOT_COL['display'],'box','commandes')
for row in range(3):
    rb(f'ecran_indicateur_{row+1}',
       [case_x/2+.018,-.165,case_mid+.040-row*.025],
       [.003,.058,.004],ROBOT_COL['screen'],'box','commandes')
rb('support_arret_urgence',[case_x/2-.06,.08,case_top+.01],[.075,.075,.02],ROBOT_COL['safety_yellow'],'box','commandes')
rb('arret_urgence_rouge',[case_x/2-.06,.08,case_top+.0325],[.05,.05,.035],ROBOT_COL['safety_red'],'cylinder_z','commandes')
rb('capteur_emplacement_avant',[0,-chassis_y/2-.012,.15],[.06,.025,.035],ROBOT_COL['display'],'box','commandes')
for i,r in enumerate(robot):
    yaw=-math.pi/2;c=math.cos(yaw);s=math.sin(yaw);x,y,z=r['center']
    box('AGV_'+r['name'],'ROBOT','robot',[5+x*c-y*s,4.8+x*s+y*c,UP+z],r['size'],r['color'],True,yaw,r['mesh'])

labels=[
 {'level':'N1','p':[5.7,4.55,UP+.04],'text':'COLLECTE · 8 × 6 m','color':'#1764D5'},
 {'level':'N1','p':[6,1.55,UP+.04],'text':'PIÈCE A · 4 × 3 m'},
 {'level':'N1','p':[2.88,1.55,UP+.04],'text':'PIÈCE B · H'},
 {'level':'N1','p':[-5.12,1,UP+.12],'text':'ASCENSEUR A','color':'#7755B7'},
 {'level':'RDC','p':[12,4.8,.04],'text':'DÉPÔT 1 · REPLI'},
 {'level':'RDC','p':[12,7.92,.04],'text':'DÉPÔT 2'},
 {'level':'RDC','p':[12,10.5,.04],'text':'DÉPÔT 3 · PRIORITAIRE','color':'#1764D5'},
 {'level':'RDC','p':[-5.12,1,.12],'text':'ASCENSEUR A','color':'#7755B7'},
 {'level':'RDC','p':[7.8,10.4,.035],'text':'ATTENTE','color':'#7755B7'},
]+[{'level':'RDC','p':[sum(o['rect'][::2])/2,13.04,.53],'text':'C'+str(i+1),'color':'#1764D5'} for i,o in enumerate(plan['levels']['RDC']['reception_rectangles'])]
payload={'meta':P,'objects':scene,'labels':labels,'plan':plan,
         'notes':['Le robot représente quatre tiroirs indépendants en disposition 2 × 2, à 40 kg nominaux par compartiment.',
                  'Les dimensions intérieures des tiroirs, la structure, les charges et les mécanismes sont des hypothèses à valider.',
                  'Les valeurs 2,40 m (murs), 2,10 m (portes) et +3,00 m (niveau de départ) sont des hypothèses.',
                  'Le modèle est statique : navigation, ascenseur motorisé et transfert des sacs seront intégrés ensuite.']}
(DATA/'scene_3d.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')

def mesh_box():
    vs=[]; ns=[]; ids=[]
    faces=[([1,0,0],[(.5,-.5,-.5),(.5,.5,-.5),(.5,.5,.5),(.5,-.5,.5)]),
           ([-1,0,0],[(-.5,.5,-.5),(-.5,-.5,-.5),(-.5,-.5,.5),(-.5,.5,.5)]),
           ([0,1,0],[(.5,.5,-.5),(-.5,.5,-.5),(-.5,.5,.5),(.5,.5,.5)]),
           ([0,-1,0],[(-.5,-.5,-.5),(.5,-.5,-.5),(.5,-.5,.5),(-.5,-.5,.5)]),
           ([0,0,1],[(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)]),
           ([0,0,-1],[(-.5,.5,-.5),(.5,.5,-.5),(.5,-.5,-.5),(-.5,-.5,-.5)])]
    for normal,pts in faces:
        i=len(vs);vs+=pts;ns+=[normal]*4;ids += [i,i+1,i+2,i,i+2,i+3]
    return np.array(vs,dtype='<f4'),np.array(ns,dtype='<f4'),np.array(ids,dtype='<u2')
def mesh_rounded_box(segments=6,bevel=.04):
    vs=[];ns=[];ids=[]
    faces=[[(.5,-.5,-.5),(.5,.5,-.5),(.5,.5,.5),(.5,-.5,.5)],
           [(-.5,.5,-.5),(-.5,-.5,-.5),(-.5,-.5,.5),(-.5,.5,.5)],
           [(.5,.5,-.5),(-.5,.5,-.5),(-.5,.5,.5),(.5,.5,.5)],
           [(-.5,-.5,-.5),(.5,-.5,-.5),(.5,-.5,.5),(-.5,-.5,.5)],
           [(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)],
           [(-.5,.5,-.5),(.5,.5,-.5),(.5,-.5,-.5),(-.5,-.5,-.5)]]
    for corners in faces:
        grid=[]
        for row in range(segments+1):
            v=row/segments
            for col in range(segments+1):
                u=col/segments
                p=np.array(corners[0])*(1-u)*(1-v)+np.array(corners[1])*u*(1-v)+np.array(corners[2])*u*v+np.array(corners[3])*(1-u)*v
                inner=np.clip(p,-.5+bevel,.5-bevel)
                delta=p-inner;length=np.linalg.norm(delta)
                normal=delta/max(length,1e-12)
                point=inner+bevel*normal
                grid.append((point,normal))
        base=len(vs)
        for point,normal in grid:
            vs.append(point.tolist());ns.append(normal.tolist())
        for row in range(segments):
            for col in range(segments):
                a=base+row*(segments+1)+col;b=a+1
                d=base+(row+1)*(segments+1)+col;c=d+1
                ids.extend([a,b,c,a,c,d])
    return np.array(vs,dtype='<f4'),np.array(ns,dtype='<f4'),np.array(ids,dtype='<u2')
def mesh_cylinder(N=48):
    v=[];n=[];ids=[]
    for k in range(N):
        a=k*math.tau/N;b=(k+1)*math.tau/N
        i=len(v)
        for y,t in [(-.5,a),(.5,a),(.5,b),(-.5,b)]:v.append([.5*math.cos(t),y,.5*math.sin(t)]);n.append([math.cos(t),0,math.sin(t)])
        ids.extend([i,i+1,i+2,i,i+2,i+3])
        for y,sgn in [(-.5,-1),(.5,1)]:
            i=len(v);pts=[[0,y,0],[.5*math.cos(a),y,.5*math.sin(a)],[.5*math.cos(b),y,.5*math.sin(b)]]
            if sgn>0:pts=[pts[0],pts[2],pts[1]]
            v+=pts;n += [[0,sgn,0]]*3;ids += [i,i+1,i+2]
    return np.array(v,dtype='<f4'),np.array(n,dtype='<f4'),np.array(ids,dtype='<u2')
def mesh_cylinder_z(N=48):
    v,n,ids=mesh_cylinder(N)
    rotation=np.array([[1,0,0],[0,0,-1],[0,1,0]],dtype='<f4')
    return v@rotation.T,n@rotation.T,ids
def mesh_tire(N=64):
    profile=[(-.50,.39),(-.44,.46),(-.35,.49),(-.27,.50),(-.22,.485),
             (-.15,.50),(-.08,.485),(0,.50),(.08,.485),(.15,.50),
             (.22,.485),(.27,.50),(.35,.49),(.44,.46),(.50,.39)]
    vs=[];ns=[];ids=[]
    def triangle(a,b,c):
        normal=np.cross(b-a,c-a);length=np.linalg.norm(normal)
        normal=normal/max(length,1e-12)
        first=len(vs);vs.extend([a.tolist(),b.tolist(),c.tolist()])
        ns.extend([normal.tolist()]*3);ids.extend([first,first+1,first+2])
    rings=[]
    for y,radius in profile:
        rings.append([np.array([radius*math.cos(math.tau*j/N),y,radius*math.sin(math.tau*j/N)]) for j in range(N)])
    for row in range(len(profile)-1):
        for col in range(N):
            next_col=(col+1)%N
            a=rings[row][col];b=rings[row+1][col]
            c=rings[row+1][next_col];d=rings[row][next_col]
            triangle(a,b,c);triangle(a,c,d)
    center_low=np.array([0,profile[0][0],0])
    center_high=np.array([0,profile[-1][0],0])
    for col in range(N):
        next_col=(col+1)%N
        triangle(center_low,rings[0][col],rings[0][next_col])
        triangle(center_high,rings[-1][next_col],rings[-1][col])
    return np.array(vs,dtype='<f4'),np.array(ns,dtype='<f4'),np.array(ids,dtype='<u2')
def mesh_arrow():
    v=np.array([[.5,0,0],[-.5,.5,0],[-.5,-.5,0]],dtype='<f4')
    return v,np.array([[0,0,1]]*3,dtype='<f4'),np.array([0,1,2],dtype='<u2')
geoms={'box':mesh_box(),'rounded_box':mesh_rounded_box(),'cylinder':mesh_cylinder(),
       'cylinder_z':mesh_cylinder_z(),'tire':mesh_tire(),'arrow':mesh_arrow()}
payload['meshes']={k:{'positions':v.flatten().tolist(),'normals':n.flatten().tolist(),'indices':i.tolist()} for k,(v,n,i) in geoms.items()}

def rgb(h):return [int(h[i:i+2],16)/255 for i in [1,3,5]]
def select_objects(mode):
    r=[]
    for d in scene:
        if mode=='N1' and d['level'] not in ['N1','ROBOT']:continue
        if mode=='RDC' and d['level']!='RDC':continue
        if mode=='complete' and d['name'].startswith('RDC_cabine_'):continue
        r.append(copy.deepcopy(d))
    return r

def finish_for_object(d):
    if not d['name'].startswith('AGV_'):return 'general'
    color=d['color']
    if d['mesh']=='tire' or color==ROBOT_COL['rubber']:return 'elastomer'
    if color in [ROBOT_COL['steel'],ROBOT_COL['steel_dark']]:return 'stainless_steel'
    if color in [ROBOT_COL['shell'],ROBOT_COL['panel'],ROBOT_COL['frame']]:return 'powder_coat'
    if color in [ROBOT_COL['handle'],ROBOT_COL['gasket'],ROBOT_COL['label']]:return 'matte_polymer'
    if color in [ROBOT_COL['display'],ROBOT_COL['screen']]:return 'display'
    if color in [ROBOT_COL['safety_red'],ROBOT_COL['safety_yellow']]:return 'safety_polymer'
    return 'painted_metal'

def linear_rgb(color):
    values=rgb(color)
    return [v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]

def export_glb(mode,path,source_objects=None,model_type=None):
    if mode in ['robot','robot_eclate']:
        offsets={'chassis':[0,0,-.12],'roues':[0,0,-.34],'batterie':[0,0,-.24],
                 'commandes':[0,0,1.34],'coffre':[0,0,.78],'toit':[0,0,1.18],
                 'separateurs':[0,0,.48],'glissieres':[0,-.38,.05],
                 'tiroir_S1':[-.28,-.38,.24],'tiroir_S2':[.28,-.38,.24],
                 'tiroir_S3':[-.28,-.38,-.16],'tiroir_S4':[.28,-.38,-.16]}
        objs=[]
        for source in robot if source_objects is None else source_objects:
            d=copy.deepcopy(source)
            d['name']='AGV_'+d['name']
            d['level']=d['assembly'] if mode=='robot_eclate' or source_objects is not None else 'ROBOT'
            d['kind']='robot';d['collision']=True;d['yaw']=0;d['dimension_status']='H'
            if mode=='robot_eclate':
                shift=offsets.get(d['assembly'],[0,0,0])
                d['center']=[d['center'][i]+shift[i] for i in range(3)]
            objs.append(d)
    else:
        objs=select_objects(mode)
    gltf={'asset':{'version':'2.0','generator':'AGV bancaire V0.2'},'scene':0,'scenes':[{'nodes':[0]}],
          'nodes':[{'name':'AGV_banque_Z_up_vers_Y_up','rotation':[-math.sqrt(.5),0,0,math.sqrt(.5)],'children':[]}],
          'meshes':[],'materials':[],'buffers':[{'byteLength':0}],'bufferViews':[],'accessors':[],
          'extras':{'units':'metres','date':P['date'],'hypotheses':P['hypotheses'],'wall_height':P['wall_height_m']}}
    if mode in ['robot','robot_eclate']:
        gltf['extras'].update({'payload_mass_kg':P['robot_payload_mass_kg'],
                               'compartments':P['robot_compartment_count'],
                               'nominal_mass_per_compartment_kg':P['robot_compartment_payload_kg'],
                               'assembly_view':'exploded' if mode=='robot_eclate' else 'assembled',
                               'model_type':model_type or ('exploded_assembly' if mode=='robot_eclate' else 'complete_assembly')})
    binary=bytearray();access={}
    def buf(arr,component,type_,target):
        while len(binary)%4:binary.append(0)
        offset=len(binary);raw=arr.tobytes();binary.extend(raw)
        v=len(gltf['bufferViews']);gltf['bufferViews'].append({'buffer':0,'byteOffset':offset,'byteLength':len(raw),'target':target})
        a={'bufferView':v,'componentType':component,'count':len(arr),'type':type_}
        if type_=='VEC3':a.update(min=arr.min(axis=0).tolist(),max=arr.max(axis=0).tolist())
        idx=len(gltf['accessors']);gltf['accessors'].append(a);return idx
    for k in sorted({d['mesh'] for d in objs}):
        v,n,ids=geoms[k]
        access[k]=[buf(v,5126,'VEC3',34962),buf(n,5126,'VEC3',34962),buf(ids,5123,'SCALAR',34963)]
    mats={};meshes={};groups={}
    for d in objs:
        color=d['color'];finish=finish_for_object(d);material_key=(color,finish)
        if material_key not in mats:
            finish_values={'general':(.05,.72),'elastomer':(0,.88),'stainless_steel':(.72,.30),
                           'powder_coat':(.22,.43),'matte_polymer':(.04,.58),
                           'display':(.06,.24),'safety_polymer':(.03,.31),'painted_metal':(.32,.45)}
            metallic,roughness=finish_values[finish]
            is_robot=d['name'].startswith('AGV_')
            base_color=linear_rgb(color) if is_robot else rgb(color)
            mat={'name':finish+'_'+color[1:],
                 'pbrMetallicRoughness':{'baseColorFactor':base_color+[1],
                                         'metallicFactor':metallic,'roughnessFactor':roughness},
                 'doubleSided':d['mesh']=='arrow'}
            if is_robot and (color==ROBOT_COL['screen'] or d['name'].startswith('AGV_ecran_indicateur_')):
                mat['emissiveFactor']=[v*.32 for v in linear_rgb(color)]
            mats[material_key]=len(gltf['materials']);gltf['materials'].append(mat)
        mk=(d['mesh'],material_key)
        if mk not in meshes:
            a,b,i=access[d['mesh']];meshes[mk]=len(gltf['meshes'])
            gltf['meshes'].append({'primitives':[{'attributes':{'POSITION':a,'NORMAL':b},'indices':i,'material':mats[material_key]}]})
        level=d['level']
        if level not in groups:
            groups[level]=len(gltf['nodes']);gltf['nodes'].append({'name':level,'children':[]});gltf['nodes'][0]['children'].append(groups[level])
        idx=len(gltf['nodes']);gltf['nodes'][groups[level]]['children'].append(idx)
        yaw=d['yaw'];gltf['nodes'].append({'name':d['name'],'mesh':meshes[mk],
            'translation':d['center'],'scale':d['size'],'rotation':[0,0,math.sin(yaw/2),math.cos(yaw/2)],
            'extras':{'kind':d['kind'],'collision':d['collision'],'dimension_status':d['dimension_status'],
                      'assembly':d.get('assembly','') }})
    gltf['buffers'][0]['byteLength']=len(binary)
    js=json.dumps(gltf,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    js+=b' '*((-len(js))%4);binary+=b'\0'*((-len(binary))%4)
    full=struct.pack('<III',0x46546c67,2,12+8+len(js)+8+len(binary))+struct.pack('<II',len(js),0x4E4F534A)+js+struct.pack('<II',len(binary),0x004E4942)+binary
    path.write_bytes(full)
    return len(objs)

def sub(parent,tag,text=None,**kw):
    o=ET.SubElement(parent,tag,kw)
    if text is not None:o.text=str(text)
    return o
def export_sdf(mode,path,cut=False):
    sdf=ET.Element('sdf',version='1.9');world=sub(sdf,'world',name='banque_agv_'+mode+('_coupe' if cut else ''))
    physics=sub(world,'physics',name='physics',type='ignored');sub(physics,'max_step_size','.001');sub(physics,'real_time_factor','1')
    for file,name in [('gz-sim-physics-system','Physics'),('gz-sim-user-commands-system','UserCommands'),('gz-sim-scene-broadcaster-system','SceneBroadcaster')]:sub(world,'plugin',filename=file,name='gz::sim::systems::'+name)
    # Fixed opening camera, no external models or texture downloads.
    tx,ty,tz=(.9,1.95,UP+.3) if mode=='N1' else (4,5.7,.3 if mode=='RDC' else 2.)
    gui=sub(world,'gui',fullscreen='0')
    view=sub(gui,'plugin',filename='MinimalScene',name='3D View')
    chrome=sub(view,'gz-gui');sub(chrome,'title','Maquette AGV bancaire')
    sub(chrome,'property','false',type='bool',key='showTitleBar');sub(chrome,'property','docked',type='string',key='state')
    sub(view,'engine','ogre2');sub(view,'scene','scene');sub(view,'ambient_light','.6 .6 .6');sub(view,'background_color','.94 .96 .98')
    sub(view,'camera_pose',f'{tx+20} {ty-24} {tz+27} 0 .713 2.266')
    manager=sub(gui,'plugin',filename='GzSceneManager',name='Scene Manager')
    sub(gui,'plugin',filename='EntityTree',name='Entity tree')
    sub(world,'gravity','0 0 -9.81')
    sc=sub(world,'scene');sub(sc,'ambient','.6 .6 .6 1');sub(sc,'background','.94 .96 .98 1');sub(sc,'shadows','true')
    light=sub(world,'light',name='soleil',type='directional');sub(light,'pose','0 0 20 0 0 0');sub(light,'diffuse','.9 .9 .9 1');sub(light,'specular','.2 .2 .2 1');sub(light,'direction','-.4 .3 -1');sub(light,'cast_shadows','true')
    groups={};count=0
    for original in select_objects(mode):
        d=copy.deepcopy(original)
        if d['mesh']=='arrow':continue
        if cut and d['kind'] in ['wall','shaft','cabinwall','doorframe','doorleaf','lintel']:
            if d['kind']=='lintel':continue
            base=(UP if d['level']=='N1' else 0)
            if d['level']=='COMMON':continue
            d['size'][2]=min(d['size'][2],.85);d['center'][2]=base+d['size'][2]/2
        g=d['level']
        if g not in groups:
            model=sub(world,'model',name='maquette_'+g);sub(model,'static','true');groups[g]=sub(model,'link',name='structure_'+g)
        link=groups[g];name=d['name'];pos=d['center'];size=d['size'];roll=math.pi/2 if d['mesh']=='cylinder' else 0
        pose=' '.join(f'{v:.6f}' for v in pos+[roll,0,d['yaw']])
        visual=sub(link,'visual',name=name);sub(visual,'pose',pose)
        def geometry(parent):
            geom=sub(parent,'geometry')
            if d['mesh']=='cylinder':
                q=sub(geom,'cylinder');sub(q,'radius',size[0]/2);sub(q,'length',size[1])
            else:sub(sub(geom,'box'),'size',' '.join(map(str,size)))
        geometry(visual)
        material=sub(visual,'material');col=' '.join(map(str,rgb(d['color'])+[1]));sub(material,'ambient',col);sub(material,'diffuse',col)
        if d['collision']:
            co=sub(link,'collision',name=name+'_collision');sub(co,'pose',pose);geometry(co)
        count+=1
    ET.indent(sdf,space='  ');ET.ElementTree(sdf).write(path,encoding='utf-8',xml_declaration=True)
    return count

counts={}
for mode,n in [('complete','batiment_complet'),('N1','niveau_depart'),('RDC','rez_de_chaussee')]:
    counts[n]={'glb_objects':export_glb(mode,MODEL/(n+'.glb')),'sdf_visuals':export_sdf(mode,MODEL/(n+'.sdf'))}
    if mode!='complete':export_sdf(mode,MODEL/(n+'_coupe.sdf'),True)
counts['robot_agv']={'glb_objects':export_glb('robot',MODEL/'robot_agv.glb')}
counts['robot_agv_eclate']={'glb_objects':export_glb('robot_eclate',MODEL/'robot_agv_eclate.glb')}

PARTS=MODEL/'pieces'
STAGES=MODEL/'assemblage'
SUBASSEMBLIES=MODEL/'sous_ensembles'
PARTS.mkdir(exist_ok=True)
STAGES.mkdir(exist_ok=True)
SUBASSEMBLIES.mkdir(exist_ok=True)
def slug(value):
    value=value.replace('é','e').replace('è','e').replace('ê','e').replace('à','a').replace('ç','c')
    return re.sub(r'[^A-Za-z0-9_-]+','_',value).strip('_').lower()

parts_catalog=[]
for index,part in enumerate(robot,1):
    filename=f'{index:03d}_{slug(part["name"])}.glb'
    standalone=copy.deepcopy(part)
    standalone['center']=[0,0,0]
    export_glb('robot',PARTS/filename,[standalone],model_type='individual_part')
    parts_catalog.append({'id':f'piece_{index:03d}','name':part['name'],'assembly':part['assembly'],
                          'file':f'pieces/{filename}','mesh':part['mesh'],'size_m':part['size']})

wheel_names={'moteur_reducteur_gauche','roue_motrice_gauche','moyeu_moteur_gauche'}
wheel_parts=[part for part in robot if part['name'] in wheel_names or part['name'].startswith('ecrou_roue_gauche_')]
wheel_origin=next(part['center'] for part in wheel_parts if part['name']=='roue_motrice_gauche')
wheel_catalog=[]
for variant in ['assemblee','eclatee']:
    wheel_model=[]
    for source in wheel_parts:
        part=copy.deepcopy(source)
        part['center']=[part['center'][i]-wheel_origin[i] for i in range(3)]
        if variant=='eclatee':
            if part['name']=='moteur_reducteur_gauche':part['center'][1]-=.18
            elif part['name']=='moyeu_moteur_gauche':part['center'][1]+=.10
            elif part['name'].startswith('ecrou_roue_gauche_'):part['center'][1]+=.22
        wheel_model.append(part)
    filename=f'roue_motrice_{variant}.glb'
    export_glb('robot',SUBASSEMBLIES/filename,wheel_model,model_type='wheel_subassembly_'+variant)
    wheel_catalog.append({'id':f'roue_motrice_{variant}',
                          'title':'Roue motrice '+('assemblée' if variant=='assemblee' else 'éclatée'),
                          'file':f'sous_ensembles/{filename}','component_count':len(wheel_model)})

assembly_steps=[
    ('01_chassis','Poser et assembler le châssis',['chassis']),
    ('02_roues','Installer les roues et les roulettes',['roues']),
    ('03_batterie','Installer la batterie et son support',['batterie']),
    ('04_coffre','Monter le coffre principal',['coffre']),
    ('05_separateurs','Ajouter les séparateurs des compartiments',['separateurs']),
    ('06_glissieres','Installer les glissières des tiroirs',['glissieres']),
    ('07_tiroir_S1','Assembler et poser le tiroir S1',['tiroir_S1']),
    ('08_tiroir_S2','Assembler et poser le tiroir S2',['tiroir_S2']),
    ('09_tiroir_S3','Assembler et poser le tiroir S3',['tiroir_S3']),
    ('10_tiroir_S4','Assembler et poser le tiroir S4',['tiroir_S4']),
    ('11_commandes','Installer les commandes et les composants électroniques',['commandes']),
    ('12_toit','Fermer le coffre avec le toit',['toit']),
]
stage_catalog=[]
included=[]
for number,(step_id,title,assemblies) in enumerate(assembly_steps,1):
    included.extend(assemblies)
    stage_objects=[part for part in robot if part['assembly'] in included]
    filename=f'etape_{number:02d}_{step_id.split("_",1)[1]}.glb'
    output=STAGES/filename
    object_count=export_glb('robot',output,stage_objects,model_type='assembly_step')
    stage_catalog.append({'step':number,'id':step_id,'title':title,'assemblies':assemblies,
                          'file':f'assemblage/{filename}','object_count':object_count})

robot_catalog={'title':'Pièces individuelles et étapes d’assemblage du robot AGV',
               'units':'metres','part_count':len(parts_catalog),'stage_count':len(stage_catalog),
               'parts':parts_catalog,'subassemblies':wheel_catalog,'assembly_steps':stage_catalog}
(MODEL/'catalogue_robot.json').write_text(json.dumps(robot_catalog,ensure_ascii=False,indent=2),encoding='utf-8')

template=(ROOT/'visualiseur_template.html').read_text(encoding='utf-8')
html=template.replace('__SCENE_DATA__',json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
(ROOT/'Maquette_AGV_Batiment_3D.html').write_text(html,encoding='utf-8')

def validate():
    assert P['robot_compartment_count']*P['robot_compartment_payload_kg']==P['robot_payload_mass_kg']
    assert len([d for d in scene if d['level']=='ROBOT' and d['name'].endswith('_facade')])==P['robot_compartment_count']
    facade_heights={d['name'][:2]:d['center'][2] for d in robot if d['name'].endswith('_facade')}
    assert facade_heights['S1']==facade_heights['S2']
    assert facade_heights['S3']==facade_heights['S4']
    assert facade_heights['S1']>facade_heights['S3']
    assert P['robot_compartment_clear_m'][0]*2+0.06<=P['cargo_enclosure_m'][0]
    assert P['robot_compartment_clear_m'][1]+0.06<=P['cargo_enclosure_m'][1]
    assert P['robot_compartment_clear_m'][2]*2+0.09<=P['cargo_enclosure_m'][2]
    results=[]
    for mode,n in [('complete','batiment_complet'),('N1','niveau_depart'),('RDC','rez_de_chaussee')]:
        path=MODEL/(n+'.glb');blob=path.read_bytes();magic,version,length=struct.unpack_from('<III',blob)
        assert (magic,version,length)==(0x46546c67,2,len(blob))
        jl,jt=struct.unpack_from('<II',blob,12);g=json.loads(blob[20:20+jl]);assert jt==0x4E4F534A
        off=20+jl;bl,bt=struct.unpack_from('<II',blob,off);assert bt==0x004E4942
        assert g['buffers'][0]['byteLength']<=bl
        for v in g['bufferViews']:assert v['byteOffset']+v['byteLength']<=bl
        for a in g['accessors']:assert a['count']>0
        sd=ET.parse(MODEL/(n+'.sdf')).getroot();assert sd.attrib['version']=='1.9'
        assert len(sd.findall('.//visual'))==counts[n]['sdf_visuals']
        names=[x.attrib['name'] for x in sd.findall('.//visual')];assert len(names)==len(set(names))
        results.append({'model':n,'GLB':'PASS','SDF_XML':'PASS','objects':counts[n]['glb_objects']})
    robot_blob=(MODEL/'robot_agv.glb').read_bytes()
    magic,version,length=struct.unpack_from('<III',robot_blob)
    assert (magic,version,length)==(0x46546c67,2,len(robot_blob))
    jl,jt=struct.unpack_from('<II',robot_blob,12)
    robot_gltf=json.loads(robot_blob[20:20+jl])
    assert jt==0x4E4F534A
    robot_nodes=[node['name'] for node in robot_gltf['nodes']]
    assert len([name for name in robot_nodes if name.endswith('_facade')])==P['robot_compartment_count']
    for slot in range(1,P['robot_compartment_count']+1):
        assert f'AGV_S{slot}_plaque_identification' in robot_nodes
        assert f'AGV_S{slot}_marquage_0_a' in robot_nodes
    robot_materials=[material['name'] for material in robot_gltf['materials']]
    assert any(name.startswith('powder_coat_') for name in robot_materials)
    assert any(name.startswith('stainless_steel_') for name in robot_materials)
    assert any(name.startswith('elastomer_') for name in robot_materials)
    assert robot_gltf['extras']['payload_mass_kg']==P['robot_payload_mass_kg']
    results.append({'model':'robot_agv','GLB':'PASS','compartment_facades':P['robot_compartment_count'],
                    'objects':counts['robot_agv']['glb_objects']})
    exploded_blob=(MODEL/'robot_agv_eclate.glb').read_bytes()
    magic,version,length=struct.unpack_from('<III',exploded_blob)
    assert (magic,version,length)==(0x46546c67,2,len(exploded_blob))
    jl,jt=struct.unpack_from('<II',exploded_blob,12)
    exploded_gltf=json.loads(exploded_blob[20:20+jl])
    assert jt==0x4E4F534A and exploded_gltf['extras']['assembly_view']=='exploded'
    exploded_names=[node['name'] for node in exploded_gltf['nodes']]
    assert all(any(name.startswith('tiroir_S'+str(i)) for name in exploded_names) for i in range(1,5))
    results.append({'model':'robot_agv_eclate','GLB':'PASS','objects':counts['robot_agv_eclate']['glb_objects']})
    for part,entry in zip(robot,parts_catalog):
        blob=(MODEL/entry['file']).read_bytes()
        magic,version,length=struct.unpack_from('<III',blob)
        jl,jt=struct.unpack_from('<II',blob,12)
        gltf=json.loads(blob[20:20+jl])
        part_nodes=[node['name'] for node in gltf['nodes'] if 'mesh' in node]
        assert (magic,version,length)==(0x46546c67,2,len(blob)) and jt==0x4E4F534A
        assert gltf['extras']['model_type']=='individual_part'
        assert part_nodes==['AGV_'+part['name']]
    assembled_groups=set()
    for stage,entry in zip(assembly_steps,stage_catalog):
        assembled_groups.update(stage[2])
        blob=(MODEL/entry['file']).read_bytes()
        magic,version,length=struct.unpack_from('<III',blob)
        jl,jt=struct.unpack_from('<II',blob,12)
        gltf=json.loads(blob[20:20+jl])
        mesh_nodes=[node for node in gltf['nodes'] if 'mesh' in node]
        assert (magic,version,length)==(0x46546c67,2,len(blob)) and jt==0x4E4F534A
        assert gltf['extras']['model_type']=='assembly_step'
        assert len(mesh_nodes)==entry['object_count']
        assert entry['object_count']==sum(part['assembly'] in assembled_groups for part in robot)
    for entry in wheel_catalog:
        blob=(MODEL/entry['file']).read_bytes()
        magic,version,length=struct.unpack_from('<III',blob)
        jl,jt=struct.unpack_from('<II',blob,12)
        gltf=json.loads(blob[20:20+jl])
        mesh_nodes=[node['name'] for node in gltf['nodes'] if 'mesh' in node]
        assert (magic,version,length)==(0x46546c67,2,len(blob)) and jt==0x4E4F534A
        assert gltf['extras']['model_type']=='wheel_subassembly_'+entry['id'].rsplit('_',1)[1]
        assert len(mesh_nodes)==entry['component_count']==len(wheel_parts)
        assert all(any(name.endswith(part['name']) for name in mesh_nodes) for part in wheel_parts)
    results.append({'model':'robot_parts','GLB':'PASS','files':len(parts_catalog)})
    results.append({'model':'robot_assembly_steps','GLB':'PASS','files':len(stage_catalog)})
    results.append({'model':'wheel_subassemblies','GLB':'PASS','files':len(wheel_catalog)})
    # Geometry fidelity: every 2D wall rectangle is extruded once at its level.
    for level,key,z in [('N1','N?',UP),('RDC','RDC',0)]:
        walls=[d for d in scene if d['level']==level and d['kind']=='wall']
        assert len(walls)==len(plan['levels'][key]['wall_rectangles'])
        for d,src in zip(walls,plan['levels'][key]['wall_rectangles']):
            x0,y0,x1,y1=src['rect'];assert np.allclose(d['center'][:2],[(x0+x1)/2,(y0+y1)/2]);assert np.allclose(d['size'][:2],[x1-x0,y1-y0])
    # Normals must agree with outward triangle winding for all generated geometry.
    for k,(v,n,i) in geoms.items():
        for tri in i.reshape((-1,3)):
            a,b,c=v[tri];normal=np.cross(b-a,c-a)
            assert np.dot(normal,n[tri].mean(axis=0))>0,k
    report={'date':P['date'],'source_plan_sha256':hashlib.sha256((DATA/'geometrie_plan_retenu.json').read_bytes()).hexdigest(),
            'checks':results,'wall_footprints_match_accepted_plan':True,'mesh_normals_and_winding':'PASS',
            'Gazebo_execution':'NOT_RUN - Gazebo absent de cet environnement',
            'robot_design_checks':{'compartments':P['robot_compartment_count'],'nominal_payload_kg':P['robot_payload_mass_kg'],'four_drawer_geometry':'PASS'},
            'limitations':['Maquette statique, pas de navigation autonome ni de commande d’ascenseur.','La conception mécanique du robot est un avant-projet : masses, stabilité, pièces, dimensions utiles et essais restent à valider.']}
    (ROOT/'verification_maquette.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

def render_preview():
    """Orthographic technical render with a depth buffer, using the GLB meshes."""
    from PIL import Image, ImageDraw, ImageFont
    def font(size,bold=False):
        filenames=['arialbd.ttf','DejaVuSans-Bold.ttf'] if bold else ['arial.ttf','DejaVuSans.ttf']
        candidates=[Path('C:/Windows/Fonts')/filenames[0],Path('/usr/share/fonts/truetype/dejavu')/filenames[-1]]
        for path in candidates:
            if path.exists():return ImageFont.truetype(str(path),size)
        return ImageFont.load_default(size=size)
    az=-.95;el=1.02
    toward=np.array([math.cos(el)*math.cos(az),math.cos(el)*math.sin(az),math.sin(el)])
    right=np.cross(-toward,[0,0,1]);right/=np.linalg.norm(right)
    up=np.cross(right,-toward)
    background=(245,248,251);pw,ph=1400,830
    light=np.array([-.3,-.4,1.]);light/=np.linalg.norm(light)
    panels=[]
    for mode in ['N1','RDC']:
        transformed=[];projected=[]
        for src in select_objects(mode):
            d=copy.deepcopy(src)
            if d['kind']=='lintel':continue
            if d['kind'] in ['wall','shaft','cabinwall','doorframe','doorleaf']:
                base=UP if d['level']=='N1' else 0
                d['size'][2]=min(d['size'][2],.85);d['center'][2]=base+d['size'][2]/2
            v,n,ids=geoms[d['mesh']];c=math.cos(d['yaw']);s=math.sin(d['yaw'])
            rot=np.array([[c,-s,0],[s,c,0],[0,0,1]])
            world=(v*np.array(d['size']))@rot.T+np.array(d['center'])
            uv=np.column_stack((world@right,world@up,world@toward))
            transformed.append((d,uv,n@rot.T,ids));projected.append(uv)
        joined=np.concatenate(projected);lo=joined.min(axis=0);hi=joined.max(axis=0)
        factor=min((pw-100)/(hi[0]-lo[0]),(ph-100)/(hi[1]-lo[1]))
        center=(lo+hi)/2
        screen=lambda uv:np.column_stack(((uv[:,0]-center[0])*factor+pw/2,-(uv[:,1]-center[1])*factor+ph/2,uv[:,2]))
        pixels=np.empty((ph,pw,3),dtype=np.uint8);pixels[:]=background
        depth=np.full((ph,pw),-np.inf,dtype=np.float32)
        for d,uv,n,ids in transformed:
            xyz=screen(uv);basecolor=np.array(rgb(d['color']))*255
            for tri in ids.reshape((-1,3)):
                normal=n[tri].mean(axis=0);normal/=max(np.linalg.norm(normal),1e-9)
                if np.dot(normal,toward)<0:continue
                t=xyz[tri];x0=max(0,int(math.floor(t[:,0].min())));x1=min(pw-1,int(math.ceil(t[:,0].max())));y0=max(0,int(math.floor(t[:,1].min())));y1=min(ph-1,int(math.ceil(t[:,1].max())))
                if x0>x1 or y0>y1:continue
                a,b,c=t;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(den)<1e-8:continue
                X,Y=np.meshgrid(np.arange(x0,x1+1)+.5,np.arange(y0,y1+1)+.5)
                wa=((b[1]-c[1])*(X-c[0])+(c[0]-b[0])*(Y-c[1]))/den
                wb=((c[1]-a[1])*(X-c[0])+(a[0]-c[0])*(Y-c[1]))/den
                wc=1-wa-wb;z=wa*a[2]+wb*b[2]+wc*c[2]
                old=depth[y0:y1+1,x0:x1+1]
                mask=(wa>=-1e-7)&(wb>=-1e-7)&(wc>=-1e-7)&(z>=old-1e-6)
                shade=.55+.40*max(float(np.dot(normal,light)),0)
                color=np.clip(basecolor*shade,0,255).astype(np.uint8)
                old[mask]=z[mask];pixels[y0:y1+1,x0:x1+1][mask]=color
        im=Image.fromarray(pixels);draw=ImageDraw.Draw(im);used=[]
        for lab in labels:
            if lab['level']!=mode or lab['text']=='ATTENTE':continue
            p=np.array(lab['p']);uv=np.array([[p@right,p@up,p@toward]]);x,y,z=screen(uv)[0]
            f=font(17,True);text=lab['text'];bbox=draw.textbbox((0,0),text,font=f);tw=bbox[2]-bbox[0];th=bbox[3]-bbox[1]
            box_=(int(x-tw/2-5),int(y-th/2-5),int(x+tw/2+5),int(y+th/2+5))
            if box_[0]<0 or box_[2]>=pw or box_[1]<0 or box_[3]>=ph:continue
            if any(box_[0]<r[2] and box_[2]>r[0] and box_[1]<r[3] and box_[3]>r[1] for r in used):continue
            used.append(box_);draw.rectangle(box_,fill='white')
            draw.text((x-tw/2,y-th/2-bbox[1]),text,font=f,fill=lab.get('color','#32495E'))
        panels.append(im)
    full=Image.new('RGB',(2960,1230),background);draw=ImageDraw.Draw(full)
    draw.text((65,32),'AGV BANCAIRE',font=font(23,True),fill='#216BDD')
    draw.text((65,75),'Maquette 3D du bâtiment',font=font(47,True),fill='#172D42')
    draw.text((65,140),'Deux vues en coupe du plan retenu. Les dimensions provisoires restent modifiables.',font=font(22),fill='#5B7083')
    draw.text((2500,40),'V0.2 · 21 OCTOBRE 2026',font=font(19),fill='#8B5816')
    draw.text((65,215),'01  NIVEAU DE DÉPART · +3,00 m H',font=font(23,True),fill='#172D42')
    draw.text((1525,215),'02  REZ-DE-CHAUSSÉE · 0,00 m',font=font(23,True),fill='#172D42')
    full.paste(panels[0],(50,255));full.paste(panels[1],(1510,255))
    x=65
    for title,col in [('Trajet prévu','#216BDD'),('Sortie vers attente','#8F65BB'),('Portes ouvertes','#279E8D'),('Ascenseur','#9D8CC5')]:
        draw.line((x,1125,x+45,1125),fill=col,width=7);draw.text((x+58,1111),title,font=font(21),fill='#32495E');x+=350
    draw.text((65,1162),'H = hypothèse. Murs de 2,40 m H affichés en coupe à 0,85 m. Portes de 1,20 × 2,10 m H.',font=font(19),fill='#5B7083')
    draw.text((65,1193),'Robot en avant-projet : tiroirs assistés, charges, stabilité et interfaces à valider.',font=font(19),fill='#5B7083')
    full.save(ROOT/'Apercu_Maquette_AGV_3D.png',optimize=True)

def update_manifest():
    manifest_path=ROOT/'manifest_fichiers.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    known={entry['path'] for entry in manifest['files']}
    generated=['modeles/robot_agv_eclate.glb','modeles/catalogue_robot.json']
    generated.extend(path.relative_to(ROOT).as_posix() for folder in [PARTS,STAGES,SUBASSEMBLIES] for path in sorted(folder.glob('*.glb')))
    for relative in generated:
        if relative not in known:
            manifest['files'].append({'path':relative,'bytes':0,'sha256':''})
    for entry in manifest['files']:
        path=ROOT/entry['path']
        data=path.read_bytes()
        entry['bytes']=len(data)
        entry['sha256']=hashlib.sha256(data).hexdigest()
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    report=validate()
    render_preview()
    update_manifest()
    print(json.dumps(report,ensure_ascii=False,indent=2))
