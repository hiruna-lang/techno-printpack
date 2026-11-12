'use strict';
if(window.gsap&&window.ScrollTrigger&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
 gsap.registerPlugin(ScrollTrigger);
 gsap.from('.about-hero .container > div > *',{y:15,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 gsap.from('.ref-hero-content > div > *',{y:15,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 document.querySelectorAll('.corp-heading, .corp-about > div, .corp-process-layout > div').forEach(el=>gsap.from(el,{y:16,opacity:0,duration:.65,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:el,start:'top 92%',once:true}}));
 gsap.from('.opening-copy > *',{y:14,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 gsap.from('.opening-photo',{y:12,opacity:0,duration:.85,delay:.1,ease:'power2.out',clearProps:'all'});
 gsap.from('.hero-copy > *, .internal-hero .container > *',{y:30,opacity:0,duration:.85,stagger:.12,ease:'power3.out',clearProps:'all'});
 gsap.from('.hero-image img',{scale:1.07,duration:1.8,ease:'power2.out',clearProps:'transform'});
 const hero=document.querySelector('.page-index .corp-hero');
 const heroStage=hero?.querySelector('.hero-image-stage');
 if(hero&&heroStage){
  const heroSlides=[...heroStage.querySelectorAll('img')];
  const animateHeroSlide=slide=>{
   gsap.killTweensOf(slide);
   gsap.fromTo(slide,{y:34,rotateY:-8,rotateZ:-1.2,scale:.92,transformOrigin:'50% 70%'},{y:0,rotateY:0,rotateZ:0,scale:1,duration:1.25,ease:'power3.out'});
   gsap.to(slide,{y:-7,rotateZ:.35,duration:3.4,repeat:-1,yoyo:true,ease:'sine.inOut',delay:1.25});
  };
  animateHeroSlide(heroSlides[0]);
  heroStage.addEventListener('hero-slide-change',event=>animateHeroSlide(event.detail.slide));
  gsap.to(heroStage,{y:35,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:1}});
  gsap.to(heroStage.querySelector('.hero-feature-strip'),{y:-5,duration:3.8,repeat:-1,yoyo:true,ease:'sine.inOut'});
 }
 document.querySelectorAll('.reveal').forEach(el=>gsap.from(el,{y:35,opacity:0,duration:.8,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:el,start:'top 92%',once:true}}));
 gsap.matchMedia().add('(min-width: 1100px)',()=>{document.querySelectorAll('.wide-photo img').forEach(el=>gsap.fromTo(el,{objectPosition:'center 45%'},{objectPosition:'center 65%',ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'bottom top',scrub:1}}));});
}
