#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract preview summaries from existing essays and build dharma-summaries.json + dharma-essays index.
This reuses the existing essays (chunks 39-145) as the dharma subsection content.
"""

import json
import os
import re
import sys
from pathlib import Path

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REPO_ROOT = Path(__file__).parent
ESSAYS_DIR = REPO_ROOT / "data" / "essays"
OUTPUT_DIR = REPO_ROOT / "data"
DHARMA_ESSAYS_DIR = OUTPUT_DIR / "dharma-essays"

# Create dharma-essays directory if it doesn't exist
DHARMA_ESSAYS_DIR.mkdir(parents=True, exist_ok=True)

# Chunks 39-145 are the De Harmonia Mundi subsections (dharma 1-107)
DHARMA_START_CHUNK = 39
DHARMA_END_CHUNK = 145
DHARMA_COUNT = DHARMA_END_CHUNK - DHARMA_START_CHUNK + 1  # 107

def extract_preview(essay_text, max_sentences=7):
    """Extract 5-10 sentence preview from essay markdown, stripping headers."""
    # Remove markdown headers (## and #)
    clean_text = re.sub(r'^#+\s+.+$\n?', '', essay_text, flags=re.MULTILINE)
    # Remove leading/trailing whitespace and extra blank lines
    clean_text = re.sub(r'\n\n+', '\n', clean_text.strip())

    # Split on periods, keeping sentence fragments together
    sentences = re.split(r'(?<=[.!?])\s+', clean_text.strip())

    # Take up to max_sentences, stripping each
    preview_sentences = []
    for s in sentences:
        s = s.strip()
        if s and len(preview_sentences) < max_sentences:
            preview_sentences.append(s)

    preview = ' '.join(preview_sentences)
    # Ensure it ends with punctuation
    if preview and preview[-1] not in '.!?':
        preview += '.'
    return preview

def build_dharma_index():
    """Build dharma-summaries.json from existing essays."""
    summaries = []

    for chunk_num in range(DHARMA_START_CHUNK, DHARMA_END_CHUNK + 1):
        dharma_num = chunk_num - DHARMA_START_CHUNK + 1
        chunk_id = str(chunk_num).zfill(3)
        essay_file = ESSAYS_DIR / f"chunk_{chunk_id}.json"

        if not essay_file.exists():
            print(f"  [SKIP] chunk_{chunk_id}.json not found, skipping dharma {dharma_num}")
            continue

        try:
            with open(essay_file, 'r', encoding='utf-8') as f:
                essay_data = json.load(f)

            # Extract preview from the essay body
            essay_text = essay_data.get('essay', '')
            # Remove markdown markers for cleaner preview
            essay_text = re.sub(r'\[cite\](.+?)\[/cite\]', r'\1', essay_text)
            essay_text = re.sub(r'<cite>(.+?)</cite>', r'\1', essay_text)
            preview = extract_preview(essay_text)

            summary_entry = {
                "dharma_num": dharma_num,
                "chunk": chunk_num,
                "heading": essay_data.get('heading', ''),
                "pages": essay_data.get('pages', ''),
                "preview": preview
            }
            summaries.append(summary_entry)
            print(f"  [OK] dharma {dharma_num} (chunk {chunk_num}): {essay_data.get('heading', '')[:50]}")
        except Exception as e:
            print(f"  [ERR] Error processing chunk_{chunk_id}: {e}")

    # Write dharma-summaries.json
    output_file = OUTPUT_DIR / "dharma-summaries.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    print(f"\n[OK] Written {len(summaries)} summaries to {output_file.name}")

def symlink_dharma_essays():
    """Create symlinks from dharma-essays/ to existing essays (or copy if symlinks unsupported)."""
    copied_count = 0
    for chunk_num in range(DHARMA_START_CHUNK, DHARMA_END_CHUNK + 1):
        chunk_id = str(chunk_num).zfill(3)
        source_file = ESSAYS_DIR / f"chunk_{chunk_id}.json"
        dharma_file = DHARMA_ESSAYS_DIR / f"chunk_{chunk_id}.json"

        if not source_file.exists():
            continue

        # On Windows, prefer copy over symlink for compatibility
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Ensure the essay structure has 'essay' field (not 'card_summary' or other)
            if 'essay' not in data:
                print(f"  [SKIP] chunk_{chunk_id}.json missing 'essay' field")
                continue

            with open(dharma_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            copied_count += 1
        except Exception as e:
            print(f"  [ERR] Error copying chunk_{chunk_id}: {e}")

    print(f"[OK] Prepared {copied_count} dharma essay files")

if __name__ == '__main__':
    print("Building De Harmonia Mundi index...")
    print(f"Processing chunks {DHARMA_START_CHUNK}–{DHARMA_END_CHUNK} ({DHARMA_COUNT} subsections)...\n")

    build_dharma_index()
    print()
    symlink_dharma_essays()

    print("\n[OK] De Harmonia Mundi index complete!")
