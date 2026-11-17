---
name: casualize-names
description: Convert formal names to casual versions for cold email personalization - first names, company names, and city names. Use when user asks to casualize names, make names friendly, or prepare lead data for emails.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

# Casualize Names

## Goal
Convert formal names (first names, company names, cities) to casual, friendly versions for cold emails and calls.

## Scripts
- `./scripts/casualize_batch.py` - Main script (all 3 fields at once)
- `./scripts/casualize_company_names_batch.py` - Company names only
- `./scripts/casualize_first_names_batch.py` - First names only
- `./scripts/casualize_city_names_batch.py` - City names only

## Quick Start
```bash
python3 -u ./scripts/casualize_batch.py "GOOGLE_SHEET_URL"
python3 -u ./scripts/casualize_batch.py "GOOGLE_SHEET_URL" --overwrite   # re-process existing
```

## How It Works
1. Processes records in batches of 50, with 5 parallel workers
2. Claude converts all three fields in one API call
3. Batch updates the sheet; only processes rows with emails
Performance: ~35 records/sec (3,000 records in about 90 seconds)

## Rules
**First names:** common nicknames ("William" -> "Will", "Jennifer" -> "Jen"); keep original if none; keep it professional.

**Company names:** remove leading "The", legal suffixes (LLC, Inc, Corp, Ltd) and generic words (Realty, Group, Solutions, Services); keep the core brand; use "you guys" for overly generic names.
- "Keller Williams Realty Inc" -> "Keller Williams"
- "The Teal Umbrella Family Dental Healthcare" -> "Teal Umbrella"

**City names:** local nicknames ("San Francisco" -> "SF", "Philadelphia" -> "Philly"); keep original if none.

## Output
Three new columns: `casual_first_name`, `casual_company_name`, `casual_city_name`

## Environment
```
ANTHROPIC_API_KEY=your_key
```
