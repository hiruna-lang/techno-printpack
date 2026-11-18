'use strict';
if (window.gsap && window.ScrollTrigger && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  gsap.registerPlugin(ScrollTrigger);
  const animateIfPresent = (selector, vars) => {
    const targets = document.querySelectorAll(selector);
    if (targets.length) gsap.from(targets, vars);
  };

  animateIfPresent('.about-hero .container > div > *', { y: 14, opacity: 0, duration: 0.6, stagger: 0.07, ease: 'power2.out', clearProps: 'all' });
  animateIfPresent('.banner-copy > *', { y: 10, duration: 0.6, stagger: 0.05, ease: 'power2.out', clearProps: 'transform' });
  animateIfPresent('.ref-hero-content > div > *', { y: 14, opacity: 0, duration: 0.6, stagger: 0.07, ease: 'power2.out', clearProps: 'all' });
  animateIfPresent('.opening-copy > *', { y: 12, opacity: 0, duration: 0.6, stagger: 0.07, ease: 'power2.out', clearProps: 'all' });
  animateIfPresent('.opening-photo', { y: 10, opacity: 0, duration: 0.75, delay: 0.08, ease: 'power2.out', clearProps: 'all' });
  animateIfPresent('.hero-copy > *, .internal-hero .container > *', { y: 18, opacity: 0, duration: 0.7, stagger: 0.09, ease: 'power3.out', clearProps: 'all' });
  animateIfPresent('.hero-image img', { scale: 1.04, duration: 1.4, ease: 'power2.out', clearProps: 'transform' });

  document.querySelectorAll('.corp-heading, .corp-about > div, .corp-process-layout > div, .page-next-cta-inner').forEach(el => {
    gsap.from(el, { y: 14, opacity: 0, duration: 0.6, ease: 'power2.out', clearProps: 'all', scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
  });

  document.querySelectorAll('.reveal').forEach(el => {
    gsap.from(el, { y: 24, opacity: 0, duration: 0.7, ease: 'power2.out', clearProps: 'all', scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
  });

  gsap.matchMedia().add('(min-width: 1100px)', () => {
    document.querySelectorAll('.wide-photo img').forEach(el => {
      gsap.fromTo(el, { objectPosition: 'center 45%' }, { objectPosition: 'center 62%', ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: 1 } });
    });
  });
}
