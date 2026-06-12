#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recover expanded essays from workflow agent transcripts and write them
into data/dharma-essays/. Each agent transcript's first line names the
chunk it expanded; its last assistant text block is the expanded essay.
"""

import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TRANSCRIPT_DIR = Path(r"C:\Users\PC\.claude\projects\C--Dev\285f47c9-09ea-4b6b-8147-fd96bd24ea3a\subagents\workflows\wf_64638b13-450")
REPO = Path(__file__).parent
DHARMA_DIR = REPO / "data" / "dharma-essays"

MIN_WORDS = 1500  # accept essays that at least approach the 2000-4000 target


def last_assistant_text(jsonl_path):
    """Return (chunk_num, final assistant text) from a transcript."""
    chunk_num = None
    last_text = None
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get('message') or {}
            content = msg.get('content')
            if chunk_num is None and rec.get('type') == 'user':
                text = content if isinstance(content, str) else json.dumps(content)
                m = re.search(r'chunk_(\d+)\.json', text)
                if m:
                    chunk_num = int(m.group(1))
            if rec.get('type') == 'assistant' and isinstance(content, list):
                texts = [b.get('text', '') for b in content if b.get('type') == 'text']
                if texts:
                    last_text = '\n'.join(t for t in texts if t.strip())
    return chunk_num, last_text


def clean_essay(text):
    """Strip a leading conversational line if the agent added one before the essay."""
    lines = text.split('\n')
    # Drop leading lines until we hit a heading or a substantial paragraph
    start = 0
    for i, line in enumerate(lines[:6]):
        s = line.strip()
        if s.startswith('#') or len(s) > 200:
            start = i
            break
        if s and not s.startswith('#') and len(s) < 200 and i == 0 and (
                'here' in s.lower() or 'expanded' in s.lower() or 'essay' in s.lower()):
            start = i + 1
    return '\n'.join(lines[start:]).strip()


def main():
    recovered, skipped, errors = [], [], []

    for jsonl in sorted(TRANSCRIPT_DIR.glob('agent-*.jsonl')):
        chunk_num, text = last_assistant_text(jsonl)
        if chunk_num is None or not text:
            errors.append((jsonl.name, 'no chunk id or no text'))
            continue
        essay = clean_essay(text)
        words = len(essay.split())
        target = DHARMA_DIR / f"chunk_{chunk_num:03d}.json"
        if not target.exists():
            errors.append((jsonl.name, f'chunk_{chunk_num:03d}.json missing'))
            continue
        if words < MIN_WORDS:
            skipped.append((chunk_num, words))
            continue
        with open(target, 'r', encoding='utf-8') as f:
            data = json.load(f)
        old_words = len(data.get('essay', '').split())
        if words <= old_words:
            skipped.append((chunk_num, words))
            continue
        data['essay'] = essay
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        recovered.append((chunk_num, old_words, words))

    recovered.sort()
    print(f"Recovered {len(recovered)} expanded essays:")
    for c, old, new in recovered:
        print(f"  chunk_{c:03d}: {old} -> {new} words")
    if skipped:
        print(f"\nSkipped {len(skipped)} (too short or not longer than current):")
        for c, w in sorted(skipped):
            print(f"  chunk_{c:03d}: {w} words")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, why in errors:
            print(f"  {name}: {why}")

    # Word-count distribution check
    counts = []
    for f in sorted(DHARMA_DIR.glob('chunk_*.json')):
        with open(f, 'r', encoding='utf-8') as fh:
            d = json.load(fh)
        counts.append(len(d.get('essay', '').split()))
    in_range = sum(1 for c in counts if c >= 2000)
    print(f"\nFinal state: {len(counts)} essays, {in_range} at 2000+ words, "
          f"min {min(counts)}, avg {sum(counts)//len(counts)}, max {max(counts)}")


if __name__ == '__main__':
    main()
