# *L'armonia del mondo* — Francesco Zorzi: Scholarly Summaries

**Website:** https://t3dy.github.io/ZorziHarmoniaMundi/

---

A browse-and-search website of detailed scholarly summaries for all 163 sections of Francesco Zorzi's *De Harmonia Mundi* (*L'armonia del mondo*), in the critical Italian edition by Saverio Campanini (Bompiani, Il Pensiero Occidentale, 2010). Each section has a concise index-card summary and a full essay with verbatim excerpts.

---

## About the Text

**Francesco Zorzi** (Giorgio, 1466–1540) was a Venetian Franciscan friar and one of the most ambitious Christian Kabbalists of the Renaissance. His *De Harmonia Mundi totius cantica tria* (Venice, 1525) is a vast cosmological synthesis drawing on Scripture, Neoplatonism, Kabbalah, Pythagoreanism, and the Church Fathers to demonstrate a single harmonic order pervading the divine, angelic, celestial, and human realms.

The Bompiani 2010 edition (3,087 pp.) presents the full Latin text alongside a complete Italian translation by Saverio Campanini, with an extensive *Saggio introduttivo* (prefatory essay, ~166 pp.) and critical apparatus.

---

## Site Structure

```
/
├── index.html          # Card grid — all 163 chunks, searchable
├── chunk.html          # Essay template (URL: chunk.html?id=NNN)
├── assets/
│   └── style.css       # Scholarly typographic design
└── data/
    ├── summaries.json  # Index: chunk metadata + card summaries (163 entries)
    └── essays/
        ├── chunk_001.json  … chunk_163.json   # Full essay per chunk
```

### Navigation
- **Homepage** (`index.html`): 163 cards in a responsive grid, with live search across headings and summaries.
- **Chunk page** (`chunk.html?id=NNN`): Full essay for one section, with prev/next navigation.

---

## How the Summaries Were Made

### Step 1 — PDF extraction

The source PDF (~18 MB, 3,087 pages) was extracted using **pdfplumber** (Python). A custom script (`convert_zorzi.py`) applied the following pipeline:

1. **Page extraction** — `pdfplumber.open()` with tight tolerances (`x_tolerance=2, y_tolerance=3`) for the dense scholarly typeface.
2. **Section detection** — Regex patterns matched structural markers: `LIBRO`, `TONO`, `CANTICO`, `CAPITOLO`, `PROEMIO`, `NOTE AL…`, `BIBLIOGRAFIA`, etc., plus all-caps lines identifying major divisions.
3. **Chunking** — Sections were merged or split to target ~12,000 characters (~3,000 tokens) per chunk, splitting at paragraph boundaries when a section exceeded the target.
4. **De-hyphenation** — End-of-line hyphenation was removed (`-\n([a-z])` → `\1`).

Result: **163 markdown files** covering the complete edition — introductory essay, proemium, three *Cantici* with their *Toni* and *Moduli*, critical notes, bibliography, and indices.

### Step 2 — Summary generation

Summaries were generated using **Claude Sonnet 4.6** via Claude Code's multi-agent workflow system. Each of the 163 chunks was processed by an independent agent with specialist instructions in:

- Renaissance Christian Kabbalah
- Venetian Neoplatonism
- The textual tradition of *De Harmonia Mundi*

Each agent produced:

**Card summary** (3–5 sentences, plain prose):
A specific, named-detail description of the chunk's contents for the homepage grid — identifying the exact theological arguments, scriptural citations, Kabbalistic concepts, and interlocutors at stake.

**Full essay** (400–800+ words, markdown):
An exhaustive scholarly summary structured with headings, covering: the central argument, all significant claims, sources cited (Scripture, Zohar, Plato, Proclus, Pico della Mirandola, Ficino, Reuchlin, Church Fathers, etc.), verbatim Italian/Latin excerpts from the text, Campanini's editorial notes, and technical terminology introduced.

Verbatim excerpts are reproduced under **fair use** principles for the purpose of scholarly commentary and criticism.

All 163 agents ran in parallel, completing the full corpus in a single session.

### Step 3 — Site build and deployment

- Static HTML/CSS/JS — no build framework, no runtime dependencies.
- Deployed to **GitHub Pages** from the `main` branch.
- Typography uses Georgia/Garamond serif stack with a parchment-and-ink colour palette appropriate to the subject matter.

---

## Deployment

```bash
# Clone and open locally
git clone https://github.com/t3dy/ZorziHarmoniaMundi.git
cd ZorziHarmoniaMundi
python -m http.server 8080
# → http://localhost:8080
```

GitHub Pages is served from the `main` branch root.

---

## Source

> Francesco Zorzi, *L'armonia del mondo*, a cura di Saverio Campanini.  
> Milano: Bompiani (Il Pensiero Occidentale), 2010. 3087 pp.  
> ISBN: 978-88-452-6499-1

---

## License

Summary texts © 2026 — generated for scholarly, non-commercial use.  
Verbatim quotations from the Bompiani edition reproduced under fair use for criticism and commentary.
