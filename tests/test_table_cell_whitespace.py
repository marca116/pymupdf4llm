"""Regression test for table cell whitespace (00004633.pdf, page 25).

PyMuPDF emits each glyph cluster as its own span, with word-boundary
spaces sometimes living at the leading or trailing edge of a span. The
cell extractor used to strip those edges, joining adjacent spans into
runs like "5.0mLof0.9% NaCl Injection" instead of "5.0 mL of 0.9% NaCl
Injection".
"""
import os
from typing import cast

import pymupdf4llm


PDF = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "pdfs", "00004633.pdf"
)


def test_reconstitution_table_preserves_word_boundaries():
    md = cast(str, pymupdf4llm.to_markdown(PDF, pages=[24]))

    for needle in (
        "5.0 mL of 0.9% NaCl Injection",
        "25 mL of 0.9% NaCl Injection",
    ):
        assert needle in md, f"Expected '{needle}' in output"

    # The pre-fix output had these joined-up runs.
    for bad in ("5.0mLof", "mLof0.9", "0.9%NaCl"):
        assert bad not in md, f"Unexpected joined run '{bad}' in output"
