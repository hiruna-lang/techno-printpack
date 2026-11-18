'use strict';
// Only the product images change. Copy, layout and the first frame are static HTML.
{
 const banner=document.querySelector('.packaging-banner');
 const stage=banner?.querySelector('.banner-product-stage');
 if(stage){
  const slides=[...stage.querySelectorAll('.banner-product')];
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  const interval=5500;
  const failed=new Set(),loads=new Map(),pausedAnimations=new Set();
  let active=0,timer=null,deadline=0,generation=0,inView=true,pageHidden=false;
  const canRun=()=>slides.length>1&&!document.hidden&&!pageHidden&&!motion.matches&&inView;

  function loadSlide(index){
   if(!loads.has(index)){
    const image=slides[index];
    if(image.dataset.src){
     image.srcset=image.dataset.srcset;
     image.src=image.dataset.src;
     delete image.dataset.src;
    }
    const ready=image.decode().catch(error=>{failed.add(index);throw error;});
    loads.set(index,ready);
   }
   return loads.get(index);
  }
  function nextIndex(){
   for(let offset=1;offset<slides.length;offset++){
    const next=(active+offset)%slides.length;
    if(!failed.has(next))return next;
   }
   return -1;
  }
  function prepareNext(){
   const next=nextIndex();
   if(next>=0)loadSlide(next).catch(()=>{});
  }
  function armTimer(){
   clearTimeout(timer);
   if(canRun()&&nextIndex()>=0)timer=setTimeout(advance,Math.max(0,deadline-performance.now()));
  }
  async function advance(){
   timer=null;
   if(!canRun())return;
   const next=nextIndex(),currentGeneration=generation;
   if(next<0)return;
   try{
    await loadSlide(next);
    if(!canRun()||currentGeneration!==generation)return;
    slides[active].classList.remove('is-active');
    active=next;
    slides[active].classList.add('is-active');
   }catch(_){/* Preserve the current image and skip an unavailable asset. */}
   if(!canRun()||currentGeneration!==generation)return;
   // Absolute deadlines avoid accumulating decode/timer delays between frames.
   deadline+=interval;
   if(deadline<=performance.now())deadline=performance.now()+interval;
   prepareNext();armTimer();
  }
  function syncPlayback(){
   clearTimeout(timer);timer=null;generation++;
   if(!canRun()){
    // Freeze an in-progress fade/zoom as well as the automatic image changes.
    stage.getAnimations?.({subtree:true}).forEach(animation=>{
     if(animation.playState==='running'){animation.pause();pausedAnimations.add(animation);}
    });
    if(motion.matches)pausedAnimations.clear();
    return;
   }
   pausedAnimations.forEach(animation=>{if(animation.playState==='paused')animation.play();});
   pausedAnimations.clear();
   deadline=performance.now()+interval;
   prepareNext();armTimer();
  }
  document.addEventListener('visibilitychange',syncPlayback);
  motion.addEventListener('change',syncPlayback);
  window.addEventListener('pagehide',()=>{pageHidden=true;syncPlayback();});
  window.addEventListener('pageshow',()=>{pageHidden=false;syncPlayback();});
  if('IntersectionObserver'in window)new IntersectionObserver(([entry])=>{
   if(inView!==entry.isIntersecting){inView=entry.isIntersecting;syncPlayback();}
  },{threshold:.08}).observe(banner);
  syncPlayback();
 }
}
