#!/usr/bin/env python3
"""
latex_to_epub.py — Technology Explorer Series
Converts the LaTeX book source into KDP-ready EPUB via Pandoc.

Pipeline:
  1. Read all chapter .tex files in order
  2. Strip/convert LaTeX macros to Pandoc-flavoured Markdown
  3. Replace TikZ diagrams with pre-rendered image references
  4. Convert tcolorbox callouts to styled blockquotes
  5. Output a single .md file per book
  6. Call Pandoc to produce EPUB with metadata + CSS

Usage:
  python latex_to_epub.py "The Secret Life of the Internet"
  python latex_to_epub.py --all

Prerequisites:
  pip install pypandoc_binary
  (Pandoc is bundled with pypandoc_binary — no separate install needed)
"""

import re
import os
import sys
import glob

try:
    import pypandoc
except ImportError:
    print("ERROR: pypandoc_binary not installed. Run: pip install pypandoc_binary")
    sys.exit(1)


# ============================================================
#  INLINE FORMATTING
# ============================================================

def clean_inline(text):
    """Convert inline LaTeX to Markdown. Does NOT handle \\term inside \\item labels."""
    text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'*\1*', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)
    text = re.sub(r'\\url\{([^}]*)\}', r'[\1](\1)', text)
    text = re.sub(r'\\textemdash\{?\}?', '\u2014', text)
    text = re.sub(r'\\textbar\{?\}?', '|', text)
    text = re.sub(r'\\ldots', '\u2026', text)
    text = re.sub(r'\\,', '', text)
    text = text.replace('~', ' ')
    text = text.replace("``", "\u201c").replace("''", "\u201d")
    return text


# ============================================================
#  ITEM / LIST PROCESSING
# ============================================================

def process_items(text):
    r"""Handle \item[label] patterns BEFORE clean_inline to avoid double-bold.
    \item[\term{X}] → - **X** —   (single bold layer)
    \item[\textbf{X}] → - **X** —
    \item[Plain] → - **Plain** —
    \item → -
    """
    text = re.sub(r'\\item\[\\(?:gloss)?term\{([^}]+)\}\]\s*', r'- **\1** \u2014 ', text)
    text = re.sub(r'\\item\[\\textbf\{([^}]+)\}\]\s*', r'- **\1** \u2014 ', text)
    text = re.sub(r'\\item\[([^\]]+)\]\s*', r'- **\1** \u2014 ', text)
    text = re.sub(r'\\item\s*', '- ', text)
    return text


# ============================================================
#  CHAPTER CONVERSION
# ============================================================

CALLOUTS = {
    'bigidea': '\U0001f4a1 Big Idea',
    'picturethis': '\U0001f3a8 Imagine This',
    'tryit': '\u270b Try It',
    'funfact': '\u2b50 Fun Fact',
    'newwords': '\U0001f4d6 New Words',
    'quickmap': '\U0001f5fa\ufe0f Quick Map',
    'experiment': '\U0001f52c Experiment',
    'quickcheck': '\u2713 Quick Check',
}


def convert_chapter(text):
    """Convert a single .tex chapter to clean Markdown."""

    # Remove comments
    text = re.sub(r'(?m)^%.*$', '', text)
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)

    # Structure
    text = re.sub(r'\\chapter\{(.+?)\}', r'# \1', text)
    text = re.sub(r'\\section\*?\{(.+?)\}', r'## \1', text)
    text = re.sub(r'\\subsection\*?\{(.+?)\}', r'### \1', text)

    # Chapter opening
    def fmt_opening(m):
        body = re.sub(r'\s+', ' ', m.group(1).strip())
        return f'\n*{clean_inline(body)}*\n'
    text = re.sub(r'\\chapteropening\{(.*?)\}', fmt_opening, text, flags=re.DOTALL)

    # Chapter badge
    text = re.sub(r'\\chapterbadge\{(.+?)\}', r'> **\1**\n', text)

    # Character speech
    def fmt_char(m):
        name = m.group(1).strip()
        speech = re.sub(r'\s+', ' ', m.group(2).strip())
        speech = clean_inline(speech)
        return f'\n> **{name}:** *\u201c{speech}\u201d*\n'
    text = re.sub(r'\\character\{(.+?)\}\{(.*?)\}', fmt_char, text, flags=re.DOTALL)

    # Callout boxes
    for env, title in CALLOUTS.items():
        pat = r'\\begin\{' + env + r'\}(?:\[.*?\])?(.*?)\\end\{' + env + r'\}'
        def mk_callout(m, t=title):
            body = m.group(1).strip()
            body = re.sub(r'\\begin\{(?:description|itemize|enumerate)\}(?:\[.*?\])?', '', body)
            body = re.sub(r'\\end\{(?:description|itemize|enumerate)\}', '', body)
            body = process_items(body)
            body = clean_inline(body)
            body = re.sub(r'\\(?:gloss)?term\{([^}]*)\}', r'**\1**', body)
            lines = [l.strip() for l in body.split('\n') if l.strip()]
            quoted = '\n'.join(f'> {l}' for l in lines)
            return f'\n> **{t}**\n>\n{quoted}\n'
        text = re.sub(pat, mk_callout, text, flags=re.DOTALL)

    # Remember So Far recap boxes
    def fmt_recap(m):
        body = m.group(1).strip()
        body = process_items(body)
        body = clean_inline(body)
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        quoted = '\n'.join(f'> {l}' for l in lines)
        return f'\n> **\U0001f504 Remember So Far**\n>\n{quoted}\n'
    text = re.sub(r'\\begin\{tcolorbox\}\[.*?Remember So Far.*?\](.*?)\\end\{tcolorbox\}',
                  fmt_recap, text, flags=re.DOTALL)

    # Remaining tcolorbox
    text = re.sub(r'\\begin\{tcolorbox\}\[.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{tcolorbox\}', '', text)
    text = re.sub(r'\\end\{tcolorbox\}', '', text)

    # Diagrams
    def fmt_diag(m):
        cap = m.group(1).strip()
        slug = re.sub(r'[^a-z0-9]+', '-', cap.lower()).strip('-')[:50]
        return f'\n![{cap}](assets/diagrams/{slug}.png)\n'
    text = re.sub(r'\\begin\{diagram\}\[(.*?)\](.*?)\\end\{diagram\}', fmt_diag, text, flags=re.DOTALL)

    # TikZ standalone
    text = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
                  '\n*[See illustration in print edition]*\n', text, flags=re.DOTALL)

    # List environments
    text = re.sub(r'\\begin\{itemize\}', '', text)
    text = re.sub(r'\\end\{itemize\}', '', text)
    text = re.sub(r'\\begin\{enumerate\}(?:\[.*?\])?', '', text)
    text = re.sub(r'\\end\{enumerate\}', '', text)
    text = re.sub(r'\\begin\{description\}(?:\[.*?\])?', '', text)
    text = re.sub(r'\\end\{description\}', '', text)

    # Remaining items
    text = process_items(text)

    # Tables
    text = re.sub(r'\\begin\{tabular[x]?\}.*?\\end\{tabular[x]?\}',
                  '\n*[See table in print edition]*\n', text, flags=re.DOTALL)

    # Remaining inline
    text = clean_inline(text)
    text = re.sub(r'\\(?:gloss)?term\{([^}]*)\}', r'**\1**', text)

    # Section rule
    text = re.sub(r'\\sectionrule', '\n---\n', text)

    # Noise
    noise = [
        r'\\vspace\{[^}]*\}', r'\\needspace\{[^}]*\}', r'\\hfill',
        r'\\noindent', r'\\centering', r'\\begin\{center\}', r'\\end\{center\}',
        r'\\begin\{figure\}.*?\\end\{figure\}', r'\\resizebox\{[^}]*\}\{[^}]*\}\{',
        r'\\rule\{[^}]*\}\{[^}]*\}', r'\\label\{[^}]*\}', r'\\index\{[^}]*\}',
        r'\\hline', r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}',
        r'\\markboth\{[^}]*\}\{[^}]*\}', r'\\thispagestyle\{[^}]*\}',
    ]
    for pat in noise:
        text = re.sub(pat, '', text, flags=re.DOTALL)

    # Remaining \cmd{arg}
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Clean braces and whitespace
    text = text.replace('{', '').replace('}', '')
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+\n', '\n', text)
    return text.strip()


# ============================================================
#  BOOK ASSEMBLY
# ============================================================

# Character data per book
CHARACTERS = {
    "The Secret Life of the Internet": [
        ("Dot", "A tiny glowing packet of information \u2014 your main guide."),
        ("Bee Browser", "A cheerful bee who takes you to any website."),
        ("Willa Wifi", "Invisible waves that carry signals through the air."),
        ("Rory Router", "The friendly box that directs traffic in your home."),
        ("Sunny Server", "A powerful computer that stores and sends information."),
        ("Captain Cable", "The undersea cable that carries data across oceans."),
        ("Scout Search", "The detective who finds anything on the internet."),
        ("Cloud Pal", "Faraway computers that store your files safely."),
    ],
}


def build_book_markdown(book_dir):
    """Assemble all chapters into a single Markdown document."""
    book_name = os.path.basename(book_dir)
    chapters_dir = os.path.join(book_dir, 'chapters')
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, '*.tex')))

    parts = [f'---\ntitle: "{book_name}"\nauthor: "Fansci Solutions"\nlang: en-GB\n---\n']

    # Character page (if available)
    chars = CHARACTERS.get(book_name, [])
    if chars:
        parts.append('\n# Meet Your Guides\n\n')
        for name, desc in chars:
            parts.append(f'![{name}](assets/characters/{name}.png)\n')
            parts.append(f'**{name}** \u2014 {desc}\n\n')
        parts.append('---\n\n')

    # Chapters
    for cf in chapter_files:
        with open(cf, 'r', encoding='utf-8') as f:
            tex = f.read()
        parts.append(convert_chapter(tex))
        parts.append('\n\n')

    # Glossary
    glossary_path = os.path.join(book_dir, 'glossary.tex')
    if os.path.exists(glossary_path):
        with open(glossary_path, 'r', encoding='utf-8') as f:
            tex = f.read()
        parts.append('\n# Glossary\n\n')
        glos = convert_chapter(tex)
        glos = re.sub(r'^Glossary\s*\n', '', glos)
        parts.append(glos)

    return '\n'.join(parts)


def write_epub_css():
    """KDP-optimized CSS with reliable font rendering."""
    return """/* Technology Explorer Series — EPUB stylesheet (KDP-optimized) */
body {
    font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.65;
    margin: 1em;
    color: #212121;
    font-size: 1em;
}
h1 { color: #2196F3; font-weight: 700; margin-top: 2em; page-break-before: always; font-size: 1.8em; }
h2 { color: #2196F3; font-weight: 700; margin-top: 1.5em; font-size: 1.4em; }
h3 { color: #FF9800; font-weight: 600; margin-top: 1em; font-size: 1.2em; }
strong, b { font-weight: 700; }
em, i { font-style: italic; }
blockquote {
    background: #f5f5f5;
    border-left: 4px solid #2196F3;
    padding: 0.8em 1em;
    margin: 1em 0;
    border-radius: 4px;
    font-size: 0.95em;
}
blockquote strong:first-child { display: block; margin-bottom: 0.4em; color: #2196F3; font-size: 1.05em; }
img { max-width: 100%; max-height: 40vh; height: auto; display: block; margin: 0.8em auto; }
hr { border: none; border-top: 1px solid #87CEEB; margin: 1.5em 0; }
ul, ol { margin-left: 1.2em; padding-left: 0.5em; }
li { margin-bottom: 0.3em; }
p { margin-bottom: 0.6em; orphans: 2; widows: 2; }
"""


# ============================================================
#  MAIN
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python latex_to_epub.py <book_folder_name>")
        print("       python latex_to_epub.py --all")
        sys.exit(1)

    base = os.path.dirname(os.path.abspath(__file__))

    if sys.argv[1] == '--all':
        books = [d for d in os.listdir(base)
                 if os.path.isdir(os.path.join(base, d))
                 and os.path.exists(os.path.join(base, d, 'main.tex'))]
    else:
        books = [sys.argv[1]]

    for book in books:
        book_dir = os.path.join(base, book)
        if not os.path.exists(os.path.join(book_dir, 'main.tex')):
            print(f"Skipping {book} (no main.tex)")
            continue

        print(f"\n{'='*60}\n  Converting: {book}\n{'='*60}")

        md_content = build_book_markdown(book_dir)
        md_path = os.path.join(book_dir, f'{book}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  \u2705 Markdown: {md_path}")

        css_path = os.path.join(book_dir, 'epub.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(write_epub_css())

        epub_path = os.path.join(book_dir, f'{book}.epub')
        cover_path = os.path.join(book_dir, 'assets', 'cover.png')

        extra_args = [
            '--toc', '--toc-depth=2', '--split-level=1',
            f'--css={css_path}',
            f'--metadata=title:{book}',
            '--metadata=creator:Fansci Solutions',
            '--metadata=lang=en-GB',
            f'--resource-path={book_dir}',
        ]
        if os.path.exists(cover_path):
            extra_args.append(f'--epub-cover-image={cover_path}')

        try:
            output = pypandoc.convert_file(md_path, 'epub3', outputfile=epub_path, extra_args=extra_args)
            size_kb = os.path.getsize(epub_path) / 1024
            print(f"  \u2705 EPUB: {epub_path} ({size_kb:.0f} KB)")
            if output:
                warnings = [l for l in output.strip().split('\n') if 'WARNING' in l and 'Resource' in l]
                if warnings:
                    print(f"  \u26a0\ufe0f  Missing images: {len(warnings)} (run render_tikz_diagrams.py first)")
        except Exception as e:
            print(f"  \u274c EPUB failed: {e}")
            print(f"     Markdown ready at: {md_path}")


if __name__ == '__main__':
    main()
