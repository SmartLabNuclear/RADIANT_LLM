"""
Nougat output post-processing without the GPL Levenshtein package.

The golden file ``fixtures/nougat_postprocess_golden.json`` holds generations
and the output of the 2.2.4 code path (``processor.post_process_generation``,
Levenshtein installed) for each. The 2.2.5 path (RapidFuzz) must reproduce it.
"""

import functools
import importlib
import json
import pathlib
import sys
import types

import pytest

from visual_parser import nougat_engine
from visual_parser.nougat_engine import postprocess_nougat_page

GOLDEN = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "nougat_postprocess_golden.json").read_text(encoding="utf-8")
)


def _tokenizer_module():
    for name in nougat_engine._NOUGAT_TOKENIZER_MODULES:
        try:
            return importlib.import_module(name)
        except ImportError:
            continue
    pytest.skip("this transformers has no Nougat tokenizer module")


def _stub_processor():
    """An object with the real Nougat post-processing methods but no tokenizer files
    (those need a model download). post_process_single only calls two other methods."""
    module = _tokenizer_module()
    cls = getattr(module, "NougatTokenizer", None) or module.NougatTokenizerFast
    tok = types.SimpleNamespace()
    for method in ("remove_hallucinated_references", "correct_tables", "post_process_single"):
        setattr(tok, method, functools.partial(getattr(cls, method), tok))
    return types.SimpleNamespace(tokenizer=tok)


@pytest.mark.parametrize("case", GOLDEN["cases"], ids=lambda c: c["name"])
def test_matches_the_2_2_4_levenshtein_output(case):
    assert postprocess_nougat_page(_stub_processor(), case["input"]) == case["expected"]


def test_the_golden_cases_actually_exercise_the_ratio_function():
    """Guard against a golden file that passes trivially: the repeated-reference case must
    change under post-processing, i.e. Levenshtein/RapidFuzz ratio really ran."""
    case = next(c for c in GOLDEN["cases"] if c["name"] == "repeated_references")
    assert "[MISSING_PAGE_POST]" in case["expected"]
    assert case["expected"] != case["input"]


def test_works_with_levenshtein_absent(monkeypatch):
    module = _tokenizer_module()
    monkeypatch.setitem(sys.modules, "Levenshtein", None)      # any import of it now fails
    monkeypatch.delattr(module, "ratio", raising=False)         # as if transformers found no Levenshtein
    case = next(c for c in GOLDEN["cases"] if c["name"] == "repeated_references")
    assert postprocess_nougat_page(_stub_processor(), case["input"]) == case["expected"]


def test_a_post_processing_error_returns_the_raw_text_not_a_failure():
    def boom(text, fix_markdown=True):
        raise ImportError("Nougat tokenizer needs the Levenshtein library")

    processor = types.SimpleNamespace(tokenizer=types.SimpleNamespace(post_process_single=boom))
    assert postprocess_nougat_page(processor, "decoded page text.") == "decoded page text."


def test_a_tokenizer_without_post_processing_returns_the_raw_text():
    processor = types.SimpleNamespace(tokenizer=types.SimpleNamespace())
    assert postprocess_nougat_page(processor, "decoded page text.") == "decoded page text."


def test_rapidfuzz_ratio_equals_levenshtein_ratio_form():
    """Indel.normalized_similarity is Levenshtein.ratio: 1 - indel_distance / (len(a) + len(b))."""
    from rapidfuzz.distance import Indel

    assert Indel.normalized_similarity("", "") == 1.0
    assert Indel.normalized_similarity("abc", "abc") == 1.0
    assert Indel.normalized_similarity("abc", "") == 0.0
    assert Indel.normalized_similarity("kitten", "sitting") == pytest.approx(1 - 5 / 13)
