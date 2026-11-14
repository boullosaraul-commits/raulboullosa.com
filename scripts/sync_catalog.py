"""Render the catalog and homepage selections from the publication registry."""
from pathlib import Path
import html, json, re, sys
ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'metadata/publications.json').read_text())['publications']
E = html.escape

def row(r):
    kind = {'essay':'Ensayo', 'conference_paper':'Ponencia', 'research_manuscript':'Manuscrito de investigación'}.get(r['publication_type'], 'Trabajo')
    version = 'v' + str(r['version']) if r.get('version') else 'versión de circulación'
    url = r['url'].removeprefix('https://raulboullosa.com')
    pdf = r['pdf'].removeprefix('https://raulboullosa.com')
    return (f'<article class="essay-row"><span class="essay-row__code">{E(r["id"])} · {E(kind)} · {E(r["datePublished"][:4])} · {E(version)}</span>'
            f'<div><a class="essay-row__title-link" href="{E(url)}"><h3 class="essay-row__title">{E(r["title"])}</h3></a>'
            f'<p>{E(r["description"])}</p></div><span class="essay-row__actions"><a href="{E(url)}">Ver ficha</a> / '
            f'<a href="{E(pdf)}" aria-label="Abrir PDF: {E(r["title"], quote=True)}">PDF</a></span></article>')

catalog = ROOT / 'dist/ensayos/index.html'
s = catalog.read_text()
start = s.index('<header class="page-hero">', s.index('<main '))
end = s.index('<!-- page-return:start -->', start)
ordered = sorted(records, key=lambda r: (r.get('datePublished') or '', r['id']), reverse=True)
body = ('<header class="page-hero"><div class="container"><p class="eyebrow">Archivo académico</p><h1>Documentos de trabajo</h1>'
        '<p>Ensayos, ponencias y manuscritos de investigación. La identificación conserva las series existentes; no indica arbitraje ni afiliación institucional. '
        'Cada ficha identifica la edición disponible, cómo citarla y, cuando se conservan, sus versiones anteriores.</p></div></header>'
        '<section class="section" id="archivo"><div class="container"><h2 id="archivo-titulo">Catálogo completo</h2><div class="essay-list">' + ''.join(map(row, ordered)) + '</div></div></section>\n')
s = s[:start] + body + s[end:]
s = s.replace('<title>Publicaciones — Raúl Boullosa</title>', '<title>Documentos de trabajo — Raúl Boullosa</title>')
updates = {catalog:s}
home = ROOT / 'dist/index.html'
s = home.read_text()
start = s.index('<section class="home-hero"')
end = s.index('<section class="section section--ink"', start)
selected = [next(r for r in records if r['id'] == i) for i in ('valle-marx-tssi-v2-5','rb-ensayos-2026-02','sitepe-2026-v14')]
body = ('<section class="home-hero"><div class="container home-hero__grid"><div><p class="eyebrow">Economía política</p><h1>Raúl Alberto Rivera Boullosa</h1></div>'
        '<div class="home-hero__aside"><p>Estudiante de Economía, Facultad de Economía, Universidad Nacional Autónoma de México.</p>'
        '<p>Intereses: teoría del valor y precios, reproducción social, circulación monetaria, inversión e historia del pensamiento económico.</p>'
        '<a class="action-link" href="/ensayos/">Explorar documentos de trabajo</a></div></div></section>'
        '<section class="section" aria-labelledby="seleccion"><div class="container"><h2 id="seleccion">Documentos destacados</h2><div class="essay-list">' + ''.join(map(row, selected)) + '</div><a class="text-link" href="/ensayos/">Ver catálogo completo</a></div></section>\n')
s = s[:start] + body + s[end:]
updates[home] = s
for p, value in updates.items():
    if p.read_text() != value:
        if '--check' in sys.argv: raise SystemExit('Catálogo desactualizado: ' + str(p))
        p.write_text(value)
