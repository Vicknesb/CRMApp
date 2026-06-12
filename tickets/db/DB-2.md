> **Epic context:** EPIC-DB · Database & Schema (Foundational Data Layer)

### DB-2 · Task · Prisma schema foundation (datasource, generator, conventions, enums)
- **Points:** 2 **SRS:** §5.6 **Depends on:** DB-1
- **Description:** Establish `schema.prisma`: datasource Postgres, `prisma-client-py` generator, global conventions (`id` UUID pk, `createdAt`/`updatedAt`, soft-delete `deletedAt`), and all shared enums (Role, LeadStatus, LeadSource, DealStage, TicketCategory, TicketPriority, TicketChannel, ProjectStatus, InvoiceStatus, ContractStatus, CampaignType, AccountTier, NotificationType, etc.).
- **Acceptance Criteria:**
  - [ ] Schema compiles (`prisma validate`); enums defined once and reused.
  - [ ] Convention mixin fields present on every model going forward.
- **Unit Tests:** [ ] `prisma validate` passes; [ ] enum values match `@crm/shared`.
- **DoD:** Global DoD + AC.