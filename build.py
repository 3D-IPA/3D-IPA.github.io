#!/usr/bin/env python3
"""
build.py — Assembles the 3D IPA Lab static site from source partials and page content.

Usage:
    python3 build.py

Source files (edit these):
    src/_partials/head.html       — shared <head> block
    src/_partials/header.html     — shared site header + navigation
    src/_partials/footer.html     — shared site footer + scripts
    src/css/wp-blocks.css         — WordPress block CSS (rarely needs editing)
    src/css/site.css              — Site-specific styles (brand colors, etc.)
    src/pages/index.html          — Home page content
    src/pages/people.html         — People page content
    src/pages/research.html       — Research page content
    src/pages/publications.html   — Publications page content
    src/pages/facilities.html     — Facilities page content
    src/pages/contact.html        — Join the Lab page content

Output (generated — do not edit directly):
    index.html
    people/index.html
    research/index.html
    publications/index.html
    facilities/index.html
    contact/index.html
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, 'src')

# ---------------------------------------------------------------------------
# Page definitions
# Each entry: (page_key, page_title, content_file, output_file, depth)
# depth=0 → root (ROOT=""), depth=1 → one level deep (ROOT="../")
# ---------------------------------------------------------------------------
PAGES = [
    ('home',         '3D IPA Lab',        'pages/index.html',        'index.html',              0),
    ('people',       'People',            'pages/people.html',       'people/index.html',        1),
    ('research',     'Research',          'pages/research.html',     'research/index.html',      1),
    ('publications', 'Publications',      'pages/publications.html', 'publications/index.html',  1),
    ('facilities',   'Facilities',        'pages/facilities.html',   'facilities/index.html',    1),
    ('contact',      'Join the Lab',      'pages/contact.html',      'contact/index.html',       1),
]

# Nav item keys in the order they appear in header.html
NAV_KEYS = ['home', 'people', 'research', 'publications', 'facilities', 'contact']

ACTIVE_CLASS = ' current-menu-item current_page_item'

def read(path):
    with open(os.path.join(SRC, path), encoding='utf-8') as f:
        return f.read()

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  wrote {path}')

def build_page(page_key, page_title, content_file, output_file, depth):
    root_prefix = '../' * depth

    head    = read('_partials/head.html')
    header  = read('_partials/header.html')
    content = read(content_file)
    footer  = read('_partials/footer.html')

    # -- Substitute {{ROOT}} throughout --
    for part in ('head', 'header', 'footer'):
        locals()[part]  # ensure defined
    head    = head.replace('{{ROOT}}', root_prefix)
    header  = header.replace('{{ROOT}}', root_prefix)
    footer  = footer.replace('{{ROOT}}', root_prefix)

    # -- Page title --
    head = head.replace('{{PAGE_TITLE}}', page_title)

    # -- Active nav item: add class + aria-current to the current page's <li>/<a> --
    for key in NAV_KEYS:
        KEY = key.upper()
        if key == page_key:
            header = header.replace(f'{{{{ACTIVE_{KEY}}}}}', ACTIVE_CLASS)
            header = header.replace(f'{{{{ARIA_{KEY}}}}}', ' aria-current="page"')
        else:
            header = header.replace(f'{{{{ACTIVE_{KEY}}}}}', '')
            header = header.replace(f'{{{{ARIA_{KEY}}}}}', '')

    html = head + '\n' + header + '\n' + content + '\n' + footer
    write(output_file, html)

def main():
    print('Building 3D IPA Lab site...')
    for args in PAGES:
        build_page(*args)
    print('Done.')

if __name__ == '__main__':
    main()
