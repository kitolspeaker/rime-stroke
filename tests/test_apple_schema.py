"""Static smoke tests for Apple-style six-key stroke scheme.

These tests simulate Rime spelling algebra; they are NOT a substitute
for a real librime / Windows Weasel deployment test.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = yaml.safe_load((ROOT / "stroke_apple.schema.yaml").read_text(encoding="utf-8"))
CANONICAL = "hspnz"
APPLE = "jklui"


def spellings(code: str) -> set[str]:
    """Simplified model of derive/xlit order for a single dictionary code."""
    values = {code}
    for item in SCHEMA["speller"]["algebra"]:
        if item.startswith("derive/"):
            _, pattern, replacement, _ = item.split("/", 3)
            additions = set()
            for current in values:
                if re.search(pattern, current):
                    py_replacement = re.sub(r"\\$(\\d+)", lambda m: r"\\g<" + m.group(1) + ">", replacement)
                    additions.add(re.sub(pattern, py_replacement, current))
            values.update(additions)
        elif item.startswith("xlit/"):
            _, old, new, _ = item.split("/", 3)
            values = {v.translate(str.maketrans(old, new)) for v in values}
        else:
            raise AssertionError("Unexpected formula: " + item)
    return values


class AppleStrokeSchemaTest(unittest.TestCase):
    def test_schema_identity(self):
        self.assertEqual(SCHEMA["schema"]["schema_id"], "stroke_apple")
        self.assertEqual(SCHEMA["translator"]["dictionary"], "stroke")
        self.assertEqual(SCHEMA["speller"]["alphabet"], "jkluio")

    def test_keyboard_for_each_stroke(self):
        for original, expected in zip(CANONICAL, APPLE):
            with self.subTest(original=original):
                self.assertIn(expected, spellings(original))

    def test_sixth_key_is_single_stroke_wildcard(self):
        # Every first-five position can be replaced by O.
        for index in range(5):
            candidate = APPLE[:index] + "o" + APPLE[index + 1:]
            self.assertIn(candidate, spellings(CANONICAL))

    def test_multiple_early_wildcards(self):
        self.assertIn("ooooo", spellings(CANONICAL))

    def test_first_four_plus_last(self):
        self.assertIn("jkluu", spellings("hspnzzn"))
        self.assertIn("jkluiiu", spellings("hspnzzn"))

    def test_late_wildcard_limit(self):
        self.assertIn("jkluio", spellings("hspnzh"))
        self.assertNotIn("jklui" + "o" * 2, spellings("hspnzhz"))

    def test_alphabet_bounds(self):
        for code in ("hspnz", "hspnzzn", "pnnzhspn", "h" * 35):
            result = spellings(code)
            self.assertLess(len(result), 100)
            self.assertTrue(all(set(word) <= set("jkluio") for word in result))

    def test_numeric_pad_mapping(self):
        bindings = SCHEMA["key_binder"]["bindings"]
        expected = "jkluio"
        for number, value in enumerate(expected, 1):
            self.assertTrue(any(
                b.get("accept") == f"KP_{number}" and b.get("send") == value
                for b in bindings
            ))


if __name__ == "__main__":
    unittest.main()
