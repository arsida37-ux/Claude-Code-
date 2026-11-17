---
name: create-proposal
description: Generate PandaDoc proposals from client information or sales call transcripts. Use when user asks to create a proposal, generate a quote, draft a contract, or prepare a client document.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

> **Setup status:** Instructions installed. The `scripts/` folder is not downloaded yet. Ask Claude to "install the scripts for this skill". It will pull them from the course Drive folder (IDs in `.claude/skills/SOURCES.md`). It will also switch Google Sheets steps to Excel if you need that.

> **Adapt before use:** This skill comes from a course and is set up for the course author's business (team names Nick, Peter, Sam, his signature and his own spreadsheets). Before running it, Claude must swap in the user's own name, team, templates and sheet IDs, and confirm with the user before sending any email.

# Proposal Generation

## Goal
Create PandaDoc proposals for clients, either from structured information or by extracting details from sales call transcripts.

## Inputs (one of)
**Option A: Structured data:** client first/last name, email, company; project title; 4 key problems; 4 key benefits; project duration; investment breakdown (Month 1, Month 2, Month 3+).

**Option B: Call transcript:** extract all details from it.

## Scripts
- `./scripts/create_proposal.py` - Creates PandaDoc proposal via API
- `./scripts/read_sheet.py` - Read client data from sheets if needed

## Process
### 1. Gather Information
- Use structured data directly, or extract from the transcript: client info, project context and title, 4 pain points, 4 solutions/benefits, financial terms
- Ask for any missing critical information

### 2. Generate Content
Expand the 4 problems and 4 benefits into strategic paragraphs.
- **Problems:** direct "you" language; focus on revenue impact and dollar amounts; specific and actionable. Example: "Right now, your top-of-funnel is converting very poorly to booked meetings..."
- **Benefits:** address the client directly; emphasize ROI and payback period; concrete deliverables.
- Also generate: slide footer "Confidential | [Company] Strategic Initiative | [Date]", contract footer "[Company]-[ProjectTitle]-[YYYY-MM]", created date (YYYY-MM-DD).

### 3. Create the Proposal
```bash
python3 ./scripts/create_proposal.py <<'JSON'
{
  "client": {"firstName": "...", "lastName": "...", "email": "...", "company": "..."},
  "project": {
    "title": "...",
    "problems": {"problem01": "...", "problem02": "...", "problem03": "...", "problem04": "..."},
    "benefits": {"benefit01": "...", "benefit02": "...", "benefit03": "...", "benefit04": "..."},
    "monthOneInvestment": "...", "monthTwoInvestment": "...", "monthThreeInvestment": "..."
  },
  "generated": {"slideFooter": "...", "contractFooterSlug": "...", "createdDate": "..."}
}
JSON
```

### 4. Follow-Up Email (draft, confirm with user before sending)
- Subject: "Re: [Brief Project Context] Discussion"
- Thank them for discussing their challenges
- 2-4 numbered sections with bold headers, each with a description and "Steps:" bullets
- Close: "I'll send you a full proposal shortly..." and sign with the user's own name

### 5. Notify User
Give the PandaDoc "internalLink" for review and confirm the email status.

## Environment
```
PANDADOC_API_KEY=your_key
```
