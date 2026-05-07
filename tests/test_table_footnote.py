"""Regression test for table footnote extraction (00013368.pdf, page 34).

PyMuPDF's table detector vertically merges a sparse column-0 header cell
with empty cells below it, so text under the actual data rows is swallowed
into the header cell.
"""
import os
from typing import cast

import pymupdf4llm


PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "00013368.pdf")


def test_table_5_footnote_not_truncated():
    md = cast(str, pymupdf4llm.to_markdown(PDF, pages=[33]))

    assert "~~b~~" not in md
    assert "~~c~~" not in md

    for needle in ("13-27 mL/min", "32-46 mL/min", "> 100 mL/min"):
        assert needle in md, f"Expected footnote text '{needle}' in output"
