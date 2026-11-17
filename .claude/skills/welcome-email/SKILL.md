---
name: welcome-email
description: Send welcome email sequence to new clients. Use when user asks to send welcome emails, onboard new client with emails, or trigger welcome sequence.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

> **Adapt before use:** This skill comes from a course and is set up for the course author's business (team names Nick, Peter, Sam, his signature and his own spreadsheets). Before running it, Claude must swap in the user's own name, team, templates and sheet IDs, and confirm with the user before sending any email.

# Welcome Client Emails

## Goal
Send a 3-email welcome sequence from three team members when a new client signs. The course version sends from Nick (welcome, expectations), Peter (technical setup) and Sam (support intro). Replace these with the user's own team.

## Scripts
- `./scripts/welcome_client_emails.py` - Send welcome sequence

## Process
1. Receive client info (name, email, company)
2. Email 1: welcome and expectations
3. Email 2: technical setup
4. Email 3: support intro

## Usage
```bash
python3 ./scripts/welcome_client_emails.py --client_name "John Doe" --client_email "john@company.com" --company "Acme Corp"
```

Each email is personalized with client details and sent from a different team member to build relationships.
