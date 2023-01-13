"""
This module contains shared fixtures.
"""

import pytest

from pages.result import BlobulatorResultPage
from pages.newquery import BlobulatorNewQuery
from playwright.sync_api import Page, BrowserContext


@pytest.fixture
def search_page(page: Page, url: str) -> BlobulatorNewQuery:
    return BlobulatorNewQuery(page, url)


@pytest.fixture(params=["http://127.0.0.1:5000"])
def url(request):
    return request.param


@pytest.fixture(params=["P37840"])
def uniprot_id(request):
    return request.param


@pytest.fixture
def uniprot_results(
    context: BrowserContext, search_page: Page, uniprot_id: str
) -> BlobulatorResultPage:

    search_page.load()
    page = search_page.uniprot_search(uniprot_id, context)

    return BlobulatorResultPage(page)
