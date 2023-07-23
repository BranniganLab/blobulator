# -*- coding: utf-8 -*-

"""
This module contains Blobulator New Query Page
"""

from playwright.sync_api import Page, BrowserContext
from .result import BlobulatorResultPage


class BlobulatorNewQuery:
    def __init__(self, page: Page, url: str) -> None:
        self.page = page
        self.compute_seq_button = page.locator(
            ':nth-match(:text("Compute"), 2)'
        )
        self.compute_uniprot_button = page.locator(
            ':nth-match(:text("Compute"), 1)'
        )
        self.search_input = page.locator("#aa_sequence")
        self.url = url
        self.uniprot_input = page.locator("#uniprot_id")

    def load(self) -> None:
        self.page.goto(self.url)

    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.compute_seq_button.click()

    def uniprot_search(self, uniprot_id: str, context: BrowserContext) -> Page:
        self.uniprot_input.fill(uniprot_id)

        with context.expect_page() as page_info:
            self.compute_uniprot_button.click(),
        page = page_info.value

        return page
