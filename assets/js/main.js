'use strict';
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const menuButton=document.querySelector('.menu-toggle');
const navigation=document.querySelector('#navigation');
function closeMenu(){navigation.classList.remove('open');menuButton.setAttribute('aria-expanded','false');closeDropdowns();}
menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';navigation.classList.toggle('open',open);menuButton.setAttribute('aria-expanded',String(open));});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&navigation.classList.contains('open')){closeMenu();menuButton.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.header'))closeMenu();});
navigation.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
window.matchMedia('(min-width: 1101px)').addEventListener('change',closeMenu);
const dropdowns=[...document.querySelectorAll('.nav-dropdown')];
function revealLinkedDetails(){
 const target=document.getElementById(location.hash.slice(1));
 if(target instanceof HTMLDetailsElement)target.open=true;
}
window.addEventListener('hashchange',revealLinkedDetails);
window.addEventListener('pageshow',revealLinkedDetails);
revealLinkedDetails();
function closeDropdowns(except){document.querySelectorAll('.nav-dropdown').forEach(item=>{if(item!==except){item.classList.remove('is-open');item.querySelector('.dropdown-toggle').setAttribute('aria-expanded','false');}});}
function openDropdown(item){closeDropdowns(item);item.classList.add('is-open');item.querySelector('.dropdown-toggle').setAttribute('aria-expanded','true');}
dropdowns.forEach(item=>{
 const toggle=item.querySelector('.dropdown-toggle');
 const links=[...item.querySelectorAll('.dropdown-panel>a, .dropdown-panel>button')];
 toggle.addEventListener('click',()=>{if(item.classList.contains('is-open'))closeDropdowns();else openDropdown(item);});
 item.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'&&innerWidth>1100)openDropdown(item);});
 item.addEventListener('pointerleave',()=>{if(innerWidth>1100&&!item.contains(document.activeElement))closeDropdowns();});
 item.addEventListener('focusout',e=>{if(innerWidth>1100&&!item.contains(e.relatedTarget))closeDropdowns();});
 item.addEventListener('keydown',e=>{
  const index=links.indexOf(document.activeElement);
  if(e.key==='Escape'&&item.classList.contains('is-open')){e.preventDefault();e.stopPropagation();closeDropdowns();toggle.focus();}
  else if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();openDropdown(item);const next=index<0?(e.key==='ArrowDown'?0:links.length-1):(index+(e.key==='ArrowDown'?1:-1)+links.length)%links.length;links[next].focus();}
  else if(index>=0&&(e.key==='Home'||e.key==='End')){e.preventDefault();links[e.key==='Home'?0:links.length-1].focus();}
 });
});
const sentinel=document.createElement('div');sentinel.style.cssText='position:absolute;top:80px;width:1px;height:1px;pointer-events:none';document.body.prepend(sentinel);
if('IntersectionObserver'in window)new IntersectionObserver(([entry])=>document.querySelector('.header').classList.toggle('stuck',!entry.isIntersecting)).observe(sentinel);
document.querySelector('.top').addEventListener('click',()=>{window.scrollTo({top:0,behavior:reducedMotion.matches?'instant':'smooth'});document.querySelector('.brand').focus({preventScroll:true});});
document.querySelector('#year').textContent=new Date().getFullYear();
if(window.lucide)lucide.createIcons();
const heroPhotoArea=document.querySelector('.ref-hero-photo');
if(heroPhotoArea){
 const firstPhoto=heroPhotoArea.querySelector('img');
 const slides=[firstPhoto];
 firstPhoto.classList.add('hero-slide','is-active');
 [['1618','Manufacturing team operating corrugated machinery'],['1577','Corrugated packaging inside the factory']].forEach(([key,alt])=>{
  const photo=firstPhoto.cloneNode(false);
  photo.src=`assets/media/factory-111A${key}-1600.webp`;
  photo.srcset=`assets/media/factory-111A${key}-640.webp 640w, assets/media/factory-111A${key}-1600.webp 1600w`;
  photo.alt=alt;photo.classList.remove('is-active');photo.setAttribute('aria-hidden','true');photo.removeAttribute('fetchpriority');
  heroPhotoArea.append(photo);slides.push(photo);
 });
 let current=0,timer=null,paused=false;
 const pause=document.createElement('button');pause.type='button';pause.className='hero-autoplay-toggle';pause.textContent='Ⅱ';pause.setAttribute('aria-label','Pause image slideshow');heroPhotoArea.append(pause);
 function stop(){clearInterval(timer);timer=null;}
 function start(){
  stop();pause.hidden=reducedMotion.matches;
  if(paused||reducedMotion.matches||document.hidden)return;
  timer=setInterval(()=>{
   const next=(current+1)%slides.length;
   if(!slides[next].complete||!slides[next].naturalWidth)return;
   slides[current].classList.remove('is-active');slides[current].setAttribute('aria-hidden','true');
   slides[next].classList.add('is-active');slides[next].removeAttribute('aria-hidden');current=next;
   heroPhotoArea.dataset.slide=String(current);
  },5000);
 }
 pause.addEventListener('click',()=>{paused=!paused;pause.textContent=paused?'▶':'Ⅱ';pause.setAttribute('aria-label',paused?'Play image slideshow':'Pause image slideshow');start();});
 document.addEventListener('visibilitychange',start);reducedMotion.addEventListener('change',start);
 window.addEventListener('pagehide',stop);window.addEventListener('pageshow',start);start();
}
if(window.Swiper&&document.querySelector('.swiper'))new Swiper('.swiper',{slidesPerView:1,spaceBetween:24,speed:reducedMotion.matches?0:500,navigation:{nextEl:'.slide-next',prevEl:'.slide-prev'},keyboard:{enabled:true,onlyInViewport:true},a11y:{enabled:true},breakpoints:{701:{slidesPerView:2},1100:{slidesPerView:3}}});
// Native navigation remains immediate; entry motion also works with back/forward cache.
window.addEventListener('pageshow',()=>{document.body.classList.remove('page-enter');requestAnimationFrame(()=>document.body.classList.add('page-enter'));});
window.setupFilters=function(selector){
 const items=[...document.querySelectorAll(selector)];
 const buttons=[...document.querySelectorAll('[data-filter]')];
 const status=document.querySelector('.result-count');
 function filter(value){
  buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===value)));
  let count=0;
  items.forEach(item=>{item.hidden=value!=='all'&&item.dataset.category!==value;if(!item.hidden)count++;});
  if(status)status.textContent=`${count} ${selector.includes('gallery')?'photographs':'packaging options'}`;
  const empty=document.querySelector('.empty-state');if(empty)empty.hidden=count!==0;
  document.dispatchEvent(new Event('galleryfilter'));
  if(window.ScrollTrigger)ScrollTrigger.refresh();
 }
 function filterFromHash(){const hash=location.hash.slice(1);filter(buttons.some(b=>b.dataset.filter===hash)?hash:'all');}
 buttons.forEach(b=>b.addEventListener('click',()=>filter(b.dataset.filter)));
 window.addEventListener('hashchange',filterFromHash);
 filterFromHash();
};
