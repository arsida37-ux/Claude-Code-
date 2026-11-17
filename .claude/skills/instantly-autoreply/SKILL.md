---
name: instantly-autoreply
description: Auto-generate intelligent replies to incoming Instantly email threads using knowledge bases. Use when user asks about email auto-replies, Instantly responses, or automated email handling.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

> **Adapt before use:** This skill comes from a course and is set up for the course author's business (team names Nick, Peter, Sam, his signature and his own spreadsheets). Before running it, Claude must swap in the user's own name, team, templates and sheet IDs, and confirm with the user before sending any email.

# Instantly Auto-Reply

## Goal
Auto-generate replies to incoming emails from Instantly campaigns using campaign-specific knowledge bases.

## Scripts
- `./scripts/instantly_autoreply.py` - Main auto-reply script

## How It Works
1. Receives an incoming email thread from an Instantly webhook
2. Looks up the campaign ID in the knowledge base sheet
3. Retrieves campaign context (offers, credentials, tone)
4. Generates a reply with Claude
5. Sends the reply through the Instantly API

## Knowledge Base
The course version points at the author's private spreadsheet. The user needs their own sheet with one row per campaign: Campaign ID, Campaign Name, Knowledge Base (service details, offers, credentials), Reply Examples (tone/style).

## Usage
```bash
python3 ./scripts/instantly_autoreply.py --thread_id <id>
```

## Environment
```
INSTANTLY_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```
