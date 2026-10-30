"""Keep site navigation, breadcrumbs and section indexes consistent."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- page-navigation:start -->'
END = '<!-- page-navigation:end -->'
LINKS = [('/', 'Inicio'), ('/ensayos/', 'Publicaciones'),
         ('/investigacion/', 'Investigación'), ('/sobre-mi/', 'Sobre mí'),
         ('https://open.substack.com/pub/raulboullosa', 'Substack ↗')]


def menu(active, current='page'):
    return ''.join('<a href="' + url + '"' +
                   (' aria-current="' + current + '"' if url == active else '') + '>' +
                   label + '</a>' for url, label in LINKS)


def sync(check=False):
    changed = []
    records = {r['path'].removeprefix('dist/'): r for r in
               json.loads((ROOT / 'metadata/publications.json').read_text())['publications']}
    for path in sorted((ROOT / 'dist').rglob('*.html')):
        original = path.read_text()
        if 'http-equiv="refresh"' in original or '/__qa/' in str(path):
            continue
        relative = str(path.relative_to(ROOT / 'dist'))
        is_work = relative.startswith(('ensayos/', 'publicaciones/')) and relative != 'ensayos/index.html'
        if relative == 'index.html':
            active, label = '/', 'Inicio'
        elif relative == 'ensayos/index.html' or is_work:
            active, label = '/ensayos/', 'Publicaciones'
        elif relative == 'investigacion/index.html':
            active, label = '/investigacion/', 'Investigación'
        elif relative == 'sobre-mi/index.html':
            active, label = '/sobre-mi/', 'Sobre mí'
        else:
            active, label = None, 'Página no encontrada'
        header = ('<header class="masthead"><div class="container masthead__inner">'
                  '<a class="brand" href="/" aria-label="Raúl Boullosa, inicio">'
                  '<span class="brand__mark" aria-hidden="true">RB<span class="brand__slash">/</span></span>'
                  '<span>Raúl Boullosa</span></a><nav class="nav" aria-label="Navegación principal">' +
                  menu(active, 'true' if is_work else 'page') + '</nav></div></header>')
        updated, count = re.subn(r'<header class="masthead">.*?</header>',
                                 lambda _: header, original, count=1, flags=re.S)
        assert count == 1, relative
        updated = re.sub(r'(<nav class="footer__nav"[^>]*>).*?(</nav>)',
                         lambda m: m[1] + menu(active, 'true' if is_work else 'page') + m[2], updated, count=1, flags=re.S)
        updated = re.sub(r'\s*' + re.escape(START) + '.*?' + re.escape(END) + r'\s*', '', updated, flags=re.S)
        if active != '/':
            crumbs = '<li><a href="/">Inicio</a></li>'
            if is_work:
                crumbs += '<li><a href="/ensayos/">Publicaciones</a></li>'
                current = 'SITEPE v14' if relative.startswith('publicaciones/') else (
                    'Ensayo ' + re.search(r'Archivo / Ensayo (\d+)|Texto seleccionado / Ensayo (\d+)', updated).group(0).split('Ensayo ')[-1])
            else:
                current = label
            crumbs += '<li><span aria-current="page">' + html.escape(current) + '</span></li>'
            sections = re.findall(r'<h2\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', updated, re.S)
            anchors = []
            for anchor, text in sections:
                text = html.unescape(re.sub('<[^>]+>', '', text))
                if text == 'Texto':
                    text = 'Documento'
                if text == 'Referencia sugerida':
                    text = 'Cómo citar'
                anchors.append('<a href="#' + anchor + '">' + html.escape(text) + '</a>')
            if is_work:
                anchors.insert(0, '<a class="page-index__primary" href="' +
                               records[relative]['pdf'].removeprefix('https://raulboullosa.com') +
                               '">Abrir PDF</a>')
            index = ''
            if anchors:
                index = ('<details class="page-index"' + (' open' if is_work or active == '/ensayos/' else '') +
                         '><summary>En esta página</summary><nav aria-label="Secciones de esta página">' +
                         ''.join(anchors) + '</nav></details>')
            navigation = (START + '<div class="container page-navigation">'
                          '<nav class="breadcrumbs" aria-label="Ruta de navegación"><ol>' +
                          crumbs + '</ol></nav>' + index + '</div>' + END + '\n')
            updated, count = re.subn(r'(<main\b[^>]*>)', lambda m: m[1] + '\n' + navigation,
                                     updated, count=1)
            assert count == 1
        # Consistent visible labels; the PDF link opens the definitive edition.
        updated = updated.replace('>Leer</a>', '>Ver ficha</a>').replace('>Ficha</a>', '>Ver ficha</a>')
        updated = updated.replace('>Abrir ficha →</a>', '>Ver ficha</a>')
        updated = updated.replace('>PDF A5 ↓</a>', '>Abrir PDF A5</a>').replace('>PDF A4 ↓</a>', '>Abrir PDF A4</a>')
        updated = updated.replace('La lectura HTML se incorporará en esta misma dirección estable; la ficha y la referencia no cambiarán.',
                                  'Los datos bibliográficos de esta edición y su referencia se encuentran al final de esta ficha.')
        def label_pdf(match):
            attrs, url, tail = match.groups()
            pdf = next((r for r in records.values() if
                        r['pdf'].removeprefix('https://raulboullosa.com') == url), None)
            if not pdf:
                return match[0]
            attributes = attrs + ' href="' + url + '"' + tail
            attributes = re.sub(r'\s+aria-label="[^"]*"', '', attributes)
            return '<a' + attributes + ' aria-label="Abrir PDF: ' + html.escape(pdf['title'], quote=True) + '">'
        updated = re.sub(r'<a([^>]*?)\s+href="(/pdf/[^"]+)"([^>]*)>', label_pdf, updated)
        # Shared return action at the bottom of every content page.
        updated = re.sub(r'\s*<!-- page-return:start -->.*?<!-- page-return:end -->\s*', '', updated, flags=re.S)
        back = ('<!-- page-return:start --><nav class="container page-return" aria-label="Continuar la navegación">' +
                ('<a href="/ensayos/">← Volver a publicaciones</a>' if is_work else '<a href="/">← Volver a inicio</a>') +
                '<a href="#contenido">Volver arriba ↑</a></nav><!-- page-return:end -->\n')
        updated = updated.replace('</main>', '\n' + back + '</main>', 1)
        if updated != original:
            changed.append(relative)
            if not check:
                path.write_text(updated)
    if check and changed:
        raise SystemExit('Stale navigation: ' + ', '.join(changed))
    print(f'Site navigation: {len(changed)} pages updated.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    sync(check=parser.parse_args().check)
