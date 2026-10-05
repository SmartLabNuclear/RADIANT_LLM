from visual_parser.prompts import FIGURE_PROMPT, IMAGE_DESCRIPTION_PROMPT


def test_figure_prompt_instructs_verbatim_table_transcription():
    """Regression test for the table-transcription addition: tables were
    already being captured as 'visuals' without this, but relied on the
    model's own judgment under the more general 'list labels VERBATIM'
    instruction rather than an explicit, guaranteed requirement."""
    assert "table" in FIGURE_PROMPT.lower()
    assert "VERBATIM and IN FULL" in FIGURE_PROMPT
    assert "row/column association" in FIGURE_PROMPT


def test_figure_prompt_and_image_prompt_use_matching_discrepancy_terminology():
    """Regression test: the two prompts' final heading must use the same
    label and boilerplate 'nothing found' phrase, so the two JSONL outputs
    (02_visuals_kb.jsonl / image_descriptions.jsonl) don't drift into
    inconsistent wording for the same underlying concept."""
    assert "**Discrepancy Check**" in FIGURE_PROMPT
    assert "No discrepancies detected" in FIGURE_PROMPT
    assert "**Discrepancy Check**" in IMAGE_DESCRIPTION_PROMPT
    assert "No discrepancies detected" in IMAGE_DESCRIPTION_PROMPT
    assert "Consistency Check" not in IMAGE_DESCRIPTION_PROMPT
    assert "inconsistencies detected" not in IMAGE_DESCRIPTION_PROMPT
