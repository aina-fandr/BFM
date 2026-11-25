const fs=require("fs"),path=require("path"),dir=process.argv[2],file=path.join(dir,"AGV_Banc.kicad_pcb");
let pcb=fs.readFileSync(file,"utf8");
const ids=Object.fromEntries([...pcb.matchAll(/^\(net (\d+) "([^"]+)"\)/gm)].map(m=>[m[2],+m[1]]));
const seg=(a,b,n,l)=>'(segment (start '+a.join(" ")+') (end '+b.join(" ")+') (width 0.35) (layer "'+l+'.Cu") (net '+ids[n]+'))';
function replace(a,b,n,l,replacement){
 const original=seg(a,b,n,l);if(!pcb.includes(original))throw Error(original);pcb=pcb.replace(original,replacement);
}
if (!pcb.includes("(start 7 20.08)")) {
for(const y of [17.54,33.54,49.54]){
 replace([56,y],[56,y+16],"GND_LOG","F",[[[56,y],[54,y]],[[54,y],[54,y+16]],[[54,y+16],[56,y+16]]].map(([a,b])=>seg(a,b,"GND_LOG","F")).join("\n"));
}
replace([70,19.08],[76,19.08],"GND_LOG","B",seg([70,19.08],[76,19.08],"GND_LOG","F"));
replace([76,19.08],[78,17],"GND_LOG","B",seg([76,19.08],[78,17],"GND_LOG","F"));
replace([78,17],[80,17],"GND_LOG","B",seg([78,17],[80,17],"GND_LOG","F"));
replace([70,14],[80,14],"5V","B",seg([70,14],[80,14],"5V","F"));
const capTracks=[];
for(const y of [20.08,36.08,52.08,68.08]){
 capTracks.push(seg([10,y],[7,y],"RET_CAPT","F"));
 if(y<68)capTracks.push(seg([7,y],[7,Math.round((y+16)*100)/100],"RET_CAPT","F"));
}
pcb=pcb.replace(/\)\s*$/,capTracks.join("\n")+"\n)");
}
const tracks=[...pcb.matchAll(/\(segment \(start ([-.\d]+) ([-.\d]+)\) \(end ([-.\d]+) ([-.\d]+)\) \(width 0.35\) \(layer "([FB])\.Cu"\) \(net (\d+)\)\)/g)].map(m=>({a:[+m[1],+m[2]],b:[+m[3],+m[4]],layer:m[5],net:+m[6]}));
const pads=[];
let origin;
for(const line of pcb.split("\n")){
 const f=line.match(/^\(footprint "([^"]+)" \(layer "F.Cu"\) \(at ([.\d]+) ([.\d]+)\)/);
 if(f)origin=[+f[2],+f[3]];
 const p=line.match(/^\(pad "(\d+)" thru_hole circle \(at ([-.\d]+) ([-.\d]+)\).*\(net (\d+)/);
 if(p)pads.push({p:[origin[0]+ +p[2],origin[1]+ +p[3]],net:+p[4]});
}
const dist=(p,a,b)=>{
 const dx=b[0]-a[0],dy=b[1]-a[1],den=dx*dx+dy*dy;
 const t=den?Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)):0;
 return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);
};
const cross=(a,b,p)=>(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);
let errors=[];
for(const t of tracks)for(const p of pads)if(t.net!==p.net&&dist(p.p,t.a,t.b)<1.325-1e-8)errors.push(["pad",t,p]);
for(let i=0;i<tracks.length;i++)for(let j=i+1;j<tracks.length;j++){
 const a=tracks[i],b=tracks[j];
 if(a.net===b.net||a.layer!==b.layer)continue;
 const collision=cross(a.a,a.b,b.a)*cross(a.a,a.b,b.b)<0&&cross(b.a,b.b,a.a)*cross(b.a,b.b,a.b)<0;
 if(collision||Math.min(dist(a.a,b.a,b.b),dist(a.b,b.a,b.b),dist(b.a,a.a,a.b),dist(b.b,a.a,a.b))<.55-1e-8)errors.push(["track",a,b]);
}
for(const net of Object.values(ids)){
 const group=pads.filter(p=>p.net===net);
 const available=tracks.filter(t=>t.net===net);
 const seen=new Set();
 const locations=[group[0].p];
 for(let i=0;i<locations.length;i++){
  for(const t of available){
   if(seen.has(t)||dist(locations[i],t.a,t.b)>1e-7)continue;
   seen.add(t);locations.push(t.a,t.b);
  }
 }
 const missing=group.filter(p=>!locations.some(q=>Math.hypot(p.p[0]-q[0],p.p[1]-q[1])<1e-7));
 if(missing.length)errors.push(["connectivity",net,missing]);
}
console.log(JSON.stringify({pads:pads.length,tracks:tracks.length,errors}));
if(errors.length)process.exit(1);
const xy=([x,y])=>"X"+Math.round(x*1e6)+"Y"+Math.round((72-y)*1e6);
for(const layer of ["F","B"]){
 const name=path.join(dir,"Gerber","AGV_Banc-"+layer+"_Cu.gbr");
 const pre=fs.readFileSync(name,"utf8").split("\nD11*\n")[0];
 fs.writeFileSync(name,pre+"\nD11*\n"+tracks.filter(t=>t.layer===layer).flatMap(t=>[xy(t.a)+"D02*",xy(t.b)+"D01*"]).join("\n")+"\nM02*\n");
}
fs.writeFileSync(file,pcb);
