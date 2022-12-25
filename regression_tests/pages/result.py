"""
This module contains BlobulatorResultPage
"""

from playwright.sync_api import Page
from typing import List


class BlobulatorResultPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.snps = page.locator("id=snp_triangles")
        self.tab = page.locator("id=result-tab")
        self.uniprot_id = page.get_by_text("Uniprot ID:")
        self.mutate_box = page.locator("#mutatebox")

    def click_nth_snp(self, N: int) -> None:
        self.snps.nth(N).wait_for()
        return self.snps.nth(N).click()

    def get_nth_snp_tooltip(self, N: int) -> None:
        self.snps.nth(N).wait_for()
        self.snps.nth(N).hover(force=True)
        the_tooltip = self.page.locator("#tooltip")
        the_text = the_tooltip.all_text_contents()
        return the_text
