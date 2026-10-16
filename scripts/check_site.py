"""Validate static portfolio pages and local navigation without dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'public'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.refs = []
        self.tags = set()
        self.errors = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.add(tag)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append(f"duplicate id: {attrs['id']}")
            self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == 'img' and 'alt' not in attrs:
            self.errors.append('image missing alt attribute')
        if tag == 'html' and not attrs.get('lang'):
            self.errors.append('html missing language')


def validate(root=ROOT):
    root = root.resolve()
    pages = {p.resolve(): Page(p) for p in root.rglob('*.html')}
    errors = []
    if root / 'index.html' not in pages:
        errors.append('public/index.html is required')
    for path, page in pages.items():
        for tag in ('html', 'head', 'title', 'body', 'main'):
            if tag not in page.tags:
                page.errors.append(f'missing {tag}')
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (root / unquote(url.path).lstrip('/') if url.path.startswith('/')
                      else path.parent / unquote(url.path)) if url.path else path
            target = target.resolve()
            if not target.is_relative_to(root):
                page.errors.append(f'link outside publish directory: {ref}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                page.errors.append(f'missing local target: {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                page.errors.append(f'missing anchor: {ref}')
        errors.extend(f'{path.relative_to(root)}: {error}' for error in page.errors)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Validated {len(pages)} HTML page(s): local links, anchors, structure, image alt text.')

if __name__ == '__main__':
    validate()
