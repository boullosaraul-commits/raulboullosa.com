"""Check site hierarchy, navigation, publication routes and local links.

Use --inventory with a JSON list of tracked repository paths when binary
assets are present upstream but not materialized in this checkout.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.headings, self.navs = [], [], [], []
        self.current_nav = None
        self.mains = 0
        self.redirect = 'http-equiv="refresh"' in text
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.headings.append(int(tag[1]))
        if tag == 'main':
            self.mains += 1
        if tag == 'nav':
            self.current_nav = {'label': attrs.get('aria-label'), 'links': []}
            self.navs.append(self.current_nav)
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs)
            if self.current_nav is not None:
                self.current_nav['links'].append(attrs)

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.current_nav = None


def check(inventory=()):
    dist = ROOT / 'dist'
    pages = {p.relative_to(dist).as_posix(): Page(p.read_text())
             for p in dist.rglob('*.html') if '__qa' not in p.parts}
    tracked = set(inventory)
    navigation = None
    checked_links = 0
    for name, page in pages.items():
        assert len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {name}'
        assert page.mains == 1 and page.headings.count(1) == 1, f'Page landmarks: {name}'
        if not page.redirect:
            assert 'contenido' in page.ids, f'Missing skip-link target: {name}'
            for previous, current in zip(page.headings, page.headings[1:]):
                assert current <= previous + 1, f'Skipped heading level: {name}'
            main = next(n for n in page.navs if n['label'] == 'Navegación principal')
            footer = next(n for n in page.navs if n['label'] == 'Navegación institucional')
            urls = [a['href'] for a in main['links']]
            if navigation is None:
                navigation = urls
            assert urls == navigation == [a['href'] for a in footer['links']], f'Different menus: {name}'
            if name != '404.html':
                assert sum('aria-current' in a for a in main['links']) == 1, f'Active section: {name}'
            if name != 'index.html':
                assert any(n['label'] == 'Ruta de navegación' for n in page.navs), f'Breadcrumbs: {name}'
        for attrs in page.links:
            url = urlsplit(attrs['href'])
            if url.scheme and url.scheme not in ('http', 'https'):
                continue
            if url.netloc and url.netloc != 'raulboullosa.com':
                continue
            if not url.path:
                target = name
            elif url.path.startswith('/'):
                target = unquote(url.path.lstrip('/'))
                target = target + 'index.html' if not target or target.endswith('/') else target
            else:
                target = (Path(name).parent / unquote(url.path)).as_posix()
            assert (dist / target).is_file() or 'dist/' + target in tracked, f'Broken link: {name} -> {attrs["href"]}'
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, f'Broken anchor: {name} -> {attrs["href"]}'
            if target.startswith('pdf/'):
                assert attrs.get('aria-label'), f'Unlabelled PDF: {name}'
            checked_links += 1
    records = json.loads((ROOT / 'metadata/publications.json').read_text())['publications']
    for record in records:
        page = pages[record['path'].removeprefix('dist/')]
        sections = next(n for n in page.navs if n['label'] == 'Secciones de esta página')
        assert any(a['href'] == '#referencia' for a in sections['links']), record['id']
        assert any(a['href'].startswith('/pdf/') for a in sections['links']), record['id']
    print(f'PASS: {len(pages)} HTML routes, {len(records)} publication pages, {checked_links} internal links; common menus, hierarchy and anchors.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', type=Path)
    args = parser.parse_args()
    check(json.loads(args.inventory.read_text()) if args.inventory else ())
