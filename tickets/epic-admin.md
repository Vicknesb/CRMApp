# EPIC-ADMN · Admin & Configuration

> **Epic goal:** RBAC config, custom fields/layouts, workflow automation, admin panel, profile/preferences. **SRS:** AD-001/002, §7.2.
> **Mockups:** `12-admin.html`, `13-profile.html`. **Depends on:** EPIC-AUTH.

---

### ADMN-1 · Story · Config schema (CustomField, Layout, Workflow, Permission)
- **Points:** 3 **SRS:** AD-002 **Depends on:** AUTH-1
- **Description:** CustomField (module, key, type, options), Layout (module, config), Workflow (trigger, conditions, actions), Permission (role, module, action, fieldRules). Seed.
- **AC:** [ ] migration + seed.
- **Unit Tests:** [ ] repo CRUD.

### ADMN-2 · Story · RBAC field/record permission management
- **Points:** 5 **SRS:** AD-001 **Depends on:** ADMN-1, AUTH-7
- **Description:** CRUD permission rules; apply live in policy layer.
- **AC:** [ ] rule change alters API access/redaction live.
- **Unit Tests:** [ ] rule apply; [ ] field redaction toggle; [ ] record scope.

### ADMN-3 · Story · Custom fields & layouts
- **Points:** 5 **SRS:** AD-002 **Depends on:** ADMN-1
- **Description:** define custom fields; render dynamically on module forms.
- **AC:** [ ] new custom field appears + persists on target module.
- **Unit Tests:** [ ] field definition; [ ] dynamic value persist.

### ADMN-4 · Story · Workflow automation engine
- **Points:** 5 **SRS:** AD-002 **Depends on:** ADMN-1
- **Description:** trigger→condition→action engine (e.g., lead status change → create task/notify).
- **AC:** [ ] defined workflow fires on trigger.
- **Unit Tests:** [ ] condition eval; [ ] action exec; [ ] no-trigger no-op.

### ADMN-5 · Task · Frontend hooks
- **Points:** 2 **Depends on:** ADMN-2, ADMN-3, ADMN-4
- **AC:** [ ] `useUsers/usePermissions/useCustomFields/useWorkflows`.
- **Unit Tests:** [ ] fetch + invalidation.

### ADMN-6 · Story · UI: Admin panel — Users & roles
- **Points:** 3 **SRS:** §7.2 **Depends on:** ADMN-5
- **AC:** [ ] mirror `12-admin.html` Users tab; CRUD users + role assign.
- **Unit Tests:** [ ] user create; [ ] role change.

### ADMN-7 · Story · UI: Admin panel — Permissions & custom fields
- **Points:** 3 **SRS:** AD-001/002 **Depends on:** ADMN-5
- **AC:** [ ] permission matrix + custom field builder tabs.
- **Unit Tests:** [ ] permission toggle; [ ] add field.

### ADMN-8 · Story · UI: Admin panel — Workflows & integrations & audit
- **Points:** 3 **SRS:** AD-002 **Depends on:** ADMN-5, AUTH-8
- **AC:** [ ] workflow builder, integrations config, audit log viewer tabs.
- **Unit Tests:** [ ] workflow save; [ ] audit filter.

### ADMN-9 · Story · UI: Profile & preferences
- **Points:** 3 **SRS:** §7.1 **Depends on:** ADMN-5, AUTH-3
- **Description:** mirror `13-profile.html` (Personal, Performance, Notifications, Security/2FA, Preferences incl. theme).
- **AC:** [ ] profile + prefs persist; 2FA manage.
- **Unit Tests:** [ ] save profile; [ ] theme pref persist.

### ADMN-10 · Task · Seed/fixtures (config samples)
- **Points:** 1 **Depends on:** ADMN-1
- **AC:** [ ] sample permissions/fields/workflows seeded.
- **Unit Tests:** [ ] idempotent.

### ADMN-11 · Check · Admin module-wide check
- **Points:** 2 **Depends on:** ADMN-1…10
- **AC:** [ ] permission change + custom field + workflow fire E2E; ≥80% coverage; AD-001/002 satisfied.
- **Unit Tests:** [ ] integration covering rule change→access effect→workflow trigger.
