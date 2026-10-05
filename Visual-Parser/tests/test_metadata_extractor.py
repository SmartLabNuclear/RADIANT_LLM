import json

import pytest

from visual_parser import metadata_extractor


# ---------------------------------------------------------------------------
# _parse_metadata_response
# ---------------------------------------------------------------------------

def test_parse_well_formed_object():
    raw = json.dumps({"title": "A Report", "authors": ["A. Author"]})
    parsed = metadata_extractor._parse_metadata_response(raw, "doc.pdf")
    assert parsed == {"title": "A Report", "authors": ["A. Author"]}


def test_parse_prose_wrapped_object():
    raw = 'Sure, here you go:\n```json\n{"title": "X"}\n```\nLet me know if you need more.'
    parsed = metadata_extractor._parse_metadata_response(raw, "doc.pdf")
    assert parsed == {"title": "X"}


def test_parse_unwraps_single_element_list():
    raw = json.dumps([{"title": "Y"}])
    parsed = metadata_extractor._parse_metadata_response(raw, "doc.pdf")
    assert parsed == {"title": "Y"}


def test_parse_recovers_real_answer_when_prose_has_a_stray_brace():
    """Regression test: the naive find('{')/rfind('}') substring approach
    this function replaced would have grabbed from the stray brace in
    'Figure {3}' through to the real object's closing brace, producing an
    invalid blob. The JSONDecoder.raw_decode() walk must skip past it and
    recover the real object instead."""
    raw = (
        'Regarding Figure {3}, here is the metadata:\n'
        '{"title": "Real Title"}'
    )
    parsed = metadata_extractor._parse_metadata_response(raw, "doc.pdf")
    assert parsed == {"title": "Real Title"}


def test_parse_handles_literal_brace_inside_field_text():
    raw = 'Answer:\n{"title": "Shows the set {A, B, C} on the x-axis"}\nDone.'
    parsed = metadata_extractor._parse_metadata_response(raw, "doc.pdf")
    assert parsed == {"title": "Shows the set {A, B, C} on the x-axis"}


def test_parse_raises_when_no_json_recoverable():
    with pytest.raises(RuntimeError):
        metadata_extractor._parse_metadata_response("not json at all {{{", "doc.pdf")


# ---------------------------------------------------------------------------
# _validate_metadata_fields
# ---------------------------------------------------------------------------

def test_validate_passes_through_well_formed_fields():
    parsed = {
        "title": "A Report",
        "authors": ["A. Author", "B. Author"],
        "publication_date": "2026-01-01",
        "report_number": "RPT-1",
        "doi": "10.1000/xyz",
        "keywords": ["nuclear", "safety"],
    }
    assert metadata_extractor._validate_metadata_fields(parsed, "doc.pdf") == parsed


def test_validate_drops_non_string_string_field():
    """Regression test: a weak/non-compliant model can return a string-typed
    field as something else (e.g. a nested object) instead of the documented
    plain string. Before this fix, a malformed field like this would have
    been written straight into 03_metadata_kb.jsonl with no warning."""
    parsed = {"title": {"text": "A Report"}, "doi": "10.1000/xyz"}
    result = metadata_extractor._validate_metadata_fields(parsed, "doc.pdf")
    assert result == {"doi": "10.1000/xyz"}


def test_validate_drops_non_list_list_field():
    parsed = {"authors": "A. Author, B. Author"}  # string instead of list
    result = metadata_extractor._validate_metadata_fields(parsed, "doc.pdf")
    assert result == {}


def test_validate_drops_list_field_with_non_string_elements():
    parsed = {"keywords": ["nuclear", {"safety": "high"}]}
    result = metadata_extractor._validate_metadata_fields(parsed, "doc.pdf")
    assert result == {}


def test_validate_passes_through_unknown_fields_unchanged():
    """A field outside the documented schema (the model inventing an extra
    key) has no basis to be judged -- pass it through rather than lose real
    data the schema didn't anticipate."""
    parsed = {"title": "X", "isbn": "978-0-00-000000-0"}
    result = metadata_extractor._validate_metadata_fields(parsed, "doc.pdf")
    assert result == {"title": "X", "isbn": "978-0-00-000000-0"}
