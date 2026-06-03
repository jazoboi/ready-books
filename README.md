# Ready Books — Technology Explorer Series

**Author:** Fansci Solutions  
**Target Audience:** Ages 8–12 (Book 3: 10–13)  
**Format:** LaTeX (pdflatex + makeindex)

---

## Series Status

| # | Title | Status | Age Band |
|---|-------|--------|----------|
| 1 | The Secret Life of the Internet | ✅ Review fixes applied | 9–12 |
| 2 | Inside a Smartphone: The Tiny World in Your Hand | ✅ Review fixes applied | 9–12 |
| 3 | Robot World: Meet the Machines That Help Us | ✅ Review fixes applied (substantial) | 10–13 |

---

## Review Changes Applied

Based on the Professional Pre-Publication Review (see `Review.txt`), the following
changes have been applied to this repository:

### Book 1 — The Secret Life of the Internet

- [x] **Recap boxes** added to Chapters 4, 5, and 6 ("Remember So Far") to reduce cognitive density in the networking/packet sections
- [x] **"Digital Explorer's Backpack"** naming confirmed (was already applied in source)
- [x] Accessibility `\alttext` macro already present in preamble

### Book 2 — Inside a Smartphone

- [x] **Pronunciation guides** added to New Words sections in Chapters 2, 3, and 4 (the most terminology-dense chapters)
- [x] **Gloves oversimplification** already qualified ("Most ordinary gloves…") in source
- [x] **Chapter 10 tone shift** smoothed with scenario-based `picturethis` boxes (app permissions analogy, screen time narrative)

### Book 3 — Robot World

- [x] **Age repositioning** — visible "Recommended for ages 10–13" note added to Welcome page
- [x] **Series bridge** — "Before You Begin" box linking to Books 1 & 2 added to front matter
- [x] **Glossary duplicates removed** — "Autonomy" (duplicate of "Autonomous") and second "Infrared" entry
- [x] **Cross-book callback** added to Chapter 3 (sensors link to Book 2's Sensa)
- [x] **Cross-book callback** added to Chapter 10 opening (recap of internet + smartphone sensors)
- [x] **Guided reflection prompts** — "Think and Talk" ethics discussion box added to Chapter 10

---

## Remaining Open Items (Not Yet Applied)

These items require design/production work beyond text editing:

### Production / Design
- [ ] Tagged PDFs + alt text for all diagrams (accessibility, Critical)
- [ ] Clickable TOC / EPUB navigation for digital versions
- [ ] Reduce text density by 10–15% across all books; increase whitespace
- [ ] Enlarge diagram labels (minimum 9–10pt for print)
- [ ] Mobile-optimized layouts / vector SVG diagrams for EPUB
- [ ] CMYK proof testing, spine-width verification, gutter spacing checks
- [ ] Build EPUB3 versions with scalable SVG diagrams

### Content / Editorial
- [ ] Stronger diversity and human representation in illustrations
- [ ] Cover image for Robot World (`assets/cover.png`)
- [ ] Refine character TikZ illustrations into full-body drawings (all books)
- [ ] Final proofread and page-break tuning (all books)
- [ ] First compile test of Robot World on MiKTeX
- [ ] Consider adding Chapter 11 (connectivity) to Book 2

---

## Compile Instructions

Each book compiles independently:

```bash
cd "The Secret Life of the Internet"
pdflatex main.tex
makeindex main.idx
pdflatex main.tex
pdflatex main.tex
```

Three passes resolve cross-references, index, and TOC.

---

## File Structure (per book)

```
<Book Title>/
├── main.tex              # Root document
├── preamble.tex          # Packages, colours, callout macros
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
