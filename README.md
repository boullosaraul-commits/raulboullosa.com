# raulboullosa.com

Archivo académico personal de Raúl Alberto Rivera Boullosa: documentos, investigación y materiales relacionados.

## Arquitectura

- `/`: presentación, líneas de investigación y documentos destacados.
- `/ensayos/`: catálogo de documentos de trabajo y ponencias, con la numeración histórica de **RB · Ensayos 2026**.
- `/ensayos/<slug>/`: fichas de los ensayos; las rutas históricas se conservan.
- `/publicaciones/`: acceso al catálogo; las fichas de SITEPE y Valle–Marx–TSSI permanecen en sus rutas propias.
- `/investigacion/`: líneas y proyectos en desarrollo.
- `/sobre-mi/`: perfil académico del autor.
- `/textos/` y `/proyectos/`: páginas de traslado para preservar enlaces anteriores.
- `/pdf/`: archivos publicados; `/citations/`: referencias bibliográficas descargables.

## Fuentes y comprobaciones

El sitio es estático: `dist/` contiene los archivos públicos. `metadata/publications.json` centraliza los metadatos de las fichas, el catálogo y las referencias. Para aplicar cambios al registro, ejecutar `python scripts/sync_catalog.py` y `python scripts/sync_metadata.py`.

Antes de integrar cambios, ejecutar:

```sh
python scripts/sync_catalog.py --check
python scripts/sync_metadata.py --check
python scripts/check_site.py
sha256sum -c metadata/pdf-sha256-2026-11-14.txt
```

El registro de hashes comprueba que los PDF coinciden con el inventario del 14 de noviembre de 2026; no demuestra por sí solo su identidad respecto de una copia externa aprobada. La revisión editorial, visual y del sitio publicado requiere comprobaciones adicionales.

## Despliegue

Cloudflare Workers publica los archivos de `dist/`. El estado de compilación se consulta por SHA. La comprobación del dominio público debe contrastar su contenido con el commit de producción.
