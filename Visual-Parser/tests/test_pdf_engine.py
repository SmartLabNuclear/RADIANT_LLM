import io
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from pdf_fixtures import PageSpec, build_pdf, encrypt_with_empty_password, make_jpeg, write_pdf
from PIL import Image

from visual_parser import pdf_engine
from visual_parser.text_extractor import lightweight_extract_pdfs

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _write(path, pages):
    path.write_bytes(build_pdf(pages))
    return str(path)


def test_page_count_and_text_in_page_order(tmp_path):
    path = write_pdf(tmp_path / "doc.pdf", ["alpha page", "bravo page", "charlie page"])
    with pdf_engine.open_pdf(path) as pdf:
        assert pdf.page_count == 3
        assert [pdf.page_text(i).strip() for i in range(3)] == ["alpha page", "bravo page", "charlie page"]


def test_text_uses_unix_line_endings(tmp_path):
    path = _write(tmp_path / "lines.pdf", [PageSpec(lines=["first line", "second line"])])
    with pdf_engine.open_pdf(path) as pdf:
        text = pdf.page_text(0)
    assert "\r" not in text
    assert text.split("\n")[:2] == ["first line", "second line"]


@pytest.mark.parametrize("raw, expected", [
    # SAM input syntax and numbers drawn as separate text runs
    ("[ EOS ]", "[EOS]"),
    ("[ pump_p_coastdown ]", "[pump_p_coastdown]"),
    ("see [ 12 ] and [ 13 ] for details", "see [12] and [13] for details"),
    ("values [ 2.5, 3.4, 4.15 ] m", "values [2.5, 3.4, 4.15] m"),
    ("2.151 E -02 and 9.789 E -03 and 1.000 E +00", "2.151E-02 and 9.789E-03 and 1.000E+00"),
    # a hyphen at a line end arrives as U+0002; keep it as a hyphen like MuPDF did
    ("model\x02\ning of high\x02temperature", "model-\ning of high-temperature"),
    # other control characters are dropped; tab and newline stay
    ("a\x00b\x01c\x7fd\te\nf", "abcd\te\nf"),
    ("line one\r\nline two\rline three", "line one\nline two\nline three"),
])
def test_tidy_text_fixes(raw, expected):
    assert pdf_engine.tidy_text(raw) == expected


@pytest.mark.parametrize("untouched", [
    "Table 5 gives the E values",                      # E not between a digit and a signed number
    "grade 3 E grade",                                 # no sign after E
    "[1] A. Author, Title (2020)",                     # a normal citation marker
    "x [ unclosed bracket and more text",              # no closing bracket
    "[ " + "word " * 40 + "]",                         # too long to be a spaced token
    "a [ nested [brackets] ] b",                       # nested brackets are not rewritten
])
def test_tidy_text_leaves_ordinary_text_alone(untouched):
    assert pdf_engine.tidy_text(untouched) == untouched


def test_render_png_is_a_decodable_png(tmp_path):
    path = write_pdf(tmp_path / "doc.pdf", ["hello"])
    with pdf_engine.open_pdf(path) as pdf:
        png = pdf.render_png(0, dpi=72)
    assert png.startswith(PNG_MAGIC)
    image = Image.open(io.BytesIO(png))
    assert image.size == (612, 792)          # letter page at 72 dpi is 1 px per point


def test_render_scale_follows_dpi(tmp_path):
    path = write_pdf(tmp_path / "doc.pdf", ["hello"])
    with pdf_engine.open_pdf(path) as pdf:
        low = pdf.render_pil(0, dpi=72).size
        high = pdf.render_pil(0, dpi=144).size
    assert high == (low[0] * 2, low[1] * 2)


def test_rotated_page_renders_and_reads(tmp_path):
    path = _write(tmp_path / "rot.pdf", [PageSpec(lines=["rotated text"], rotate=90)])
    with pdf_engine.open_pdf(path) as pdf:
        assert pdf.render_pil(0, dpi=72).size == (792, 612)      # width and height swapped
        assert pdf.page_text(0).strip() == "rotated text"


def test_cropbox_smaller_than_mediabox(tmp_path):
    path = _write(tmp_path / "crop.pdf", [PageSpec(lines=["cropped"], mediabox=(0, 0, 600, 800), cropbox=(0, 400, 300, 800))])
    with pdf_engine.open_pdf(path) as pdf:
        assert pdf.render_pil(0, dpi=72).size == (300, 400)      # the CropBox, not the MediaBox
        assert "cropped" in pdf.page_text(0)


def test_encrypted_pdf_with_empty_user_password(tmp_path):
    plain = build_pdf([PageSpec(lines=["secret but open"])])
    path = tmp_path / "enc.pdf"
    path.write_bytes(encrypt_with_empty_password(plain))
    assert b"/Encrypt" in path.read_bytes()
    with pdf_engine.open_pdf(str(path)) as pdf:
        assert pdf.page_count == 1
        assert pdf.page_text(0).strip() == "secret but open"
        assert pdf.render_png(0, dpi=72).startswith(PNG_MAGIC)


def test_embedded_jpeg_is_extracted(tmp_path):
    path = _write(tmp_path / "img.pdf", [PageSpec(lines=["has a picture"], jpeg=make_jpeg(64, 48)), PageSpec(lines=["none"])])
    with pdf_engine.open_pdf(path) as pdf:
        images = pdf.page_images(0)
        assert [im.size for im in images] == [(64, 48)]
        assert pdf.page_images(1) == []
        assert "has a picture" in pdf.page_text(0)


def test_non_ascii_file_name(tmp_path):
    path = write_pdf(tmp_path / "résumé 文档.pdf", ["unicode name page"])
    with pdf_engine.open_pdf(path) as pdf:
        assert pdf.page_text(0).strip() == "unicode name page"


def test_open_rejects_a_file_that_is_not_a_pdf(tmp_path):
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"this is not a pdf")
    with pytest.raises(Exception):
        pdf_engine.open_pdf(str(bad))


def test_engine_name_identifies_the_library():
    assert pdf_engine.engine_name().startswith("pypdfium2 ")


# --------------------------------------------------------------------------
# Threads: PDFium crashes or truncates text when used from several threads at
# once, so the engine serialises it. These tests would be flaky-to-failing
# without the lock; with it they must pass every time.
# --------------------------------------------------------------------------

def _make_many(tmp_path, count=8, pages=12):
    paths = []
    for n in range(count):
        texts = [f"doc{n} page{p} " + "reactor coolant flow " * 40 for p in range(pages)]
        paths.append(write_pdf(tmp_path / f"d{n}.pdf", texts))
    return paths


def _extract_all(path):
    with pdf_engine.open_pdf(path) as pdf:
        texts = [pdf.page_text(i) for i in range(pdf.page_count)]
        sizes = [pdf.render_pil(i, dpi=96).size for i in range(min(3, pdf.page_count))]
    return texts, sizes


def test_many_threads_give_the_same_result_as_one(tmp_path):
    paths = _make_many(tmp_path)
    single = [_extract_all(p) for p in paths]
    for _ in range(3):
        with ThreadPoolExecutor(max_workers=4) as pool:
            threaded = list(pool.map(_extract_all, paths))
        assert threaded == single


def test_lightweight_extraction_with_four_workers_matches_one_worker(tmp_path):
    paths = _make_many(tmp_path)

    def run(workers, out):
        out.mkdir()
        _, ok, failed, count = lightweight_extract_pdfs(
            only_process_these=paths, output_dir=str(out), max_workers=workers
        )
        rows = [json.loads(l) for l in (out / "01_chunks_kb.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        return sorted(ok), failed, count, sorted((r["chunk_id"], r["content"]) for r in rows)

    one = run(1, tmp_path / "out1")
    four = run(4, tmp_path / "out4")
    assert one[1] == [] and four[1] == []
    assert one == four
    assert one[2] > 0
