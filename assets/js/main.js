'use strict';
const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
function revealLinkedDetails(){
 const target=document.getElementById(location.hash.slice(1));
 if(target instanceof HTMLDetailsElement)target.open=true;
}
window.addEventListener('hashchange',revealLinkedDetails);
window.addEventListener('pageshow',revealLinkedDetails);
revealLinkedDetails();
const sentinel=document.createElement('div');sentinel.style.cssText='position:absolute;top:80px;width:1px;height:1px;pointer-events:none';document.body.prepend(sentinel);
if('IntersectionObserver'in window)new IntersectionObserver(([entry])=>document.querySelector('.header').classList.toggle('stuck',!entry.isIntersecting)).observe(sentinel);
document.querySelector('.top')?.addEventListener('click',()=>{window.scrollTo({top:0,behavior:reducedMotion.matches?'instant':'smooth'});document.querySelector('.brand').focus({preventScroll:true});});
const footerYear=document.querySelector('#year');
if(footerYear)footerYear.textContent=new Date().getFullYear();
if(window.lucide)lucide.createIcons();
// The homepage product showcase is enhanced by home-banner.js.
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
