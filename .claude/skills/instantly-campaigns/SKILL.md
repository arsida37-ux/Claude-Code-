---
name: instantly-campaigns
description: Create cold email campaigns in Instantly with A/B testing. Use when user asks to create email campaigns, set up cold outreach, build email sequences, or configure Instantly campaigns.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

# Instantly Campaign Creation

## Goal
Create three email campaigns in Instantly from a client description and offers. Each has A/B tested first emails and follow-ups.

## Inputs
1. **Client description:** company name, industry, target audience, value proposition
2. **Offers** (optional): 3 offers. Generated if not provided.

## Scripts
- `./scripts/instantly_create_campaigns.py` - Creates campaigns via Instantly API
- `./scripts/read_sheet.py` - Read lead data if needed

## Process
1. **Load examples:** read `.tmp/instantly_campaign_examples/campaigns.md` if present, for personalization + social proof + offer structure
2. **Generate campaigns**
   ```bash
   python3 ./scripts/instantly_create_campaigns.py --client_name "ClientName" --client_description "..." --offers "Offer 1|Offer 2|Offer 3" --target_audience "Who we're emailing" --social_proof "Credentials/results"
   ```
3. **Review output:** 3 campaigns (one per offer), each with Email 1 (two A/B variants), Email 2 (follow-up bump), Email 3 (breakup)

## Email Structure
- **Email 1:** personalization hook (`{{icebreaker}}` or custom opener), social proof, offer, soft CTA
- **Email 2:** brief friendly bump, reference the first email, restate value, clear CTA
- **Email 3:** short and direct, last-chance framing, simple yes/no ask

## Variables
`{{firstName}}`, `{{lastName}}`, `{{companyName}}`, `{{casualCompanyName}}`, `{{icebreaker}}`, `{{sendingAccountFirstName}}`

## Edge Cases
- No offers: generate 3 distinct offers from the description
- API errors: retry once, then fail with a detailed error
- Rate limits: exponential backoff

## Compliance
Cold email must follow CAN-SPAM: accurate sender, working opt-out, physical address.

## API Notes
- Schedule requires a `name` field in each schedule object
- Timezone: use `America/Chicago` (not all IANA values work)
- Instantly strips plain text outside HTML tags: wrap in `<p>`
- Use the latest Claude model for generation

## Environment
```
INSTANTLY_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```
