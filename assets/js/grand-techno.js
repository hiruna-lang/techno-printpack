'use strict';
const viewer = document.querySelector('.lightbox');
let lastPhoto;
document.querySelectorAll('.gallery-item').forEach(button => button.addEventListener('click', () => { lastPhoto = button; const source = button.querySelector('img'); viewer.querySelector('img').src = source.src; viewer.querySelector('img').alt = source.alt; viewer.querySelector('p').textContent = source.alt; viewer.showModal(); }));
viewer.querySelector('button').addEventListener('click', () => viewer.close());
viewer.addEventListener('click', event => { if (event.target === viewer) { const r = viewer.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) viewer.close(); } });
viewer.addEventListener('close', () => lastPhoto?.focus());
document.getElementById('year').textContent = new Date().getFullYear();

// Rotate only when the page is visible and motion is welcome.
const heroFrame = document.querySelector('.hero-image');
if (heroFrame) {
  const slides = [...heroFrame.querySelectorAll('.hero-slide')];
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0, timer = null;
  function stopSlides() { clearInterval(timer); timer = null; }
  function startSlides() {
    stopSlides();
    if (motion.matches || document.hidden || slides.length < 2) return;
    timer = setInterval(() => {
      const next = (current + 1) % slides.length;
      if (!slides[next].complete || !slides[next].naturalWidth) return;
      slides[current].classList.remove('is-active');
      slides[current].setAttribute('aria-hidden', 'true');
      slides[next].classList.add('is-active');
      slides[next].removeAttribute('aria-hidden');
      current = next;
    }, 5000);
  }
  document.addEventListener('visibilitychange', startSlides);
  motion.addEventListener('change', startSlides);
  window.addEventListener('pagehide', stopSlides);
  window.addEventListener('pageshow', startSlides);
  startSlides();
}
