# Inside a Smartphone: The Tiny World in Your Hand
**The Secret Life of Technology — Book 2**
Author: Fansci Solutions

---

## About This Book
A children's educational technology book (ages 8–12) that takes readers inside a
smartphone and explains how every major component works. Companion to
*The Secret Life of the Internet* (Book 1).

---

## File Structure
```
Inside a Smartphone/
├── main.tex              # Root document — compile this
├── preamble.tex          # Packages, colours, callout box macros
├── copyright.tex         # Copyright / imprint page
├── glossary.tex          # Alphabetical glossary (32 terms)
├── quiz.tex              # End-of-book quiz (6 parts + answer key)
├── teacher_guide.tex     # Parent & Teacher Guide (per chapter)
├── assets/
│   ├── characters.tex      # TikZ character icon commands
│   └── cover.png           # Cover image
└── chapters/
    ├── 01_what_is_a_smartphone.tex
    ├── 02_the_processor.tex
    ├── 03_memory_and_storage.tex
    ├── 04_the_touchscreen.tex
    ├── 05_tiny_cameras.tex
    ├── 06_the_battery.tex
    ├── 07_hidden_sensors.tex
    ├── 08_apps.tex
    ├── 09_gps.tex
    └── 10_stay_safe_and_smart.tex
```

---

## Characters
| Character | Role |
|-----------|------|
| Dot       | Returning guide from Book 1 (information packet) |
| Chip      | The processor — phone's brain |
| Memo      | Memory & storage |
| Tappy     | The touchscreen |
| Lens      | The camera |
| Zap       | The battery |
| Sensa     | The sensors |
| Appy      | Apps |
| Orbi      | GPS satellite |

---

## Callout Box Reference
| Box | Macro | Colour | Purpose |
|-----|-------|--------|---------|
| Big Idea | `bigidea` | Purple | Chapter takeaway |
| Imagine This | `picturethis` | Orange | Analogies & visualisations |
| Try It | `tryit` | Green | Hands-on reader activities |
| Experiment | `experiment` | Teal | Guided experiments (new in Book 2) |
| Quick Map | `quickmap` | Yellow | Step-by-step sequences |
| New Words | `newwords` | Soft purple | Vocabulary per chapter |
| Did You Know? | `funfact` | Coral red | Fun facts & statistics |

---

## Compile Instructions
```bash
pdflatex main.tex
makeindex main.idx
pdflatex main.tex
pdflatex main.tex
```
Three passes are needed to resolve cross-references, the index, and the TOC.

---

## Series
- Book 1: *The Secret Life of the Internet* ✅
- Book 2: *Inside a Smartphone: The Tiny World in Your Hand* ✅ (compiles)

---

## Open Items / Notes
- [x] Cover image (`assets/cover.png`) — added
- [x] `assets/characters.tex` TikZ icon commands — defined (simple icon style)
- [x] Glossary — 32 terms
- [x] Quiz — 6 parts with answer key (191 lines)
- [ ] Consider adding a Chapter 11 on connectivity (Wi-Fi, Bluetooth, 4G/5G)
  as a bridge back to Book 1's router/Wi-Fi content
- [ ] Refine character TikZ illustrations into full-body drawings
- [ ] Final proofread and page-break tuning
