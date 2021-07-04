#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class converts HTML to PDF.
"""
import xml.etree.ElementTree as ET

import typing
from lxml.etree import HTMLParser  # type: ignore [import]

from ptext.pdf.canvas.layout.page_layout.browser_layout import BrowserLayout
from ptext.pdf.canvas.layout.page_layout.page_layout import PageLayout
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.page.page_size import PageSize
from ptext.toolkit.export.html_to_pdf.tag_transformer.any_tag_transformer import (
    AnyTagTransformer,
)


class HTMLToPDF:
    """
    This class converts HTML to PDF
    """

    @staticmethod
    def convert_html_to_pdf(html: typing.Union[str, ET.Element]) -> Document:
        """
        This function converts HTML to PDF
        """

        # convert str to ET.Element
        root_element: typing.Optional[ET.Element] = None
        if isinstance(html, str):
            root_element = ET.fromstring(html, HTMLParser())
        else:
            root_element = html
        assert root_element is not None

        # build empty Document
        pdf_document: Document = Document()

        # build empty Page
        first_page: Page = Page(
            PageSize.A4_LANDSCAPE.value[0], PageSize.A4_LANDSCAPE.value[1]
        )
        pdf_document.append_page(first_page)

        # build PageLayout
        page_layout: PageLayout = BrowserLayout(first_page)

        # convert
        AnyTagTransformer().transform(root_element, [], page_layout)

        # return
        return pdf_document