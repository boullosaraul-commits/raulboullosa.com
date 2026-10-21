# raulboullosa.com

Investigación, textos seleccionados y archivo editorial de Raúl Alberto Rivera Boullosa.

## Arquitectura

- `/`: investigación actual y un único texto seleccionado: el Ensayo 02.
- `/ensayos/`: selección actual (02) seguida del archivo histórico **RB · Ensayos 2026 · 01–07**.
- `/ensayos/#archivo`: acceso directo al índice histórico completo; el 02 enlaza a la misma ficha y PDF que la selección.
- `/ensayos/<slug>/`: ficha canónica de cada ensayo.
- `/pdf/`: ediciones A5 con nombres públicos estables.
- `/investigacion/`: programa de investigación, separado del archivo de obras.
- `/sobre-mi/`: semblanza y directorio de identidad pública.
- Substack aloja el flujo de notas e intervenciones periódicas.

Los antiguos destinos `/textos/` y `/proyectos/` conservan páginas de traslado para no dejar enlaces muertos.

## Publicación

El sitio es estático. La salida pública está completa en `dist/` y no requiere compilación.

La selección editorial no altera la pertenencia a una colección. Los formatos futuros pueden incorporarse fuera de RB · Ensayos 2026, sin renumerar ni trasladar las publicaciones históricas. Las fichas y sus metadatos son HTML estático; no hay generador, componentes ni datos externos.
