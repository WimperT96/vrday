/* Efecto "entrada": el contenido aparece suavemente al entrar en pantalla.
   Uso en YAML:   efectos: {entrada: true}
   Ejemplo del patrón descrito en docs/07-efectos-y-3d.md. */
export default function entrada(seccion) {
  const objetivos = seccion.querySelectorAll(':scope > .contenedor > *, :scope > .contenedor');
  const elementos = objetivos.length ? objetivos : [seccion];
  elementos.forEach((el, i) => {
    el.setAttribute('data-efecto-entrada', '');
    el.style.transitionDelay = `${Math.min(i, 6) * 60}ms`;
  });
  const obs = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('es-visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.15 });
  elementos.forEach((el) => obs.observe(el));
}
