"""
These tests cover basic Blobulation
"""

from pages.result import BlobulatorResultPage
from pages.newquery import BlobulatorNewQuery
from playwright.sync_api import expect, Page, BrowserContext
from time import sleep


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


# When the mutation button is checked with a SNP
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


# After adjusting the hydropathy slider
def test_hydropathy_slider(page: Page, asynuclein_results: BlobulatorResultPage):
    # given the results page is loaded
    result_page = asynuclein_results

    # Get initial conditions
    result_page.blob_bars.nth(10).wait_for()
    hline_y_init = result_page.hydropathy_line.get_attribute("y1")
    blob_res10 = result_page.blob_bars.nth(10)
    res10_height_init = blob_res10.get_attribute("height")

    # Sanity check: the blob should initially be orange
    expect(blob_res10).to_have_attribute("fill", "rgb(247, 147, 30)")

    # When the hydropathy slider is set to 0.2
    target_hydropathy = 0.2
    result_page.set_pathy_slider(target_hydropathy)

    # Expect the cutoff indicator has moved down
    hline_y_current = result_page.hydropathy_line.get_attribute("y1")
    assert float(hline_y_current) > float(hline_y_init)

    # Expect the numerical input is updated to 0.2
    expect(result_page.hydropathy_field).to_have_value(str(target_hydropathy))

    # Expect the blob chart residue 10 to change heights
    assert blob_res10.get_attribute("height") > res10_height_init

    # Expect the blob chart residue 10 to now be blue
    expect(blob_res10).to_have_attribute("fill", "rgb(0, 113, 188)")


# Given the results page is loaded with P37840
# When the hydropathy slider is set to 0.6
# Expect the numerical input is updated to 0.2
# Expect the cutoff indicator has moved up
# Expect the blob chart to change heights
# Expect the blob chart to change colors


# After adjusting the blob size slider
# Given the results page is loaded with P37840
# When the blob size slider is set to 10
# Expect the numerical input is updated to 10
# Expect the blob chart to change heights
# Expect the blob chart to change colors

# Given the results page is loaded with P37840
# When the blob size slider is set to 1
# Expect the numerical input is updated to 1
# Expect the blob chart to change heights
# Expect the blob chart to change colors


# After adjusting the hydropathy numerical input
# Given the results page is loaded with P37840
# When the hydropathy numerical input is set to 1
# Expect the hydropathy slider moves left
# Expect the blob chart to change heights
# Expect the blob chart to change colors

# Given the results page is loaded with P37840
# When the hydropathy numerical input is set to 10
# Expect the hydropathy slider moves right
# Expect the blob chart to change heights
# Expect the blob chart to change colors


# After adjusting the blob size numerical input


# After clicking the hydropathy up and down buttons

# After clicking the blob size up and down buttons

# Check the download plots button

# Check the download data button

# Check that website links lead to the expected papers and websites

# Check multiple SNP residues and make sure that they update correctly after selecting a new SNP

# Run current regression tests with an introduced mutation.

# Check uniprot and ensemble IDs for both a legitimate and false ID. Make sure that the expected protein is blobulated, and a valid error is shown in the case of a false ID

# When the results page is loaded (on a non-full screen browser window) are all plots and “i” icons visible?

# For each track, are all bars visible?

# Load a large protein, does the browser load within 1 minute?

# Check links for SNP triangles, make sure they lead to the expected website

# Does everything on both the result and home pages look aligned?

# When clickable elements are selected, do they look as expected?

# Does the terminal output anything when blobulation occurs?

# Are SNP triangles centered over the correct residue?

# Does the skyline update around the correct residues?

# Does the result controls panel stay at the top of the page when scrolling?

# When zooming, check that all figures update, resid labels are legible, and the skyline updates correctly.

# Is the control panel correctly sized?

# Do all tabs contain their expected content?

# Blobulate the sequence GSGPPGPPGPPGPPGARGQAGVMGFPGPPGPPGPPGRAPTDQHIKQVCMRVIQEHFAEMAASLKRPDSGAT, and check that the smoothed kyte-doolittle hydropathies match those given by https://www.ebi.ac.uk/Tools/seqstats/emboss_pepinfo/
