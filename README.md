# scrape_leads — US Contractor Lead Finder

Finds US general-contractor businesses that have **no website listed on
Google Business Profile**, using the official Google Places API. Outputs a
CSV with business name, phone number, and address for each lead.

## Why it works this way (read before using)

You asked for decision-maker names, phone numbers, and emails for 100 US
contractors without websites. Here's what's actually feasible, and why the
tool is scoped the way it is:

- **Business name, phone, address** — reliably available via Google Places
  (Business Profile) data. This tool automates that part.
- **"No website" filter** — Places data includes a `website` field when the
  business has listed one. We treat "no website field" as "no website."
  Caveat: some businesses list a Facebook/Instagram page or a third-party
  listing (Yelp, Houzz) in that field instead of a real site — the tool
  flags these separately (`--strict-no-social`) since they're borderline.
- **Decision-maker name** — Google Places has no such field. This is almost
  never public data for a small contractor without a website. Realistic
  legitimate paths (not automated here, on purpose):
  - Call the listed number and ask — the normal, compliant way sales teams
    identify a decision-maker.
  - Some state contractor-license boards publish the license holder's name
    (e.g. CA CSLB, TX TDLR, FL DBPR). Coverage and formats differ per state
    with no unified API, so this isn't automated for all 50 states. See
    `enrichment/` for a documented example (California) you can extend.
- **Email** — essentially never public for a sole proprietor/small
  contractor without a website. This tool does **not** guess, construct, or
  scrape personal emails. Doing so reliably means either the owner tells you
  directly, or a paid B2B enrichment service (Hunter.io, Apollo, etc.) that
  it has independently sourced and warranted — that's a separate,
  user-driven step, not something to bolt on here.

The output CSV has `decision_maker_name` and `email` columns left blank
on purpose, with a `notes` column explaining how to fill them in
compliantly.

## Compliance note

If these leads are for cold outreach:
- **Phone (calls/texts):** TCPA applies to certain call/text types, especially
  autodialed/prerecorded calls and texts — check current rules for B2B
  calls in your use case before an automated campaign.
- **Email:** CAN-SPAM requires accurate sender info, a working opt-out, and
  your physical address in every commercial email.
- Scraping Google's own web/Maps UI (as opposed to using the official
  Places API) would violate Google's Terms of Service — this tool only
  uses the official API.

This tool doesn't make outreach compliant for you — that's on how you use
the output.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and set GOOGLE_PLACES_API_KEY (enable "Places API" + billing
# in Google Cloud Console — https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
```

## Usage

```bash
python3 scrape_leads.py --trade "general contractor" --target 100 --output leads.csv
```

Useful flags:

| Flag | Default | Description |
|---|---|---|
| `--trade` | `general contractor` | Trade/search term, e.g. `roofing contractor`, `plumber`, `HVAC contractor` |
| `--target` | `100` | Stop once this many no-website leads are collected |
| `--output` | `leads.csv` | Output CSV path (appended to; resumable) |
| `--states` | all | Restrict to specific state abbreviations, e.g. `--states CA TX FL` |
| `--max-cities` | none | Cap how many cities to query (useful for a quick test run) |
| `--strict-no-social` | off | Also exclude leads whose "website" is actually a Facebook/Instagram/Yelp/Houzz link |
| `--sleep` | `0.2` | Seconds to sleep between API calls (rate limiting) |
| `--resume` | off | Skip place_ids already present in `--output` from a prior run |

Run `python3 scrape_leads.py --help` for the full list.

### Cost estimate

Each city query = 1 Text Search call (~$0.032) + 1 Place Details call per
result (~$0.017 each, Basic Data fields only). Finding 100 no-website leads
typically requires reviewing several hundred candidates (most contractors
*do* have a website), so budget roughly $15–$40 in Places API usage for a
run of this size. Google gives a monthly free credit that may cover it —
check your Cloud Console billing page.

## Extending decision-maker / email enrichment

See `enrichment/ca_cslb_example.py` for a documented, working example that
looks up the license holder name for a California contractor via the
public CSLB license search. Use it as a template for other states — do not
generalize it into a scraper for personal data outside these narrow,
government-published-record cases.
