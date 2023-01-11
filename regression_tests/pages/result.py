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
        self.cutoff_input = page.locator("#cutoff_user_box")
        self.hydropathy_slider = page.locator("id=cutoff_user_slider")
        self.hydropathy_field = page.locator("id=cutoff_user_box")
        self.mouse = page.mouse
        self.hydropathy_line = page.get_by_role("presentation")

    def click_nth_snp(self, N: int) -> None:
        self.snps.nth(N).wait_for()
        return self.snps.nth(N).click()

    def get_nth_snp_tooltip(self, N: int) -> None:
        self.snps.nth(N).wait_for()
        self.snps.nth(N).hover()
        the_tooltip = self.page.get_by_text("rs1").locator("..")
        the_text = the_tooltip.inner_text()
        return the_text

    def get_mutation(self, snp_id: int):
        tooltip_text = self.get_nth_snp_tooltip(snp_id)
        mutation = tooltip_text.split()[1]
        from_res = mutation[0]
        from_resid = mutation[1:-1]
        to_res = mutation[-1]
        return from_res, from_resid, to_res
