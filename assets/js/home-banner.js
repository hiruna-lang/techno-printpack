'use strict';
// Progressive enhancement: the first product image and all copy are static HTML.
{
 const banner=document.querySelector('.packaging-banner');
 if(banner){
  const slides=[...banner.querySelectorAll('.banner-product')];
  const control=banner.querySelector('.banner-playback');
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  const failedSlides=new Set();
  let active=0,paused=motion.matches,inView=true,timer=null;
  const stop=()=>{clearTimeout(timer);timer=null;};
  function updateControl(){
   control.querySelector('.banner-playback-icon').textContent=paused?'\u25b6':'\u2161';
   control.querySelector('.banner-playback-label').textContent=paused?'Play':'Pause';
   control.setAttribute('aria-label',paused?'Play packaging images':'Pause packaging images');
  }
  async function loadSlide(slide){
   if(slide.dataset.src){
    slide.srcset=slide.dataset.srcset;
    slide.src=slide.dataset.src;
    delete slide.dataset.src;
   }
   await slide.decode();
  }
  function schedule(){
   stop();updateControl();
   if(paused||!inView||document.hidden||slides.length<2)return;
   timer=setTimeout(async()=>{
    let next=(active+1)%slides.length;
    while(failedSlides.has(next)&&next!==active)next=(next+1)%slides.length;
    if(next===active)return;
    try{
     await loadSlide(slides[next]);
     if(paused||!inView||document.hidden)return;
     slides[active].classList.remove('is-active');
     active=next;slides[active].classList.add('is-active');
    }catch(_){failedSlides.add(next);/* Keep the current image and skip this failed asset on the next cycle. */}
    schedule();
   },6500);
  }
  control.hidden=false;
  control.addEventListener('click',()=>{paused=!paused;schedule();});
  document.addEventListener('visibilitychange',schedule);
  motion.addEventListener('change',event=>{paused=event.matches;schedule();});
  window.addEventListener('pagehide',stop);
  window.addEventListener('pageshow',schedule);
  if('IntersectionObserver'in window)new IntersectionObserver(([entry])=>{inView=entry.isIntersecting;schedule();},{threshold:.08}).observe(banner);
  schedule();
 }
}
