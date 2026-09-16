// Lume — navegação, catálogo, galeria e contacto; sem dependências.
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.nav-links');
  const closeMenu = () => {
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Abrir menu');
  };
  toggle?.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  });
  menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.classList.contains('open')) { closeMenu(); toggle.focus(); }
  });
  window.matchMedia('(min-width:881px)').addEventListener('change', closeMenu);
  const chips = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-category]')];
  function filter(value, updateUrl = true) {
    if (!chips.some(c => c.dataset.filter === value)) value = 'todos';
    chips.forEach(c => { const active = c.dataset.filter === value; c.classList.toggle('active', active); c.setAttribute('aria-pressed', String(active)); });
    let count = 0;
    cards.forEach(card => { const visible = value === 'todos' || card.dataset.category === value; card.style.display = visible ? '' : 'none'; if (visible) count++; });
    document.querySelector('#catalog-status').textContent = `${count} ${count === 1 ? 'produto' : 'produtos'}`;
    if (updateUrl) { const url = new URL(location.href); if (value === 'todos') url.searchParams.delete('categoria'); else url.searchParams.set('categoria', value); history.replaceState(null, '', url); }
  }
  if (chips.length) {
    chips.forEach(c => c.addEventListener('click', () => filter(c.dataset.filter)));
    filter(new URL(location.href).searchParams.get('categoria') || 'todos', false);
  }
  const gallery = document.querySelector('.pd-gallery-main img');
  document.querySelectorAll('.gallery-thumb').forEach(button => button.addEventListener('click', () => {
    gallery.src = button.dataset.image; gallery.alt = button.dataset.alt;
    document.querySelectorAll('.gallery-thumb').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  document.querySelector('#contact-form')?.addEventListener('submit', event => {
    event.preventDefault();
    const val = id => document.getElementById(id).value.trim();
    const message = `Olá, Lume! Sou ${val('nome')}.\nAssunto: ${val('assunto')}\n${val('email') ? 'E-mail: ' + val('email') + '\n' : ''}\n${val('mensagem')}`;
    location.href = 'https://wa.me/351917980307?text=' + encodeURIComponent(message);
  });
});
