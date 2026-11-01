# Conway 繁體六鍵筆畫（Windows 小狼毫 Rime）

This is a fork of [rime-stroke](https://github.com/rime/rime-stroke). The new **stroke_apple** scheme uses [Conway Stroke Data](https://github.com/stroke-input/stroke-input-data) for **Traditional Chinese character frequency and the first five strokes**. The original Rime stroke scheme stays unchanged.

> Prototype, not an Apple product or an exact reproduction of the proprietary iPhone character ranking. It has not been tested in a live Windows Weasel installation.

## Install on Windows

1. Download both [stroke_apple.schema.yaml](stroke_apple.schema.yaml) and [stroke_apple.dict.yaml](stroke_apple.dict.yaml) using the **Raw** button (the dictionary is produced by GitHub Actions; if not yet committed, get its workflow artifact).
2. Place both files in the Windows Rime user directory: **%APPDATA%\Rime**. Do **not** overwrite the existing stroke.dict.yaml.
3. Right-click Weasel's tray icon → **輸入法設定** → select **Conway 繁體六鍵筆畫（實驗）**. If absent, choose **重新部署** and reopen the settings.
4. Redeploy, then switch to Weasel using **Win + Space**. Use **F4** to choose the scheme.

## Six keys

| Stroke | Letter | Numeric keypad |
|---|---|---|
| 一 橫 | J | 1 |
| 丨 豎 | K | 2 |
| 丿 撇 | L | 3 |
| 丶 點 | U | 4 |
| 乛 折 | I | 5 |
| ＊ 萬用 | O | 6 |

**Behavior:** Enter the first one to five strokes. Rime suggests matching characters using prefix completion. O represents exactly one unknown stroke (including multiple positions). Characters use Conway's Traditional ranking rather than the old stroke dictionary. The old macOS first-four-plus-last alias has been removed; the five-stroke **prefix** is used.

## Regenerate the Conway dictionary

The Python standard-library generator downloads fixed-revision upstream inputs and writes stroke_apple.dict.yaml. Python 3.9+ and internet access required:

~~~sh
python scripts/build_conway_dictionary.py --download
~~~

Source revision: 9cc6aab87b41a7ffe81734520f2ae01a0fc898dc (2026-10-18). Sources: sequence-characters.txt (CC BY 4.0), ranking-traditional.txt and characters-simplified.txt (public domain). See [third-party attribution](docs/CONWAY_SOURCES.md).

## Testing and limits

~~~sh
python -m pip install PyYAML==6.0.2
python -m unittest discover -s tests -v
~~~

The generated dictionary contains character-level entries, **not Apple's privately held phrase data, candidate ranking or personalized learned words**. Candidate positions will differ from iPhone. Run the [manual acceptance checks](docs/APPLE_STROKE_TESTING.md) before relying on this input method.
