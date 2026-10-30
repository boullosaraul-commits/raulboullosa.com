"""Render publication JSON-LD and bylines from metadata/publications.json.

Run from any directory: python scripts/sync_metadata.py [--check].
Unknown values are omitted from public metadata, not interpreted as negatives.
"""
import argparse
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'metadata/publications.json').read_text())
CREDIT = {
    'Conceptualization', 'Data curation', 'Formal analysis', 'Funding acquisition',
    'Investigation', 'Methodology', 'Project administration', 'Resources',
    'Software', 'Supervision', 'Validation', 'Visualization',
    'Writing – original draft', 'Writing – review & editing',
}
START = '<!-- publication-contributors:start -->'
END = '<!-- publication-contributors:end -->'


def render(record):
    result = {
        '@context': 'https://schema.org', '@type': 'ScholarlyArticle',
        '@id': record['url'] + '#publication', 'headline': record['title'],
        'description': record['description'], 'datePublished': record['datePublished'],
        'inLanguage': record['inLanguage'], 'url': record['url'],
        'encoding': {'@type': 'MediaObject', 'contentUrl': record['pdf'],
                     'encodingFormat': 'application/pdf'},
    }
    authors, roles, lines = [], [], []
    editorial = []
    for contributor in record['contributors']:
        person = DATA['people'][contributor['person']]
        entity = {'@type': 'Person', '@id': person['id'],
                  'name': person['name'], 'url': person['url']}
        if person.get('orcid'):
            entity['sameAs'] = [person['orcid']]
        if contributor.get('correspondence_emails'):
            entity['email'] = contributor['correspondence_emails']
        affiliation = contributor.get('affiliation') or person.get('affiliation')
        if affiliation:
            entity['affiliation'] = affiliation
            label = affiliation['name']
            if affiliation.get('parentOrganization'):
                label += ', ' + affiliation['parentOrganization']['name']
            lines.append('<p class="publication-affiliation">' + html.escape(label) + '.</p>')
        if contributor['author']:
            authors.append(entity)
        assert set(contributor['roles']) <= CREDIT
        if contributor['roles']:
            assert contributor['roles_status'] == 'confirmed'
            roles.append({'@type': 'Role', 'roleName': contributor['roles'],
                          'contributor': entity})
        if contributor['corresponding']:
            lines.append('<p><strong>Autor de correspondencia:</strong> ' +
                         html.escape(person['name']) + '.</p>')
            if person.get('orcid'):
                lines.append('<p><a href="' + html.escape(person['orcid'], quote=True) +
                             '" rel="me">ORCID: ' + html.escape(person['orcid'].rsplit('/', 1)[-1]) + '</a></p>')
            if contributor.get('correspondence_emails'):
                lines.append('<p><strong>Contacto:</strong> ' + ' · '.join(
                    '<a href="mailto:' + html.escape(email, quote=True) + '">' +
                    html.escape(email) + '</a>' for email in contributor['correspondence_emails']) + '</p>')
        if contributor['roles']:
            editorial.append('<p><strong>Contribuciones (CRediT):</strong> ' +
                         html.escape(person['name']) + ': ' +
                         html.escape('; '.join(contributor['roles'])) + '.</p>')
    result['author'] = authors
    if roles:
        result['contributor'] = roles
    for field in ('abstract', 'keywords', 'version', 'license', 'funding', 'copyrightNotice', 'copyrightYear'):
        if record.get(field):
            result[field] = record[field]
    if record.get('copyrightNotice'):
        result['copyrightHolder'] = [{'@type': 'Person', '@id': a['@id'], 'name': a['name']}
                                     for a in authors]
    if record.get('funding_statement'):
        editorial.append('<p><strong>Financiación:</strong> ' +
                         html.escape(record['funding_statement']) + '</p>')
    if record.get('authorship_statement'):
        editorial.append('<p><strong>Autoría:</strong> ' +
                         html.escape(record['authorship_statement']) + '</p>')
    if record.get('ai_use_statement'):
        editorial.append('<p><strong>Uso de IA:</strong> ' +
                         html.escape(record['ai_use_statement']) + '</p>')
    if record.get('copyrightNotice'):
        editorial.append('<p>' + html.escape(record['copyrightNotice']) + '</p>')
    if editorial:
        lines.append('<details><summary>Contribuciones y condiciones editoriales</summary>' +
                     ''.join(editorial) + '</details>')
    if record.get('series'):
        series = dict(record['series'])
        result['position'] = series.pop('position')
        result['isPartOf'] = series
    if record.get('subtitle'):
        result['alternativeHeadline'] = record['subtitle']
    if record.get('numberOfPages'):
        result['pagination'] = str(record['numberOfPages']) + ' páginas físicas'
    if record.get('jel'):
        result['about'] = [
            {'@type': 'DefinedTerm', 'termCode': code,
             'inDefinedTermSet': {'@type': 'DefinedTermSet', 'name': 'JEL Classification'}}
            for code in record['jel']
        ]
    script = '<script type="application/ld+json">\n' + json.dumps(
        result, ensure_ascii=False, indent=2).replace('<', '\\u003c') + '\n  </script>'
    byline = START + '\n<div class="publication-contributors">' + ''.join(lines) + '</div>\n' + END
    return script, byline


def sync(check=False):
    stale = []
    for record in DATA['publications']:
        path = ROOT / record['path']
        original = path.read_text()
        script, byline = render(record)
        pattern = r'<script type="application/ld\+json">.*?</script>'
        if re.search(pattern, original, re.S):
            updated = re.sub(pattern, lambda _: script, original, count=1, flags=re.S)
        else:
            updated = original.replace('</head>', '  ' + script + '\n</head>')
        if record.get('abstract_paragraphs'):
            paragraphs = ''.join('<p>' + html.escape(p) + '</p>'
                                 for p in record['abstract_paragraphs'])
            updated, count = re.subn(
                r'(<h2 id="resumen">Resumen</h2>\s*<div class="article-summary__copy">)\s*.*?(?=<p class="keywords">)',
                lambda m: m[1] + '\n' + paragraphs, updated, count=1, flags=re.S)
            assert count == 1, record['path']
        updated = re.sub(r'\s*' + re.escape(START) + '.*?' + re.escape(END) + r'\s*',
                         '', updated, flags=re.S)
        updated, count = re.subn(
            r'(<p class="article-byline__version">.*?</p>)(\s*</div>)',
            lambda m: m[1] + '\n' + byline + m[2], updated, count=1, flags=re.S)
        assert count == 1, record['path']
        assert updated.count(START) == 1, record['path']
        if updated != original:
            stale.append(record['path'])
            if not check:
                path.write_text(updated)
    if check and stale:
        raise SystemExit('Stale metadata: ' + ', '.join(stale))
    from export_citations import sync as sync_citations
    sync_citations(DATA, check=check)
    print(f"Verified {len(DATA['publications'])} publication records; {len(stale)} updated.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    sync(parser.parse_args().check)
