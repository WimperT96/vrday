# 10 · Guía para probar la web en tu computador

Para: cualquier persona del equipo que quiera revisar el sitio localmente.
Si solo quieres **verlo**, usa la vista previa publicada en GitHub Pages (enlace en el README).

## 0. Preparar (solo la primera vez)

Requisitos: Git y Python 3.12.

```powershell
git clone <url-del-repositorio> vrday
cd vrday
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 1. Abrir la web en modo desarrollo

```powershell
.venv\Scripts\python.exe manage.py runserver 8001
```

Abre **http://127.0.0.1:8001**. Deja la terminal abierta (Ctrl + C para apagar).

> Se usa el puerto 8001 por si el 8000 ya está ocupado por otro proyecto. Si 8001 también lo está: `runserver 8002`.
>
> En este modo verás recuadros morados **"Contenido provisional"**: marcan lo que falta completar. No aparecen en la versión publicada.

## 2. Qué revisar

| Página | Dirección | Qué deberías ver |
|---|---|---|
| Inicio | `/` | Franja "12 Y 13 DE noviembre de 2026", logotipo, óvalo "LATAM 2026", botón "Ver agenda", 4 tarjetas, convocatoria "Postulación de **artículo**", banda azul oscuro, "¿Qué es el VRD?", resumen de agenda, sede y aliados. La foto principal es un PLACEHOLDER. |
| Acerca de | `/acerca-de/` | Textos de RX, RV, RA y RM (las definiciones de RV y RA siguen intercambiadas: error heredado, pendiente). |
| Ponentes | `/ponentes/` | Conferencia magistral (provisional), mensaje "Pronto anunciaremos…", botones a ponentes 2023 y 2020. |
| Agenda | `/agenda/` | Agenda tentativa 2026 con pestañas Jueves 12 / Viernes 13. |
| Lugar | `/lugar/` | Datos de la UTPL y espacios del evento; mapa en placeholder. |
| Memorias | `/memorias/` | 5 ediciones (2023 a 2019). |
| Memorias 2023 | `/memorias/2023/` | Carrusel con flechas, video, cifras y 40 ponentes: **clic en un ponente** abre su ficha (se cierra con X, Esc o clic fuera). |
| Agenda 2023 | `/memorias/2023/agenda/#peru` | Se abre directamente la pestaña de Perú. |
| Memorias 2020 / 2019 | `/memorias/2020/` | **Clic en una foto** abre el visor (flechas o teclado). Tabla y videos. |
| Memorias 2021 | `/memorias/2021/` | Tres recuadros "Video pendiente" (heredado). |
| Videos | páginas con videos | El botón ▶ carga YouTube. |
| Contacto | `/contacto/` | Aviso "El formulario de contacto estará disponible próximamente." |
| Centro de ayuda | `/centro-de-ayuda/` | Preguntas frecuentes desplegables. |
| Arte en cuarentena | `/arte-en-cuarentena/` | Modelo 3D de Sketchfab. |
| Redirección | `/vrd-2023/` | Lleva a `/memorias/2022/`. |
| 404 | `/cualquier-cosa/` | Página "Página no encontrada". |

## 3. Probar en celular

En el navegador: **F12** y luego **Ctrl + Shift + M**, elige un teléfono y recarga. Revisa el botón ☰, el submenú de Memorias, que las tarjetas se apilen y que no haya desplazamiento horizontal.

## 4. Cambiar un texto y verlo al instante

1. Con el servidor encendido, edita `contenido/evento.yaml` (por ejemplo la línea `lema:`) y guarda.
2. Recarga el navegador (F5): el cambio aparece sin reiniciar.
3. Deshaz el cambio: `git checkout -- contenido/evento.yaml`

Si al editar un YAML la página muestra un error, casi siempre es la sangría (espacios); deshaz el cambio.

## 5. Pruebas automáticas

```powershell
.venv\Scripts\python.exe manage.py test sitio          # debe terminar en OK
.venv\Scripts\python.exe manage.py validar_contenido   # lista PENDIENTES y debe terminar en ERRORES (0)
```

## 6. Versión final (la que se publica)

```powershell
.venv\Scripts\python.exe manage.py exportar
.venv\Scripts\python.exe -m http.server 8080 --directory dist
```

Abre **http://127.0.0.1:8080**. No abras `dist\index.html` con doble clic: los enlaces necesitan un servidor.

## Si algo falla

| Síntoma | Solución |
|---|---|
| `That port is already in use` | Usa otro puerto: `runserver 8002` |
| Ves otro sitio en el navegador | Otro proyecto usa ese puerto; cambia de puerto |
| Página amarilla de error de Django | Error de formato en un YAML recién editado; deshaz el cambio |
| `python` no se reconoce | Usa la ruta completa `.venv\Scripts\python.exe` |
