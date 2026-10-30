# raulboullosa.com

Investigación, textos seleccionados y archivo editorial de Raúl Alberto Rivera Boullosa.

## Arquitectura

- `/`: investigación actual y el Ensayo 02 seguido del paper SITEPE v14.
- `/ensayos/` (Publicaciones en el menú): selección actual (02) seguida del archivo histórico **RB · Ensayos 2026 · 01–07**.
- `/ensayos/#archivo`: acceso directo al índice histórico completo; el 02 enlaza a la misma ficha y PDF que la selección.
- `/ensayos/<slug>/`: ficha canónica de cada ensayo.
- `/publicaciones/sitepe-pleno-empleo-mexico/`: ficha independiente del paper SITEPE v14.
- `/pdf/`: ediciones A5 con nombres públicos estables.
- `/investigacion/`: programa de investigación, separado del archivo de obras.
- `/sobre-mi/`: semblanza y directorio de identidad pública.
- Substack aloja el flujo de notas e intervenciones periódicas.

Los antiguos destinos `/textos/` y `/proyectos/` conservan páginas de traslado para no dejar enlaces muertos.

## Publicación

El sitio es estático. La salida pública está completa en `dist/` y no requiere compilación.

La selección editorial no altera la pertenencia a una colección. Los formatos futuros pueden incorporarse fuera de RB · Ensayos 2026, sin renumerar ni trasladar las publicaciones históricas. Las fichas son HTML estático. `metadata/publications.json` centraliza los metadatos de publicación; `scripts/sync_metadata.py` actualiza su JSON-LD y las declaraciones de correspondencia y contribución. Véase `metadata/README.md`.


## Navegación y comprobaciones

Todas las páginas de contenido comparten el menú Inicio · Publicaciones · Investigación · Sobre mí · Substack, con sección activa, ruta de navegación, índice de secciones y retorno al índice. La colección conserva sus URLs en `/ensayos/`; `/publicaciones/` conduce al mismo índice. Las fichas ofrecen PDF y acceso directo a Cómo citar. `scripts/sync_navigation.py` centraliza esas reglas y se ejecuta desde `scripts/sync_metadata.py`.

Después de editar: `python scripts/sync_metadata.py`, `python scripts/sync_metadata.py --check` y `python scripts/check_site.py`. La comprobación revisa todos los enlaces internos, anclas, niveles de encabezado y menús, además de los accesos PDF y referencia de las ocho fichas. Con un checkout parcial puede proporcionarse `--inventory` con una lista JSON de rutas rastreadas para comprobar los archivos binarios alojados en el repositorio. La verificación visual de esta intervención cubrió 13 páginas a 320, 390, 768 y 1280 píxeles, sin desbordamiento horizontal de página. Las ecuaciones largas conservan desplazamiento dentro de sus recuadros.
