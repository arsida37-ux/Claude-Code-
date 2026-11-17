---
name: onboarding-kickoff
description: Automated client onboarding after kickoff call - generates leads, creates email campaigns, sets up auto-reply. Use when user asks to onboard a new client, set up campaigns for client, or run post-kickoff automation.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

> **Adapt before use:** This skill comes from a course and is set up for the course author's business (team names Nick, Peter, Sam, his signature and his own spreadsheets). Before running it, Claude must swap in the user's own name, team, templates and sheet IDs, and confirm with the user before sending any email.

# Post-Kickoff Client Onboarding

## Goal
Automated onboarding after a kickoff call: generate leads, create campaigns, set up auto-reply.

## Inputs
**Required:** client_name, client_email, service_type, target_location, offers (3, pipe-separated), target_audience, social_proof
**Optional:** lead_limit (default 500), value_proposition

## Scripts
- `./scripts/gmaps_lead_pipeline.py` - Lead generation
- `./scripts/casualize_company_names_batch.py` - Name casualization
- `./scripts/instantly_create_campaigns.py` - Campaign creation
- `./scripts/onboarding_post_kickoff.py` - Full orchestration
- `./scripts/update_sheet.py` - Sheet updates

## Process
1. **Search query:** `{service_type} in {target_location}` (e.g. "plumbers in Austin TX")
2. **Scrape and enrich leads**
   ```bash
   python3 ./scripts/gmaps_lead_pipeline.py --search "{service_type} in {target_location}" --limit {lead_limit} --sheet-name "{client_name} - Leads" --workers 5
   ```
3. **Casualize company names**
   ```bash
   python3 ./scripts/casualize_company_names_batch.py --sheet-url "{sheet_url}" --column "business_name" --output-column "casualCompanyName"
   ```
4. **Create Instantly campaigns**
   ```bash
   python3 ./scripts/instantly_create_campaigns.py --client_name "{client_name}" --client_description "..." --offers "{offers}" --target_audience "{target_audience}" --social_proof "{social_proof}"
   ```
5. **Upload leads** evenly across the 3 campaigns via the Instantly API
6. **Add a knowledge base entry** to the auto-reply sheet
7. **Send a summary email** to the client (campaign links, lead counts, sheet URL, auto-reply details, next steps). Confirm with the user first.

## Output
```json
{"status": "success", "client_name": "...", "sheet_url": "...", "lead_count": 50, "campaigns": [], "leads_uploaded": true, "knowledge_base_updated": true, "summary_email_sent": true}
```

## Timing and Errors
- About 10-15 minutes for 50 leads
- < 10 leads: warn but continue. 0 leads: error (bad query)
- Instantly API error: capture and note for manual fix. Sheet/email failures: log but complete
