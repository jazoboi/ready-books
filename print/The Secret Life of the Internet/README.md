# The Secret Life of the Internet

**Technology Explorer Series — Book 1**  
Published by **Fansci Solutions**

---

## About this book

*The Secret Life of the Internet* is a kid-friendly, highly visual non-fiction book that explains how the internet works. Written for visual learners aged 7–12, it follows a cast of friendly characters — Dot the data packet, Bee Browser, Willa Wi-Fi, Rory Router, Sunny Server, Captain Cable, Scout Search, and Cloud Pal — on a journey from a tap on a screen to the global infrastructure that delivers content in milliseconds.

The book covers nine chapters, a glossary, an end-of-book quiz, and a Parent & Teacher Guide. All text uses British English spelling.

---

## Building the PDF

From the repository root:

```bash
cd "The Secret Life of the Internet"
latexmk -pdf main.tex
```

**Manual fallback** (if `latexmk` is unavailable):

```bash
pdflatex main.tex          # pass 1 — writes auxiliary files
makeindex main.idx         # build the back-of-book index
pdflatex main.tex          # pass 2 — incorporate index and TOC
pdflatex main.tex          # pass 3 — resolve remaining references
```

Output: `main.pdf`

---

## File map

| File / Folder | Purpose |
|---|---|
| `main.tex` | Master document; assembles all parts |
| `preamble.tex` | Packages, colour palette, custom macros |
| `copyright.tex` | Copyright page (included by `main.tex`) |
| `glossary.tex` | Alphabetical back-matter glossary |
| `quiz.tex` | End-of-book quiz and review activities |
| `teacher_guide.tex` | Parent & Teacher Guide with discussion questions and activities |
| `assets/characters.tex` | TikZ illustrations of the eight guide characters |
| `chapters/` | One `.tex` file per chapter (01–09) |

---

## Chapter overview

| # | Title | Key concepts |
|---|-------|-------------|
| 1 | What Is the Internet? | Networks, packets, ISPs |
| 2 | Websites and Browsers | URLs, DNS, HTML, browsers |
| 3 | Wi-Fi and Routers | Radio waves, routers, Ethernet |
| 4 | Servers and Data Centres | Servers, data centres, request/response |
| 5 | Undersea Cables | Optical fibres, cable layers, amplifiers |
| 6 | How Messages and Videos Travel | Packets, TCP/IP, streaming |
| 7 | Search Engines | Crawlers, indexing, ranking |
| 8 | The Cloud | Cloud storage, cloud computing, remote servers |
| 9 | Stay Safe and Curious | Passwords, privacy, digital citizenship |

---

## Callout style guide

| Environment | Colour | Icon | Purpose |
|---|---|---|---|
| `bigidea` | Blue | 💡 | One-sentence chapter takeaway |
| `picturethis` | Orange | 🎨 | Visualisation / imagination prompt |
| `tryit` | Green | 👉 | Hands-on activity |
| `quickmap` | Yellow | — | Step-by-step flow or sequence |
| `newwords` | Purple | 📖 | Chapter vocabulary box |
| `funfact` | Coral Red | ⭐ | Interesting supporting fact |
| `diagram` | Sky Blue | — | Labelled TikZ diagram with alt-text |

---

## Language note

All book-facing text is written in **British English** (colour, programme, data centre, optical fibre, etc.).

---

© Fansci Solutions. All rights reserved.
