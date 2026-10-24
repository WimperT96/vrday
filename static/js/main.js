/* ==========================================================================
   VR Day LATAM — comportamiento del sitio (sin dependencias).
   Cada función actúa solo si su componente existe en la página.
   Los efectos opcionales (docs/07) se cargan bajo demanda desde ./efectos/.
   ========================================================================== */
const reducirMovimiento = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── Menú móvil y submenús ─────────────────────────────────────────────── */
function iniciarMenu() {
  const toggle = document.querySelector('[data-menu-toggle]');
  const menu = document.getElementById('menu-principal');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const abierto = menu.classList.toggle('es-abierto');
      toggle.setAttribute('aria-expanded', String(abierto));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu.classList.contains('es-abierto')) {
        menu.classList.remove('es-abierto');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }
  document.querySelectorAll('[data-submenu-toggle]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.menu__item');
      const abierto = item.classList.toggle('es-abierto');
      btn.setAttribute('aria-expanded', String(abierto));
    });
  });
}

/* ── Diálogos (reseñas de ponentes) ────────────────────────────────────── */
function iniciarDialogos() {
  document.querySelectorAll('[data-abrir]').forEach((btn) => {
    btn.addEventListener('click', () => document.getElementById(btn.dataset.abrir)?.showModal());
  });
  document.querySelectorAll('dialog.dialogo').forEach((dlg) => {
    dlg.querySelector('[data-cerrar]')?.addEventListener('click', () => dlg.close());
    // clic fuera de la caja = cerrar
    dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
  });
}

/* ── Galerías con visor (lightbox) ─────────────────────────────────────── */
function iniciarGalerias() {
  const galerias = document.querySelectorAll('[data-galeria]');
  if (!galerias.length) return;
  const visor = document.createElement('dialog');
  visor.className = 'visor';
  visor.setAttribute('aria-label', 'Visor de imágenes');
  visor.innerHTML = `
    <figure style="margin:0">
      <img class="visor__img" alt="">
      <figcaption class="visor__pie"></figcaption>
    </figure>
    <button type="button" class="visor__btn visor__btn--prev" aria-label="Anterior"><svg class="icono"><use href="#i-flecha-izq"></use></svg></button>
    <button type="button" class="visor__btn visor__btn--next" aria-label="Siguiente"><svg class="icono"><use href="#i-flecha"></use></svg></button>
    <button type="button" class="visor__cerrar" aria-label="Cerrar"><svg class="icono"><use href="#i-cerrar"></use></svg></button>`;
  document.body.appendChild(visor);
  const img = visor.querySelector('.visor__img');
  const pie = visor.querySelector('.visor__pie');
  let items = [];
  let indice = 0;
  const mostrar = (i) => {
    indice = (i + items.length) % items.length;
    const a = items[indice];
    img.src = a.href;
    img.alt = a.dataset.alt || '';
    pie.textContent = `${indice + 1} / ${items.length}`;
  };
  visor.querySelector('.visor__btn--prev').addEventListener('click', () => mostrar(indice - 1));
  visor.querySelector('.visor__btn--next').addEventListener('click', () => mostrar(indice + 1));
  visor.querySelector('.visor__cerrar').addEventListener('click', () => visor.close());
  visor.addEventListener('click', (e) => { if (e.target === visor) visor.close(); });
  visor.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') mostrar(indice - 1);
    if (e.key === 'ArrowRight') mostrar(indice + 1);
  });
  galerias.forEach((g) => {
    const enlaces = [...g.querySelectorAll('[data-lightbox]')];
    enlaces.forEach((a, i) => a.addEventListener('click', (e) => {
      e.preventDefault();
      items = enlaces;
      mostrar(i);
      visor.showModal();
    }));
  });
}

/* ── Pestañas accesibles (agenda) ──────────────────────────────────────── */
function iniciarPestanas() {
  document.querySelectorAll('[data-pestanas]').forEach((cont) => {
    const tabs = [...cont.querySelectorAll('[role="tab"]')];
    const activar = (tab, foco = false) => {
      tabs.forEach((t) => {
        const sel = t === tab;
        t.setAttribute('aria-selected', String(sel));
        t.tabIndex = sel ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = !sel;
      });
      if (foco) tab.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => activar(t));
      t.addEventListener('keydown', (e) => {
        const mover = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (mover) { e.preventDefault(); activar(tabs[(i + mover + tabs.length) % tabs.length], true); }
      });
    });
    // Abrir la pestaña indicada en la URL (#colombia, #peru…)
    const destino = location.hash && tabs.find((t) => `#${t.getAttribute('aria-controls')}` === location.hash);
    if (destino) {
      activar(destino);
      document.getElementById(destino.getAttribute('aria-controls'))?.scrollIntoView();
    }
  });
}

/* ── YouTube ligero: carga el reproductor solo al hacer clic ───────────── */
function iniciarYoutube() {
  document.querySelectorAll('[data-youtube]').forEach((cont) => {
    cont.querySelector('button')?.addEventListener('click', () => {
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube-nocookie.com/embed/${cont.dataset.youtube}?autoplay=1&rel=0`;
      iframe.title = cont.querySelector('button').getAttribute('aria-label') || 'Video';
      iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      // YouTube exige saber desde qué sitio se incrusta (si no llega el Referer muestra
      // "Video player configuration error", error 153); esta política envía solo el dominio.
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      cont.replaceChildren(iframe);
    }, { once: true });
  });
}

/* ── Slider (scroll-snap + flechas + avance automático) ─────────────────── */
function iniciarSliders() {
  document.querySelectorAll('[data-slider]').forEach((slider) => {
    const pista = slider.querySelector('[data-slider-pista]');
    const paso = (dir) => {
      const ancho = pista.clientWidth;
      const fin = pista.scrollLeft + ancho >= pista.scrollWidth - 4;
      pista.scrollTo({ left: dir > 0 && fin ? 0 : pista.scrollLeft + dir * ancho, behavior: reducirMovimiento ? 'auto' : 'smooth' });
    };
    slider.querySelector('[data-slider-prev]')?.addEventListener('click', () => paso(-1));
    slider.querySelector('[data-slider-next]')?.addEventListener('click', () => paso(1));
    if (!reducirMovimiento) {
      let timer = setInterval(() => paso(1), 7000);
      const pausar = () => clearInterval(timer);
      slider.addEventListener('pointerenter', pausar);
      slider.addEventListener('focusin', pausar);
    }
  });
}

/* ── Efectos opcionales declarados en el YAML (campo `efectos:`) ────────── */
const EFECTOS = {
  entrada: () => import('./efectos/entrada.js'),
  red_nodos: () => import('./efectos/red-nodos.js'),
  // parallax: () => import('./efectos/parallax.js'),
  // fondo_3d: () => import('./efectos/fondo-3d.js'),
};
function iniciarEfectos() {
  if (reducirMovimiento) return;
  document.querySelectorAll('[data-efectos]').forEach(async (el) => {
    let cfg = {};
    try { cfg = JSON.parse(el.dataset.efectos); } catch { return; }
    for (const [nombre, opciones] of Object.entries(cfg)) {
      const cargar = EFECTOS[nombre];
      if (!cargar) continue;
      const modulo = await cargar();
      modulo.default(el, opciones);
    }
  });
}

iniciarMenu();
iniciarDialogos();
iniciarGalerias();
iniciarPestanas();
iniciarYoutube();
iniciarSliders();
iniciarEfectos();
