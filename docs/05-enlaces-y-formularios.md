# 05 · Formularios, enlaces externos y contenido embebido

## 1. Formularios

El sitio nuevo **no procesa formularios**. Todo formulario se reemplaza por un servicio externo.

| Dónde | Hoy | Nuevo | Estado |
|---|---|---|---|
| **Contacto** (`/contacto/`) | Formulario propio del tema: *Su nombre*, *E-mail*, *Asunto*, *Mensaje* → "Enviar" | **Google Form** con los mismos 4 campos, incrustado en la página (o botón que lo abre) | **PENDIENTE**: crear el form y pegar la URL en `contenido/paginas/contacto.yaml → url` |
| Inscripción VRDay Game LATAM (slider del Inicio) | Ya es un Google Form | Se mantiene | OK |
| Inscripción Ecuador 2023 (Agenda) | Ya es un Google Form (`forms.gle/ao4qJarbKBj5PyQP7`) | Se mantiene | OK |
| Buscador (página "Prueba") | Buscador de WordPress | Se elimina (página descartada) | — |

### Guía rápida: Google Form de contacto
1. Crear el formulario con: *Nombre* (respuesta corta, obligatorio), *Correo electrónico* (validación de email, obligatorio), *Asunto* (respuesta corta), *Mensaje* (párrafo, obligatorio).
2. En Configuración → Respuestas: activar notificaciones por correo al equipo organizador.
3. Enviar → pestaña `< >` → copiar la URL del `src` del iframe (termina en `viewform?embedded=true`).
4. Pegarla en `contacto.yaml` (`url:`). Con `modo: incrustado` se muestra dentro de la página; con `modo: boton` se abre en otra pestaña.

## 2. Enlaces de inscripción y externos

| Página | Texto | Destino | Observación |
|---|---|---|---|
| Inicio · slider 3 | Inscríbete | docs.google.com/forms/…DeDuJTw/viewform | Google Form (Game LATAM) |
| Inicio · inscripciones | Inscríbete en la programación internacional | eventbrite.es/e/…749589050027 | Evento 2023 (pasado) |
| Inicio · actividades | Stands virtuales / VRDay Game LATAM | itch.io/jam/vrdaygamelatam | **Las dos tarjetas van al mismo enlace**; ¿Stands debería ir a `/stands-virtuales/`? |
| Agenda · Colombia | Inscríbete Aquí | cipte.co/vrdaycol/inscripciones/ | |
| Agenda · Ecuador | Inscríbete Aquí | forms.gle/ao4qJarbKBj5PyQP7 | |
| Agenda · Perú | Incríbete Aquí | nfticket.events/event/?Qm… | |
| Agenda · Brasil | Assine aqui | sympla.com.br/evento/vrday-latam-2023/2233142 | |
| Agenda · Bolivia | Inscríbete Aquí | fb.me/e/v6vEyzKxo | |
| Agenda · Chile | — | (vacío) | |
| Centro de ayuda | Ayuda en línea | discordapp.com/widget?id=761688721304059944 | Dominio antiguo de Discord; verificar si el servidor sigue activo |
| Centro de ayuda | clic aquí (inscripción) | eventbrite.es/…126161954803 | Evento 2020 |
| Centro de ayuda | Facebook Live UTPL | facebook.com/utpl.loja | |
| Centro de ayuda | Web de la exposición | melylunaf.wixsite.com/soyartecuador | |
| Juego Knockout | curso de CEDIA "aquí" | catalogo.aprendiendo.ec/… (http) | Verificar vigencia |
| Juego Knockout | VR Days by bsancanCato | bsancancato.itch.io/vrday | |
| Plataforma inmersiva | Descargar manuales | `#` (sin destino) | **PENDIENTE** |
| Realidad aumentada | Videotutorial / Instructivo | `#` (sin destino) | **PENDIENTE** |

**Enlaces internos rotos del sitio actual** (se corrigen automáticamente en el nuevo): muchos enlaces internos apuntan al dominio antiguo `virtualrealityday.utpl.edu.ec/…` (p. ej. "ver más", tarjetas del Inicio, FAQ). En los YAML se escribieron como rutas internas (`/acerca-de/`, `/arte-en-cuarentena/`…).

## 3. Contenido embebido (iframes)

| Página | Proveedor | URL | Notas |
|---|---|---|---|
| Arte en cuarentena | Sketchfab | `sketchfab.com/models/fa19a6509aeb4af7b66ff032818c90f3/embed` | Galería 3D. Candidato a reemplazo por visor 3D propio (`07`) |
| Juego Knockout | itch.io | `itch.io/embed/1790971` (552×167) | Tarjeta de juego |
| Varias | YouTube | ver `04-medios.md` | Se cargarán con fachada ligera |

## 4. Servicios de terceros presentes hoy

| Servicio | ID | ¿Se mantiene? |
|---|---|---|
| Google Tag Manager | `GTM-MCV3JJR` | A decidir (guardado en `sitio.yaml → analitica`) |
| Google Analytics 4 | `G-HMBRY9T73Y` | A decidir |
| Facebook SDK (`fb-root`) | — | No se usa en ninguna página; se elimina |
