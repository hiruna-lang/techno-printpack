'use strict';
const galleryButtons = [...document.querySelectorAll('[data-gallery-filter]')];
const galleryPhotos = [...document.querySelectorAll('.story-photo')];
const photoGrid = document.querySelector('.story-photo-grid');
const galleryStatus = document.querySelector('.gallery-status');
galleryButtons.forEach(button => button.addEventListener('click', () => {
 const filter = button.dataset.galleryFilter;
 galleryButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
 galleryPhotos.forEach(photo => { photo.hidden = filter !== 'all' && photo.dataset.category !== filter; });
 photoGrid.classList.toggle('is-filtered', filter !== 'all');
 const count = galleryPhotos.filter(photo => !photo.hidden).length;
 galleryStatus.textContent = filter === 'all' ? `Showing all ${count} photos` : `Showing ${count} ${button.textContent.trim()} photos`;
}));
const lightbox = document.querySelector('.story-lightbox');
let lastPhoto;
galleryPhotos.forEach(button => button.addEventListener('click', () => {
 const photo = button.querySelector('img');
 lastPhoto = button;
 lightbox.querySelector('img').src = photo.src;
 lightbox.querySelector('img').alt = photo.alt;
 lightbox.querySelector('p').textContent = photo.alt;
 lightbox.showModal();
}));
lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', event => { if (event.target === lightbox) { const bounds = lightbox.getBoundingClientRect(); if(event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) lightbox.close(); } });
lightbox.addEventListener('close', () => lastPhoto?.focus());
