# Architecture — CRM (IT Services)

> System, container, deployment, request-lifecycle, and auth/RBAC views. Derived from the SRS (§2.3, §5) and
> the project stack. Diagrams in ASCII + Mermaid. Companion: `BUSINESS-FLOW.md`, `TECH-DESIGN.md`.

---

## 1. System context (who & what talks to the CRM)

```
        ┌─────────────────────────────────────────────────────────────┐
        │                     CRM Application                          │
 Users  │   (React SPA  ⇄  FastAPI REST  ⇄  PostgreSQL)                │  External systems
 ─────► │                                                             │ ◄──────────────────
 Sales  │                                                             │  Gmail/Outlook (email)
 Support│                                                             │  Google/Outlook Calendar
 PM     │                                                             │  Jira / Azure DevOps
 Finance│                                                             │  Slack / MS Teams
 Mktg   │                                                             │  Zoho/QuickBooks (accounting)
 Admin  │                                                             │  DocuSign/Zoho Sign (eSign)
 Mgmt   │                                                             │  Mailchimp/SendGrid (email mktg)
        └─────────────────────────────────────────────────────────────┘
```

```mermaid
flowchart TB
    subgraph Users
      U1[Sales]:::u
      U2[Support]:::u
      U3[PM]:::u
      U4[Finance]:::u
      U5[Marketing]:::u
      U6[Admin / Mgmt]:::u
    end
    CRM[(CRM Application)]
    Users --> CRM
    CRM --> EM[Email Gmail/Outlook]
    CRM --> CAL[Calendar]
    CRM --> JIRA[Jira / Azure DevOps]
    CRM --> SLACK[Slack / Teams]
    CRM --> ACC[Zoho/QuickBooks]
    CRM --> SIGN[DocuSign/Zoho Sign]
    CRM --> MAIL[Mailchimp/SendGrid]
    classDef u fill:#eef;
```

---

## 2. Container / component view

```
 ┌───────────────────────────────────────────────────────────────────────┐
 │ Browser                                                                │
 │  ┌──────────────────────────────────────────────────────────────────┐ │
 │  │ React 18 SPA (Vite + TS, Tailwind+DaisyUI, TanStack Query)        │ │
 │  │  features/<module> · components(ui/layout/charts) · lib/apiClient │ │
 │  └───────────────────────────────┬──────────────────────────────────┘ │
 └──────────────────────────────────┼────────────────────────────────────┘
                       HTTPS (JSON, httpOnly cookie JWT)
                                    ▼
 ┌───────────────────────────────────────────────────────────────────────┐
 │ FastAPI service (Python, async)                                        │
 │   middleware: auth · RBAC · error envelope · structlog                 │
 │   modules/<module>/  router → service → repository                     │
 │   core/ (config, security, logging)   db/ (Prisma client wrapper)      │
 └───────────────┬───────────────────────────────────┬───────────────────┘
                 │ Prisma Client Python              │ connectors (OAuth/tokens, webhooks)
                 ▼                                    ▼
       ┌──────────────────┐                 ┌──────────────────────────┐
       │ PostgreSQL        │                 │ External integrations     │
       │ (all module data, │                 │ email/cal/Jira/Slack/...  │
       │  audit, indexes)  │                 └──────────────────────────┘
       └──────────────────┘
```

```mermaid
flowchart TD
    SPA[React SPA] -->|REST JSON + cookie JWT| API
    subgraph API[FastAPI service]
      MW[Middleware: auth, RBAC, error, logging]
      MOD[modules: router→service→repository]
      MW --> MOD
    end
    MOD -->|Prisma Client Python| DB[(PostgreSQL)]
    MOD --> INTG[Integration connectors]
    INTG --> EXT[Email / Calendar / Jira / Slack / Accounting / eSign]
```

---

## 3. Request lifecycle (one API call)

```
 SPA fetch ─► HTTPS ─► FastAPI router
                          │ 1. auth dependency (verify JWT cookie, 2FA state)
                          │ 2. RBAC dependency (role + record/field policy)
                          │ 3. Pydantic validation (422 on bad input)
                          ▼
                       service (business logic)
                          │ 4. repository (Prisma) → PostgreSQL
                          │ 5. audit log on mutation
                          ▼
                       response envelope { data, error, meta }
                          │ 6. field-level redaction per role
                          ▼
                 SPA (TanStack Query cache) ─► UI render
```

```mermaid
sequenceDiagram
    participant SPA
    participant Router
    participant Auth
    participant RBAC
    participant Service
    participant Repo
    participant DB as PostgreSQL
    SPA->>Router: request (cookie JWT)
    Router->>Auth: verify session/2FA
    Auth->>RBAC: role + record/field policy
    RBAC->>Service: validated (Pydantic)
    Service->>Repo: query/mutate
    Repo->>DB: SQL via Prisma
    DB-->>Repo: rows
    Service->>Service: audit log (on mutation)
    Service-->>SPA: { data, error, meta } (redacted per role)
```

---

## 4. Authentication & RBAC flow (SRS §5.2)

```
 login (email+pwd) ─► verify (bcrypt) ─► 2FA enabled? ─yes─► TOTP verify
        │ no                                   │
        ▼                                      ▼
   issue JWT (httpOnly+SameSite cookie, 30-min sliding)
        │
   every request ─► auth dep ─► RBAC dep ─► (role ability) + (record owner) + (field redaction)
        │                                        │ deny ─► 403
        ▼                                        ▼ allow
   audit log (logins, mutations, admin actions)  handler runs
```

---

## 5. Deployment view (SRS §2.3)

```
 GitHub repo ──push/PR──► GitHub Actions CI/CD
   │                         lint → typecheck → pytest(+Postgres) → vitest → build → security scan → deploy gate
   ▼
 Docker images: [api] [web]  +  managed PostgreSQL
   │
   ▼
 Cloud host (AWS/Azure/GCP) — containers behind load balancer, TLS 1.3
   • horizontal scaling (stateless API)   • daily backups (30-day)   • health monitoring/alerts
```

```mermaid
flowchart LR
    G[GitHub] --> CI[GitHub Actions: lint/test/build/scan]
    CI --> IMG[Docker images: api + web]
    IMG --> CLOUD[Cloud host AWS/Azure/GCP]
    CLOUD --> LB[Load balancer + TLS 1.3]
    LB --> APIc[api containers - stateless, scalable]
    APIc --> PG[(PostgreSQL + backups)]
    CLOUD --> MON[Health monitoring + alerts]
```

---

## 6. Cross-cutting concerns

| Concern | Where it lives |
|---------|----------------|
| AuthN/AuthZ | FastAPI dependencies (auth + RBAC), middleware |
| Validation | Pydantic (API) + Zod (forms, shared) |
| Error handling | exception handlers → `{data,error,meta}`; 422 field errors |
| Logging | structlog JSON (ELK-ready), request IDs |
| Audit | audit service on all mutations/logins/admin actions |
| Caching/perf | pagination, indexes, materialized report views |
| Security | TLS 1.3, AES-256 at rest, 2FA, OWASP, session timeout |
| Observability | health checks, monitoring/alerts, CI gates |

---

## 7. Data model (ERD)

The full ERD is **generated from the live Prisma schema** in ticket **DB-15** (EPIC-DB) and will be saved as
`docs/ERD.png` + `DATA_DICTIONARY.md`. Until then, the authoritative table list is the EPIC-DB schema tickets
(DB-3…DB-11) in `tickets/epic-db.md`.
