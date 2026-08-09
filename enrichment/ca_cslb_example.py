"""TEMPLATE, NOT WIRED IN OR VERIFIED — read before using.

Illustrates one legitimate, narrow way to get a real decision-maker name
for a contractor lead: California's Contractors State License Board (CSLB)
publishes license-holder names as public record, searchable at
https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx

This is a *pattern*, not a finished tool:
- This sandbox has no outbound network access to cslb.ca.gov, so this code
  has NOT been run or verified against the live site. Test it yourself
  before relying on it.
- CSLB's search is a stateful web form (ASP.NET, view-state tokens), not a
  documented JSON API — the request shape below is illustrative and will
  likely need adjustment (inspect the actual form/network requests in a
  browser dev-tools panel and adjust field names/tokens accordingly).
- Only use this pattern for public-record government license lookups like
  this one. Do not repurpose it to scrape personal data from sites where
  it isn't an intentionally published public record (e.g. social media
  profiles) — that's a different, much less defensible thing to automate.
- Other states publish similar public license records (TX TDLR, FL DBPR,
  NY DOB, etc.) under their own search forms; each needs its own adapter
  following this same pattern.

Usage (once verified/adapted):
    from enrichment.ca_cslb_example import lookup_license_holder
    name = lookup_license_holder(business_name="Acme Roofing")
"""
import requests

CSLB_SEARCH_URL = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx"


def lookup_license_holder(business_name: str, session: requests.Session | None = None) -> str | None:
    """Look up the licensed contractor/business name of record on CSLB.

    NOT VERIFIED — this is a starting point. CSLB's search form requires
    replaying ASP.NET __VIEWSTATE/__EVENTVALIDATION tokens from an initial
    GET before the search POST will succeed. Fetch the form first, parse
    those hidden fields (e.g. with BeautifulSoup), then include them in the
    POST body alongside the business name field before this will work.
    """
    raise NotImplementedError(
        "This is a documented template only - inspect the live CSLB form "
        "(view-source / browser devtools network tab) and implement the "
        "two-step GET-then-POST flow with real field names before use."
    )
