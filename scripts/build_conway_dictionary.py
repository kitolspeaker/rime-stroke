#!/usr/bin/env python3
"""Build a five-stroke, Hong Kong Traditional Rime dictionary from Conway Stroke Data.

Sources: https://github.com/stroke-input/stroke-input-data
Conway stroke sequences: CC BY 4.0; rankings & variant lists: public domain.
The source revision is pinned for reproducibility. This is NOT Apple's lexicon.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

CONWAY_REV = "9cc6aab87b41a7ffe81734520f2ae01a0fc898dc"
RAW_BASE = (
    "https://raw.githubusercontent.com/stroke-input/stroke-input-data/"
    + CONWAY_REV + "/"
)
SOURCE_FILES = (
    "sequence-characters.txt",
    "ranking-traditional.txt",
    "characters-simplified.txt",
)
TRANS = str.maketrans("12345", "jklui")
MAX_STROKES = 5


def download_sources(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for name in SOURCE_FILES:
        request = Request(RAW_BASE + name, headers={"User-Agent": "conway-rime-dictionary-builder"})
        with urlopen(request, timeout=90) as response:
            data = response.read()
        (directory / name).write_bytes(data)


def non_comment_lines(text: str):
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


def ranking(text: str) -> dict[str, int]:
    ranks: dict[str, int] = {}
    for line in non_comment_lines(text):
        for char in line:
            ranks.setdefault(char, len(ranks))
    return ranks


def characters(text: str) -> set[str]:
    return {char for line in non_comment_lines(text) for char in line}


def make_entries(
    sequences: str, traditional_rank: str, simplified_only: str
) -> list[tuple[str, str, int]]:
    ranks = ranking(traditional_rank)
    simplified = characters(simplified_only)
    codes: dict[str, set[str]] = defaultdict(set)

    for line in non_comment_lines(sequences):
        if "\t" not in line:
            continue
        number_code, chars = line.split("\t", 1)
        if not number_code or set(number_code) - set("12345"):
            continue
        key = number_code[:MAX_STROKES].translate(TRANS)
        for char in chars.strip():
            if char not in simplified:
                codes[char].add(key)

    result = []
    for char, keys in codes.items():
        # Use Conway's explicitly ranked HK Traditional characters first.
        # Unranked CJK characters are retained but given much lower priority.
        index = ranks.get(char)
        weight = max(100_000, 2_000_000 - 400 * index) if index is not None else 100
        for key in keys:
            result.append((char, key, weight))
    return sorted(result, key=lambda row: (row[1], -row[2], ord(row[0])))


def build(source_dir: Path, output: Path) -> tuple[int, int]:
    source = {name: (source_dir / name).read_text(encoding="utf-8-sig") for name in SOURCE_FILES}
    entries = make_entries(
        source["sequence-characters.txt"],
        source["ranking-traditional.txt"],
        source["characters-simplified.txt"],
    )
    if len(entries) < 1000 and source_dir.name != "fixtures":
        raise RuntimeError(f"Unexpectedly small dictionary: {len(entries)} entries")

    header = (
        "# Rime dictionary generated from Conway Stroke Data; NOT an Apple dictionary.\n"
        "# Conway (2021-2026), CC BY 4.0, https://github.com/stroke-input/stroke-input-data\n"
        f"# Source revision: {CONWAY_REV}\n"
        "# Ranking/variant data released to the public domain by Conway.\n"
        "---\n"
        "name: stroke_apple\n"
        "version: '0.2.0'\n"
        "sort: by_weight\n"
        "use_preset_vocabulary: false\n"
        "columns:\n"
        "  - text\n"
        "  - code\n"
        "  - weight\n"
        "...\n"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        header + "".join(f"{char}\t{key}\t{weight}\n" for char, key, weight in entries),
        encoding="utf-8",
    )
    return len(entries), len({e[0] for e in entries})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=Path(".conway-cache"))
    parser.add_argument("--output", type=Path, default=Path("stroke_apple.dict.yaml"))
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if args.download:
        download_sources(args.source_dir)
    count, unique = build(args.source_dir, args.output)
    print(f"Built {args.output} ({count:,} entries / {unique:,} characters)")


if __name__ == "__main__":
    main()
