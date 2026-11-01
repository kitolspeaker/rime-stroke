"""Static tests for Conway-based five-stroke Rime scheme.

These verify the generated table and input schema, not live Weasel behavior.
"""
from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = yaml.safe_load((ROOT / "stroke_apple.schema.yaml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location(
    "builder", ROOT / "scripts" / "build_conway_dictionary.py"
)
assert spec and spec.loader
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def apply_rime_algebra(code: str) -> set[str]:
    result = {code}
    for expression in SCHEMA["speller"]["algebra"]:
        kind, pattern, substitution, _ = expression.split("/", 3)
        assert kind == "derive"
        substitution = re.sub(
            r"\$(\d+)", lambda x: "\\" + "g<" + x.group(1) + ">", substitution
        )
        for item in list(result):
            if re.search(pattern, item):
                result.add(re.sub(pattern, substitution, item))
    return result


class ConwayStrokeTests(unittest.TestCase):
    def test_schema_identity(self):
        self.assertEqual(SCHEMA["schema"]["schema_id"], "stroke_apple")
        self.assertEqual(SCHEMA["translator"]["dictionary"], "stroke_apple")
        self.assertEqual(SCHEMA["speller"]["alphabet"], "jkluio")
        self.assertEqual(SCHEMA["translator"]["enable_completion"], True)

    def test_keypad_keys(self):
        bindings = SCHEMA["key_binder"]["bindings"]
        for n, char in enumerate("jkluio", 1):
            self.assertTrue(any(
                b.get("accept") == f"KP_{n}" and b.get("send") == char
                for b in bindings
            ))

    def test_rank_cantonese_higher(self):
        rank = builder.ranking("一二三\n係唔咗嘅\n")
        self.assertLess(rank["係"], rank["唔"])
        self.assertLess(rank["唔"], rank["咗"])

    def test_five_stroke_prefix_not_last_stroke(self):
        items = builder.make_entries(
            "123451\t甲\n123452\t乙\n123459\t非法\n",
            "甲乙\n",
            "",
        )
        self.assertIn(("甲", "jklui", 2_000_000), items)
        self.assertIn(("乙", "jklui", 1_999_600), items)
        self.assertFalse(any(char == "非法" for char, _, _ in items))

    def test_filter_simplified_only_and_sort_by_rank(self):
        entries = builder.make_entries("1234\t繁简\n", "繁简\n", "简\n")
        self.assertEqual(entries, [("繁", "jklu", 2_000_000)])

    def test_unknown_stroke_any_of_first_five(self):
        variants = apply_rime_algebra("jklui")
        self.assertIn("ooooo", variants)
        for i in range(5):
            self.assertIn("jklui"[:i] + "o" + "jklui"[i + 1:], variants)

    def test_wildcard_covers_short_code(self):
        self.assertIn("o", apply_rime_algebra("j"))
        self.assertIn("oo", apply_rime_algebra("ju"))

    def test_smoke_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "sequence-characters.txt").write_text(
                "12\t係\n123456\t話\n123457\t話\n", encoding="utf-8"
            )
            (folder / "ranking-traditional.txt").write_text(
                "係話\n", encoding="utf-8"
            )
            (folder / "characters-simplified.txt").write_text(
                "仅\n", encoding="utf-8"
            )
            output = folder / "stroke_apple.dict.yaml"
            count, unique = builder.build(folder, output)
            self.assertEqual((count, unique), (2, 2))
            body = output.read_text(encoding="utf-8")
            self.assertIn("name: stroke_apple", body)
            self.assertIn("係\tjk\t2000000", body)
            self.assertIn("話\tjklui\t1999600", body)
            self.assertIn("CC BY 4.0", body)


if __name__ == "__main__":
    unittest.main()
