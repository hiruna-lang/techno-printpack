'use strict';

/**
 * Navigation controller.
 * Manages sticky scroll state, accessible dropdown panels, mobile navigation drawer,
 * and keyboard interactions.
 */
(() => {
  const header = document.querySelector('.header');
  if (!header) return;

  const navigation = header.querySelector('#navigation');
  const menuButton = header.querySelector('.menu-toggle');
  const dropdowns = [...header.querySelectorAll('.nav-dropdown')];
  const desktop = window.matchMedia('(min-width: 1101px)');
  const compactMobile = window.matchMedia('(max-width: 768px)');

  let hoverOpenTimer, hoverCloseTimer;
  const clearHover = () => {
    clearTimeout(hoverOpenTimer);
    clearTimeout(hoverCloseTimer);
  };

  // Scroll detection to update header appearance
  const onScroll = () => {
    header.classList.toggle('stuck', window.scrollY > 15);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Dropdown management
  function setDropdown(dropdown, open) {
    dropdown.classList.toggle('is-open', open);
    const toggle = dropdown.querySelector('.dropdown-toggle');
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
    const panel = dropdown.querySelector('.dropdown-panel');
    if (panel) {
      panel.inert = !open;
      panel.setAttribute('aria-hidden', String(!open));
    }
  }

  function closeAllDropdowns(except) {
    dropdowns.forEach(item => {
      if (item !== except) setDropdown(item, false);
    });
  }

  function openDropdown(item) {
    closeAllDropdowns(item);
    setDropdown(item, true);
  }

  // Mobile navigation drawer (< 1100px)
  function setMobileMenu(open) {
    clearHover();
    if (!navigation) return;
    const isMobile = !desktop.matches;
    navigation.classList.toggle('open', open && isMobile);
    if (menuButton) {
      menuButton.setAttribute('aria-expanded', String(open && isMobile));
    }
    navigation.inert = isMobile && !open;
    if (isMobile && !open) {
      navigation.setAttribute('aria-hidden', 'true');
    } else {
      navigation.removeAttribute('aria-hidden');
    }
    if (!open) {
      closeAllDropdowns();
    }
  }

  // Mobile menu button toggle
  if (menuButton) {
    menuButton.addEventListener('click', event => {
      event.stopPropagation();
      const isOpen = navigation?.classList.contains('open');
      setMobileMenu(!isOpen);
      // The drawer precedes its toggle in the DOM. Move keyboard users into
      // the opened links instead of letting the next Tab skip to the hero.
      if (!isOpen && compactMobile.matches) {
        navigation.querySelector('a[href]')?.focus({ preventScroll: true });
      }
    });
  }

  header.addEventListener('focusout', () => {
    if (!compactMobile.matches) return;
    requestAnimationFrame(() => {
      if (!header.contains(document.activeElement)) setMobileMenu(false);
    });
  });

  // Dropdowns interaction
  dropdowns.forEach(dropdown => {
    const heading = dropdown.querySelector('.nav-dropdown-heading');
    const headingLink = dropdown.querySelector('.nav-dropdown-heading > a.nav-link');
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const items = [...dropdown.querySelectorAll('.dropdown-item')];

    const toggleDropdown = event => {
      event.preventDefault();
      event.stopPropagation();
      clearHover();
      const isOpen = dropdown.classList.contains('is-open');
      if (isOpen) {
        setDropdown(dropdown, false);
      } else {
        openDropdown(dropdown);
      }
    };

    if (headingLink) {
      headingLink.addEventListener('click', toggleDropdown);
    }
    if (toggle) {
      toggle.addEventListener('click', toggleDropdown);
    }
    if (heading) {
      heading.addEventListener('click', event => {
        if (event.target === heading) toggleDropdown(event);
      });
    }

    // Hover open/close on desktop
    dropdown.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' || !desktop.matches) return;
      clearHover();
      hoverOpenTimer = setTimeout(() => openDropdown(dropdown), 75);
    });

    dropdown.addEventListener('pointerleave', event => {
      if (event.pointerType !== 'mouse' || !desktop.matches) return;
      clearHover();
      hoverCloseTimer = setTimeout(() => {
        if (!dropdown.contains(document.activeElement)) {
          setDropdown(dropdown, false);
        }
      }, 160);
    });

    // Keyboard support
    dropdown.addEventListener('keydown', event => {
      const activeIdx = items.indexOf(document.activeElement);
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        clearHover();
        openDropdown(dropdown);
        const nextIdx =
          activeIdx < 0
            ? event.key === 'ArrowDown'
              ? 0
              : items.length - 1
            : (activeIdx + (event.key === 'ArrowDown' ? 1 : -1) + items.length) % items.length;
        items[nextIdx]?.focus();
      } else if (activeIdx >= 0 && (event.key === 'Home' || event.key === 'End')) {
        event.preventDefault();
        items[event.key === 'Home' ? 0 : items.length - 1]?.focus();
      }
    });
  });

  // Global click outside to dismiss
  document.addEventListener('pointerdown', event => {
    if (!header.contains(event.target)) {
      closeAllDropdowns();
      setMobileMenu(false);
    }
  });

  // Global escape key handler
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      const openDd = dropdowns.find(d => d.classList.contains('is-open'));
      if (openDd) {
        event.preventDefault();
        clearHover();
        closeAllDropdowns();
        openDd.querySelector('.dropdown-toggle')?.focus();
        return;
      }
      if (navigation?.classList.contains('open')) {
        event.preventDefault();
        setMobileMenu(false);
        menuButton?.focus();
      }
    }
  });

  // Close menus on page navigation
  if (navigation) {
    navigation.addEventListener('click', event => {
      if (event.target.closest('.nav-dropdown-heading')) return;
      if (event.target.closest('a')) {
        setMobileMenu(false);
        closeAllDropdowns();
      }
    });
  }

  // Handle breakpoint switches
  desktop.addEventListener('change', () => {
    setMobileMenu(false);
    closeAllDropdowns();
  });

  // Initial state setup
  closeAllDropdowns();
  setMobileMenu(false);
  header.classList.add('nav-ready');
})();
