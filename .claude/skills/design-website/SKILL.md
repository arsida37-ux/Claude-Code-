---
name: design-website
description: Generate a premium single-page mockup website for a prospect's business to pitch web design services. Use when user asks to design a website, create a mockup, or build a prospect website.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

# Design Website

## Goal
Generate a polished, single-page HTML website mockup for a prospect's business, used to pitch web design services. Style: bold typography, off-white backgrounds, editorial grid layouts, terracotta accents.

## Inputs
- **Prospect data:** a Google Sheet URL + row number (1-indexed, excluding header), an Excel/CSV file, or details typed by the user
- Optional: worksheet name (defaults to first sheet)

### Expected Columns (case-insensitive, flexible)
| Column | Used for |
|---|---|
| company_name / company | Business name (hero, nav, footer) |
| description / about | About section + hero subtitle |
| keywords / services | Services grid (comma-separated) |
| phone / phone_number | Contact section |
| email / contact_email | Contact section |
| address / full_address | Contact section |
| city, state, country | Location info |
| industry / category | Image search queries |
| first_name, last_name | Owner attribution |
| title / role | Owner role |

## Scripts
- `scripts/read_prospect.py` - Read a single prospect row from Google Sheets -> JSON
- `scripts/generate_website.py` - Generate HTML website from prospect JSON

## Process
1. **Read prospect data**
   ```bash
   python3 .claude/skills/design-website/scripts/read_prospect.py --url "SHEET_URL" --row ROW_NUMBER
   ```
2. **Generate website**
   ```bash
   python3 .claude/skills/design-website/scripts/read_prospect.py --url "SHEET_URL" --row 1 | python3 .claude/skills/design-website/scripts/generate_website.py
   # or from a JSON file
   python3 .claude/skills/design-website/scripts/generate_website.py < prospect.json
   ```
3. **Preview:** open `.tmp/website_*.html` in a browser

## Outputs
- `.tmp/website_{company_slug}.html`: self-contained HTML, CSS inline, images from Unsplash

## Environment
- `UNSPLASH_ACCESS_KEY` in `.env` for stock photos (free at unsplash.com/developers). Without it, falls back to picsum.photos placeholders.
- Google OAuth credentials (token.json / credentials.json) for Sheets access

## Design System
- **Font:** Inter
- **Colors:** off-white #F2EFE6, black #000, white #FFF, terracotta #C38133
- **Type:** bold uppercase display (72-100px), section heads (36-48px), body (16-18px)
- **Layout:** full-viewport hero, 2-col about, 3-col services grid, 2x2 gallery
- **Buttons:** bordered, uppercase, letter-spaced

## Edge Cases
- Missing columns: sensible defaults (e.g. "Welcome" if no description)
- Long company names: responsive font sizing
- Special characters: HTML-escaped
