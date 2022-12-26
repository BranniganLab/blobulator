"""
These tests cover basic Blobulation
"""

from pages.result import BlobulatorResultPage
from pages.newquery import BlobulatorNewQuery
from playwright.sync_api import expect, Page, BrowserContext


def test_basic_blobulator_search(
    page: Page,
    search_page: BlobulatorNewQuery,
) -> None:

    # Given the Blobulator home page is displayed
    search_page.load()

    # When the user enters a sequence
    search_page.search("LLLLLQQ")


def test_uniprot_search(
    context: BrowserContext,
    page: Page,
    search_page: BlobulatorNewQuery,
    uniprot_id: str,
) -> None:

    # given the page loads
    search_page.load()

    # When the user searches for a uniprot id...
    page = search_page.uniprot_search(uniprot_id, context)
    result_page = BlobulatorResultPage(page)

    # Expect the result page to have the uniprot id in the header
    expect(result_page.uniprot_id).to_contain_text(uniprot_id)


def test_snp_button(page: Page, uniprot_results: BlobulatorResultPage):
    # given the results page is loaded
    result_page = uniprot_results

    snp_id = 1
    # When you click on a SNP
    result_page.click_nth_snp(snp_id)
    _, from_resid, to_res = result_page.get_mutation(snp_id)

    # Expect the mutate box to be checked
    expect(result_page.mutate_box).to_be_checked()

    # And the mutation drop down matches the SNP
    expect(result_page.page.locator("#snp_id")).to_have_value(from_resid)

    # And the mutate-to field matches the SNP
    expect(result_page.page.locator("#residue_type")).to_have_value(to_res)

    # And the snp triangle to be red
    expect(result_page.snps.nth(snp_id)).to_have_attribute("fill", "red")
