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
│   └── Robot World/
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

## Review Changes Applied

Based on the Professional Pre-Publication Review (see `Review.txt`):

### Book 1 — The Secret Life of the Internet
- [x] Recap boxes in Chapters 4, 5, 6 ("Remember So Far")
- [x] "Digital Explorer's Backpack" naming confirmed
- [x] Accessibility `\alttext` macro in preamble

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

## Compile Instructions

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
│   ├── characters.tex    # TikZ character icon commands
│   └── cover.png         # Cover image (where available)
└── chapters/
    ├── 01_*.tex … 10_*.tex
```

---

## Remaining Open Items

### Production
- [ ] CMYK proof testing on print editions
- [ ] Spine-width verification and gutter spacing checks
- [ ] EPUB3 conversion from digital edition source
- [ ] Cover image for Robot World

### Content
- [ ] Stronger diversity in illustrations
- [ ] Refine character TikZ to full-body drawings
- [ ] Final proofread and page-break tuning
- [ ] Consider Chapter 11 (connectivity) for Book 2
