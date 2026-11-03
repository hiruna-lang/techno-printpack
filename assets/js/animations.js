'use strict';
if(window.gsap&&window.ScrollTrigger&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
 gsap.registerPlugin(ScrollTrigger);
 gsap.from('.about-hero .container > div > *',{y:15,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 gsap.from('.ref-hero-content > div > *',{y:15,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 gsap.from('.opening-copy > *',{y:14,opacity:0,duration:.65,stagger:.08,ease:'power2.out',clearProps:'all'});
 gsap.from('.opening-photo',{y:12,opacity:0,duration:.85,delay:.1,ease:'power2.out',clearProps:'all'});
 gsap.from('.hero-copy > *, .internal-hero .container > *',{y:30,opacity:0,duration:.85,stagger:.12,ease:'power3.out',clearProps:'all'});
 gsap.from('.hero-image img',{scale:1.07,duration:1.8,ease:'power2.out',clearProps:'transform'});
 document.querySelectorAll('.reveal').forEach(el=>gsap.from(el,{y:35,opacity:0,duration:.8,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:el,start:'top 92%',once:true}}));
 gsap.matchMedia().add('(min-width: 1100px)',()=>{document.querySelectorAll('.wide-photo img').forEach(el=>gsap.fromTo(el,{objectPosition:'center 45%'},{objectPosition:'center 65%',ease:'none',scrollTrigger:{trigger:el,start:'top bottom',end:'bottom top',scrub:1}}));});
}
