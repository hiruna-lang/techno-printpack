'use strict';
window.setupFilters('.gallery-item');
const lightbox=document.querySelector('.lightbox'),photo=lightbox.querySelector('img'),caption=lightbox.querySelector('figcaption');let current=0,opener=null;
const visiblePhotos=()=>[...document.querySelectorAll('.gallery-item')].filter(x=>!x.hidden);
function showPhoto(index){const list=visiblePhotos();current=(index+list.length)%list.length;photo.src=list[current].dataset.full;photo.alt=list[current].dataset.caption;caption.textContent=`${current+1} / ${list.length} — ${photo.alt}`;}
document.querySelectorAll('.gallery-item').forEach(item=>item.addEventListener('click',()=>{opener=item;showPhoto(visiblePhotos().indexOf(item));lightbox.showModal();document.body.style.overflow='hidden';lightbox.querySelector('.lightbox-close').focus();}));
function closePhoto(){lightbox.close();}
lightbox.querySelector('.lightbox-close').addEventListener('click',closePhoto);
lightbox.querySelector('.lightbox-prev').addEventListener('click',()=>showPhoto(current-1));lightbox.querySelector('.lightbox-next').addEventListener('click',()=>showPhoto(current+1));
lightbox.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();showPhoto(current-1);}if(e.key==='ArrowRight'){e.preventDefault();showPhoto(current+1);}});
lightbox.addEventListener('close',()=>{document.body.style.overflow='';opener?.focus();});
lightbox.addEventListener('click',e=>{if(e.target===lightbox)closePhoto();});
