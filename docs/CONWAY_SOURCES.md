# Conway data attribution and limits

This repository's generated stroke dictionary is derived from [Conway Stroke Data](https://github.com/stroke-input/stroke-input-data), compiled by Conway (@yawnoc), copyright 2021–2026 Conway.

- **sequence-characters.txt**: five-class stroke sequences, licensed CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ .
- **ranking-traditional.txt**: frequency ordering for Traditional Chinese and Hong Kong usage, placed in the public domain by Conway.
- **characters-simplified.txt**: simplified-only character list, placed in the public domain by Conway.

Pinned upstream commit: **9cc6aab87b41a7ffe81734520f2ae01a0fc898dc**.

Transformations: take the first up to five digits of each stroke sequence, map 1–5 to J/K/L/U/I, remove simplified-only codepoints, and attach candidate weights derived from Conway's Traditional ranking. Unranked characters receive low default weights. Asterisk (O) is implemented as Rime spelling-algebra aliases for exactly one unknown stroke.

The resulting data is **not** an Apple dictionary and is not endorsed by Conway or Apple. Users must preserve attribution and license when redistributing derived data.
