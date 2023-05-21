"""
This module contains BlobulatorResultPage
"""

from playwright.sync_api import Page
from typing import List
from time import sleep


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
        self.hydropathy_line = page.get_by_test_id("cutoffline")
        self.blob_bars = page.locator("id=barChartblobPlot")
        self.lmin_slider = page.locator("id=domain_threshold_user_slider")
        self.lmin_field = page.locator("id=domain_threshold_user_box")

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

    def set_pathy_slider(self, target_hydropathy):
        self.hydropathy_slider.hover()
        self.mouse.down()

        right = 1000
        left = 0
        hydropathy = -1

        while hydropathy != target_hydropathy:
                       
            midpoint = (left+right) / 2
            self.mouse.move(midpoint, 0)
            hydropathy = float(self.hydropathy_field.input_value())

            if hydropathy < target_hydropathy:
                left = midpoint
            else:
                right = midpoint       

        self.mouse.up()
        sleep(1)
        return

    def set_lmin_slider(self, target_length):
        self.lmin_slider.hover()
        self.mouse.down()

        right = 1000
        left = 0
        length = -1

        while length != target_length:
                       
            midpoint = (left+right) / 2
            self.mouse.move(midpoint, 0)
            length = float(self.lmin_field.input_value())

            if length < target_length:
                left = midpoint
            else:
                right = midpoint       

        self.mouse.up()
        sleep(1)
        return

