# Robot World: Meet the Machines That Help Us
**The Secret Life of Technology — Book 3**
Author: Fansci Solutions

---

## About This Book
A children's educational technology book (ages 8–12) that introduces readers to
the world of robots — from factory arms and delivery drones to humanoid helpers
and surgical bots. Explores how robots sense, think, and move.

---

## Status
✅ Scaffolded — all source files in place, ready for compile and review.

---

## Primary Colour
**RoboGreen** `#00C853`

---

## File Structure
```
Robot World/
├── main.tex              # Root document — compile this
├── preamble.tex          # Packages, colours, callout box macros
├── copyright.tex         # Copyright / imprint page
├── glossary.tex          # Alphabetical glossary (51 terms)
├── quiz.tex              # End-of-book quiz (6 parts + answer key)
├── teacher_guide.tex     # Parent & Teacher Guide (per chapter)
├── assets/
│   └── characters.tex      # TikZ character icon commands
└── chapters/
    ├── 01_what_is_a_robot.tex
    ├── 02_robot_bodies.tex
    ├── 03_how_robots_sense.tex
    ├── 04_the_robot_brain.tex
    ├── 05_factory_robots.tex
    ├── 06_robots_at_home.tex
    ├── 07_robots_in_space_and_sea.tex
    ├── 08_medical_robots.tex
    ├── 09_robot_friends.tex
    └── 10_the_future_of_robots.tex
```

---

## Chapters
1. What Is a Robot?
2. Robot Bodies — Arms, Wheels, and Legs
3. How Robots Sense the World
4. The Robot Brain
5. Factory Robots
6. Robots at Home
7. Robots in Space and Deep Sea
8. Medical Robots
9. Robot Friends — Companions and Pets
10. The Future of Robots

---

## Characters
| Character | Role |
|-----------|------|
| Dot       | Returning series guide (information packet) |
| Bolt      | Factory robot arm — strong and precise |
| Whirr     | Drone — sees from above |
| Sprocket  | Wheeled rover — explores tough terrain |
| Cora      | Humanoid companion — learns from people |
| Sparks    | Micro-bot surgeon — tiny but careful |
| Tread     | Rescue robot — brave and tough |
| Echo      | Home assistant robot — listens and learns |

---

## Callout Box Reference
| Box | Macro | Colour | Purpose |
|-----|-------|--------|---------|
| Big Idea | `bigidea` | RoboGreen | Chapter takeaway |
| Imagine This | `picturethis` | Orange | Analogies & visualisations |
| Try It | `tryit` | Leaf Green | Hands-on reader activities |
| Experiment | `experiment` | Teal | Guided experiments |
| Quick Map | `quickmap` | Yellow | Step-by-step sequences |
| New Words | `newwords` | Soft purple | Vocabulary per chapter |
| Did You Know? | `funfact` | Coral red | Fun facts & statistics |
| Quick Check | `quickcheck` | Steel blue | 3-question end-of-chapter review |

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
- Book 2: *Inside a Smartphone* ✅
- **Book 3: *Robot World*** ← you are here

---

## Open Items / Notes
- [ ] Cover image (`assets/cover.png`) not yet created
- [ ] Refine character TikZ illustrations into full-body drawings
- [ ] Final proofread and page-break tuning
- [ ] First compile test on MiKTeX
