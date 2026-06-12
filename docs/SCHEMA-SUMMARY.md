# CRM Schema Summary
> Generated after EPIC-DB. Load this instead of the full schema.prisma in agent prompts.

## Tables by Module

### Auth / Identity
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `users` | id(uuid), email(citext), passwordHash, role(UserRole), isActive, deletedAt | → sessions, teams, audit_logs |
| `teams` | id, name(unique) | ↔ users via team_members |
| `team_members` | userId, teamId | PK(userId,teamId) |
| `sessions` | id, userId, token(unique), expiresAt | → users (cascade) |
| `two_factor_secrets` | id, userId(unique), secret, enabled | 1:1 users |
| `permissions` | id, role, module, action, fieldRules(json) | unique(role,module,action) |
| `audit_logs` | id, userId, action, module, recordId, oldValues, newValues | → users |

### Leads
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `leads` | id, firstName, lastName, email(citext), status, source, score, ownerId, assigneeId, deletedAt | → users, contact, account, opportunity |
| `lead_score_rules` | id, name, field, operator, value, points, isActive | |
| `lead_score_history` | id, leadId, ruleId, delta, reason | → leads (cascade) |

### Contacts
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `contacts` | id, firstName, lastName, email(citext), ownerId, deletedAt | ↔ accounts via contact_accounts |
| `contact_accounts` | contactId, accountId, isPrimary | M2M PK |
| `contact_roles` | id, contactId, role | → contacts |
| `interactions` | id, contactId, type, summary, happenedAt | → contacts |

### Accounts
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `accounts` | id, name, tier(AccountTier), healthScore, parentId(self), deletedAt | self-ref hierarchy |

### Pipeline / Opportunities
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `pipelines` | id, name(unique), isDefault | → stages |
| `stages` | id, pipelineId, name, order, probability | unique(pipelineId,order) |
| `opportunities` | id, title, value, closeDate, stageId, accountId, contactId, ownerId, deletedAt | |
| `products` | id, name, unitPrice, currency | |
| `proposals` | id, opportunityId, title, version | → opportunities (cascade) |
| `quotes` | id, opportunityId, number(unique) | → quote_line_items (cascade) |
| `quote_line_items` | id, quoteId, productId, qty, unitPrice, total | cascade on quote delete |
| `stage_history` | id, opportunityId, stageId, enteredAt, exitedAt | |

### Activities & Tasks
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `activities` | id, type, subject, relatedType, relatedId(polymorphic), userId, leadId | index(relatedType,relatedId) |
| `tasks` | id, title, status, priority, dueAt, assigneeId, relatedType, relatedId | → reminders |
| `reminders` | id, taskId, remindAt, sentAt | cascade on task delete |

### Ticketing / SLA / KB
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `tickets` | id, number(unique), status, category, priority, channel, accountId, assigneeId, deletedAt | |
| `ticket_notes` | id, ticketId, isInternal | cascade on ticket delete |
| `sla_policies` | id, accountTier, priority, firstResponseHours, resolutionHours | unique(tier,priority) |
| `sla_trackers` | id, ticketId(unique), policyId, firstResponseDue, resolutionDue | 1:1 ticket |
| `kb_categories` | id, name(unique), parentId(self) | |
| `articles` | id, title, content, categoryId, isPublished, deletedAt | |
| `article_ratings` | id, articleId, helpful | |

### Projects
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `projects` | id, name, status, accountId, opportunityId, deletedAt | |
| `phases` | id, projectId, name, order | cascade |
| `milestones` | id, projectId, phaseId, name, dueDate, order | |
| `project_tasks` | id, projectId, assigneeId, status, effortHours | |
| `documents` | id, projectId, name, url | cascade |

### Contracts & Invoicing
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `contracts` | id, number(unique), status, accountId, opportunityId, startDate, endDate, autoRenew | |
| `amendments` | id, contractId | cascade |
| `signatures` | id, contractId, signerEmail, status(SignatureStatus) | |
| `invoices` | id, number(unique), status, accountId, contractId, dueDate, totalAmount, currency | |
| `invoice_line_items` | id, invoiceId, description, qty, unitPrice, hsnCode | cascade |
| `payments` | id, invoiceId, amount, method, paidAt | cascade |

### Campaigns & Comms
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `campaigns` | id, name, type, status, deletedAt | |
| `audience_segments` | id, campaignId, filters(json) | cascade |
| `campaign_metrics` | id, campaignId, metricKey, value | cascade |
| `events` | id, campaignId?, name, startsAt | |
| `campaign_attributions` | id, campaignId, leadId?, opportunityId? | |
| `notifications` | id, userId, type, readAt, relatedType, relatedId | |
| `mentions` | id, userId, mentionedBy, relatedType, relatedId | |
| `comments` | id, authorId, relatedType, relatedId, parentId(self-thread) | |
| `email_templates` | id, name(unique), subject, body, variables(json) | |

### Admin / Integrations
| Table | Key Columns | Relations |
|-------|-------------|-----------|
| `custom_fields` | id, module, fieldName (unique per module), fieldType | |
| `layouts` | id, module, role (unique per module+role), config(json) | |
| `workflows` | id, name, module, triggerType, conditions, actions | |
| `integration_connections` | id, provider(unique), encryptedToken, status | → webhook_events |
| `webhook_events` | id, connectionId, eventType, payload | cascade |
| `consent_records` | id, email(citext), consentType, granted | |
| `recycle_bin` | id, module, recordId, recordData, purgeAt | |

## Key Enums
`UserRole` · `LeadStatus` · `LeadSourceType` · `AccountTier` · `DealStage` · `ActivityType` · `TaskStatus` · `Priority` · `TicketStatus` · `TicketCategory` · `TicketChannel` · `ProjectStatus` · `ContractStatus` · `InvoiceStatus` · `PaymentMethod` · `CampaignType` · `CampaignStatus` · `NotificationType` · `IntegrationProvider` · `SignatureStatus` · `Currency`

## Conventions
- PKs: `uuid` (`@default(uuid()) @db.Uuid`)
- Timestamps: `createdAt @default(now())`, `updatedAt @updatedAt`
- Soft delete: `deletedAt DateTime?` — always filter `deletedAt: None` in queries
- Emails: `@db.Citext` (case-insensitive, requires citext extension)
- Money: `@db.Decimal(15, 2)`, default currency `INR`
- Polymorphic: `relatedType String?` + `relatedId Uuid?` with composite index
