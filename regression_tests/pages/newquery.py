# -*- coding: utf-8 -*-

"""
This module contains Blobulator New Query Page
"""

from playwright.sync_api import Page


class BlobulatorNewQuery:
    def __init__(self, page: Page, url: str) -> None:
        self.page = page
        self.compute_seq_button = page.locator(
            ':nth-match(:text("Compute"), 2)'
        )
        self.search_input = page.locator("#aa_sequence")
        self.url = url

    def load(self) -> None:
        self.page.goto(self.url)

    def search(self, phrase: str) -> None:
        self.search_input.fill(phrase)
        self.compute_seq_button.click()
