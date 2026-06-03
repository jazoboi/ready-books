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
  - pandoc installed (apt-get install pandoc / brew install pandoc)
  - Pre-rendered diagram images in assets/diagrams/ (PNG or SVG)
  - Character images in assets/characters/

Note: Run from within the digital/<Book>/ directory or pass the path.
"""

import re
import os
import sys
import glob
import subprocess


# ============================================================
#  MACRO CONVERSION RULES
# ============================================================

def convert_chapter(text):
    """Convert a single .tex chapter to Markdown."""
    
    # --- Remove LaTeX comments ---
    text = re.sub(r'(?m)^%.*$', '', text)
    
    # --- Chapter title ---
    text = re.sub(r'\\chapter\{(.+?)\}', r'# \1', text)
    
    # --- Section / subsection ---
    text = re.sub(r'\\section\*?\{(.+?)\}', r'## \1', text)
    text = re.sub(r'\\subsection\*?\{(.+?)\}', r'### \1', text)
    
    # --- Chapter opening (italic intro) ---
    text = re.sub(
        r'\\chapteropening\{(.*?)\}',
        lambda m: f'*{clean_inline(m.group(1).strip())}*\n',
        text, flags=re.DOTALL
    )
    
    # --- Chapter badge ---
    text = re.sub(r'\\chapterbadge\{(.+?)\}', r'> **\1**\n', text)
    
    # --- Character speech boxes ---
    def convert_character(m):
        name = m.group(1).strip()
        speech = clean_inline(m.group(2).strip())
        return f'\n> **{name}:** *"{speech}"*\n'
    text = re.sub(r'\\character\{(.+?)\}\{(.*?)\}', convert_character, text, flags=re.DOTALL)
    
    # --- Callout boxes: bigidea, picturethis, tryit, funfact, newwords, quickmap, experiment, quickcheck ---
    callout_titles = {
        'bigidea': '💡 Big Idea',
        'picturethis': '🎨 Imagine This',
        'tryit': '✋ Try It',
        'funfact': '⭐ Fun Fact',
        'newwords': '📖 New Words',
        'quickmap': '🗺️ Quick Map',
        'experiment': '🔬 Experiment',
        'quickcheck': '✓ Quick Check',
    }
    
    for env, title in callout_titles.items():
        pattern = r'\\begin\{' + env + r'\}(?:\[.*?\])?(.*?)\\end\{' + env + r'\}'
        def make_callout(m, t=title):
            body = clean_inline(m.group(1).strip())
            # Convert to blockquote with title
            lines = body.split('\n')
            quoted = '\n'.join(f'> {l}' for l in lines)
            return f'\n> **{t}**\n>\n{quoted}\n'
        text = re.sub(pattern, make_callout, text, flags=re.DOTALL)
    
    # --- Diagram environments → image references ---
    def convert_diagram(m):
        caption = m.group(1).strip() if m.group(1) else "Diagram"
        # Generate a slug for the expected image filename
        slug = re.sub(r'[^a-z0-9]+', '-', caption.lower()).strip('-')[:50]
        return f'\n![{caption}](assets/diagrams/{slug}.png)\n'
    text = re.sub(r'\\begin\{diagram\}\[?(.*?)\]?(.*?)\\end\{diagram\}', convert_diagram, text, flags=re.DOTALL)
    
    # --- TikZ standalone (outside diagram env) — remove, note for manual export ---
    text = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', 
                  '\n*[Diagram — see print edition]*\n', text, flags=re.DOTALL)
    
    # --- Lists ---
    # itemize
    text = re.sub(r'\\begin\{itemize\}', '', text)
    text = re.sub(r'\\end\{itemize\}', '', text)
    text = re.sub(r'\\item\s*(?:\\textbf\{(.+?)\})?\s*', lambda m: f'- **{m.group(1)}** ' if m.group(1) else '- ', text)
    
    # enumerate
    text = re.sub(r'\\begin\{enumerate\}(?:\[.*?\])?', '', text)
    text = re.sub(r'\\end\{enumerate\}', '', text)
    # Numbered items — simplified
    counter = [0]
    def number_item(m):
        counter[0] += 1
        prefix = m.group(1) if m.group(1) else ''
        return f'{counter[0]}. {prefix} '
    text = re.sub(r'\\item\s*(?:\\textbf\{(.+?)\})?\s*', number_item, text)
    
    # --- description lists ---
    text = re.sub(r'\\begin\{description\}(?:\[.*?\])?', '', text)
    text = re.sub(r'\\end\{description\}', '', text)
    
    # --- Inline formatting ---
    text = clean_inline(text)
    
    # --- Remove remaining LaTeX commands we don't need ---
    text = re.sub(r'\\sectionrule', '\n---\n', text)
    text = re.sub(r'\\vspace\{.*?\}', '', text)
    text = re.sub(r'\\needspace\{.*?\}', '', text)
    text = re.sub(r'\\hfill', '', text)
    text = re.sub(r'\\noindent', '', text)
    text = re.sub(r'\\centering', '', text)
    text = re.sub(r'\\begin\{center\}', '', text)
    text = re.sub(r'\\end\{center\}', '', text)
    text = re.sub(r'\\begin\{tcolorbox\}(?:\[.*?\])?', '', text, flags=re.DOTALL)
    text = re.sub(r'\\end\{tcolorbox\}', '', text)
    text = re.sub(r'\\begin\{tabular[x]?\}.*?\\end\{tabular[x]?\}', '\n*[Table — see print edition]*\n', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\resizebox\{.*?\}\{.*?\}\{', '', text)
    text = re.sub(r'\\rule\{.*?\}\{.*?\}', '', text)
    text = re.sub(r'\\label\{.*?\}', '', text)
    text = re.sub(r'\\index\{.*?\}', '', text)
    text = re.sub(r'\\hline', '', text)
    text = re.sub(r'\\\\', '\n', text)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)  # catch remaining \cmd{text} → text
    text = re.sub(r'\\[a-zA-Z]+', '', text)  # remaining bare commands
    
    # --- Clean up ---
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text


def clean_inline(text):
    """Convert inline LaTeX formatting to Markdown."""
    # \textbf{...} → **...**
    text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
    # \emph{...} or \textit{...} → *...*
    text = re.sub(r'\\emph\{([^}]*)\}', r'*\1*', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)
    # \term{...} → **term** (bold, since these are vocabulary words)
    text = re.sub(r'\\term\{([^}]*)\}', r'**\1**', text)
    # \glossterm{...} → **term**
    text = re.sub(r'\\glossterm\{([^}]*)\}', r'**\1**', text)
    # \url{...}
    text = re.sub(r'\\url\{([^}]*)\}', r'[\1](\1)', text)
    # \textemdash → —
    text = re.sub(r'\\textemdash\{\}?', '—', text)
    # \textbar → |
    text = re.sub(r'\\textbar\{\}?', '|', text)
    # \ldots → …
    text = re.sub(r'\\ldots', '…', text)
    # Remove \, spacing
    text = re.sub(r'\\,', '', text)
    # ~ → space
    text = text.replace('~', ' ')
    # { and } cleanup
    text = text.replace('{', '').replace('}', '')
    return text


def build_book_markdown(book_dir):
    """Assemble all chapters into a single Markdown document."""
    
    chapters_dir = os.path.join(book_dir, 'chapters')
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, '*.tex')))
    
    parts = []
    
    # Front matter (could add from main.tex welcome section)
    book_name = os.path.basename(book_dir)
    parts.append(f'---\ntitle: "{book_name}"\nauthor: "Fansci Solutions"\nlang: en-GB\n---\n')
    
    for cf in chapter_files:
        with open(cf, 'r', encoding='utf-8') as f:
            tex = f.read()
        md = convert_chapter(tex)
        parts.append(md)
        parts.append('\n\n')
    
    # Glossary
    glossary_path = os.path.join(book_dir, 'glossary.tex')
    if os.path.exists(glossary_path):
        with open(glossary_path, 'r', encoding='utf-8') as f:
            tex = f.read()
        parts.append('\n# Glossary\n\n')
        parts.append(convert_chapter(tex))
    
    return '\n'.join(parts)


def write_epub_css():
    """Generate a simple CSS for KDP EPUB styling."""
    return """
/* Technology Explorer Series — EPUB stylesheet */
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    margin: 1em;
    color: #212121;
}
h1 { color: #2196F3; margin-top: 2em; page-break-before: always; }
h2 { color: #2196F3; margin-top: 1.5em; }
h3 { color: #FF9800; margin-top: 1em; }
blockquote {
    background: #f5f5f5;
    border-left: 4px solid #2196F3;
    padding: 0.8em 1em;
    margin: 1em 0;
    border-radius: 4px;
}
blockquote strong:first-child {
    display: block;
    margin-bottom: 0.4em;
    color: #2196F3;
}
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1em auto;
}
hr { border: none; border-top: 1px solid #87CEEB; margin: 1.5em 0; }
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python latex_to_epub.py <book_folder_name>")
        print("       python latex_to_epub.py --all")
        sys.exit(1)
    
    base = os.path.dirname(os.path.abspath(__file__))
    
    if sys.argv[1] == '--all':
        books = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
    else:
        books = [sys.argv[1]]
    
    for book in books:
        book_dir = os.path.join(base, book)
        if not os.path.exists(os.path.join(book_dir, 'main.tex')):
            continue
        
        print(f"\n{'='*60}")
        print(f"  Converting: {book}")
        print(f"{'='*60}")
        
        # Build markdown
        md_content = build_book_markdown(book_dir)
        
        # Write intermediate .md
        md_path = os.path.join(book_dir, f'{book}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  ✅ Markdown: {md_path}")
        
        # Write CSS
        css_path = os.path.join(book_dir, 'epub.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(write_epub_css())
        print(f"  ✅ CSS: {css_path}")
        
        # Build EPUB via Pandoc
        epub_path = os.path.join(book_dir, f'{book}.epub')
        cover_path = os.path.join(book_dir, 'assets', 'cover.png')
        
        cmd = [
            'pandoc', md_path,
            '-o', epub_path,
            '--css', css_path,
            '--toc',
            '--toc-depth=2',
            '--epub-chapter-level=1',
            '--metadata', f'title={book}',
            '--metadata', 'creator=Fansci Solutions',
            '--metadata', 'lang=en-GB',
        ]
        
        if os.path.exists(cover_path):
            cmd.extend(['--epub-cover-image', cover_path])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"  ✅ EPUB: {epub_path}")
            else:
                print(f"  ⚠️  Pandoc warning: {result.stderr[:200]}")
                print(f"  📄 Markdown ready at: {md_path}")
                print(f"     Run manually: pandoc '{md_path}' -o '{epub_path}' --css '{css_path}' --toc")
        except FileNotFoundError:
            print(f"  ⚠️  Pandoc not installed. Markdown ready at: {md_path}")
            print(f"     Install: pip install pandoc OR apt-get install pandoc")
            print(f"     Then run: pandoc '{md_path}' -o '{epub_path}' --css '{css_path}' --toc")
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Pandoc timed out. Try running manually.")


if __name__ == '__main__':
    main()
