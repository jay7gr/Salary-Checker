/* Kloster Lebensquell — small progressive enhancements */

(function () {
  'use strict';

  // Sticky nav on scroll
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 60) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Mobile toggle (simple)
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      links.style.display = open ? 'flex' : '';
      links.style.position = open ? 'absolute' : '';
      links.style.top = open ? '100%' : '';
      links.style.left = open ? '0' : '';
      links.style.right = open ? '0' : '';
      links.style.background = open ? 'var(--ivory)' : '';
      links.style.padding = open ? '2rem' : '';
      links.style.flexDirection = open ? 'column' : '';
      links.style.gap = open ? '1.5rem' : '';
      links.style.borderBottom = open ? '1px solid var(--line)' : '';
      // Ensure links render in forest color when the menu is open over ivory
      if (open) {
        links.querySelectorAll('a').forEach(a => a.style.color = 'var(--forest-deep)');
      } else {
        links.querySelectorAll('a').forEach(a => a.style.color = '');
      }
    });
  }

  // Reveal on scroll
  const revealTargets = document.querySelectorAll(
    '.section-head, .pillar, .team-card, .sched-item, .grid-2 .col-prose, .grid-2-wide .col-prose, .grid-2-wide .col-image, blockquote, .cta-inner, .prog-block'
  );
  revealTargets.forEach(el => el.classList.add('reveal'));

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealTargets.forEach(el => io.observe(el));
  } else {
    revealTargets.forEach(el => el.classList.add('in'));
  }

  // Smooth anchor for in-page links (accounts for sticky nav)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href');
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          const y = target.getBoundingClientRect().top + window.scrollY - 80;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      }
    });
  });

  // Gentle parallax on hero image
  const heroImg = document.querySelector('.hero-image');
  if (heroImg && window.matchMedia('(min-width: 760px)').matches) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (y < window.innerHeight) {
        heroImg.style.transform = `scale(1.05) translateY(${y * 0.15}px)`;
      }
    }, { passive: true });
  }

  // Contact form (demo, no backend)
  const form = document.getElementById('enquiry-form');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const status = form.querySelector('.form-status');
      if (status) {
        status.textContent = 'Thank you. Your enquiry has been received. A member of our medical team will write to you personally within forty-eight hours.';
        status.style.color = 'var(--gold)';
      }
      form.reset();
    });
  }
})();
