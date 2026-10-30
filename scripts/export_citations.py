"""Build UTF-8 bibliographic downloads from the publication registry."""
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- citation-exports:start -->'
END = '<!-- citation-exports:end -->'
HEAD_START = '<!-- citation-discovery:start -->'
HEAD_END = '<!-- citation-discovery:end -->'


def one_line(text):
    return ' '.join(text.split())


def bib_escape(text):
    substitutions = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}',
                     '&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#',
                     '$': r'\$', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(substitutions.get(char, char) for char in one_line(text))


def formats(record, people):
    authors = [people[c['person']] for c in record['contributors'] if c['author']]
    names = [{'family': a['family_name'], 'given': a['given_names']} for a in authors]
    title = record['title']
    if record.get('subtitle'):
        title += ': ' + record['subtitle']
    date = [int(part) for part in record['datePublished'].split('-')]
    note = 'Versión ' + record['version'] if record.get('version') else record['edition_label']
    series = record.get('series')
    if series:
        note = series['name'] + ', ' + str(series['position']).zfill(2) + '. ' + note
    csl = {
        'id': record['id'],
        'type': 'paper-conference' if record['publication_type'] == 'conference_paper' else 'report',
        'title': title, 'author': names, 'issued': {'date-parts': [date]},
        'URL': record['url'], 'language': record['inLanguage'], 'note': note,
    }
    if series:
        csl['collection-title'] = series['name']
        csl['number'] = str(series['position']).zfill(2)
    if record.get('abstract'):
        csl['abstract'] = one_line(record['abstract'])
    if record.get('keywords'):
        csl['keyword'] = '; '.join(record['keywords'])
    if record.get('numberOfPages'):
        csl['number-of-pages'] = str(record['numberOfPages'])
    if record['publication_type'] == 'conference_paper':
        csl['event-title'] = 'SITEPE 2026'
    fields = {
        'author': ' and '.join(a['family'] + ', ' + a['given'] for a in names),
        'title': title, 'year': str(date[0]), 'url': record['url'],
        'note': note, 'language': record['inLanguage'],
    }
    if record.get('abstract'):
        fields['abstract'] = record['abstract']
    if record.get('keywords'):
        fields['keywords'] = '; '.join(record['keywords'])
    lines = ['@misc{' + record['id'] + ',']
    for key, value in fields.items():
        escaped = bib_escape(value)
        if key == 'title':
            escaped = '{' + escaped + '}'
        lines.append('  ' + key + ' = {' + escaped + '},')
    if len(date) >= 2:
        lines.append('  month = ' + ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][date[1] - 1] + ',')
    lines.append('}')
    ris = [('TY', 'CPAPER' if record['publication_type'] == 'conference_paper' else 'RPRT'),
           ('ID', record['id'])]
    ris += [('AU', a['family'] + ', ' + a['given']) for a in names]
    ris += [('TI', title), ('PY', str(date[0])),
            ('DA', '/'.join(str(n).zfill(2) for n in date) + '/'),
            ('UR', record['url']), ('L1', record['pdf']), ('LA', record['inLanguage']),
            ('N1', note)]
    if record.get('version'):
        ris.append(('ET', record['version']))
    if series:
        ris += [('T2', series['name']), ('IS', str(series['position']).zfill(2))]
    if record.get('abstract'):
        ris.append(('AB', record['abstract']))
    ris += [('KW', key) for key in record.get('keywords', [])]
    ris.append(('ER', ''))
    return {
        'bib': '\n'.join(lines) + '\n',
        'ris': '\n'.join(key + '  - ' + one_line(value) for key, value in ris) + '\n',
        'csl.json': json.dumps([csl], ensure_ascii=False, indent=2) + '\n',
    }


def sync(data, check=False):
    changed = []
    for record in data['publications']:
        if not record.get('citation_exports'):
            continue
        downloads = formats(record, data['people'])
        links = []
        discoveries = []
        types = {'bib': ('BibTeX', 'application/x-bibtex'),
                 'ris': ('RIS', 'application/x-research-info-systems'),
                 'csl.json': ('CSL-JSON', 'application/vnd.citationstyles.csl+json')}
        for ext, contents in downloads.items():
            relative = 'citations/' + record['id'] + '.' + ext
            path = ROOT / 'dist' / relative
            if not path.exists() or path.read_text() != contents:
                changed.append(str(path.relative_to(ROOT)))
                if not check:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(contents, encoding='utf-8')
            label, mime = types[ext]
            links.append('<a class="action-link" href="/' + relative +
                         '" download type="' + mime + '">' + label + ' ↓</a>')
            discoveries.append('<link rel="alternate" type="' + mime +
                               '" href="/' + relative + '" title="' + label + '">')
        title = record['title'] + (': ' + record['subtitle'] if record.get('subtitle') else '')
        meta = [('citation_title', title), ('citation_publication_date', record['datePublished'].replace('-', '/')),
                ('citation_language', record['inLanguage']), ('citation_pdf_url', record['pdf'])]
        meta += [('citation_author', data['people'][c['person']]['family_name'] + ', ' +
                  data['people'][c['person']]['given_names']) for c in record['contributors'] if c['author']]
        head = HEAD_START + '\n' + '\n'.join(discoveries + [
            '<meta name="' + key + '" content="' + html.escape(value, quote=True) + '">'
            for key, value in meta]) + '\n' + HEAD_END
        visible = (START + '\n<p><strong>Descargar referencia bibliográfica</strong></p>' +
                   '\n<div class="article-actions">' + ' '.join(links) + '</div>\n' + END)
        path = ROOT / record['path']
        original = path.read_text()
        updated = re.sub(re.escape(HEAD_START) + '.*?' + re.escape(HEAD_END),
                         lambda _: head, original, flags=re.S) if HEAD_START in original else original.replace('</head>', head + '\n</head>')
        if START in updated:
            updated = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: visible, updated, flags=re.S)
        else:
            updated, count = re.subn(r'(<p class="citation">.*?</p>)',
                                    lambda m: m[1] + '\n' + visible, updated, count=1, flags=re.S)
            assert count == 1, record['id']
        if original != updated:
            changed.append(record['path'])
            if not check:
                path.write_text(updated)
    if check and changed:
        raise SystemExit('Stale citation exports: ' + ', '.join(changed))
    print(f'Bibliographic downloads: {len(changed)} files updated.')
