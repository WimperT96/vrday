# 07 · Preparación para efectos, animaciones y 3D

La primera versión será sobria y estática, pero la base queda lista para sumar dinamismo **sin reescribir páginas ni contenido**.

## 1. Principios

1. **Mejora progresiva:** cada página funciona completa sin JavaScript. Los efectos se añaden encima.
2. **Carga bajo demanda:** el JS de un efecto solo se descarga si la página lo usa (importación dinámica).
3. **Contenido ≠ efecto:** el YAML dice *qué* efecto quiere una sección; el código decide *cómo*.
4. **Respeto por el usuario:** todo efecto se desactiva con `prefers-reduced-motion`, en equipos lentos y en pantallas pequeñas si es pesado.
5. **Rendimiento:** presupuesto de ~200 KB de JS por página antes de 3D; los modelos 3D se cargan cuando entran en pantalla.

## 2. Los "ganchos" que ya quedan en el contenido

Cada sección admite un campo opcional `efectos:` (reservado desde ahora, vacío por defecto):

```yaml
- tipo: cabecera
  titulo: Agenda
  fondo: fondos/cabecera-paginas.png
  efectos:
    entrada: aparecer          # animación al entrar en pantalla
    fondo_3d: particulas       # escena Three.js detrás del contenido
    parallax: 0.3
```

La plantilla lo transforma en atributos HTML:

```html
<section class="seccion seccion--cabecera" data-componente="cabecera"
         data-efectos='{"entrada":"aparecer","fondo_3d":"particulas","parallax":0.3}'>
```

Y `static/js/main.js` actúa como registro:

```js
// main.js — carga solo lo que la página necesita
const efectos = {
  entrada:  () => import('./efectos/entrada.js'),      // GSAP ScrollTrigger / IntersectionObserver
  parallax: () => import('./efectos/parallax.js'),
  fondo_3d: () => import('./efectos/fondo-3d.js'),     // Three.js
  modelo_3d:() => import('./efectos/modelo-3d.js'),    // <model-viewer>
};
const reducir = matchMedia('(prefers-reduced-motion: reduce)').matches;

document.querySelectorAll('[data-efectos]').forEach(async (el) => {
  if (reducir) return;
  const cfg = JSON.parse(el.dataset.efectos);
  for (const nombre of Object.keys(cfg)) {
    const mod = await efectos[nombre]?.();
    mod?.default(el, cfg[nombre]);
  }
});
```

Agregar un efecto nuevo = crear `static/js/efectos/<nombre>.js` que exporte `default(elemento, config)` y usar `<nombre>` en un YAML.

## 3. Estructura del HTML pensada para capas

Cada sección se genera con esta estructura, para poder poner un fondo animado **detrás** del contenido sin tocarlo:

```html
<section class="seccion" data-componente="…">
  <div class="seccion__fondo" aria-hidden="true"></div>   <!-- imagen, video o <canvas> 3D -->
  <div class="seccion__contenido"> … </div>             <!-- texto, siempre por encima y legible -->
</section>
```

- `z-index` y `isolation: isolate` definidos en `base.css`.
- Los tokens de color (`02-identidad-visual.md`) se exponen también a JS (`getComputedStyle`) para que las escenas 3D usen la misma paleta.

## 4. Oportunidades concretas por página

> Con la identidad 2026 (tema claro, ver `02-identidad-visual.md`) los efectos deben ser **sutiles y luminosos**: líneas de circuito que se dibujan al hacer scroll, nodos que pulsan, anillos HUD alrededor de fotos y cifras, partículas azul/lavanda de baja opacidad sobre blanco. Nada de neón saturado.

| Página / sección | Idea (identidad 2026) | Tecnología sugerida | Dificultad |
|---|---|---|---|
| Hero del Inicio | Anillos HUD animados sobre la mano, líneas de circuito que se trazan, resplandor holográfico que sigue al mouse | SVG + CSS/GSAP | Baja-media |
| Tarjetas de características | Ícono lineal que se "dibuja" al entrar (stroke-dashoffset) | SVG + IntersectionObserver | Baja |
| Banda navy | Partículas azules y red de nodos detrás del titular | Canvas 2D o Three.js | Media |
| Logo (visor) | Isotipo del visor en 3D, rotación suave | `<model-viewer>` | Media |

Ideas generales (válidas también):


| Página / sección | Idea | Tecnología sugerida | Dificultad |
|---|---|---|---|
| Cabeceras de todas las páginas | Partículas y fragmentos flotantes como `cabecera-paginas.png`, reaccionando al mouse | Three.js (instanced mesh) o shader 2D | Media |
| Inicio · slider | Transición con distorsión líquida entre artes (estilo del arte 2023) | Swiper + WebGL (shader) | Media |
| Inicio · cifras | Contadores que suben al entrar en pantalla | IntersectionObserver (sin librería) | Baja |
| Inicio · mapa de países | Globo 3D o mapa con los 8 países resaltados y enlace a su agenda | three-globe / SVG animado | Media-alta |
| Inicio · logo | Visor VR del logo en 3D girando suavemente | `<model-viewer>` con un .glb del logo | Media (requiere modelar) |
| Ponentes | Tarjetas con inclinación 3D (tilt) y anillo de degradé animado | CSS + JS ligero | Baja |
| Arte en cuarentena | Galería 3D propia en lugar del iframe de Sketchfab (descargar el modelo si la licencia lo permite) | `<model-viewer>` o Three.js | Media |
| Plataforma inmersiva | Recorrido 360° de capturas | Pannellum / Photo Sphere Viewer | Baja |
| Memorias | Galería con desplazamiento horizontal y aparición escalonada | GSAP ScrollTrigger | Baja |
| Agenda | Línea de tiempo animada por país | CSS + GSAP | Baja |
| Global | Modo "WebXR": ver un modelo con el visor o en RA en el móvil | `<model-viewer ar>` / WebXR | Alta |

## 5. Carpeta para modelos 3D

```
static/modelos-3d/
├── logo-vrday.glb           (futuro)
├── arte-en-cuarentena.glb   (futuro, si la licencia lo permite)
└── LEEME.md                 formato glTF/GLB, texturas ≤ 2048 px, comprimir con Draco/Meshopt
```

Uso desde YAML (futuro):

```yaml
- tipo: modelo_3d
  titulo: Arte en cuarentena
  modelo: modelos-3d/arte-en-cuarentena.glb
  poster: arte-en-cuarentena/como-interactuar-computador.jpg   # imagen mientras carga / sin WebGL
  ar: true
```

## 6. Checklist técnico para cuando se añadan efectos

- [ ] `prefers-reduced-motion` respetado (el efecto no se carga).
- [ ] Sin WebGL → se muestra la imagen de fondo normal.
- [ ] El texto sigue siendo legible sobre el fondo animado (contraste ≥ 4,5:1).
- [ ] Pausar animaciones cuando la pestaña no está visible (`visibilitychange`) y cuando la sección sale de pantalla.
- [ ] Medir con Lighthouse: LCP < 2,5 s y CLS < 0,1 en móvil.
