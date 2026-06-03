#!/usr/bin/env python3
"""
render_tikz_diagrams.py — Technology Explorer Series
Extracts TikZ diagrams from chapter .tex files and renders them as PNG images.

No root access or system LaTeX needed — uses tectonic (auto-downloaded) + pypdfium2.

Usage:
  python render_tikz_diagrams.py                    # Process current directory
  python render_tikz_diagrams.py path/to/book/      # Process specific book

Prerequisites (pip install):
  pypdfium2

The script will auto-download tectonic if not present.
"""

import os
import re
import sys
import stat
import subprocess
import tarfile
import urllib.request

# ============================================================
#  TECTONIC SETUP (auto-download)
# ============================================================

TECTONIC_VERSION = "0.15.0"
TECTONIC_URL = f"https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic@{TECTONIC_VERSION}/tectonic-{TECTONIC_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
TECTONIC_PATH = "/tmp/tectonic_bin/tectonic"


def ensure_tectonic():
    """Download tectonic if not already present."""
    if os.path.exists(TECTONIC_PATH):
        return TECTONIC_PATH
    
    print("Downloading tectonic LaTeX engine...")
    os.makedirs("/tmp/tectonic_bin", exist_ok=True)
    urllib.request.urlretrieve(TECTONIC_URL, "/tmp/tectonic.tar.gz")
    with tarfile.open("/tmp/tectonic.tar.gz", "r:gz") as tar:
        tar.extractall("/tmp/tectonic_bin")
    os.chmod(TECTONIC_PATH, os.stat(TECTONIC_PATH).st_mode | stat.S_IEXEC)
    
    result = subprocess.run([TECTONIC_PATH, '--version'], capture_output=True, text=True)
    print(f"  ✅ {result.stdout.strip()}")
    return TECTONIC_PATH


# ============================================================
#  COLOUR PALETTES (shared across all books)
# ============================================================

COLOUR_DEFS = r"""
\definecolor{InternetBlue}{HTML}{2196F3}
\definecolor{WarmOrange}{HTML}{FF9800}
\definecolor{LeafGreen}{HTML}{4CAF50}
\definecolor{SunYellow}{HTML}{FFC107}
\definecolor{CoralRed}{HTML}{F44336}
\definecolor{SoftPurple}{HTML}{9C27B0}
\definecolor{SkyBlue}{HTML}{87CEEB}
\definecolor{LightGray}{HTML}{F5F5F5}
\definecolor{DarkText}{HTML}{212121}
\definecolor{TechPurple}{HTML}{7B1FA2}
\definecolor{RoboGreen}{HTML}{00C853}
\definecolor{NeonGreen}{HTML}{76FF03}
\definecolor{SteelBlue}{HTML}{607D8B}
"""

STANDALONE_PREAMBLE = r"""\documentclass[border=10pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[sfdefault]{sourcesanspro}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,shapes,shapes.symbols,positioning,decorations.pathmorphing,calc,shadows,fit,backgrounds}
\usepackage{fontawesome5}
\usepackage{array}
\usepackage{tabularx}
\usepackage{ragged2e}
\usepackage{enumitem}
\newcolumntype{Y}{>{\RaggedRight\arraybackslash}X}
""" + COLOUR_DEFS + r"""
\begin{document}
"""

STANDALONE_END = r"""
\end{document}
"""


# ============================================================
#  EXTRACTION & RENDERING
# ============================================================

def extract_diagrams(tex_content):
    """Extract all \\begin{diagram}[caption]...\\end{diagram} from a .tex file."""
    pattern = r'\\begin\{diagram\}\[(.*?)\](.*?)\\end\{diagram\}'
    return re.findall(pattern, tex_content, re.DOTALL)


def caption_to_filename(caption):
    """Convert a diagram caption to a slug filename."""
    return re.sub(r'[^a-z0-9]+', '-', caption.lower()).strip('-')[:50] + '.png'


def render_tikz_to_png(tikz_body, output_path, scale=4):
    """Compile TikZ code to PNG via tectonic + pypdfium2."""
    import pypdfium2 as pdfium
    
    tex = STANDALONE_PREAMBLE + tikz_body + STANDALONE_END
    
    tmp_dir = "/tmp/tikz_render"
    os.makedirs(tmp_dir, exist_ok=True)
    tex_path = os.path.join(tmp_dir, "diagram.tex")
    
    with open(tex_path, 'w') as f:
        f.write(tex)
    
    result = subprocess.run(
        [TECTONIC_PATH, tex_path],
        capture_output=True, text=True, timeout=120, cwd=tmp_dir
    )
    
    pdf_path = os.path.join(tmp_dir, "diagram.pdf")
    if not os.path.exists(pdf_path):
        return False, result.stderr[-200:]
    
    pdf = pdfium.PdfDocument(pdf_path)
    page = pdf[0]
    bitmap = page.render(scale=scale)
    img = bitmap.to_pil()
    img.save(output_path, optimize=True)
    
    return True, f"{img.size[0]}x{img.size[1]}px, {os.path.getsize(output_path)//1024}KB"


# ============================================================
#  MAIN
# ============================================================

def main():
    book_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    book_dir = os.path.abspath(book_dir)
    
    chapters_dir = os.path.join(book_dir, 'chapters')
    output_dir = os.path.join(book_dir, 'assets', 'diagrams')
    
    if not os.path.isdir(chapters_dir):
        print(f"Error: No chapters/ directory found in {book_dir}")
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)
    ensure_tectonic()
    
    # Process all chapters
    chapter_files = sorted(f for f in os.listdir(chapters_dir) if f.endswith('.tex'))
    total = 0
    success = 0
    
    for cf in chapter_files:
        with open(os.path.join(chapters_dir, cf), 'r') as f:
            tex = f.read()
        
        diagrams = extract_diagrams(tex)
        if not diagrams:
            continue
        
        print(f"\n{cf}:")
        for caption, body in diagrams:
            total += 1
            filename = caption_to_filename(caption)
            output_path = os.path.join(output_dir, filename)
            
            ok, info = render_tikz_to_png(body.strip(), output_path)
            if ok:
                success += 1
                print(f"  ✅ {filename} ({info})")
            else:
                print(f"  ❌ {filename}: {info}")
    
    print(f"\n{'='*50}")
    print(f"Rendered {success}/{total} diagrams → {output_dir}")


if __name__ == '__main__':
    main()
