# 02 · Identidad visual — VR Day LATAM 2026

**Fuentes:** `referencias/identidad/mockup-web-inicio-2026.png` (maqueta del Inicio), `referencias/identidad/afiche-postulacion-2026.jpg` (afiche de postulación) y `referencias/identidad/descripcion-identidad.md` (descripción recibida).
Esta identidad **reemplaza** la estética oscura/neón del sitio 2023 (resumida al final como archivo histórico).

---

## 1. Validación

### Veredicto: ✅ aprobada, con 3 ajustes obligatorios y 5 recomendados

La identidad es coherente entre la maqueta y el afiche, se ajusta a lo que dice la descripción ("80 % tecnología institucional + 20 % futurismo inmersivo") y funciona bien para un evento universitario internacional. Es clara, luminosa y distinta del sitio actual.

| Aspecto | Descripción recibida | Lo que muestran las imágenes | Resultado |
|---|---|---|---|
| Fondo claro dominante | Blanco / muy claro | `#F4F8FC`, `#EDF3FA`, `#E3E9F4` | ✅ Coincide |
| Azul eléctrico principal | `#4D9CF6` aprox. | Maqueta `#479DFF`–`#50A1FD` · **Afiche `#6DAAFE`** | ⚠ Dos azules distintos (ver ajuste 2) |
| Navy para textos y bloques | `#071A38` aprox. | `#061835`, `#0F2344` | ✅ Coincide |
| Acento lavanda holográfico | pequeños acentos | `#E8D4F2`, `#D9D0F0`, `#E4C8F8` (resplandores) | ✅ Coincide |
| CTA azul con texto blanco | Sí | Sí | ❌ **No cumple contraste** (ajuste 1) |
| Tipografía geométrica | Sí | "Virtual Reality" y textos: sans geométrica tipo Poppins | ✅ |
| "DAY" grande y geométrico | Sí | Letra display cuadrada/redondeada, propia del logo | ✅ (ajuste 3: entregarlo en vector) |
| Líneas de circuito, nodos, hexágonos, HUD, esquinas recortadas | Sí | Presentes, baja opacidad | ✅ |
| Alternar blanco / navy | Sí | Banda navy "Un evento que conecta…" | ✅ |

### Ajustes obligatorios

**1. Contraste del azul (accesibilidad).** Medido con la fórmula WCAG 2.1:

| Combinación | Contraste | AA texto normal (4,5) | AA texto grande (3,0) |
|---|---|---|---|
| Texto blanco sobre `#4D9CF6` (botón de la maqueta) | **2,84 : 1** | ❌ | ❌ |
| Texto blanco sobre `#6DAAFE` (píldora del afiche) | **2,38 : 1** | ❌ | ❌ |
| `#4D9CF6` como texto/enlace sobre blanco | 2,84 : 1 | ❌ | ❌ |
| `#4D9CF6` sobre navy `#071A38` | 6,10 : 1 | ✅ | ✅ |
| Navy `#071A38` sobre fondo `#F4F8FC` | 16,2 : 1 | ✅ | ✅ |

El azul de marca es precioso para grandes superficies y el logo, pero **no sirve como fondo de texto blanco ni como color de enlaces**. Solución que conserva la estética: separar dos azules.

- **Azul marca `#4D9CF6`** → logo, "DAY", ilustraciones, íconos grandes, resplandores, bordes y detalles decorativos.
- **Azul acción `#1F6FD6`** → botones con texto blanco (4,88 : 1 ✅), enlaces y texto azul pequeño (4,88 : 1 sobre blanco ✅).
- El botón puede llevar un degradé sutil `#1F6FD6 → #4D9CF6` **solo si el texto queda sobre la zona oscura**; lo más seguro es sólido `#1F6FD6` con resplandor `#4D9CF6` alrededor.

**2. Un solo azul de marca.** La maqueta usa `#4D9CF6` y el afiche `#6DAAFE` (más claro, posiblemente por exportación). Se fija `#4D9CF6` como oficial (coincide con la descripción) y `#6DAAFE` pasa a ser el tono claro `azul-300`. Conviene avisar a quien diseña las piezas gráficas.

**3. Logo en vector.** "DAY", "LATAM" (letras irregulares) y la banda de fecha "12 Y 13 DE" usan letras dibujadas o una fuente display que no está en Google Fonts. En la web deben ir como **SVG**, no como texto. Se necesitan del diseñador:
- Logo completo horizontal (como en el encabezado) y versión apilada (como en el hero).
- Isotipo (visor) solo → favicon.
- Versión en blanco para fondos navy.
- Nombre de la fuente de "DAY" / "12 Y 13 DE" (si es una fuente con licencia web, se puede usar en titulares cortos).

### Recomendaciones

1. **Texto secundario gris-azul**, no azul claro: en la maqueta las descripciones de las tarjetas van en azul claro (~`#5E8CC4`), demasiado tenue. Usar `#4A5B78` (≈ 6,9 : 1).
2. **Lavanda solo como luz**, nunca para texto sobre blanco (contraste < 1,5 : 1). Para un violeta legible usar `#7C4DDB` (5,3 : 1).
3. **Fotografía:** la persona del hero aparece en ambas piezas; confirmar que la imagen tiene derechos de uso (parece generada por IA o de banco de imágenes) y pedir el archivo en alta resolución y sin fondo.
4. **La maqueta es una imagen conceptual**: sirve como dirección de arte, no como diseño cerrado (faltan estados hover, móvil y el resto de páginas). Las decisiones de este documento completan lo que falta.
5. **Menú de la maqueta ≠ estructura actual**: ver sección 5.

---

## 2. Tokens de diseño (definitivos)

Se escribirán en `static/css/tokens.css`. Cambiar la marca = editar solo ese archivo.

```css
:root {
  /* Fondos (tema claro por defecto) */
  --vr-blanco:       #FFFFFF;
  --vr-fondo:        #F4F8FC;  /* fondo general */
  --vr-fondo-2:      #EAF1FA;  /* secciones alternas claras */
  --vr-borde:        #D6E2F0;  /* bordes de tarjetas y separadores */

  /* Navy (texto principal y secciones de contraste) */
  --vr-navy-900:     #071A38;
  --vr-navy-800:     #0F2344;
  --vr-navy-700:     #1B3358;

  /* Azules */
  --vr-azul-500:     #4D9CF6;  /* MARCA: logo, "DAY", ilustraciones, íconos grandes, brillos */
  --vr-azul-300:     #6DAAFE;  /* marca claro (afiches, fondos de píldoras decorativas) */
  --vr-azul-100:     #E5F0FD;  /* fondos suaves, chips */
  --vr-azul-accion:  #1F6FD6;  /* ACCIÓN: botones con texto blanco, enlaces, foco */
  --vr-azul-accion-hover: #1A5FB8;

  /* Holográfico */
  --vr-lavanda-200:  #E6D5F7;  /* resplandores y degradés de fondo */
  --vr-violeta-600:  #7C4DDB;  /* texto/acento violeta legible */

  /* Texto */
  --vr-texto:        #071A38;  /* = navy-900 */
  --vr-texto-2:      #4A5B78;  /* secundario */
  --vr-texto-inv:    #FFFFFF;  /* sobre navy */
  --vr-texto-inv-2:  #B9CBE6;  /* secundario sobre navy */

  /* Degradés */
  --vr-degrade-holo: radial-gradient(60% 60% at 70% 40%, #C9E0FD 0%, #E6D5F7 45%, transparent 75%);
  --vr-degrade-azul: linear-gradient(90deg, #1F6FD6, #4D9CF6);

  /* Formas */
  --vr-radio-pildora: 999px;   /* botones, chips, marco "LATAM 2026" */
  --vr-radio-card:    20px;
  --vr-corte:         16px;    /* esquinas recortadas (clip-path) de marcos HUD */
  --vr-sombra-card:   0 8px 30px rgba(7, 26, 56, .06);
  --vr-brillo-azul:   0 8px 24px rgba(77, 156, 246, .35);
}
```

### Contraste verificado

| Texto | Fondo | Contraste | Uso |
|---|---|---|---|
| `--vr-texto` navy | `--vr-fondo` | 16,2 | todo |
| `--vr-texto-2` | blanco | ≈ 6,9 | párrafos secundarios |
| Blanco | `--vr-azul-accion` | 4,88 | botones |
| `--vr-azul-accion` | blanco / `--vr-fondo` | 4,88 / 4,57 | enlaces |
| `--vr-azul-500` | navy | 6,10 | titulares azules en secciones navy ("conecta") |
| `--vr-azul-300` | navy | 7,28 | detalles sobre navy |
| `--vr-violeta-600` | blanco | 5,33 | acentos violeta |
| `--vr-texto` navy | `--vr-azul-100` | 15,0 | texto de chips/etiquetas |
| `--vr-azul-accion` | `--vr-azul-100` | 4,23 | ❌ en chips usar navy |
| `--vr-azul-500` | blanco | 2,84 | ❌ solo decorativo o texto ≥ 48 px como "DAY" (que es logo) |

## 3. Tipografía

| Rol | Fuente | Pesos | Notas |
|---|---|---|---|
| Logo, "DAY", "LATAM", banda de fecha | **SVG del diseñador** | — | No es texto editable |
| Titulares y navegación | **Poppins** (alojada en `static/fonts/`) | 600, 700, 800 | Geométrica, igual carácter que "Virtual Reality" del logo |
| Texto corrido, agendas, reseñas | **Poppins** 400/500 *o* **Inter** 400/500 | — | Poppins basta para mantener unidad; Inter si se prefiere más legibilidad en textos largos (reseñas de ponentes) |
| Horas y cifras | La misma, con `font-variant-numeric: tabular-nums` | — | Alinea la agenda |

Escala fluida: H1 44→72 px · H2 32→48 · H3 22→28 · cuerpo 16→18 · pequeño 14. Titulares en navy con una palabra clave en azul (como "Un evento que **conecta**").
Mayúsculas solo en la banda de fecha y etiquetas cortas.

## 4. Elementos gráficos y componentes

| Elemento | Especificación |
|---|---|
| **Líneas de circuito y nodos** | SVG en `static/img/decor/`, trazo 1 px `--vr-azul-500` al 15–25 % de opacidad, nodos circulares de 4–6 px. Detrás del contenido, nunca sobre texto. |
| **Hexágonos** | Contorno 1 px, opacidad 10–20 %, en fondos del hero y secciones alternas. |
| **Círculos HUD** | Anillos concéntricos finos (como sobre la mano del hero); usarlos para destacar fotos, cifras o el ícono del visor. |
| **Esquinas recortadas** | `clip-path` con corte de 16 px en el marco del hero, en la transición a secciones navy y en tarjetas destacadas. |
| **Marco "LATAM 2026"** | Contorno azul 2 px, radio píldora. Reutilizable para "etiquetas de edición". |
| **Resplandor holográfico** | `--vr-degrade-holo` detrás de las fotos (azul → lavanda). |
| **Botón primario** | Píldora, alto 56 px, fondo `--vr-azul-accion`, texto blanco 600, flecha → a la derecha, `--vr-brillo-azul`. |
| **Botón secundario** | Píldora, fondo blanco/translúcido, borde 1,5 px `--vr-azul-accion`, texto navy, ícono lineal azul a la izquierda. |
| **Tarjetas** | Blancas, radio 20 px, borde `--vr-borde`, sombra `--vr-sombra-card`, ícono lineal azul arriba, título navy 600, texto `--vr-texto-2`. Separadores verticales finos entre tarjetas en fila (como en la maqueta). |
| **Íconos** | Lineales, trazo 1,75 px, azul marca (grandes) o azul acción (pequeños). Librería sugerida: **Lucide** (tiene visor VR, cubo, usuarios, bombilla, calendario). |
| **Secciones navy** | Fondo `--vr-navy-900` con foto a la derecha fundida, líneas de circuito en azul, titular blanco + palabra en `--vr-azul-500`. |
| **Menú** | Fondo blanco translúcido con desenfoque al hacer scroll; ítem activo en azul acción con subrayado 2 px. CTA "Inscríbete" siempre visible. |
| **Fotos de ponentes** | Circulares con anillo HUD azul fino (las fotos actuales `-modified` ya vienen recortadas). |

## 5. Estructura que sugiere la maqueta

**Menú de la maqueta:** Inicio · Acerca de · Ponentes · Agenda · Lugar · Contacto + botón **Inscríbete**.
**Menú actual:** Inicio · Acerca de · Agenda · Plataforma inmersiva · Memorias ▾ · Centro de ayuda · Contacto.

Propuesta que une ambos sin perder páginas:

```
Inicio · Acerca de · Ponentes · Agenda · Lugar · Memorias ▾ · Contacto      [Inscríbete →]
                                                   ├ VRD 2023 (nueva memoria)
                                                   ├ VRD 2022 · 2021 · 2020 · 2019
Pie de página: Plataforma inmersiva · Centro de ayuda · Memorias · Aliados
```

- **Ponentes** (nueva): lista de `ponentes.yaml` filtrada por edición 2026 (hoy vacía → placeholders).
- **Lugar** (nueva): sede UTPL, Loja (dato de la agenda 2026). Faltan dirección y mapa.
- **Plataforma inmersiva** y **Centro de ayuda** describen la edición 2020 → pasan al pie hasta que se actualicen.
- El contenido 2023 del Inicio y la Agenda pasa a `/memorias/2023/`.

✅ **Aprobado y aplicado** en `contenido/sitio.yaml` (ver `01-mapa-del-sitio.md §0`).

**Secciones del nuevo Inicio (según la maqueta):** hero (fecha + logo + lema + 2 botones + foto) → 4 tarjetas (Conferencias · Exhibición de soluciones · Networking · Talleres prácticos) → banda navy "Un evento que conecta ideas, tecnología y personas" → convocatoria → ¿Qué es el VRD? → resumen de agenda → sede y aliados → memorias 2023. Implementado en `contenido/paginas/inicio.yaml` con datos de `contenido/evento.yaml`.

## 6. Recursos gráficos a solicitar al diseñador

- [~] Logo 2026 en SVG: horizontal y versión blanca ✅ (sacados del .ai: `marca/logo-vrday-2026.svg`, `-blanco.svg`); faltan apilado e isotipo
- [ ] Nombre y licencia de la fuente de "DAY" / "12 Y 13 DE"
- [ ] Foto del hero en alta resolución, fondo transparente o limpio + confirmación de derechos
- [x] Banda navy: sin foto, red de nodos animada (efecto `red_nodos`, docs/07)
- [ ] Patrones SVG: circuitos, hexágonos, anillos HUD
- [ ] Logos individuales de sede y aliados (UTPL, RAIN y 16 aliados) en SVG o PNG transparente — hoy solo existen dentro del afiche
- [ ] Favicon y `apple-touch-icon` (desde el isotipo)
- [x] Imagen para compartir en redes 1200×630 → `marca/compartir-2026.jpg` (recorte del afiche 2026)

## 7. Cómo se aplica al contenido existente

- Todas las páginas actuales (memorias, juegos, arte, heredadas) usan la nueva identidad automáticamente: el estilo vive en las plantillas, no en el YAML.
- Las imágenes antiguas con estética oscura (artes 2023, cabeceras) se muestran como **fotografías dentro de marcos** (tarjetas con radio y borde), no como fondos de página, para que no rompan el tema claro.
- `medios/fondos/*` (fondos oscuros 2023) dejan de usarse como fondo general; se conservan para las páginas de memorias 2023.
- Efectos y 3D (`07-efectos-y-3d.md`): adaptar a tema claro (líneas de circuito animadas, anillos HUD que pulsan, partículas azul/lavanda sobre blanco).

---

## Anexo · Identidad anterior (2023, archivo)

Logo "VR DAY latam" blanco sobre esfera azul; arte de campaña neón líquido cian→violeta→magenta sobre azul noche (`#000A32`); tema WordPress con `#009EE2`; tipografías Montserrat + Open Sans. Se conserva únicamente en las páginas de memorias.
