const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const entries = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && !reduceMotion.matches) {
  const observer = new IntersectionObserver(items => {
    for (const item of items) {
      if (item.isIntersecting) {
        item.target.classList.remove('pending');
        item.target.classList.add('in-view');
        observer.unobserve(item.target);
      }
    }
  }, { threshold: 0.08 });
  entries.forEach(entry => { entry.classList.add('pending'); observer.observe(entry); });
  reduceMotion.addEventListener('change', event => {
    if (event.matches) { entries.forEach(entry => entry.classList.remove('pending')); observer.disconnect(); }
  });
}
// Content is expanded without JavaScript; enhance with accessible animated controls.
document.querySelectorAll('.milestone-toggle').forEach(button => {
  const panel = document.getElementById(button.getAttribute('aria-controls'));
  button.hidden = false;
  button.setAttribute('aria-expanded', 'false');
  panel.classList.remove('open');
  panel.setAttribute('inert', '');
  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(expanded));
    button.querySelector('.toggle-label').textContent = expanded ? 'Close selected experience' : 'View selected experience';
    panel.classList.toggle('open', expanded);
    panel.toggleAttribute('inert', !expanded);
  });
});
