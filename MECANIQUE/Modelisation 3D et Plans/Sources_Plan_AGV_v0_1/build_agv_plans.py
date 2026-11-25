from pathlib import Path
import math, json, html, textwrap, zipfile
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'pdf'
SRC = OUT / 'sources'
TMP = ROOT / 'tmp' / 'pdfs'
for p in (OUT, SRC, TMP): p.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

W, H = 420*mm, 297*mm
INK='#172B3B'; MUTED='#647686'; LIGHT='#E7EDF2'; BLUE='#1764D5'
TEAL='#087D68'; AMBER='#A86413'; PAPER='#F5F8FB'; GREY='#A8B6C2'
VIOLET='#7755B7'; WHITE='#FFFFFF'

class Page:
    def __init__(self): self.items=[]
    def rect(self,x,y,w,h,fill=None,stroke=None,lw=.7,dash=None):
        self.items.append(('rect',x,y,w,h,fill,stroke,lw,dash))
    def line(self,pts,color=INK,lw=1,dash=None):
        self.items.append(('line',pts,color,lw,dash))
    def poly(self,pts,fill=None,stroke=None,lw=.7):
        self.items.append(('poly',pts,fill,stroke,lw))
    def circle(self,x,y,r,fill=None,stroke=None,lw=.7,dash=None):
        self.items.append(('circle',x,y,r,fill,stroke,lw,dash))
    def text(self,x,y,s,size=8,color=INK,bold=False,anchor='start',angle=0):
        self.items.append(('text',x,y,str(s),size,color,bold,anchor,angle))
    def wrap(self,x,y,s,width,size=8,color=INK,bold=False,leading=None):
        font='DV-B' if bold else 'DV'; leading=leading or size*1.48
        yy=y
        for para in str(s).split('\n'):
            line=''
            for word in para.split():
                test=(line+' '+word).strip()
                if pdfmetrics.stringWidth(test,font,size)>width and line:
                    self.text(x,yy,line,size,color,bold); yy-=leading; line=word
                else: line=test
            self.text(x,yy,line,size,color,bold); yy-=leading
        return yy
    def pdf(self,c):
        for a in self.items:
            c.saveState(); kind=a[0]
            if kind=='text':
                _,x,y,s,sz,col,bold,anc,angle=a
                c.setFillColor(col); c.setFont('DV-B' if bold else 'DV',sz)
                c.translate(x,y); c.rotate(angle)
                {'start':c.drawString,'middle':c.drawCentredString,'end':c.drawRightString}[anc](0,0,s)
            else:
                if kind=='line':
                    _,pts,col,lw,dash=a; c.setStrokeColor(col); c.setLineWidth(lw)
                    if dash: c.setDash(*dash)
                    q=c.beginPath(); q.moveTo(*pts[0])
                    for xy in pts[1:]: q.lineTo(*xy)
                    c.drawPath(q,stroke=1,fill=0)
                elif kind=='poly':
                    _,pts,fill,stroke,lw=a
                    if fill: c.setFillColor(fill)
                    if stroke: c.setStrokeColor(stroke)
                    c.setLineWidth(lw); q=c.beginPath(); q.moveTo(*pts[0])
                    for xy in pts[1:]: q.lineTo(*xy)
                    q.close(); c.drawPath(q,fill=int(bool(fill)),stroke=int(bool(stroke)))
                elif kind=='rect':
                    _,x,y,w,h,fill,stroke,lw,dash=a
                    if fill: c.setFillColor(fill)
                    if stroke: c.setStrokeColor(stroke)
                    if dash: c.setDash(*dash)
                    c.setLineWidth(lw); c.rect(x,y,w,h,fill=int(bool(fill)),stroke=int(bool(stroke)))
                elif kind=='circle':
                    _,x,y,r,fill,stroke,lw,dash=a
                    if fill: c.setFillColor(fill)
                    if stroke: c.setStrokeColor(stroke)
                    if dash: c.setDash(*dash)
                    c.setLineWidth(lw); c.circle(x,y,r,fill=int(bool(fill)),stroke=int(bool(stroke)))
            c.restoreState()
    def svg(self,path):
        esc=lambda s: html.escape(str(s),quote=True)
        data=[f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {W} {H}">',
              '<title>AGV bancaire - avant-projet coté V0.1</title>',
              '<rect width="100%" height="100%" fill="white"/>']
        def style(fill,stroke,lw,dash=None):
            d=f'fill="{fill or "none"}" stroke="{stroke or "none"}" stroke-width="{lw}"'
            if dash: d+=' stroke-dasharray="'+' '.join(map(str,dash))+'"'
            return d
        for a in self.items:
            kind=a[0]
            if kind=='text':
                _,x,y,s,sz,col,bold,anc,angle=a
                data.append(f'<text x="{x}" y="{H-y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{sz}" font-weight="{700 if bold else 400}" fill="{col}" text-anchor="{anc}" transform="rotate({-angle} {x} {H-y})">{esc(s)}</text>')
            elif kind=='rect':
                _,x,y,w,h,fill,stroke,lw,dash=a
                data.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" {style(fill,stroke,lw,dash)}/>')
            elif kind=='circle':
                _,x,y,r,fill,stroke,lw,dash=a
                data.append(f'<circle cx="{x}" cy="{H-y}" r="{r}" {style(fill,stroke,lw,dash)}/>')
            elif kind=='poly':
                _,pts,fill,stroke,lw=a
                ps=' '.join(f'{x},{H-y}' for x,y in pts)
                data.append(f'<polygon points="{ps}" {style(fill,stroke,lw)}/>')
            elif kind=='line':
                _,pts,col,lw,dash=a
                ps=' '.join(f'{x},{H-y}' for x,y in pts)
                data.append(f'<polyline points="{ps}" {style(None,col,lw,dash)} stroke-linejoin="round"/>')
        data.append('</svg>'); path.write_text('\n'.join(data),encoding='utf-8')

class Map:
    def __init__(self,p,ox,oy,scale): self.p=p; self.ox=ox; self.oy=oy; self.s=1000*mm/scale
    def xy(self,x,y): return self.ox+x*self.s,self.oy+y*self.s
    def box(self,r,fill=None,stroke=None,lw=.7,dash=None):
        x0,y0,x1,y1=r; self.p.rect(*self.xy(x0,y0),(x1-x0)*self.s,(y1-y0)*self.s,fill,stroke,lw,dash)
    def line(self,pts,color=INK,lw=1,dash=None): self.p.line([self.xy(*p) for p in pts],color,lw,dash)
    def txt(self,x,y,s,sz=8,col=INK,bold=False,anc='middle',angle=0): self.p.text(*self.xy(x,y),s,sz,col,bold,anc,angle)
    def circle(self,x,y,r,fill=None,stroke=None,lw=.7,dash=None): self.p.circle(*self.xy(x,y),r*self.s,fill,stroke,lw,dash)
    def arrow(self,a,b,color=BLUE,lw=1.8,head=5):
        A=self.xy(*a); B=self.xy(*b); self.p.line([A,B],color,lw)
        angle=math.atan2(B[1]-A[1],B[0]-A[0]); cs=math.cos(angle); sn=math.sin(angle)
        self.p.poly([B,(B[0]-head*cs+head*.46*sn,B[1]-head*sn-head*.46*cs),(B[0]-head*cs-head*.46*sn,B[1]-head*sn+head*.46*cs)],color)
    def route(self,pts,color=BLUE,lw=2,dash=None):
        self.line(pts,color,lw,dash)
        for a,b in zip(pts,pts[1:]):
            length=math.dist(a,b)
            if length>.6:
                t=.55
                q=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
                r=(a[0]+(b[0]-a[0])*(t+.05),a[1]+(b[1]-a[1])*(t+.05))
                self.arrow(q,r,color,lw,5)
    def dimh(self,x0,x1,yobj,ydim,label,hyp=False):
        col=AMBER if hyp else TEAL
        self.line([(x0,yobj),(x0,ydim+.07)],GREY,.5)
        self.line([(x1,yobj),(x1,ydim+.07)],GREY,.5)
        self.line([(x0,ydim),(x1,ydim)],col,.65)
        for x in [x0,x1]: self.line([(x-.055,ydim-.07),(x+.055,ydim+.07)],col,.8)
        X,Y=self.xy((x0+x1)/2,ydim)
        sw=pdfmetrics.stringWidth(label,'DV-B',7.3)
        self.p.rect(X-sw/2-3,Y+2,sw+6,11,WHITE)
        self.p.text(X,Y+4,label,7.3,col,True,'middle')
    def dimv(self,y0,y1,xobj,xdim,label,hyp=False):
        col=AMBER if hyp else TEAL
        self.line([(xobj,y0),(xdim+.07,y0)],GREY,.5)
        self.line([(xobj,y1),(xdim+.07,y1)],GREY,.5)
        self.line([(xdim,y0),(xdim,y1)],col,.65)
        for y in [y0,y1]: self.line([(xdim-.07,y-.055),(xdim+.07,y+.055)],col,.8)
        X,Y=self.xy(xdim,(y0+y1)/2)
        sw=pdfmetrics.stringWidth(label,'DV-B',7.3)
        self.p.rect(X-12,Y-sw/2-3,12,sw+6,WHITE)
        self.p.text(X-4,Y,label,7.3,col,True,'middle',90)
    def node(self,x,y,n,col=BLUE):
        X,Y=self.xy(x,y); self.p.circle(X,Y,8,WHITE,col,1.2); self.p.text(X,Y-2.7,n,7.2,col,True,'middle')
    def robot(self,x,y,yaw=0,col=BLUE):
        L=.55; B=.35; cs=math.cos(yaw); sn=math.sin(yaw)
        pts=[(x+u*cs-v*sn,y+u*sn+v*cs) for u,v in [(-L,-B),(L,-B),(L,B),(-L,B)]]
        self.p.poly([self.xy(*q) for q in pts],'#D8E9FF',col,1.2)
        self.arrow((x-.25*cs,y-.25*sn),(x+.4*cs,y+.4*sn),col,1.2,4)
    def compass(self,x,y):
        self.arrow((x,y),(x,y+1),INK,1,5); self.txt(x,y+1.17,'N',8,bold=True)
        self.arrow((x,y),(x+.6,y),MUTED,.7,3); self.txt(x+.75,y-.06,'E',6,MUTED)
    def scalebar(self,x,y,length=2):
        for i in range(length): self.box((x+i,y,x+i+1,y+.08),INK if i%2==0 else WHITE,INK,.5)
        for i in range(length+1): self.txt(x+i,y-.25,str(i),6,MUTED)
        self.txt(x+length+.3,y-.25,'m',6,MUTED)

def wall(x0,y0,x1,y1,name='mur'): return {'rect':[x0,y0,x1,y1],'name':name}
def R(x0,y0,x1,y1): return [x0,y0,x1,y1]
shaft=R(-6.22,-.1,-4.02,2.1)
shaft_walls=[wall(-6.37,-.25,-6.22,2.25,'ascenseur ouest'),wall(-4.02,-.25,-3.87,2.25,'ascenseur est'),wall(-6.22,2.1,-4.02,2.25,'ascenseur nord'),wall(-6.22,-.25,-5.72,-.1,'ascenseur seuil gauche'),wall(-4.52,-.25,-4.02,-.1,'ascenseur seuil droite')]
n1_floors=[R(0,0,8,6),R(-6.22,-2.1,1.76,-.3),R(.28,-.3,1.48,0),R(-5.72,-.3,-4.52,-.1),shaft]
n1_walls=[wall(-.15,-.15,0,6.15),wall(8,-.15,8.15,6.15),wall(0,6,8,6.15),wall(0,-.15,.28,0),wall(1.48,-.15,8,0),
wall(1.76,0,1.88,3.12,'pièce B ouest'),wall(1.88,3,2.28,3.12,'pièce B nord gauche'),wall(3.48,3,8,3.12,'pièces nord'),
wall(3.88,0,4,1.4,'pièce A ouest bas'),wall(3.88,2.6,4,3,'pièce A ouest haut'),
wall(-6.37,-2.25,-6.22,-.3),wall(-6.22,-2.25,1.91,-2.1),wall(1.76,-2.1,1.91,-.3),
wall(-6.22,-.3,-5.72,-.15),wall(-4.52,-.3,.28,-.15),wall(1.48,-.3,1.76,-.15),wall(.13,-.3,.28,0),wall(1.48,-.3,1.63,0)]+shaft_walls
n1_furniture=[wall(3.1,3.4,4.5,4,'bureau 1'),wall(5.7,3.4,7.1,4,'bureau 2'),wall(3.4,5.55,7.6,5.95,'comptoir personnel')]
n1_route=[[5,4.8],[5,4.65],[.88,4.65],[.88,-1.2],[-5.12,-1.2],[-5.12,1]]

rdc_floors=[shaft,R(-5.72,-.3,-4.52,-.1),R(-6.22,-2.1,-2.22,-.3),R(-3.87,-.3,-2.37,3.9),R(-4.02,3.9,6.88,5.7),
R(6.88,3.3,9.88,13.54),R(10,3.3,14,6.3),R(10,6.42,14,9.42),R(10,9.54,14,13.54),
R(9.88,4.2,10,5.4),R(9.88,7.32,10,8.52),R(9.88,10.94,10,12.14)]
rdc_walls=shaft_walls+[
wall(-6.37,-2.25,-6.22,-.3),wall(-6.22,-2.25,-2.07,-2.1),wall(-2.22,-2.1,-2.07,-.3),
wall(-6.22,-.3,-5.72,-.15),wall(-4.52,-.3,-3.87,-.15),wall(-2.37,-.3,-2.22,-.15),
wall(-4.02,-.3,-3.87,3.9),wall(-2.37,-.3,-2.22,3.9),wall(-4.17,3.9,-4.02,5.85),wall(-4.02,5.7,6.88,5.85),wall(-2.22,3.75,6.88,3.9),
wall(6.73,3.3,6.88,4.2),wall(6.73,5.4,6.88,13.69),wall(6.88,3.15,14.15,3.3),wall(6.88,13.54,14.15,13.69),wall(14,3.3,14.15,13.54),
wall(9.88,3.3,10,4.2),wall(9.88,5.4,10,7.32),wall(9.88,8.52,10,10.94),wall(9.88,12.14,10,13.54),
wall(10,6.3,14,6.42),wall(10,9.42,14,9.54)]
zones=[R(10.35,12.64,11.35,13.39),R(11.5,12.64,12.5,13.39),R(12.655,12.64,13.645,13.39)]
rdc_objects=[wall(*q,'réception C'+str(i+1)) for i,q in enumerate(zones)]
rdc_route=[[-5.12,1],[-5.12,-1.2],[-3.12,-1.2],[-3.12,4.8],[6.88,4.8],[8.8,4.8],[8.8,11.54],[10.85,11.54],[10.85,11.95]]
wait_route=[[13.15,11.54],[7.8,11.54],[7.8,10.4]]

def frame(p,num,title,subtitle,scale):
    p.rect(0,0,W,H,WHITE)
    p.rect(24,H-44,5,24,BLUE)
    p.text(40,H-30,'AGV BANCAIRE',10,BLUE,True)
    p.text(40,H-55,title,20,INK,True)
    p.text(40,H-74,subtitle,8.5,MUTED)
    p.text(W-30,H-29,'AVANT-PROJET  V0.1',10,AMBER,True,'end')
    p.text(W-30,H-46,'20 OCTOBRE 2026',8,MUTED,False,'end')
    p.text(W-30,H-63,'DIMENSIONS NON RELEVÉES SUR SITE',7,AMBER,True,'end')
    p.line([(30,H-88),(W-30,H-88)],LIGHT,1)
    p.line([(30,40),(W-30,40)],LIGHT,1)
    p.text(30,23,'Cotes en mètres | D = donnée fournie | H = hypothèse de conception | Contrôle géométrique de principe',7,MUTED)
    p.text(W-30,23,f'A3 paysage | {scale} | {num:02d} / 03',7,MUTED,False,'end')

def sidebar(p,title,blocks):
    x=925; w=235
    p.rect(x,66,w,H-169,PAPER)
    p.text(x+15,H-124,title,11,INK,True)
    y=H-149
    for head,body in blocks:
        p.text(x+15,y,head,8.6,BLUE,True); y-=16
        y=p.wrap(x+15,y,body,w-30,8,INK,leading=12)
        y-=20
    return y

def legend(p,x,y):
    p.line([(x,y),(x+24,y)],BLUE,2); p.text(x+32,y-3,'Mission principale',7.5,INK)
    p.line([(x+160,y),(x+184,y)],VIOLET,1.6,[4,3]); p.text(x+192,y-3,'Retour vers attente',7.5,INK)
    p.text(x+390,y-3,'D : fourni',7.5,TEAL,True)
    p.text(x+468,y-3,'H : provisoire',7.5,AMBER,True)

def floors_walls(m,floors,walls):
    for q in floors: m.box(q,'#F9FBFD')
    for a in walls: m.box(a['rect'],INK)

def sliding(m,a,b,label=None,txt_offset=(0,0)):
    m.line([a,b],TEAL,1.25,[3,2])
    dx=b[0]-a[0]; dy=b[1]-a[1]
    p=(a[0]+dx*.15,a[1]+dy*.15); q=(a[0]+dx*.85,a[1]+dy*.85)
    # Thin symbolic leaf, placed in the wall line; openings are clear in the control model.
    if label: m.txt((a[0]+b[0])/2+txt_offset[0],(a[1]+b[1])/2+txt_offset[1],label,6.8,AMBER,True)

pages=[]
p=Page(); frame(p,1,'Niveau de départ - collecte et accès à l’ascenseur','Salle de collecte au nord du couloir. Niveau supérieur N? : numéro et altitude à confirmer.','1:50')
m=Map(p,418,305,50)
floors_walls(m,n1_floors,n1_walls)
for q in n1_furniture: m.box(q['rect'],'#D9E1E8',GREY,.6)
m.txt(5.5,5.68,'PERSONNEL / COMPTOIR',7.3,INK,True)
m.txt(3.8,3.63,'BUREAU 1 · H',6.8,INK,True)
m.txt(6.4,3.63,'BUREAU 2 · H',6.8,INK,True)
m.txt(6,1.9,'PIÈCE A',10,INK,True); m.txt(6,1.59,'4,00 × 3,00 m · D',8,TEAL,True)
m.txt(2.88,1.75,'PIÈCE B',9,INK,True); m.txt(2.88,1.44,'2,00 × 3,00 m · H',6.5,AMBER,True)
m.txt(6.55,4.95,'COLLECTE',8.2,TEAL,True)
m.txt(6.55,4.66,'8,00 × 6,00 m · D',7.3,TEAL,True)
m.txt(.35,2.8,'PASSAGE OUEST',7,MUTED,True,angle=90)
m.txt(-2.4,-1.85,'COULOIR DU NIVEAU DE DÉPART',7,MUTED,True)
m.box(shaft,'#E6E1F5',INK,.5)
m.txt(-5.12,1.55,'ASC. A',9,VIOLET,True)
m.txt(-5.12,1.24,'2,20 × 2,20 · H',6.5,AMBER,True)
m.txt(-5.12,.36,'vers RDC',7,VIOLET)
m.route(n1_route)
m.robot(5,4.8,-math.pi/2)
m.txt(5.55,4.23,'S0',7,BLUE,True)
for x,y,n in [(.88,4.65,'1'),(.88,-1.2,'2'),(-5.12,-1.2,'3')]: m.node(x,y,n)
sliding(m,(.28,-.075),(1.48,-.075),'P0 · 1,20 H',(1.05,-.18))
sliding(m,(-5.72,-.175),(-4.52,-.175),'PA · 1,20 H',(1.48,.05))
sliding(m,(2.28,3.06),(3.48,3.06),'PB · 1,20 H',(0,.24))
sliding(m,(3.94,1.4),(3.94,2.6))
m.txt(4.24,2.04,'PC',6,AMBER,True)
m.dimh(0,8,6.15,6.63,'8,00 m · D')
m.dimv(0,6,8.15,8.68,'6,00 m · D')
m.dimh(4,8,0,.4,'4,00 m · D')
m.dimv(0,3,8,7.58,'3,00 m · D')
m.dimh(1.88,3.88,0,.4,'2,00 m · H',True)
m.dimh(0,1.76,.72,.72,'1,76 m · H',True)
m.dimh(-5.12,.88,-1.2,-2.82,'6,00 m · D - axe à axe')
m.dimv(-2.1,-.3,-6.37,-6.85,'1,80 m · H',True)
m.circle(.88,4.65,.791,None,GREY,.55,[2,2])
m.compass(-6.2,4.15); m.scalebar(-6.05,3.6,2)
p.wrap(47,121,'Lecture du parcours : S0 > 1 : rejoindre le passage ouest ; 1 > 2 : sortir au sud-ouest ; 2 > 3 : tourner à droite et parcourir 6 m ; 3 > A : tourner à droite et entrer.',835,8.2,INK)
legend(p,47,81)
sidebar(p,'Implantation du niveau N?',[
('Données conservées','Salle 8 × 6 m. Pièce A au sud-est : 4 × 3 m. Deux bureaux. Sortie au sud-ouest. Liaison vers l’ascenseur : environ 6 m.'),
('Choix provisoires','Pièce B de 2 × 3 m, adossée à la pièce A. Porte au nord. Bureaux et comptoir placés pour préserver le passage du robot.'),
('Sens du premier virage','Le robot démarre orienté au sud. Pour rejoindre l’ouest, il tourne à droite. Cette interprétation corrige la contradiction gauche / ouest du récit.'),
('Passages proposés','P0, PA, PB, PC : 1,20 m utiles H. Couloir : 1,80 m H. Pièce B et murs placés pour laisser 1,76 m utiles à l’ouest.'),
('Repère commun','Le centre de la cabine A reste à x = -5,12 m ; y = 1,00 m aux deux niveaux. Origine : angle intérieur sud-ouest de la collecte.'),
('Statut du dessin','Aucune cote n’a été relevée sur site. Les cotes D proviennent du descriptif ; les cotes H doivent être corrigées avec un croquis ou des mesures.')])
pages.append(p)

p=Page(); frame(p,2,'Rez-de-chaussée - transfert et dépôts','Ascenseur A au même emplacement en plan. Trois zones de tri proposées dans le dépôt 3.','1:100')
m=Map(p,350,230,100)
floors_walls(m,rdc_floors,rdc_walls)
m.box(shaft,'#E6E1F5',INK,.5)
m.txt(-5.12,1.42,'ASC. A',7.3,VIOLET,True)
m.txt(-5.12,1.02,'2,20 × 2,20 H',5.6,AMBER,True)
m.circle(-5.12,.62,.35,None,VIOLET,.65,[2,2])
m.txt(-5.12,.5,'180° H',5.4,VIOLET)
for x,y in [(-3.12,-1.2),(-3.12,4.8)]: m.box((x-.9,y-.9,x+.9,y+.9),'#EDF3FE',GREY,.5,[2,2])
for i,(a,b) in enumerate([(3.3,6.3),(6.42,9.42),(9.54,13.54)],1):
    if i==3:
        m.txt(12,10.25,'DÉPÔT 3',9,BLUE,True)
        m.txt(12,9.91,'PRIORITAIRE · 4 × 4 m H',6.2,AMBER,True)
    else:
        m.txt(12,(a+b)/2+.4,f'DÉPÔT {i}',8.4,INK,True)
        m.txt(12,(a+b)/2-.05,'REPLI AUTORISÉ' if i==1 else 'RÔLE NON DÉFINI',6.3,AMBER,True)
        m.txt(12,(a+b)/2-.45,'4 × 3 m · H',6.4,AMBER)
    sliding(m,(9.94,(a+b)/2-.6),(9.94,(a+b)/2+.6))
for i,q in enumerate(zones):
    m.box(q,['#DAF1E7','#E0EAFB','#EEE3F8'][i],['#27976D',BLUE,VIOLET][i],.7)
    m.txt((q[0]+q[2])/2,13.06,'C'+str(i+1),7,INK,True)
    m.txt((q[0]+q[2])/2,12.76,'ZONE H',4.9,AMBER,True)
    m.circle((q[0]+q[2])/2,11.95,.13,WHITE,BLUE,.8)
    if i>0: m.line([((q[0]+q[2])/2,11.95),((q[0]+q[2])/2,11.05)],BLUE,.7,[2,2])
m.line([(10.85,11.05),(13.15,11.05)],BLUE,.7,[2,2])
m.box((7.3,9.7,8.3,11.1),'#F0EAF8',VIOLET,.5,[3,2])
m.txt(7.8,10.33,'ATT.',6,VIOLET,True)
m.txt(8.55,12.85,'HALL · 3,00 m H',6.7,AMBER,True)
m.txt(-2.7,1.65,'COULOIR 1',6.4,MUTED,True,angle=90)
m.txt(1.7,4.12,'COULOIR 2 · LARGEUR 1,80 m H',6.8,MUTED,True)
m.route(rdc_route)
m.route(wait_route,VIOLET,1.2,[4,3])
m.route([[8.8,4.8],[10.7,4.8]],AMBER,1.1,[4,3])
m.robot(7.8,10.4,-math.pi/2,VIOLET)
for x,y,n in [(-5.12,-1.2,'4'),(-3.12,-1.2,'5'),(-3.12,4.8,'6'),(6.88,4.8,'7')]: m.node(x,y,n)
sliding(m,(-5.72,-.175),(-4.52,-.175))
sliding(m,(6.805,4.2),(6.805,5.4))
m.txt(6.1,5.84,'P1 · 1,20 H',6.3,AMBER,True)
m.dimh(-5.12,-3.12,-1.2,-2.88,'2,00 m · D')
m.dimv(-1.2,4.8,-3.87,-7.2,'6,00 m · D - axe à axe')
m.dimh(-3.87,-2.37,2.7,2.7,'1,50 m · D')
m.dimh(-3.12,6.88,5.85,6.65,'10,00 m · D - axe à porte')
m.dimh(6.88,9.88,13.69,14.35,'3,00 m · H',True)
m.dimh(10,14,13.69,14.35,'4,00 m · H',True)
m.dimv(9.54,13.54,14.15,14.95,'4,00 m · H',True)
m.dimv(6.42,9.42,14.15,14.95,'3,00 m · H',True)
m.dimv(3.3,6.3,14.15,14.95,'3,00 m · H',True)
m.compass(-6.6,11.2); m.scalebar(-6.6,10.5,3)
p.wrap(47,121,'Lecture : A > 4 : sortie vers le sud ; 4 > 5 : gauche, 2 m ; 5 > 6 : gauche, 6 m ; 6 > 7 : droite, 10 m ; puis accès au dépôt 3, tri et sortie vers l’attente.',835,8.2,INK)
legend(p,47,81)
sidebar(p,'Hypothèses du rez-de-chaussée',[
('Ascenseur à porte unique H','Entrée et sortie au sud. Demi-tour dans la cabine avant la sortie au RDC. Cette manœuvre disparaîtrait avec une cabine traversante adaptée.'),
('Distances du récit','2 m, puis 6 m, puis 10 m. Les distances sont interprétées entre axes de virage, puis jusqu’à la porte P1. Largeur du couloir de 6 m : 1,50 m.'),
('Deux virages élargis H','Zones de 1,80 × 1,80 m aux repères 5 et 6. Elles facilitent les rotations de l’empreinte d’essai avec sa marge. Leur présence réelle est à vérifier.'),
('Dépôt prioritaire : n° 3','Trois zones C1 / C2 / C3 dans la même salle : hypothèse de travail. Réceptions et positions d’accostage indicatives, sans mécanisme encore dimensionné.'),
('Autres salles','Dépôt 1 : solution de repli après autorisation. Dépôt 2 : fonction à préciser. La disposition des trois portes et les dimensions des salles sont entièrement provisoires.'),
('Après livraison','Sortie du dépôt 3 et attente dans l’emplacement violet. Aucune instruction de retour n’est déclenchée automatiquement.')])
pages.append(p)

# Collision verification with a conservative, rectangular clearance envelope.
def obb(x,y,yaw,L=1.30,B=.90):
    c=math.cos(yaw);s=math.sin(yaw)
    return [(x+u*c-v*s,y+u*s+v*c) for u,v in [(-L/2,-B/2),(L/2,-B/2),(L/2,B/2),(-L/2,B/2)]]
def intersects(poly,r):
    x0,y0,x1,y1=r; rect=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    axes=[(1,0),(0,1)]
    for a,b in zip(poly,poly[1:]+poly[:1]): axes.append((-(b[1]-a[1]),b[0]-a[0]))
    for ax,ay in axes:
        u=[x*ax+y*ay for x,y in poly];v=[x*ax+y*ay for x,y in rect]
        if max(u)<=min(v)+1e-9 or max(v)<=min(u)+1e-9:return False
    return True
def point_on_floors(x,y,floors):
    return any(a-1e-8<=x<=c+1e-8 and b-1e-8<=y<=d+1e-8 for a,b,c,d in floors)
def inside_union(poly,floors):
    # Floor-union containment is checked by dense interior samples (50 mm),
    # including the polygon corners and edge samples.
    cx=sum(p[0] for p in poly)/4;cy=sum(p[1] for p in poly)/4
    u=((poly[1][0]-poly[0][0])/1.3,(poly[1][1]-poly[0][1])/1.3)
    v=((poly[3][0]-poly[0][0])/.9,(poly[3][1]-poly[0][1])/.9)
    for i in range(27):
        for j in range(19):
            a=-.65+i*1.3/26;b=-.45+j*.9/18
            if not point_on_floors(cx+a*u[0]+b*v[0],cy+a*u[1]+b*v[1],floors):return False
    return True
def motion_samples(points,initial_yaw=None,reverse=False):
    last=initial_yaw
    for a,b in zip(points,points[1:]):
        yaw=math.atan2(b[1]-a[1],b[0]-a[0]) + (math.pi if reverse else 0)
        if last is not None:
            diff=(yaw-last+math.pi)%(2*math.pi)-math.pi
            steps=max(1,math.ceil(abs(diff)/math.radians(2)))
            for i in range(steps+1):yield a[0],a[1],last+diff*i/steps,'rotation'
        steps=max(1,math.ceil(math.dist(a,b)/.025))
        for i in range(steps+1):yield a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps,yaw,'translation'
        last=yaw
def check_path(name,pts,floors,objects,initial_yaw=None,reverse=False):
    failures=[]; count=0
    for x,y,yaw,kind in motion_samples(pts,initial_yaw,reverse):
        count+=1; poly=obb(x,y,yaw)
        hits=[o['name'] for o in objects if intersects(poly,o['rect'])]
        outside=not inside_union(poly,floors)
        if hits or outside:
            if len(failures)<8:failures.append({'x':round(x,3),'y':round(y,3),'yaw':round(yaw,3),'kind':kind,'collisions':hits,'outside_floor':outside})
    return {'name':name,'samples':count,'status':'PASS' if not failures else 'FAIL','first_failures':failures}

checks=[]
checks.append(check_path('N? : collecte vers cabine',n1_route,n1_floors,n1_walls+n1_furniture))
checks.append(check_path('RDC : cabine vers dépôt 3 / C1',rdc_route,rdc_floors,rdc_walls+rdc_objects))
checks.append(check_path('RDC : retour du dépôt vers attente',wait_route,rdc_floors,rdc_walls+rdc_objects,math.pi/2))
# Each reception uses a withdrawal to y=11.05, transit, then a northward docking.
for i,x in enumerate([10.85,12.0,13.15]):
    checks.append(check_path('Accostage C'+str(i+1),[[10.85 if i==1 else 12.0,11.05],[x,11.05],[x,11.95]] if i else [[x,11.05],[x,11.95]],rdc_floors,rdc_walls+rdc_objects,math.pi/2))
    checks.append(check_path('Recul après réception C'+str(i+1),[[x,11.95],[x,11.05 if i<2 else 11.54]],rdc_floors,rdc_walls+rdc_objects,math.pi/2,reverse=True))
checks.append(check_path('RDC : repli dépôt 1',[[8.8,4.8],[11.2,4.8]],rdc_floors,rdc_walls+rdc_objects))
lift_hits=[]
for i in range(91):
    poly=obb(-5.12,1,math.pi/2+math.pi*i/90)
    if any(intersects(poly,o['rect']) for o in shaft_walls) or not inside_union(poly,[shaft]):lift_hits.append(i)
checks.append({'name':'Demi-tour de 180° dans cabine','samples':91,'status':'PASS' if not lift_hits else 'FAIL','first_failures':lift_hits[:8]})

model={
 'project':'AGV bancaire - plan de principe', 'version':'0.1', 'date':'2026-10-20',
 'units':'m', 'coordinate_system':{'x':'est','y':'nord','z':'haut','origin':'angle intérieur sud-ouest de la collecte','floor_elevations':{'RDC':0,'N?':3.0},'upper_elevation_is_hypothesis':True},
 'dimension_status':{'D':'donnée fournie dans le récit, non relevée sur site','H':'hypothèse de conception'},
 'robot':{'cargo_enclosure_given_m':[1,.5,.75],'trial_footprint_hypothesis_m':[1.1,.7],'geometric_clearance_hypothesis_m':.1,'conservative_control_envelope_m':[1.3,.9],'cargo_content_mass_kg':160,'cargo_mass_is_estimate':True},
 'lift':{'center_xy':[-5.12,1],'clear_inside_hypothesis_m':[2.2,2.2],'clear_door_hypothesis_m':1.2,'south_single_door_is_hypothesis':True,'turn_inside_before_exit_rdc':True},
 'levels':{'N?':{'walkable_rectangles':n1_floors,'wall_rectangles':n1_walls,'furniture_rectangles':n1_furniture,'route_xy':n1_route},'RDC':{'walkable_rectangles':rdc_floors,'wall_rectangles':rdc_walls,'reception_rectangles':rdc_objects,'route_xy':rdc_route,'exit_to_wait_route_xy':wait_route,'waiting_pose_xy_yaw':[7.8,10.4,-math.pi/2]}},
 'sorting':{'is_hypothesis_all_categories_inside_depot_3':True,'C1':[100,200,500],'C2':[1000,2000,5000],'C3':[10000,20000],'priority_depot':3,'authorized_fallback_depot':1,'depot_2_role':None},
 'checks':{'method':'Sampled oriented rectangular footprint against wall/furniture rectangles; sampled floor containment; doors modelled open. Translation step <= 0.025 m; angular step <= 2 degrees. Envelope 1.30 x 0.90 m includes a conservative 0.10 m margin around trial body.','limitations':'Geometry only; no braking, dynamics, bag transfer, moving people or localisation uncertainty simulation. Site dimensions remain unverified.','results':checks}
}
(SRC/'geometrie_AGV_v0_1.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')

p=Page(); frame(p,3,'Hypothèses, repères et vérifications','Base modifiable pour préparer le bâtiment 3D. Les éléments H ne décrivent pas une mesure réelle du bâtiment.','sans échelle')

def table(p,x,y,width,columns,rows,col_fracs,fontsize=8,rowheight=29):
    xx=[x]
    for f in col_fracs:xx.append(xx[-1]+width*f)
    p.rect(x,y-rowheight,width,rowheight,INK)
    for i,h in enumerate(columns):p.text(xx[i]+9,y-18,h,fontsize,WHITE,True)
    yy=y-rowheight
    for n,row in enumerate(rows):
        p.rect(x,yy-rowheight,width,rowheight,PAPER if n%2==0 else WHITE)
        p.line([(x,yy-rowheight),(x+width,yy-rowheight)],LIGHT,.5)
        for i,s in enumerate(row):p.text(xx[i]+9,yy-rowheight/2-3,str(s),fontsize,INK)
        yy-=rowheight
    return yy

p.text(40,718,'01  Ce qui est fourni et ce qui est proposé',12,INK,True)
y=table(p,40,700,680,['Élément','Valeur','Statut'],[
('Salle de collecte','8,00 × 6,00 m','D'),('Pièce A au sud-est','4,00 × 3,00 m','D'),('Parcours hors salles','6 m / ascenseur / 2 m / 6 m / 10 m','D - environ'),('Largeur couloir intermédiaire','1,50 m utile','D'),('Coffre du robot','1,00 × 0,50 × 0,75 m','D / sens H'),('Pièce B / bureaux / emplacement exact','2 × 3 m / tables 1,40 × 0,60 m','H'),('Murs / cloisons','0,15 m / 0,12 m','H'),('Portes de circulation','1,20 m utiles, coulissantes','H'),('Cabine ascenseur','2,20 × 2,20 m utiles, porte au sud','H'),('Dépôts 1 et 2 / dépôt 3','4 × 3 m / 4 × 4 m utiles','H'),('Hall / dernier couloir / virages','3,00 m / 1,80 m / carrés 1,80 m','H'),('Écart d’altitude N? - RDC','3,00 m pour la future maquette','H')],[.38,.48,.14],7.4,27)
p.text(40,y-30,'02  Contrôle de passage de l’empreinte d’essai',12,INK,True)
p.wrap(40,y-49,'Châssis proposé pour les essais : 1,10 × 0,70 m. Enveloppe de contrôle : 1,30 × 0,90 m, incluant 0,10 m de marge sur chaque face. Diamètre conservateur de rotation : 1,58 m. Portes considérées ouvertes.',680,8.2,INK)
result_text='Tous les parcours géométriques contrôlés passent.' if all(q['status']=='PASS' for q in checks) else 'Un ou plusieurs contrôles doivent encore être corrigés.'
p.text(40,y-101,result_text,9,TEAL if all(q['status']=='PASS' for q in checks) else AMBER,True)
p.wrap(40,y-119,'Contrôles échantillonnés tous les 2,5 cm au plus et tous les 2° au plus : murs, mobilier, seuils, rotations, accès aux trois zones, repli dépôt 1 et retour en attente. Le détail est conservé dans les sources JSON.',680,8,INK)
p.wrap(40,y-165,'Portée : faisabilité géométrique de cet avant-projet uniquement. Les masses, le freinage, les personnes en mouvement, les erreurs de localisation et le déchargement mécanique seront étudiés dans la simulation.',680,8,MUTED)

p.rect(755,92,405,645,PAPER)
p.text(773,710,'03  Repères de parcours',12,INK,True)
table(p,773,692,368,['Repère','x (est)','y (nord)'],[
('S0 - chargement','5,00','4,80'),('1 - passage ouest','0,88','4,65'),('2 - sortie / virage','0,88','-1,20'),('3 / 4 - palier ascenseur','-5,12','-1,20'),('A - centre cabine','-5,12','1,00'),('5 - après 2 m','-3,12','-1,20'),('6 - après 6 m','-3,12','4,80'),('7 - porte après 10 m','6,88','4,80'),('Attente après dépôt','7,80','10,40')],[.56,.22,.22],7.3,24)
p.text(773,407,'04  Tri proposé dans le dépôt 3',11,INK,True)
table(p,773,391,368,['Zone','Billets en Ar'],[('C1','100 / 200 / 500'),('C2','1 000 / 2 000 / 5 000'),('C3','10 000 / 20 000')],[.20,.80],8,25)
p.text(773,268,'05  Informations à corriger en priorité',11,INK,True)
p.wrap(773,249,'1. Forme et taille de la pièce B, des bureaux et de leurs portes.\n2. Largeur réelle de chaque porte et des paliers de virage.\n3. Cabine, nombre de portes, niveaux et hauteur d’étage.\n4. Disposition et taille des trois dépôts.\n5. Confirmation : trois zones de catégories dans le dépôt 3.\n6. Dimensions des sacs et du châssis complet.',368,8,INK,leading=12)
pages.append(p)

pdfpath=OUT/'Plan_AGV_Bancaire_Deux_Niveaux_v0_1.pdf'
c=canvas.Canvas(str(pdfpath),pagesize=(W,H),pageCompression=1)
c.setTitle('AGV bancaire - Plan 2D coté des deux niveaux - V0.1')
c.setAuthor('Projet AGV bancaire')
c.setSubject('Avant-projet de simulation : collecte, ascenseur, dépôts et hypothèses')
for i,p in enumerate(pages,1):
    p.pdf(c);c.showPage()
    p.svg(SRC/f'plan_{i:02d}.svg')
c.save()

readme='''AGV BANCAIRE - AVANT-PROJET 2D V0.1
Date : 20 octobre 2026

Contenu
- plan_01.svg : niveau de départ, échelle 1:50 en A3 paysage.
- plan_02.svg : rez-de-chaussée, échelle 1:100 en A3 paysage.
- plan_03.svg : hypothèses et repères, sans échelle.
- geometrie_AGV_v0_1.json : coordonnées, rectangles de sols, murs, mobilier,
  itinéraires, zones de tri et résultats des contrôles géométriques.
- build_agv_plans.py : générateur Python (ReportLab et polices DejaVu Sans).

Conventions
Toutes les coordonnées du JSON sont en mètres. X est orienté vers l’est,
Y vers le nord, Z vers le haut. Origine à l’angle intérieur sud-ouest de
la salle de collecte. L’ascenseur A est au même X/Y aux deux niveaux.
L’altitude du niveau de départ est seulement proposée à +3 m.
D = dimension issue du descriptif utilisateur, non relevée sur site.
H = hypothèse géométrique de conception. Les cotes des pièces sont utiles,
entre faces intérieures. Les portes sont cotées en largeur libre. Les
distances de déplacement sont interprétées d’axe à axe, sauf le dernier
segment de 10 m qui va de l’axe du virage à la porte P1.

Hypothèses majeures
La première rotation dans la salle de collecte est à droite pour rejoindre
l’ouest en étant initialement orienté au sud. Les trois catégories sont
provisoirement implantées dans le dépôt 3. Le dépôt 1 est un repli à autoriser.
La cabine possède une porte au sud et permet un demi-tour avant la sortie.
Les virages RDC 5 et 6 comportent des zones élargies à 1,80 x 1,80 m.

Validation
Les contrôles testent une enveloppe orientée 1,30 x 0,90 m, construite autour
d’un châssis d’essai 1,10 x 0,70 m avec une marge de 0,10 m sur chaque face.
Pas de translation <= 0,025 m ; pas angulaire <= 2 degrés.
Test SAT pour les collisions, inclusion du sol échantillonnée à 0,05 m.
Toutes les portes sont considérées ouvertes. Le JSON donne les résultats.
Ce contrôle de principe ne valide pas le freinage, les masses et la stabilité,
la présence humaine, la localisation ni le mécanisme de transfert des sacs.

Les dessins SVG sont modifiables dans un éditeur vectoriel. Imprimer le PDF
à 100 % sur papier A3 pour respecter les échelles nominales ; une impression
« adapter à la page » les modifie. Utiliser les barres d’échelle après export.
'''
(SRC/'LIRE_MOI.txt').write_text(readme,encoding='utf-8')
# The source is included so dimensions and assumptions can be regenerated.
(SRC/'build_agv_plans.py').write_text(Path(__file__).read_text(encoding='utf-8'),encoding='utf-8')
with zipfile.ZipFile(OUT/'Sources_Plan_AGV_v0_1.zip','w',zipfile.ZIP_DEFLATED) as z:
    for q in sorted(SRC.iterdir()):z.write(q,q.name)
(TMP/'verification.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(pdfpath),'checks':checks},ensure_ascii=False,indent=2))
