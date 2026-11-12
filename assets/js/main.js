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
const heroPhotoStage=document.querySelector('.page-index .ref-hero-photo');
if(heroPhotoStage){
 const heroVideo=heroPhotoStage.querySelector('.hero-video');
 if(heroVideo){
  const heroImages=['box-hero-1.png','box-hero-2.png','box-hero-3.png','box-hero-4.png','box-hero-5.png','box-hero-6.png'];
  const stage=document.createElement('div');
  stage.className='hero-image-stage';
  heroImages.forEach((source,index)=>{
   const image=document.createElement('img');
   image.src=`assets/media/hero-products/${source}`;
   image.alt='';
   image.className=index===0?'is-active':'';
   image.loading='eager';
   image.setAttribute('aria-hidden','true');
   stage.append(image);
  });
  heroVideo.replaceWith(stage);
  const videoToggle=heroPhotoStage.querySelector('.hero-video-toggle');
  if(videoToggle)videoToggle.remove();
  let active=0;
   const pagination=[...document.querySelectorAll('.hero-pagination button')];
   const showSlide=index=>{
    const slides=stage.querySelectorAll('img');
    slides[active].classList.remove('is-active');
    active=(index+slides.length)%slides.length;
    slides[active].classList.add('is-active');
    pagination.forEach((button,buttonIndex)=>button.toggleAttribute('aria-current',buttonIndex===active));
   };
   pagination.forEach((button,index)=>button.addEventListener('click',()=>showSlide(index)));
   if(!reducedMotion.matches)window.setInterval(()=>showSlide(active+1),5000);
 }
}
const heroVideo=document.querySelector('.hero-video');
if(heroVideo){
 const control=document.querySelector('.hero-video-toggle');
 let userPaused=false;
 function updateControl(){
  const paused=heroVideo.paused;
  control.textContent=paused?'\u25B6':'\u2161';
  control.setAttribute('aria-label',paused?'Play manufacturing video':'Pause manufacturing video');
 }
 function syncPlayback(){
  if(document.hidden||userPaused||reducedMotion.matches){heroVideo.pause();return;}
  heroVideo.play().catch(updateControl);
 }
 control.hidden=false;
 control.addEventListener('click',()=>{
  if(heroVideo.paused){userPaused=false;heroVideo.play().catch(updateControl);}
  else{userPaused=true;heroVideo.pause();}
 });
 heroVideo.addEventListener('play',updateControl);
 heroVideo.addEventListener('pause',updateControl);
 heroVideo.addEventListener('error',()=>{control.hidden=true;});
 document.addEventListener('visibilitychange',syncPlayback);
 reducedMotion.addEventListener('change',syncPlayback);
 window.addEventListener('pagehide',()=>heroVideo.pause());
 window.addEventListener('pageshow',syncPlayback);
 updateControl();syncPlayback();
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
  items.forEach(item=>{const categories=(item.dataset.categories||item.dataset.category||'').split(' ');item.hidden=value!=='all'&&!categories.includes(value);if(!item.hidden)count++;});
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
