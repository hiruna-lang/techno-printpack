'use strict';

(() => {
  const section = document.querySelector('.profile-marks-section');
  const original = section?.querySelector('.profile-marks-grid');
  if (!original) return;

  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const viewport = document.createElement('div');
  viewport.className = 'marks-viewport';
  viewport.setAttribute('role', 'group');
  viewport.setAttribute('aria-labelledby', 'profile-marks-title');
  viewport.setAttribute('aria-live', 'off');
  const track = document.createElement('div');
  track.className = 'marks-track';
  track.id = 'quality-marks-track';
  const clone = original.cloneNode(true);
  clone.classList.add('marks-clone');
  clone.hidden = true;
  clone.inert = true;
  clone.setAttribute('aria-hidden', 'true');
  clone.querySelectorAll('[id]').forEach(element => element.removeAttribute('id'));
  clone.querySelectorAll('img').forEach(image => { image.alt = ''; });

  original.before(viewport);
  viewport.append(track);
  track.append(original, clone);
  let ready = false;
  let loading = false;
  let visible = false;
  let pageActive = true;

  function updatePlayback() {
    const enhanced = ready && !motion.matches;
    section.classList.toggle('marks-is-animated', enhanced);
    clone.hidden = !enhanced;
    section.dataset.marksRunning = String(enhanced && visible && pageActive && !document.hidden);
  }

  async function loadMarks() {
    if (loading) return;
    loading = true;
    const images = [...original.querySelectorAll('img'), ...clone.querySelectorAll('img')];
    images.forEach(image => { image.loading = 'eager'; });
    try {
      await Promise.all(images.map(image => image.decode()));
      ready = true;
      updatePlayback();
    } catch {
      // Keep the original grid if a logo cannot load or decode.
    }
  }

  document.addEventListener('visibilitychange', updatePlayback);
  window.addEventListener('pagehide', () => { pageActive = false; updatePlayback(); });
  window.addEventListener('pageshow', () => { pageActive = true; updatePlayback(); });
  motion.addEventListener('change', updatePlayback);

  updatePlayback();
  if ('IntersectionObserver' in window) {
    // Prepare the single-row layout before it reaches the viewport.
    const preload = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { loadMarks(); preload.disconnect(); }
    }, { rootMargin: '400px 0px' });
    preload.observe(section);
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      updatePlayback();
    }, { threshold: .01 }).observe(section);
  } else {
    visible = true;
    loadMarks();
  }
})();
