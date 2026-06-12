# EPIC-INTG · Integration Framework

> **Epic goal:** Shared connector framework + the external integrations from SRS §6 (email, calendar, Slack/Teams, Jira, accounting, eSignature, email-marketing). Module epics consume these.
> **SRS:** §6. **Depends on:** EPIC-AUTH. Priority per §6 (Must/Should/Nice noted).

---

### INTG-1 · Story · Connector framework (OAuth, token vault, webhooks)
- **Points:** 5 **SRS:** §6 **Depends on:** AUTH-1
- **Description:** generic OAuth2 connect flow, encrypted token storage per user/org, webhook receiver + signature verification, retry/backoff.
- **AC:** [ ] connectors register; tokens encrypted; webhooks verified.
- **Unit Tests:** [ ] token encrypt/decrypt; [ ] webhook signature valid/invalid; [ ] retry backoff.

### INTG-2 · Story · Email sync (Gmail/Outlook) — Must
- **Points:** 5 **SRS:** §6 **Depends on:** INTG-1
- **Description:** OAuth connect; auto-log inbound/outbound as Activities; send-from-CRM.
- **AC:** [ ] mailbox connect; emails auto-logged to contacts; send works.
- **Unit Tests:** [ ] message→activity mapping; [ ] send payload; [ ] token refresh.

### INTG-3 · Story · Slack/Teams (Must)
- **Points:** 3 **SRS:** §6 **Depends on:** INTG-1
- **Description:** channel config; route deal/ticket events + @mentions.
- **AC:** [ ] events post to channel.
- **Unit Tests:** [ ] event→message; [ ] channel routing (mock).

### INTG-4 · Story · Jira / Azure DevOps (Must)
- **Points:** 5 **SRS:** §6 (PR-002) **Depends on:** INTG-1
- **Description:** issue mapping + bidirectional sync primitives (used by PROJ-7).
- **AC:** [ ] issue create/update push; inbound webhook apply.
- **Unit Tests:** [ ] field mapping; [ ] webhook handler (mock).

### INTG-5 · Story · Accounting (Zoho/QuickBooks) — Should
- **Points:** 3 **SRS:** §6 (IN-002) **Depends on:** INTG-1
- **Description:** invoice push + payment status pull (used by INV-6).
- **AC:** [ ] invoice sync; status callback.
- **Unit Tests:** [ ] sync payload; [ ] status apply (mock).

### INTG-6 · Story · eSignature (DocuSign/Zoho Sign) — Should
- **Points:** 3 **SRS:** §6 (CT-001) **Depends on:** INTG-1
- **Description:** signing request + status callback (used by CONTR-5).
- **AC:** [ ] envelope create; callback status.
- **Unit Tests:** [ ] request payload; [ ] callback (mock).

### INTG-7 · Story · Email marketing (Mailchimp/SendGrid) — Nice
- **Points:** 3 **SRS:** §6 (MK-001) **Depends on:** INTG-1
- **Description:** campaign send + metric ingest (used by CAMP-4).
- **AC:** [ ] send + metrics webhook.
- **Unit Tests:** [ ] metric ingest mapping (mock).

### INTG-8 · Task · Calendar sync (Google/Outlook) — Must
- **Points:** 3 **SRS:** §6 **Depends on:** INTG-1
- **AC:** [ ] sync meetings/tasks; meeting-scheduler links.
- **Unit Tests:** [ ] event mapping (mock).

### INTG-9 · Task · LinkedIn Sales Navigator (Should)
- **Points:** 2 **SRS:** §6 **Depends on:** INTG-1
- **AC:** [ ] import contacts/company data.
- **Unit Tests:** [ ] import mapping (mock).

### INTG-10 · Task · Twilio/MSG91 SMS & telephony (Should)
- **Points:** 2 **SRS:** §6 **Depends on:** INTG-1
- **AC:** [ ] outbound SMS; call logging.
- **Unit Tests:** [ ] SMS payload (mock).

### INTG-11 · Task · UI: Integrations settings hub
- **Points:** 3 **SRS:** §7.2 **Depends on:** INTG-1
- **AC:** [ ] connect/disconnect + status for each integration.
- **Unit Tests:** [ ] connection state render.

### INTG-12 · Check · Integrations module-wide check
- **Points:** 2 **Depends on:** INTG-1…11
- **AC:** [ ] each Must integration verified end-to-end (mock servers); ≥80% coverage; §6 Must items satisfied (Nice may be deferred w/ note).
- **Unit Tests:** [ ] integration smoke per connector (mock).
