'use strict';
// KosmoTIC City · Vista visual V1.2
// Mapa con accesos superpuestos sobre la imagen original de la ciudad, aportada
// y autorizada para su publicación por Antonio Alarcón (generada bajo su
// dirección con IA del ecosistema Inter-IA), y listado accesible estático.
// Ambos abren el mismo detalle de cada espacio.
// Preservación de enlaces heredados del portal (antes en /city/#ancla)
const legacyAnchors={'kosmotic':'kosmotic','biblioteca-city':'biblioteca-city','negocios-city':'negocios-city','comunidad-city':'comunidad-city','academia-city':'academia-city','proyectos-city':'proyectos-city','membresias-city':'membresias-city','inventario':'inventario','principios':'principios','genesis':'genesis','retos':'retos','proposito':'proposito','practica':'practica','areas':'areas','mapa':'mapa','contenido':'contenido','academia':'academia-city','acceso':'membresias-city','confianza-city':'confianza-city','comercio-city':'comercio-city','cultura-city':'cultura-city','datos-city':'datos-city','observatorio-city':'observatorio-city','sostenibilidad-city':'sostenibilidad-city','contenido-futuro':'areas','genesis-titulo':'genesis-titulo','horizonte-futuro':'principios','mapa-titulo':'mapa-titulo','meta-inv-clear':'meta-inv-clear','meta-inv-count':'meta-inv-count','meta-inv-query':'meta-inv-query','metacerebro':'metacerebro','navegacion-final':'navegacion-final','participar':'comunidad-city','principios-titulo':'principios-titulo'};
const legacyDest=legacyAnchors[location.hash.slice(1)];
if(legacyDest){location.replace('./portal/#'+legacyDest)}
const spaces=[
{id:'biblioteca',status:'En obras · primeras referencias disponibles',content:'biblioteca-city',x:50.7,y:20.0,w:17.0,h:26.0,name:'Biblioteca KosmoTIC',description:'Espacio previsto para organizar y descubrir recursos, documentos y conocimiento.'},
{id:'negocios',status:'En obras',content:'negocios-city',x:31.2,y:23.0,w:17.0,h:16.0,name:'Centro de Negocios y Red',description:'Espacio previsto para conectar iniciativas, organizaciones y oportunidades de colaboración.'},
{id:'confianza',status:'En obras',content:'confianza-city',x:22.6,y:40.0,w:14.0,h:18.0,name:'Círculo de Confianza',description:'Espacio previsto para relaciones basadas en confianza, transparencia y colaboración.'},
{id:'comunidad',status:'En obras',content:'comunidad-city',x:50.5,y:47.0,w:20.0,h:19.0,name:'Comunidad KosmoTIC',description:'Punto de encuentro central de las personas que forman la ciudad.'},
{id:'inter-ia',status:'Presentación piloto disponible',content:'inter-ia',x:71.0,y:23.9,w:18.0,h:18.8,name:'Inter-IA · Laboratorio Cognitivo',description:'Espacio de presentación del laboratorio cognitivo Inter-IA, bajo supervisión humana.'},
{id:'formacion',status:'En obras · práctica L10 disponible',content:'academia-city',x:90.0,y:31.0,w:10.7,h:22.0,name:'Formación y Talento',description:'Espacio previsto para aprendizaje, habilidades y desarrollo del talento.'},
{id:'comercio',status:'En preparación',content:'comercio-city',x:77.3,y:42.1,w:13.7,h:16.8,name:'Comercio Local',description:'Espacio previsto para dar visibilidad al comercio y a la actividad local.'},
{id:'innovacion',status:'En obras',content:'proyectos-city',x:88.5,y:61.5,w:17.0,h:22.0,name:'Innovación y Proyectos',description:'Espacio previsto para iniciativas y proyectos en evolución.'},
{id:'cultura',status:'En preparación',content:'cultura-city',x:19.5,y:61.5,w:16.0,h:22.0,name:'Cultura y Patrimonio',description:'Espacio previsto para contenidos culturales y patrimoniales.'},
{id:'sostenibilidad',status:'En preparación',content:'sostenibilidad-city',x:36.0,y:66.0,w:16.0,h:18.0,name:'Sostenibilidad y Entorno',description:'Espacio previsto para iniciativas relacionadas con el entorno y la sostenibilidad.'},
{id:'datos',status:'En preparación',content:'datos-city',x:69.0,y:64.0,w:16.0,h:21.0,name:'Datos y Resultados',description:'Espacio previsto para información y resultados verificables.'},
{id:'observatorio',status:'En preparación',content:'observatorio-city',x:9.8,y:37.5,w:10.5,h:15.0,name:'Observatorio SACT',description:'Espacio previsto para observación y seguimiento de cuestiones tecnológicas relevantes.'}
];
const reduced=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const detail=document.getElementById('detalle'),title=document.getElementById('detail-title'),description=document.getElementById('detail-description');
let lastTrigger=null;
function showSpace(id,trigger){
const s=spaces.find(item=>item.id===id);if(!s)return false;
if(trigger)lastTrigger=trigger;
title.textContent=s.name;description.textContent=s.description;
const st=document.getElementById('detail-status');if(st){st.innerHTML='<span aria-hidden="true">●</span> '+(s.status||'En preparación · Información pendiente de validar')}
const cl=document.getElementById('content-link');
if(s.content){cl.href='./portal/#'+s.content;cl.hidden=false;cl.textContent='Ver contenido publicado en el portal'}else{cl.hidden=true}
detail.hidden=false;
try{history.replaceState(null,'','#'+s.id)}catch(e){}
detail.scrollIntoView({block:'start',behavior:'instant'});
detail.focus({preventScroll:true});
return true}
function closeDetail(){
detail.hidden=true;
try{history.replaceState(null,'','#espacios')}catch(e){}
document.getElementById('spaces-title').scrollIntoView({behavior:'instant'});
const back=lastTrigger&&document.contains(lastTrigger)?lastTrigger:document.querySelector('.space-link');
back.focus({preventScroll:true})}
// Si la imagen no está disponible (p. ej. pendiente de acreditación), ocultar el mapa
const img=document.querySelector('#mapa-visual img');
function imageFailed(){document.getElementById('mapa-visual').hidden=true;document.getElementById('mapa-pendiente').hidden=false}
if(img){if(img.complete&&img.naturalWidth===0)imageFailed();else img.addEventListener('error',imageFailed)}
// Accesos del mapa (mejora progresiva sobre la imagen)
const hotspots=document.getElementById('hotspots');
if(hotspots){for(const s of spaces){const b=document.createElement('button');b.type='button';b.className='hotspot';b.style.left=s.x+'%';b.style.top=s.y+'%';b.style.width=s.w+'%';b.style.height=s.h+'%';b.textContent=s.name;b.setAttribute('aria-label','Explorar '+s.name);b.addEventListener('click',()=>showSpace(s.id,b));hotspots.append(b)}}
// Barra inferior: Inicio + 12 accesos, mismos destinos que el listado
const iconmenu=document.getElementById('iconmenu');
if(iconmenu){
const order=[{id:null,name:'Inicio'},...spaces];
order.forEach((sp,i)=>{
const b=document.createElement('button');b.type='button';b.className='iconlink';
b.style.left=(4+i*7.46)+'%';b.style.top='93.5%';
if(sp.id){b.setAttribute('aria-label','Explorar '+sp.name);b.addEventListener('click',()=>showSpace(sp.id,b))}
else{b.setAttribute('aria-label','Ir al inicio de la ciudad');b.addEventListener('click',()=>{detail.hidden=true;try{history.replaceState(null,'','#inicio')}catch(e){};window.scrollTo({top:0,behavior:reduced()?'instant':'smooth'});document.querySelector('.brand').focus({preventScroll:true})})}
iconmenu.append(b)})}
// Listado estático: los enlaces fijan el marcador; el detalle se abre con hashchange
for(const a of document.querySelectorAll('.space-link')){const s=spaces.find(sp=>a.getAttribute('href').endsWith('#'+sp.content));if(s){a.addEventListener('click',ev=>{ev.preventDefault();showSpace(s.id,a)})}}
document.getElementById('close-detail').addEventListener('click',closeDetail);
document.querySelectorAll('.return').forEach(el=>el.addEventListener('click',ev=>{ev.preventDefault();closeDetail()}));
function openFromHash(){const id=decodeURIComponent(location.hash.slice(1));if(spaces.some(s=>s.id===id))showSpace(id)}
window.addEventListener('hashchange',openFromHash);
openFromHash();
