# 06 · Problemas de contenido detectados

Criterio aplicado: **se conserva el contenido tal cual** (incluidas erratas) salvo unas pocas correcciones evidentes de estructura y nombres, marcadas ✅.
Todo lo demás queda listado aquí para que decidas. Cada punto indica el archivo YAML donde se corrige.

Prioridad: 🔴 afecta la credibilidad o es un error de hecho · 🟠 desactualizado o incompleto · 🟡 errata o detalle.

## 1. Decisión general: el sitio está congelado en 2023

🔴 Todo el sitio sigue promocionando el **VR Day Latam 2023** (18-nov-2023) en tiempo futuro ("Nuestro evento **contará** con…", "Inscríbete…"), con enlaces de inscripción de eventos ya pasados. Además:
- El Inicio invita a "Entérate lo que fue el **VRD 2022**" aunque 2023 ya ocurrió y no tiene página de memorias.
- El **Centro de ayuda** y la **Plataforma inmersiva** describen la edición **2020** (VirBELA, 21-nov-2020, 250 cupos, "VRDayEc 2021").
- *Acerca de* menciona VirBELA como plataforma del evento (2020).

**Actualización:** las piezas de identidad 2026 confirman una nueva edición (**12 y 13 de noviembre de 2026**, postulación de artículos hasta el **15 de octubre de 2026**). Por lo tanto se recomienda la opción (b): convertir el contenido 2023 del Inicio y la Agenda en memoria (`/memorias/2023/`) y construir el Inicio 2026 a partir de `contenido/evento.yaml` y de la maqueta. Propuesta de menú en `02-identidad-visual.md §5`. ✅ **Aprobado y aplicado:** el Inicio y la Agenda muestran 2026; el contenido 2023 está en `/memorias/2023/` y `/memorias/2023/agenda/`, sin cambios.

## 2. Errores de hecho

| # | Dónde | Problema | Propuesta | Archivo |
|---|---|---|---|---|
| 1 🔴 | Acerca de | Las definiciones de **Realidad Virtual** y **Realidad Aumentada** están **intercambiadas** (la de RV describe la RA y viceversa). | Intercambiar los dos `cuerpo:` | `paginas/acerca-de.yaml` |
| 2 🔴 | Menú → VRD 2022 | La URL es `/vrd-2023/`. | ✅ Nueva URL `/memorias/2022/` + redirección | `sitio.yaml` |
| 3 🟠 | Agenda 2019 | La página `/agenda-2019/` contiene la agenda de **2020**. | ✅ Movida a `/memorias/2020/agenda/` + redirección | `memorias/2020-agenda.yaml` |
| 4 🟠 | Memorias 2022 | La galería incluye la foto de **ganadores de 2019** y repite una foto. | ✅ Foto repetida quitada; la de 2019 quedó comentada | `memorias/2022.yaml` |
| 5 🟠 | Inicio · ¿Qué es el VRD? | Dice que se celebra el **21 de noviembre**; la edición 2023 fue el 18 de noviembre. | Revisar redacción | `paginas/inicio.yaml` |
| 6 🟡 | Acerca de VRD anterior | Dice "lunes 18 de noviembre" y luego "sábado 21 de noviembre de 2020". | Revisar | `memorias/2020-acerca-de.yaml` |

## 3. Contenido incompleto o de relleno (placeholders heredados)

| Dónde | Qué falta | Archivo |
|---|---|---|
| Ponentes | **16 reseñas vacías**: Arturo Núñez, Nickolas Syris, Alicia Gabriela Paredes, Dino Garzoni, José Oswaldo Guamán, Neysa Rivadeneira, Oscar Cartagena, "No determinado", Tatiana Cabrera (2023); Elvira Rincón, Jorge Gutiérrez, Julio Cabrero, Lorena González López, Paulo Guerra, Samir Vargas, Verónica Rodríguez (2020) | `ponentes.yaml` (campo `notas`) |
| Ponentes | Un ponente de 2023 se llama literalmente **"No determinado"** (foto `no-determinado.png`, Ecuador) | `ponentes.yaml` |
| Memorias 2021 | 3 reproductores de YouTube **sin video** | `memorias/2021.yaml` |
| Plataforma inmersiva | Botón "Descargar manuales" sin archivo (`#`) | `plataforma-inmersiva.yaml` |
| Agenda 2023 · Chile | Sin enlace de inscripción; sin título "Chile" | `agenda.yaml` |
| Agenda 2023 · Ecuador | Charlas "CITEC - Tema:" y "UNAE - Tema:" sin tema | `agenda.yaml` |
| Agenda 2023 · Colombia | Taller en "Aula -----" | `agenda.yaml` |
| Agenda 2023 · Ecuador | Sesión "Globant" sin ponente | `agenda.yaml` |
| Agenda 2020 | Artistas: "Juan Pérez, Juan Pérez, Juan Pérez" (relleno) | `memorias/2020-agenda.yaml` |
| Acerca de VRD anterior | "¿Quién organiza?" es **lorem ipsum** | `memorias/2020-acerca-de.yaml` |
| Páginas heredadas | Textos duplicados, "Títulos profesionales", testimonios demo (José Pérez / Juan Díaz), enlaces "Videotutorial" e "Instructivo" sin destino | `heredadas/*.yaml` |
| Inicio | Solo 3 de 8 banderas enlazaban a la Agenda | ✅ Se enlazaron las 6 con agenda; Panamá y Argentina no tienen agenda |
| Pie | Sin redes sociales, sin texto legal, logos sin enlace | `sitio.yaml` |

## 4. Inconsistencias en la Agenda 2023 (horas y orden)

| País | Sesión | Problema |
|---|---|---|
| Ecuador | "Mahu…" `12:05am - 12:20am`, "Carrera Innovadoras…" `12:25am - 12:40am` | Deben ser **pm** |
| Ecuador | IEEE `11:45pm - 12:00pm` | Hora imposible y fuera de orden (coincide con Globant 11:45am) |
| Ecuador | `13:00pm`, `15:00pm`, `17:00pm` | Mezcla de formato 24 h con am/pm |
| Ecuador | Dos sesiones a las `15:00pm - 15:10pm` | Posible choque |
| Ecuador | UNAE: mismos 3 ponentes en 10:45 y 11:25 | Posible copia |
| Perú | GAME JAM `17:00am - 18:00pm` | am → pm |
| Brasil | "Painel SPCine" `12:30pm - 1:30pm` después de las 16:30 | Parece copiado de Perú |
| Chile | `10:00am - 10:10pm` | pm → am |

Recomendación para el sitio nuevo: escribir las horas en formato 24 h (`14:00 – 14:30`) de forma uniforme.

## 5. Nombres de personas

| Caso | Detalle | Acción |
|---|---|---|
| ✅ Alicia **Gabirela** Paredes | Errata del Inicio; la Agenda dice Gabriela | Corregido |
| ✅ José **Owsaldo** Guamán | Errata del Inicio; la Agenda dice Oswaldo | Corregido |
| ✅ Milton **Salcan** | Inicio dice Salcan; Agenda "Sancan"; su reseña "Sancán Lapo" | Corregido a Milton Sancán |
| ✅ Andrés Castro | Reseña del Inicio mezclada ("Artista y profesor de la UniversiIngeniero de Soporte…") | Se usó la versión limpia de la Agenda |
| Mohamenth / Mohammad | La tarjeta dice "Mohamenth"; la reseña y la agenda, "Mohammad" | Confirmar |
| Edisson David Cuasapas / "Edison Guaspa" | Misma charla (ENCUBA), nombres distintos | Confirmar |
| Neysa Rivadeneira / Rivadineira | Varía entre páginas | Confirmar |
| Julio Cabrero / Cabero | La tarjeta 2020 dice "Cabrero"; la agenda 2020, "Cabero" (Universidad de Sevilla) | Confirmar |
| Katherine Villacorta / Villacota; Sergio Gómez / Goméz; Nickolas / Nicolas Syris | Variantes entre páginas | Se usó la primera; confirmar |
| Institución | En la mayoría de ponentes 2023 el campo "Institución" contiene el **país** | Se separó en `pais` / `institucion`; completar instituciones |

## 6. Privacidad

- 🟠 La reseña de **Fabian Bonilla** incluye su correo personal (`fabianbonillart@gmail.com`). Se conservó; conviene confirmar que quiere publicarlo.

## 7. Erratas (se conservan; corregir si se desea)

| Texto actual | Corrección | Archivo |
|---|---|---|
| Ignaguración Vicerectora UCACUE | Inauguración Vicerrectora UCACUE | `agenda.yaml` |
| Incríbete Aquí (Perú) | Inscríbete aquí | `agenda.yaml` |
| Alianza Francea de Cochabamba | Alianza Francesa de Cochabamba | `agenda.yaml` |
| Eléctricos y Eléctronicos | Eléctricos y Electrónicos | `agenda.yaml` |
| Fouder de Beyond afterlife | Founder de Beyond Afterlife | `ponentes.yaml` |
| Amerícas | Américas | `ponentes.yaml` |
| desde la cédula hasta el cuerpo humano (2019) | célula | `memorias/2019.yaml` |
| realidadaumentada | realidad aumentada | `memorias/2020-acerca-de.yaml` |
| trasmisión | transmisión | `centro-de-ayuda.yaml` |
| "las dos primeras personas que tenga" | que tengan | `centro-de-ayuda.yaml`, `juego-cuidemonos…yaml` |
| Realidad Extendida / Realidad eXtendida / RX | Unificar la grafía | varios |
