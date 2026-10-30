# Registro maestro de publicaciones

`publications.json` conserva las fichas de RB · Ensayos 2026 · 01–07 y del paper SITEPE v14 como ocho objetos distintos. Editar el registro y ejecutar `python scripts/sync_metadata.py`; después comprobar con `python scripts/sync_metadata.py --check`. El resultado sigue siendo HTML estático, sin dependencia de JavaScript en el navegador.

El registro distingue autoría (`author`), contribuciones CRediT (`roles`, siempre una lista) y correspondencia (`corresponding`). Raúl Alberto Rivera Boullosa queda designado como autor de correspondencia de estos trabajos individuales; esto no publica una dirección de correo.

Los roles permanecen vacíos y con estado `pending_confirmation` hasta verificar las contribuciones de cada trabajo. No se deducen papeles CRediT de la autoría individual. Para publicarlos, completar la lista con los términos admitidos y cambiar `roles_status` a `confirmed`. El generador conserva `author` como Person y expresa contribuciones verificadas mediante `contributor` y Schema.org Role.

ORCID, afiliación de cada publicación, licencia y financiación desconocidos se representan como `null` y se omiten de la salida pública. `funding: null` no significa ausencia de financiación. No reutilizar la afiliación actual del perfil como evidencia de una afiliación histórica de publicación.

Las fechas mantienen la precisión comprobada de las fichas existentes (mes). La fecha de modificación de esta capa de metadatos no se convierte en fecha de publicación ni de modificación del texto. Las palabras clave de SITEPE son una selección editorial basada en la sinopsis publicada; no se presentan como una transcripción del PDF. Se conserva la sinopsis existente sin convertirla en el abstract íntegro del paper.

SITEPE y Ensayo 05 se enlazan como documentos relacionados, sin afirmar identidad entre versiones ni una relación de sustitución. El PDF, su ruta y su contenido permanecen intactos.

Esta es una fuente interna y una salida web Schema.org; no constituye un depósito Crossref ni un XML Schema 5.5. Un futuro exportador Crossref deberá validar tipos, roles e identificadores contra su esquema oficial. No añadir `correspondingAuthor` o `contributor_role` como si fueran propiedades Schema.org: la correspondencia se conserva en el registro y se muestra en la ficha.
