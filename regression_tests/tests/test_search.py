"""
These tests cover basic Blobulation
"""

from pages.result import BlobulatorResultPage
from pages.newquery import BlobulatorNewQuery
from playwright.sync_api import expect, Page


def test_basic_blobulator_search(
    page: Page,
    search_page: BlobulatorNewQuery,
    result_page: BlobulatorResultPage,
) -> None:

    # Given the Blobulator home page is displayed
    search_page.load()

    # When the user enters a sequence
    search_page.search("LLLLLQQ")

    # # Then the search result query is the phrase
    # expect(result_page.search_input).to_have_value('panda')

    # # And the search result links pertain to the phrase
    # assert result_page.result_link_titles_contain_phrase('panda')

    # # And the search result title contains the phrase
    # expect(page).to_have_title('panda at DuckDuckGo')
