> **Epic context:** EPIC-INTG · Integration Framework

### INTG-1 · Story · Connector framework (OAuth, token vault, webhooks)
- **Points:** 5 **SRS:** §6 **Depends on:** AUTH-1
- **Description:** generic OAuth2 connect flow, encrypted token storage per user/org, webhook receiver + signature verification, retry/backoff.
- **AC:** [ ] connectors register; tokens encrypted; webhooks verified.
- **Unit Tests:** [ ] token encrypt/decrypt; [ ] webhook signature valid/invalid; [ ] retry backoff.