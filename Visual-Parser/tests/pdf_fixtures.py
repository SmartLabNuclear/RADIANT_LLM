"""
pdf_fixtures.py -- build small test PDFs by hand, with no PDF library.

Each page is one text string (or several lines) in standard Helvetica. A page
can also be rotated, have a CropBox smaller than its MediaBox, or carry an
embedded JPEG. ``encrypt_with_empty_password`` makes an encrypted copy using
pypdf (a declared Visual-Parser dependency).
"""

from __future__ import annotations

import io
from collections.abc import Sequence
from dataclasses import dataclass

from PIL import Image


@dataclass
class PageSpec:
    lines: Sequence[str]
    rotate: int = 0                                     # /Rotate (0, 90, 180, 270)
    mediabox: tuple[int, int, int, int] = (0, 0, 612, 792)
    cropbox: tuple[int, int, int, int] | None = None
    jpeg: bytes | None = None                        # embedded image, drawn at 50,300 size 200x150


def _esc(text: str) -> bytes:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("latin-1")


def make_jpeg(width: int = 64, height: int = 48, colour=(200, 30, 30)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (width, height), colour).save(buf, format="JPEG")
    return buf.getvalue()


def build_pdf(pages: Sequence[PageSpec]) -> bytes:
    """Return the bytes of a valid PDF with one page per PageSpec."""
    objects: list[bytes] = []   # objects[i] is object number i + 1

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    catalog = add(b"")          # placeholder, filled in below
    pages_obj = add(b"")        # placeholder
    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    kids = []
    for spec in pages:
        stream = b"BT /F1 12 Tf 72 720 Td 16 TL " + b" ".join(
            b"(" + _esc(line) + b") Tj T*" for line in spec.lines
        ) + b" ET"
        resources = f"/Font << /F1 {font} 0 R >>".encode()
        if spec.jpeg is not None:
            width, height = Image.open(io.BytesIO(spec.jpeg)).size
            image = add(
                f"<< /Type /XObject /Subtype /Image /Width {width} /Height {height} "
                f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode "
                f"/Length {len(spec.jpeg)} >>\nstream\n".encode() + spec.jpeg + b"\nendstream"
            )
            resources += f" /XObject << /Im1 {image} 0 R >>".encode()
            stream += b" q 200 0 0 150 50 300 cm /Im1 Do Q"
        content = add(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
        mb = " ".join(str(v) for v in spec.mediabox)
        extra = f" /Rotate {spec.rotate}" if spec.rotate else ""
        if spec.cropbox is not None:
            extra += " /CropBox [" + " ".join(str(v) for v in spec.cropbox) + "]"
        kids.append(add(
            f"<< /Type /Page /Parent {pages_obj} 0 R /MediaBox [{mb}]{extra} "
            f"/Resources << {resources.decode()} >> /Contents {content} 0 R >>".encode()
        ))

    objects[catalog - 1] = f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode()
    objects[pages_obj - 1] = (
        "<< /Type /Pages /Kids [" + " ".join(f"{k} 0 R" for k in kids) + f"] /Count {len(kids)} >>"
    ).encode()

    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(out.tell())
        out.write(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = out.tell()
    out.write(f"xref\n0 {len(objects) + 1}\n".encode())
    out.write(b"0000000000 65535 f \n")
    for off in offsets:
        out.write(f"{off:010d} 00000 n \n".encode())
    out.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    return out.getvalue()


def write_pdf(path, texts: Sequence[str], **page_kwargs) -> str:
    """Write a PDF with one page per string in *texts*; return the path as a str."""
    path.write_bytes(build_pdf([PageSpec(lines=[t], **page_kwargs) for t in texts]))
    return str(path)


def encrypt_with_empty_password(pdf_bytes: bytes) -> bytes:
    """An RC4-128 encrypted copy whose user password is empty (opens without a prompt)."""
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(pdf_bytes)))
    writer.encrypt(user_password="", owner_password="owner-secret", algorithm="RC4-128")
    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()
