# Windows manual acceptance checklist — Conway scheme

1. Deploy stroke_apple.schema.yaml and stroke_apple.dict.yaml on Windows Weasel and confirm that the independent original stroke scheme still works.
2. Verify J/K/L/U/I on single-stroke and multi-stroke codes; verify KP_1..KP_6 on an actual numeric keypad.
3. Verify one and multiple O wildcards within the first five positions. Compare candidate differences against iPhone Traditional Stroke.
4. Verify that a long character can be found by its **first five strokes**, not the optional macOS first-four-plus-last convention.
5. Verify Hong Kong common characters such as 係, 唔, 冇, 嘅, 咗 are available and ranked appropriately for their codes.
6. Verify that repeated candidate selection can change user ranking when Rime user dictionary learning is enabled.
7. Test typing with F4 scheme switching, Space selection, Backspace, numeric candidate selection, and fast typing on Windows.

Current status: **GitHub static test only; Weasel end-to-end test pending.** No Apple iPhone candidate ranking, phrase prediction, or lexicon data are bundled. See README and docs/CONWAY_SOURCES.md.

Suggested iPhone comparison fixture:
| strokes | iOS language/version | candidates 1–10 | Weasel candidates | notes |
|---|---|---|---|---|
| 1 | zh-Hant / TBD | TBD | TBD | first horizontal stroke |
| 2 | zh-Hant / TBD | TBD | TBD | first vertical stroke |
| 12345 | zh-Hant / TBD | TBD | TBD | first five strokes |
| 12*45 | zh-Hant / TBD | TBD | TBD | wildcard |
