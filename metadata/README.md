# Registro maestro de publicaciones

`publications.json` conserva las fichas de RB · Ensayos 2026 · 01–07 y del paper SITEPE v14 como ocho objetos distintos. Editar el registro y ejecutar `python scripts/sync_metadata.py`; después comprobar con `python scripts/sync_metadata.py --check`. El resultado sigue siendo HTML estático, sin dependencia de JavaScript en el navegador.

El registro distingue autoría (`author`), contribuciones CRediT (`roles`, siempre una lista) y correspondencia (`corresponding`). Raúl Alberto Rivera Boullosa queda designado como autor de correspondencia de estos trabajos individuales; esto no publica una dirección de correo.

Los roles sin confirmación permanecen vacíos y con estado `pending_confirmation` hasta verificar las contribuciones de cada trabajo. No se deducen papeles CRediT de la autoría individual. Para publicarlos, completar la lista con los términos admitidos y cambiar `roles_status` a `confirmed`. El generador conserva `author` como Person y expresa contribuciones verificadas mediante `contributor` y Schema.org Role.

ORCID, licencia y financiación desconocidos se representan como `null` y se omiten de la salida pública. `funding: null` no significa ausencia de financiación. No reutilizar la afiliación actual del perfil como evidencia de una afiliación histórica de publicación.

Las fechas mantienen la precisión comprobada de las fichas existentes (mes). La fecha de modificación de esta capa de metadatos no se convierte en fecha de publicación ni de modificación del texto. Las fichas de SITEPE v14 y Ensayo 02 v1.01 transcriben sus resúmenes documentales. SITEPE incorpora sus palabras clave y códigos JEL declarados. Las palabras clave y los códigos JEL del Ensayo 02 son una clasificación editorial aprobada al cierre; no se presentan como una transcripción del PDF. La afiliación declarada se conserva por publicación dentro de cada contribución; no se propaga a los otros trabajos. `numberOfPages` mide páginas físicas del archivo PDF: Ensayo 02 tiene 57, incluido el colofón final.

SITEPE y Ensayo 05 se enlazan como documentos relacionados, sin afirmar identidad entre versiones ni una relación de sustitución. El PDF, su ruta y su contenido permanecen intactos.

Esta es una fuente interna y una salida web Schema.org; no constituye un depósito Crossref ni un XML Schema 5.5. Un futuro exportador Crossref deberá validar tipos, roles e identificadores contra su esquema oficial. No añadir `correspondingAuthor` o `contributor_role` como si fueran propiedades Schema.org: la correspondencia se conserva en el registro y se muestra en la ficha.

## Declaraciones confirmadas por el autor · 30 de octubre de 2026

El ORCID confirmado es https://orcid.org/0009-0000-7097-4634. Para SITEPE v14 y Ensayo 02 v1.01, el autor confirmó Conceptualization, Methodology, Investigation, Formal analysis, Writing – original draft y Writing – review & editing; declaró ausencia de financiación y autorizó publicar ambos correos de correspondencia. Conserva todos los derechos; no se asigna una licencia abierta ni una URL de licencia inexistente. Los desarrollos de software, datos, visualización o validación adicionales del Ensayo 02 no se atribuyen a esta edición porque el autor indicó que quedan fuera de ella. El autor confirmó que no hubo contribuciones de otras personas y que utilizó IA de manera incidental. Las fichas conservan esas declaraciones sin atribuir tareas específicas a herramientas de IA. Los roles y condiciones no se propagan a los demás ensayos.

## Cierre de estas dos fichas

SITEPE v14 y Ensayo 02 v1.01 quedan cerrados en esta intervención. Ensayo 02 incorpora las ocho palabras clave propuestas y JEL E42 (principal), D85 y E11. Las declaraciones finales son: «El autor declara que no hubo contribuciones de otras personas» y «Se utilizó inteligencia artificial de manera incidental». El cierre sólo afecta a estas dos fichas; no afirma que los campos pendientes de los demás ensayos estén resueltos. Los PDF definitivos permanecen sin modificación.

## Exportación bibliográfica sin DOI

`python scripts/sync_metadata.py` también genera BibTeX, RIS y CSL-JSON para las fichas con `citation_exports: true`, mediante `scripts/export_citations.py`. `--check` detecta archivos o enlaces desactualizados. Los seis archivos públicos se encuentran en `dist/citations/`; las fichas ofrecen enlaces de descarga y descubrimiento. Cada registro conserva nombre normalizado, título, mes de publicación, versión, URL canónica, resumen y palabras clave. RIS añade la URL del PDF. La afiliación no se convierte en editorial; no se inventan DOI, revista, actas ni fechas de presentación. Las fechas sólo precisas al mes se exportan sin añadir un día. BibTeX utiliza `@misc` y conserva serie y versión en `note`; CSL-JSON utiliza `report` y `paper-conference`; RIS utiliza `RPRT` y `CPAPER`. La versión queda en las notas para mantener su lectura entre gestores. Los datos de contribución, correspondencia, derechos y declaraciones editoriales completos siguen disponibles en la ficha y el registro maestro; no todos los formatos bibliográficos tienen campos interoperables para ellos.
