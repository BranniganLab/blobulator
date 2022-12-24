"""
This module contains shared fixtures.
"""

import pytest

from pages.result import BlobulatorResultPage
from pages.newquery import BlobulatorNewQuery
from playwright.sync_api import Page


@pytest.fixture
def result_page(page: Page) -> BlobulatorResultPage:
    return BlobulatorResultPage(page)


@pytest.fixture
def search_page(page: Page, url: str) -> BlobulatorNewQuery:
    return BlobulatorNewQuery(page, url)


@pytest.fixture(params=["https://www.blobulator.branniganlab.org"])
def url(request):
    return request.param
