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
