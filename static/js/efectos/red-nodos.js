/* Efecto "red_nodos": la red de la banda navy se dibuja al entrar en pantalla
   (líneas que se trazan desde el centro, nodos que aparecen y pulsos de luz).
   Uso en YAML (sección banda con `nodos:`):   efectos: {red_nodos: true}
   Sin este efecto la red se ve completa y quieta (docs/07-efectos-y-3d.md). */
export default function redNodos(seccion) {
  const red = seccion.querySelector('[data-red-nodos]');
  if (!red) return;
  red.classList.add('red-nodos--animada');
  const obs = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('es-visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.35 });
  obs.observe(red);
}
