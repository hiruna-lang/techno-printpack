'use strict';
const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('#farm-nav');
function closeFarmMenu(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav.classList.contains('open')){closeFarmMenu();toggle.focus();}});
document.addEventListener('click',event=>{if(!event.target.closest('header'))closeFarmMenu();});
nav.addEventListener('click',event=>{if(event.target.closest('a'))closeFarmMenu();});
window.matchMedia('(min-width:761px)').addEventListener('change',closeFarmMenu);
document.querySelector('#year').textContent=new Date().getFullYear();
const photos=[...document.querySelectorAll('.hero-images img')];
const dots=[...document.querySelectorAll('.slide-dots button')];
if(photos.length){
 const hero=document.querySelector('.hero');
 const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
 let current=0,timer=null,paused=motion.matches,hovering=false;
 function show(index){
  current=index;
  photos.forEach((photo,i)=>{photo.classList.toggle('active',i===index);photo.setAttribute('aria-hidden',String(i!==index));});
  dots.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===index)));
 }
 function schedule(){
  clearTimeout(timer);
  if(!paused&&!hovering&&!document.hidden)timer=setTimeout(()=>{const next=(current+1)%photos.length;if(photos[next].complete&&photos[next].naturalWidth)show(next);schedule();},5000);
 }
 dots.forEach((dot,index)=>dot.addEventListener('click',()=>{show(index);schedule();}));
 hero.addEventListener('mouseenter',()=>{hovering=true;schedule();});
 hero.addEventListener('mouseleave',()=>{hovering=false;schedule();});
 hero.addEventListener('focusin',()=>{hovering=true;schedule();});
 hero.addEventListener('focusout',event=>{if(!hero.contains(event.relatedTarget)){hovering=false;schedule();}});
 document.addEventListener('visibilitychange',schedule);
 motion.addEventListener('change',()=>{paused=motion.matches;schedule();});
 window.addEventListener('pagehide',()=>clearTimeout(timer));
 window.addEventListener('pageshow',schedule);
 show(0);schedule();
}
const form=document.querySelector('#enquiry-form');
if(form){const selection=new URLSearchParams(window.location.search).get('produce');if([...form.elements.produce.options].some(option=>option.value===selection))form.querySelector('select').value=selection;form.addEventListener('submit',event=>{event.preventDefault();const data=new FormData(form);const subject='Green Techno Farm enquiry: '+form.elements.produce.selectedOptions[0].text;const body=`Name: ${data.get('name')}\nEmail: ${data.get('email')}\n\n${data.get('message')}`;location.href='mailto:info@technoind.biz?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);document.querySelector('#form-status').textContent='Your enquiry is ready in your email app. You can also email us directly at info@technoind.biz.';});}
