# Ready Books — Technology Explorer Series

**Author:** Fansci Solutions  
**Target Audience:** Ages 8–12 (Book 3: 10–13)  
**Format:** LaTeX (pdflatex + makeindex)

---

## Repository Structure

```
ready-books/
├── print/                    # Print-optimized editions
│   ├── The Secret Life of the Internet/
│   ├── Inside a Smartphone/
│   └── Robot World/
├── digital/                  # Digital/screen-optimized editions
│   ├── The Secret Life of the Internet/
│   ├── Inside a Smartphone/
│   ├── Robot World/
│   ├── latex_to_epub.py      # LaTeX → Markdown → EPUB converter
│   └── render_tikz_diagrams.py  # TikZ → PNG renderer (no system LaTeX needed)
├── regenerated characters/   # AI-generated full-body character PNGs
├── character_prompts.md      # Image generation prompts for all characters
├── Review.txt                # Full pre-publication review
└── README.md                 # This file
```

Both `print/` and `digital/` contain identical content (chapters, glossary, quiz, teacher guide) but differ in their `preamble.tex` settings for output optimization.

---

## Print vs Digital — Key Differences

| Setting | Print Edition | Digital Edition |
|---------|--------------|-----------------|
| Trim / page size | 7 × 9 in (children's non-fiction standard) | 8.5 × 11 in (tablet/screen) |
| Margins | Inner 1.1 in (gutter-safe), outer 0.85 in | 0.75 in all sides (max content area) |
| Colour model | CMYK (press-ready) | sRGB (screen standard) |
| Hyperlinks | Hidden (no blue text in print) | Active, coloured, clickable |
| PDF bookmarks | Disabled | Enabled + expanded by default |
| Line spacing | Standard (1.0) | 1.15× (screen readability) |
| Accessibility | Alt-text macro available | Tagged PDF (`accessibility` package) |
| Diagram labels | `\diagramlabel{}` enforces 10pt minimum | `\screendiagram` auto-scales to viewport |

---

## Series Status

| # | Title | Age Band | Status |
|---|-------|----------|--------|
| 1 | The Secret Life of the Internet | 9–12 | ✅ Review fixes applied |
| 2 | Inside a Smartphone: The Tiny World in Your Hand | 9–12 | ✅ Review fixes applied |
| 3 | Robot World: Meet the Machines That Help Us | 10–13 | ✅ Review fixes applied (substantial) |

---

## Compile Instructions

### PDF (Print or Digital)

Each book compiles independently from within its folder:

```bash
cd print/The\ Secret\ Life\ of\ the\ Internet
pdflatex main.tex
makeindex main.idx
pdflatex main.tex
pdflatex main.tex
```

Three passes resolve cross-references, index, and TOC. Same process for `digital/`.

---

### EPUB (for KDP / eBook Distribution)

The EPUB pipeline converts the digital edition's LaTeX source into a KDP-ready EPUB3 file. It handles all custom macros (callout boxes, character dialogue, terminology) and embeds pre-rendered TikZ diagrams as images.

#### Prerequisites

```bash
pip install pypandoc_binary pypdfium2
```

No system LaTeX install needed — the renderer uses **tectonic** (auto-downloaded on first run).

#### Step 1: Render TikZ Diagrams to PNG

This extracts every `\begin{diagram}...\end{diagram}` block from the chapter files, compiles each as a standalone PDF via tectonic, and converts to high-resolution PNG.

```bash
cd digital/
python render_tikz_diagrams.py "The Secret Life of the Internet"
```

Output: `The Secret Life of the Internet/assets/diagrams/*.png`

To render all three books at once:

```bash
python render_tikz_diagrams.py "The Secret Life of the Internet"
python render_tikz_diagrams.py "Inside a Smartphone"
python render_tikz_diagrams.py "Robot World"
```

#### Step 2: Convert LaTeX to EPUB

This reads all chapter `.tex` files, converts custom LaTeX macros to Pandoc-flavoured Markdown, then calls Pandoc to produce EPUB3 with cover image and styled CSS.

```bash
python latex_to_epub.py "The Secret Life of the Internet"
```

Output:
- `The Secret Life of the Internet/The Secret Life of the Internet.md` (intermediate Markdown)
- `The Secret Life of the Internet/epub.css` (KDP-friendly stylesheet)
- `The Secret Life of the Internet/The Secret Life of the Internet.epub` (final EPUB3)

To convert all books:

```bash
python latex_to_epub.py --all
```

#### Step 3: Validate (Optional)

Use [epubcheck](https://www.w3.org/publishing/epubcheck/) to validate before KDP upload:

```bash
java -jar epubcheck.jar "The Secret Life of the Internet.epub"
```

#### How the Conversion Handles Custom Macros

| LaTeX Element | EPUB Output |
|---------------|-------------|
| `\character{Name}{speech}` | Styled blockquote with bold name |
| `\begin{bigidea}` | Blockquote with 💡 emoji heading |
| `\begin{picturethis}` | Blockquote with 🎨 emoji heading |
| `\begin{tryit}` | Blockquote with ✋ emoji heading |
| `\begin{funfact}` | Blockquote with ⭐ emoji heading |
| `\begin{diagram}[caption]` | `![caption](assets/diagrams/slug.png)` |
| `\term{word}` | **bold** text |
| `\chapteropening{text}` | Italicised intro paragraph |
| TikZ (standalone) | Pre-rendered PNG from Step 1 |
| tcolorbox (remaining) | Stripped; content preserved |
| `\sectionrule` | Horizontal rule (`---`) |

#### Troubleshooting

| Issue | Fix |
|-------|-----|
| "Could not fetch resource" warnings | Run `render_tikz_diagrams.py` first (Step 1) |
| Tectonic download fails | Check internet access; or manually download from [GitHub releases](https://github.com/tectonic-typesetting/tectonic/releases) and place binary at `/tmp/tectonic_bin/tectonic` |
| Pandoc not found | Ensure `pypandoc_binary` is installed (`pip install pypandoc_binary`) |
| Tables show as "[See table in print edition]" | Complex LaTeX tables don't reflow in EPUB; simplify or replace with lists |
| Diagram PNGs too narrow | Increase `scale` param in `render_tikz_diagrams.py` (default: 4) |

---

## Review Changes Applied

Based on the Professional Pre-Publication Review (see `Review.txt`):

### Book 1 — The Secret Life of the Internet
- [x] Recap boxes in Chapters 4, 5, 6 ("Remember So Far")
- [x] "Digital Explorer's Backpack" naming confirmed
- [x] Accessibility `\alttext` macro in preamble
- [x] Ch1 diagram wrapped in `\resizebox` for print trim

### Book 2 — Inside a Smartphone
- [x] Pronunciation guides in New Words (Chapters 2, 3, 4)
- [x] "Most ordinary gloves…" qualification confirmed
- [x] Chapter 10 tone smoothed with scenario `picturethis` boxes

### Book 3 — Robot World
- [x] Age repositioned to 10–13 (visible on Welcome page)
- [x] "Before You Begin" series bridge in front matter
- [x] Glossary deduplicated ("Autonomy", "Infrared")
- [x] Cross-book callbacks in Chapters 3 and 10
- [x] "Think and Talk" guided reflection prompts in Chapter 10

---

## File Structure (per book, both editions)

```
<Book Title>/
├── main.tex              # Root document
├── preamble.tex          # Edition-specific settings (PRINT or DIGITAL)
├── copyright.tex         # Copyright / imprint page
├── glossary.tex          # Back-of-book glossary
├── quiz.tex              # End-of-book quiz + answer key
├── teacher_guide.tex     # Parent & Teacher Guide
├── assets/
│   ├── characters/       # Full-body character PNGs (Book 1 done)
│   ├── characters.tex    # \includegraphics character commands
│   ├── diagrams/         # Pre-rendered TikZ diagram PNGs (for EPUB)
│   └── cover.png         # Cover image (where available)
└── chapters/
    ├── 01_*.tex … 10_*.tex
```

---

## Remaining Open Items

### Production
- [ ] CMYK proof testing on print editions
- [ ] Spine-width verification and gutter spacing checks
- [x] EPUB3 conversion pipeline (working — Book 1 complete)
- [ ] Cover image for Robot World
- [ ] Render diagrams for Books 2 and 3

### Content
- [ ] Stronger diversity in illustrations
- [x] Character TikZ → full-body PNGs (Book 1 done, Books 2–3 pending)
- [ ] Final proofread and page-break tuning
- [ ] Consider Chapter 11 (connectivity) for Book 2
