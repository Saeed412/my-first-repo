const toggle = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
const yearEl = document.querySelector('#current-year');

if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

if (toggle && mobileMenu) {
  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!isOpen));
    mobileMenu.hidden = isOpen;
    mobileMenu.classList.toggle('open', !isOpen);
  });
}

const floatingWidget = document.querySelector('.floating-widget ul');

if (floatingWidget) {
  const items = Array.from(floatingWidget.children);
  let index = 0;

  setInterval(() => {
    floatingWidget.style.transition = 'transform 0.6s ease';
    floatingWidget.style.transform = 'translateY(-1.8rem)';

    setTimeout(() => {
      floatingWidget.style.transition = 'none';
      floatingWidget.style.transform = 'translateY(0)';
      floatingWidget.appendChild(items[index % items.length]);
      index += 1;
    }, 600);
  }, 4000);
}

const detailsList = document.querySelectorAll('.faq details');

detailsList.forEach((detail) => {
  detail.addEventListener('toggle', () => {
    if (detail.open) {
      detailsList.forEach((other) => {
        if (other !== detail) {
          other.open = false;
        }
      });
    }
  });
});
