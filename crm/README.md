# Cold Call CRM

A single-file CRM for cold calling. No install, no server.

## Open it
Double-click `crm/index.html` (opens in your browser).

## Workflow
1. **Data** tab → import the CSV from `scrape_leads.py` (or any CSV with name + phone).
2. **Call** tab → tap the phone number, talk, tap an outcome. Next lead loads automatically.
3. **Leads** tab → search, filter, edit any lead.
4. **Stats** tab → dials, connects, meetings.

## Queue order
1. Follow-ups that are due
2. New leads
3. Retries (no answer / voicemail come back next day)

Meeting / Won / Lost / Do-not-call leave the queue.

## Your data
Saved in your browser only. Use **Data → Full backup** regularly.
