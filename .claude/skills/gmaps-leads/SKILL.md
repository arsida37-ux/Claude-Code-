---
name: gmaps-leads
description: Scrape Google Maps for B2B leads with deep website enrichment and contact extraction. Use when user asks to find local businesses, scrape Google Maps, generate contractor lists, or build local service business databases.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

# Google Maps Lead Generation

## Goal
Generate high-quality B2B leads from Google Maps with deep contact enrichment by scraping websites and using Claude to extract structured contact data.

## Inputs
| Parameter | Required | Description |
|---|---|---|
| `--search` | Yes | Search query (e.g., "plumbers in Austin TX") |
| `--limit` | No | Max results (default: 10) |
| `--sheet-url` | No | Existing sheet to append to |
| `--workers` | No | Parallel workers (default: 3) |

## Scripts
- `./scripts/gmaps_lead_pipeline.py` - Main orchestration
- `./scripts/gmaps_parallel_pipeline.py` - Parallel version
- `./scripts/scrape_google_maps.py` - Google Maps scraper
- `./scripts/extract_website_contacts.py` - Website contact extractor
- `./scripts/update_sheet.py` - Google Sheets sync

## Usage
```bash
# Create new sheet with 10 leads
python3 ./scripts/gmaps_lead_pipeline.py --search "plumbers in Austin TX" --limit 10

# Append to existing sheet
python3 ./scripts/gmaps_lead_pipeline.py --search "dentists in Miami FL" --limit 25 --sheet-url "https://docs.google.com/spreadsheets/d/..."

# Higher volume
python3 ./scripts/gmaps_lead_pipeline.py --search "roofing contractors in Austin TX" --limit 50 --workers 5
```

## Pipeline Steps
1. **Google Maps Scrape** - Apify `compass/crawler-google-places` returns listings
2. **Website Scraping** - Fetches main page + up to 5 contact pages
3. **Web Search Enrichment** - DuckDuckGo search for owner contact info
4. **Claude Extraction** - Claude extracts structured contacts
5. **Google Sheet Sync** - Appends new leads, deduplicates by lead_id

## Output Schema (36 fields)
- **Business:** business_name, category, address, city, state, zip_code, phone, website, rating, review_count
- **Contacts:** emails, additional_phones, business_hours
- **Social:** facebook, twitter, linkedin, instagram, youtube, tiktok
- **Owner:** owner_name, owner_title, owner_email, owner_phone, owner_linkedin
- **Team:** JSON array of team members
- **Metadata:** lead_id, scraped_at, search_query, pages_scraped, enrichment_status

## Cost
About $0.012-0.022 per lead (Apify + Claude). 100 leads: about $1.50-2.50.

## Troubleshooting
- **"No businesses found"**: Include location in query
- **403 Forbidden**: ~10-15% of sites block scrapers (handled gracefully)
- **Auth issues**: Delete `token.json` and re-authenticate
- **Duplicates**: Uses lead_id (MD5 of name|address) for deduplication

## Environment
```
APIFY_API_TOKEN=your_token
ANTHROPIC_API_KEY=your_key
```
