# 12. Publicar en vrdaylatam.org (dominio propio en GitHub Pages)

El sitio se publica con GitHub Pages desde el repositorio **WimperT96/vrday**. El dominio sigue
registrado en GoDaddy: solo se cambia hacia dónde apunta. El hosting WordPress de GoDaddy deja de
usarse para la web.

> **Estado: activo desde el 26-oct-2026.** DNS en GitHub Pages, HTTPS forzado y publicación en modo producción.

**La publicación ya está preparada.** El workflow (`.github/workflows/publicar-pages.yml`) detecta solo el modo:

| En Settings › Pages | Se publica | Buscadores | Marcas "Contenido provisional" |
|---|---|---|---|
| Sin dominio propio | Vista previa en `https://wimpert96.github.io/vrday/` | No indexa | Visibles |
| Custom domain = `vrdaylatam.org` | Producción en `https://vrdaylatam.org/` | Indexa (sitemap y robots.txt) | Ocultas |

## Estado del DNS antes del cambio (26-oct-2026)

| Tipo | Nombre | Valor |
|---|---|---|
| A | `@` | `160.153.0.159` (WordPress de GoDaddy) |
| CNAME | `www` | `vrdaylatam.org` |
| MX | — | ninguno: el dominio no tiene correo, no hay nada que proteger |

Anotar estos valores antes de tocar nada: sirven para deshacer el cambio.

## Paso 1 — Quien administra GoDaddy: cambiar el DNS (~10 min)

GoDaddy › Mis productos › Dominios › **vrdaylatam.org** › **DNS** (Administrar DNS):

1. **Borrar** el registro **A** de `@` que apunta a `160.153.0.159`.
2. **Crear 4 registros A** con nombre `@` (TTL: 1 hora o el predeterminado):
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
3. **Editar** el registro **CNAME** de `www` para que apunte a `wimpert96.github.io` (en lugar de `vrdaylatam.org`).
4. No tocar los demás registros.

> Si GoDaddy no deja borrar el registro A porque el dominio está "conectado" al hosting de
> WordPress, primero hay que desconectarlo: Managed WordPress › el sitio › Configuración › Dominio.

## Paso 2 — En GitHub: activar el dominio (~2 min)

github.com/WimperT96/vrday › **Settings › Pages**:

1. En **Custom domain** escribir `vrdaylatam.org` y pulsar **Save**. GitHub comprueba el DNS
   (puede decir "DNS check in progress" unos minutos).
2. Cuando aparezca disponible (normalmente en menos de 1 hora), marcar **Enforce HTTPS**.
3. Volver a publicar para que salga en modo producción: **Actions › Publicar sitio (GitHub Pages) ›
   Run workflow** (o cualquier push a `main`).

Recomendado (evita que otro repositorio pueda reclamar el dominio): github.com › foto de perfil ›
Settings › **Pages › Add a domain** → `vrdaylatam.org`. GitHub da un registro **TXT**
(`_github-pages-challenge-WimperT96`) que se agrega en el DNS de GoDaddy y luego se pulsa *Verify*.

## Paso 3 — Comprobar

- `https://vrdaylatam.org/` muestra el sitio nuevo; `https://www.vrdaylatam.org/` redirige al anterior.
- `https://vrdaylatam.org/robots.txt` dice `Allow: /`.
- Las URLs del WordPress anterior siguen funcionando: las 21 páginas existen o redirigen
  (comprobado con su sitemap). Solo dan 404 las 13 páginas de demostración del tema Kallyas
  (`/portfolio/…`, `/layout_manager/…`), que nunca fueron contenido del evento.
- Opcional: dar de alta el sitio en Google Search Console y enviar `https://vrdaylatam.org/sitemap.xml`.

El cambio de DNS tarda de minutos a un par de horas en verse en todas partes. Mientras tanto
algunos visitantes pueden ver todavía el WordPress, o un aviso de certificado si entran por
`https` antes de que GitHub emita el certificado. Conviene hacerlo en un horario tranquilo.

## Si alguna página se ve sin estilos tras el cambio

Pasó el 26-oct-2026 con la portada: GitHub siguió entregando a los navegadores (que piden la versión
comprimida) la copia de la vista previa, con rutas `/vrday/…`, aunque la versión sin comprimir ya era la nueva.
Se arregla con una publicación nueva (cualquier push a `main` o *Actions › Run workflow*). Para comprobarlo:

```bash
curl -s --compressed -H "Accept-Encoding: gzip, br" https://vrdaylatam.org/ | grep -c '/vrday/'   # debe dar 0
```

## Deshacer

Volver a poner en GoDaddy el registro A de `@` en `160.153.0.159` (y quitar los cuatro de GitHub),
el CNAME de `www` en `vrdaylatam.org`, y borrar el Custom domain en Settings › Pages. La siguiente
publicación vuelve sola al modo vista previa.
