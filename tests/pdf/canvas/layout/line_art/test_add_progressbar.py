import unittest
from datetime import datetime
from pathlib import Path

from borb.io.read.types import Decimal
from borb.pdf import FlexibleColumnWidthTable
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.shape.progressbar import ProgressSquare
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
    FixedColumnWidthTable,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from tests.test_util import compare_visually_to_ground_truth, check_pdf_using_validator


class TestAddProgressbar(unittest.TestCase):
    """
    This test creates a PDF with a dragon-curve in it.
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.add_page(page)
        layout = SingleColumnLayout(page)

        # write test information
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                    font_color=HexColor("00ff00"),
                )
            )
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(Paragraph("This test creates a PDF with a ProgressBar in it"))
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        t: FixedColumnWidthTable = FixedColumnWidthTable(
            number_of_columns=2, number_of_rows=11
        )
        t.add(Paragraph("Percentage", font="Helvetica-Bold"))
        t.add(Paragraph("ProgressSquare", font="Helvetica-Bold"))
        for i in range(0, 100, 10):
            t.add(Paragraph(str(i)))
            t.add(
                ProgressSquare(
                    percentage=(i / 100),
                    stroke_color=HexColor("#6F8F72"),
                    fill_color=HexColor("#8FD694"),
                )
            )
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)

        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)

        # compare visually
        compare_visually_to_ground_truth(out_file)
        check_pdf_using_validator(out_file)
