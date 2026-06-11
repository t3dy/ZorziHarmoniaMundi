#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process the Kabbalistic synthesis essay: convert citations to hyperlinks.
Citations format: [Section N: "Heading" · pp. X–Y]
Convert to: <a href="dharma-essay.html?id=0NN">Section N: "Heading" · pp. X–Y</a>
"""

import re
import json
from pathlib import Path

# Read the essay text
essay_text = """# Kabbalah and Christian Mysticism in Francesco Zorzi's *De Harmonia Mundi*

## Introduction: Zorzi as Christian Cabalist Synthesizer

When the Venetian Franciscan Francesco Zorzi (1466–1540) published his *De Harmonia Mundi totius cantica tria* in 1525, he produced what Saverio Campanini, in his monumental critical edition (*L'armonia del mondo*, Bompiani, 2010), identifies as one of the supreme monuments of Renaissance Christian Cabala. The work is colossal — three thousand pages in Campanini's modern Italian presentation — and its architecture is itself a statement of doctrine: three *Cantica*, each subdivided into *Toni* and *Moduli*, organized as though the cosmos were a single tuned instrument and the book its score. Campanini's own framing is unambiguous: "Ermetismo e qabbalah cristiana sono i poli ai quali Zorzi si orientò" — Hermeticism and Christian Kabbalah are the two poles toward which Zorzi oriented himself [Section 3: "Christian-Cabalist Synthesis" · pp. 1–13]. He places Zorzi among the foremost practitioners of *qabbalah cristiana* alongside Giovanni Pico della Mirandola, Johannes Reuchlin, and Pietro Galatino, and names "la centralità della speculazione mistica ebraica" — the centrality of Jewish mystical speculation — as the "autentico culmine esoterico," the authentic esoteric summit, of the entire enterprise [Section 3 · pp. 1–13].

The thesis of this essay is that Kabbalah is not ornamental in *De Harmonia Mundi* but structural. Campanini's most consequential interpretive claim is precisely this: the Sefirotic logic — the doctrine that the one God may be conceived in ten articulations, each of which not merely contains but *is* all the others — is "the only logic that makes coherent" Zorzi's vast symbolic-musical system in which "everything signifies everything" [Section 3: "The 'idem et non idem' logic" · pp. 50–54]. Strip out the Kabbalah and the book collapses into an unmotivated heap of correspondences. With it, the heap becomes a cosmos. This is why, as we shall see, the Counter-Reformation censors eventually found the work *inexpurgable*: once everything "smelling of Judaism" was to be condemned, separating the wheat from the tares "si rivela del tutto illusorio" — proves entirely illusory — because the Judaizing thread runs through the whole fabric [Section 3: "Censorship corollary" · pp. 50–54].

Zorzi's distinctive contribution was to fuse three traditions that the fifteenth century had inherited as separate streams: the Pythagorean-Platonic doctrine of cosmic harmony (the world as a tuned instrument, transmitted through Timaeus of Locri, Plato's *Timaeus*, and the late-antique commentators Proclus, Porphyry, Severus, Adrastus, and Calcidius); the Hermetic-Neoplatonic metaphysics of emanation and the divine Intelligences; and the Jewish Kabbalah of the Sefirot, the divine Names, and the mysticism of the Hebrew letters. The genius of *De Harmonia Mundi* lies in showing these three to be one — a single *philosophia perennis* or *prisca theologia* in which the Pythagorean decad, the Neoplatonic henads, and the ten Sefirot are revealed as the same truth spoken in three tongues. The remainder of this essay traces that fusion through its cosmological, numerical, textual, theological, and contemplative dimensions.

## Section 1: Kabbalistic Cosmology in *De Harmonia Mundi*

### The Ten Sefirot and the 3+7 Division

The doctrinal keystone of Zorzi's Kabbalistic cosmology stands in the *Tonus Quintus* of *Cantica I*, the chapter titled "GLI INTERVALLI DEI GENERI PRIMARI" ("The intervals of the primary genera"). Here Zorzi states with unusual directness what the Jews teach in their innermost secrets:

> "gli ebrei, nei loro arcani più segreti, affermano che l'anima procede dal grande Nome di Dio composto da quattro lettere, mentre il mondo discende ed è governato dalle dieci sefirot. In effetti il comando va attribuito solo alle tre sefirot superiori, mentre alle altre sette spetta l'esecuzione, perciò chiamano le sette sefirot inferiori, sefirot della creazione."

— the soul proceeds from the great four-lettered Name of God, while the world descends from and is governed by the ten Sefirot; command belongs only to the three upper Sefirot, while execution falls to the other seven, which are therefore called the *sefirot of creation* [Section 1: "Sephirot as emanations" · pp. 677–728].

This single sentence encodes the central architecture of theosophical Kabbalah. The Hebrew term *sefirot* (סְפִירוֹת, singular *sefirah*) derives from a root cluster associated with counting/numbering (*s-p-r*, as in *mispar*, number), and also resonates with *sappir* (sapphire, brilliance) and *sippur* (telling/narration) — a polysemy the Kabbalists exploited deliberately. The Sefirot are the ten emanations, attributes, or "numerations" through which the hidden Godhead becomes manifest and through which it creates and governs the world. The division Zorzi reports — three upper Sefirot of "command" versus seven lower Sefirot of "creation/execution" — corresponds to the standard Kabbalistic separation of the three supernal, intellective Sefirot (Keter, Chokhmah, Binah) from the seven "Sefirot of construction" (the *sefirot ha-binyan*: Chesed, Gevurah, Tiferet, Netzach, Hod, Yesod, Malkhut). The latter are conventionally tied to the seven days of creation. Zorzi has grasped this scheme accurately and rendered it faithfully."""

# Parse citations: [Section N: "Heading" · pp. X–Y]
# Convert to hyperlinks pointing to dharma-essay.html?id=0NN
citation_pattern = r'\[Section (\d+):\s*"([^"]+)"\s*·\s*pp?\.\s*([^\]]+)\]'

def citation_to_link(match):
    section_num = int(match.group(1))
    heading = match.group(2)
    pages = match.group(3)

    # Section N → chunk (39 + N - 1)
    chunk_num = 38 + section_num
    chunk_id = str(chunk_num).padStart(3, '0') if chunk_num < 1000 else str(chunk_num)

    # Return HTML link
    return f'<a href="dharma-essay.html?id={chunk_id}" class="citation">Section {section_num}: "{heading}" · pp. {pages}</a>'

# Process essay text
processed = re.sub(citation_pattern, citation_to_link, essay_text)

print("Citation processing test:")
matches = re.findall(citation_pattern, essay_text)
print(f"Found {len(matches)} citations")
for section, heading, pages in matches[:3]:
    section_num = int(section)
    chunk_num = 38 + section_num
    chunk_id = str(chunk_num).zfill(3)
    print(f"  Section {section_num} → chunk {chunk_num} (id={chunk_id}): {heading}")

# Build HTML page
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kabbalah and Christian Mysticism — L'armonia del mondo</title>
  <meta name="description" content="Comprehensive synthesis of Kabbalistic and Christian cabalist content in Francesco Zorzi's De Harmonia Mundi.">
  <link rel="stylesheet" href="assets/style.css">
  <style>
    .kabbalah-wrap {{
      max-width: 900px;
      margin: 0 auto;
    }}
    .kabbalah-toc {{
      background: var(--card-bg);
      border: 1px solid var(--card-brd);
      border-radius: 6px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}
    .kabbalah-toc h3 {{
      margin: 0 0 1rem 0;
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--gold);
    }}
    .kabbalah-toc ul {{
      list-style: none;
      padding: 0;
    }}
    .kabbalah-toc li {{
      margin-bottom: 0.5rem;
    }}
    .kabbalah-toc a {{
      color: var(--link);
      text-decoration: none;
    }}
    .kabbalah-toc a:hover {{
      text-decoration: underline;
    }}
    .kabbalah-body {{
      font-size: 1.05rem;
      line-height: 1.85;
    }}
    .kabbalah-body h1 {{
      font-size: 2rem;
      font-weight: 400;
      color: var(--rust);
      margin: 0 0 1rem 0;
      line-height: 1.2;
    }}
    .kabbalah-body h2 {{
      font-size: 1.4rem;
      font-weight: 400;
      color: var(--rust);
      margin: 2.5rem 0 0.8rem 0;
      border-bottom: 1px solid var(--rule);
      padding-bottom: 0.4rem;
    }}
    .kabbalah-body h3 {{
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--ink);
      margin: 1.8rem 0 0.6rem 0;
    }}
    .kabbalah-body p {{
      margin-bottom: 1.2rem;
    }}
    .kabbalah-body blockquote {{
      padding: 0;
      margin: 1.2rem 0 1.2rem 2rem;
      font-style: italic;
      font-size: 0.98rem;
      color: #3a2a10;
    }}
    .kabbalah-body cite {{
      display: inline;
      font-style: normal;
      font-family: var(--sans);
      font-size: 0.8rem;
      color: var(--muted);
      margin-left: 0.5em;
    }}
    .citation {{
      color: var(--rust);
      text-decoration: none;
      border-bottom: 1px dotted var(--gold);
    }}
    .citation:hover {{
      background: #ede4ce;
      text-decoration: none;
    }}
    @media (max-width: 900px) {{
      .kabbalah-wrap {{
        padding: 0 1rem;
      }}
      .kabbalah-body {{
        font-size: 1rem;
      }}
    }}
  </style>
</head>
<body>

<header>
  <div class="subtitle">Philosophical Synthesis</div>
  <h1><em>L'armonia del mondo</em></h1>
  <div class="meta">Francesco Zorzi · Kabbalah and Christian Mysticism</div>
</header>

<nav class="breadcrumb">
  <a href="index.html">Summaries</a> · <a href="dharma.html">De Harmonia Mundi</a> · <a href="timeline.html">Timeline</a> · <a href="#">Kabbalah & Mysticism</a>
</nav>

<main>
  <div class="kabbalah-wrap">
    <div class="kabbalah-toc">
      <h3>Contents</h3>
      <ul>
        <li><a href="#intro">Introduction: Zorzi as Christian Cabalist Synthesizer</a></li>
        <li><a href="#section1">Section 1: Kabbalistic Cosmology</a></li>
        <li><a href="#section2">Section 2: Harmonic Correspondence and Number Theory</a></li>
        <li><a href="#section3">Section 3: Hebrew Sources and Textual Authorities</a></li>
        <li><a href="#section4">Section 4: Christian Integration</a></li>
        <li><a href="#section5">Section 5: Mystical Praxis</a></li>
        <li><a href="#conclusion">Conclusion: Legacy and Significance</a></li>
      </ul>
    </div>

    <div class="kabbalah-body">
      <div id="essay-content">
        <!-- Essay will be inserted here -->
      </div>
    </div>
  </div>
</main>

<footer>
  <p>
    Comprehensive synthesis of Kabbalistic and Christian cabalist content in De Harmonia Mundi.
    All citations are hyperlinked to the relevant subsections.
    Verbatim excerpts reproduced under fair use for scholarly commentary. ·
    <a href="https://github.com/t3dy/ZorziHarmoniaMundi" target="_blank">GitHub</a>
  </p>
</footer>

<script>
function parseMarkdown(md) {{
  let html = md
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/^&gt;&gt;\\s?(.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^&gt;\\s?(.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/<\\/blockquote>\\n<blockquote>/g, '\\n')
    .replace(/&lt;cite&gt;(.+?)&lt;\\/cite&gt;/g, '<cite>$1</cite>')
    .replace(/<\\/blockquote>\\n+<cite>/g, '<cite>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\\*\\*\\*(.+?)\\*\\*\\*/g, '<strong><em>$1</em></strong>')
    .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
    .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
    .replace(/^---+$/gm, '<hr>')
    .replace(/\\n{{2,}}/g, '\\n</p><p>\\n')
    .replace(/\\n/g, '<br>');
  return '<p>' + html + '</p>';
}}

// Load essay JSON
async function init() {{
  try {{
    const r = await fetch('data/kabbalah-essay.json');
    if (!r.ok) throw new Error(r.status);
    const data = await r.json();
    const processed = parseMarkdown(data.essay);
    document.getElementById('essay-content').innerHTML = processed;
  }} catch(e) {{
    document.getElementById('essay-content').innerHTML =
      '<p class="error-msg">Essay not yet loaded.</p>';
  }}
}}

init();
</script>
</body>
</html>"""

# Write HTML template
with open('kabbalah.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Save essay as JSON for loading via fetch
essay_data = {
    "title": "Kabbalah and Christian Mysticism in Francesco Zorzi's De Harmonia Mundi",
    "wordCount": 6262,
    "essay": essay_text  # Will be replaced with actual full text
}

# For now, just verify the setup works
print("\nHTML page template created: kabbalah.html")
print("Next: Update with full essay text and commit.")
