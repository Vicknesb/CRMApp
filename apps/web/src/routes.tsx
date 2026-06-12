import { Routes, Route, Navigate } from 'react-router-dom'
import { PageShell } from './components/layout/PageShell'
import { LoginPage } from './features/auth/pages/LoginPage'
import { ProtectedRoute } from './features/auth/components/ProtectedRoute'
import { LeadsListPage } from './features/leads/pages/LeadsListPage'
import { LeadFormPage } from './features/leads/pages/LeadFormPage'
import { ContactsListPage } from './features/contacts/pages/ContactsListPage'
import { ContactFormPage } from './features/contacts/pages/ContactFormPage'
import { AccountsListPage } from './features/accounts/pages/AccountsListPage'
import { AccountFormPage } from './features/accounts/pages/AccountFormPage'
import { PipelineListPage } from './features/pipeline/pages/PipelineListPage'
import { OpportunityFormPage } from './features/pipeline/pages/OpportunityFormPage'
import { TasksPage } from './features/activities/pages/TasksPage'
import { TicketsListPage } from './features/tickets/pages/TicketsListPage'
import { TicketFormPage } from './features/tickets/pages/TicketFormPage'
import { IntegrationsPage } from './features/integrations/pages/IntegrationsPage'
import { ProjectsListPage } from './features/projects/pages/ProjectsListPage'
import { ProjectFormPage } from './features/projects/pages/ProjectFormPage'
import { ProjectDetailPage } from './features/projects/pages/ProjectDetailPage'
import { ContractsListPage } from './features/contracts/pages/ContractsListPage'
import { ContractFormPage } from './features/contracts/pages/ContractFormPage'
import { InvoicesListPage } from './features/invoices/pages/InvoicesListPage'
import { InvoiceFormPage } from './features/invoices/pages/InvoiceFormPage'

function PlaceholderPage({ title }: { title: string }): JSX.Element {
  return (
    <PageShell title={title}>
      <div className="flex items-center justify-center h-64">
        <p className="text-base-content/50">{title} — coming soon</p>
      </div>
    </PageShell>
  )
}

export function AppRoutes(): JSX.Element {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<PlaceholderPage title="Dashboard" />} />

        {/* Leads */}
        <Route path="/leads" element={<PageShell title="Leads"><LeadsListPage /></PageShell>} />
        <Route path="/leads/new" element={<PageShell title="New Lead"><LeadFormPage /></PageShell>} />
        <Route path="/leads/:id/edit" element={<PageShell title="Edit Lead"><LeadFormPage /></PageShell>} />

        {/* Contacts */}
        <Route path="/contacts" element={<PageShell title="Contacts"><ContactsListPage /></PageShell>} />
        <Route path="/contacts/new" element={<PageShell title="New Contact"><ContactFormPage /></PageShell>} />
        <Route path="/contacts/:id/edit" element={<PageShell title="Edit Contact"><ContactFormPage /></PageShell>} />

        {/* Accounts */}
        <Route path="/accounts" element={<PageShell title="Accounts"><AccountsListPage /></PageShell>} />
        <Route path="/accounts/new" element={<PageShell title="New Account"><AccountFormPage /></PageShell>} />
        <Route path="/accounts/:id/edit" element={<PageShell title="Edit Account"><AccountFormPage /></PageShell>} />

        {/* Pipeline */}
        <Route path="/pipeline" element={<PageShell title="Pipeline"><PipelineListPage /></PageShell>} />
        <Route path="/pipeline/new" element={<PageShell title="New Opportunity"><OpportunityFormPage /></PageShell>} />
        <Route path="/pipeline/:id/edit" element={<PageShell title="Edit Opportunity"><OpportunityFormPage /></PageShell>} />

        {/* Activities / Tasks */}
        <Route path="/activities" element={<PageShell title="Tasks"><TasksPage /></PageShell>} />

        {/* Tickets */}
        <Route path="/tickets" element={<PageShell title="Tickets"><TicketsListPage /></PageShell>} />
        <Route path="/tickets/new" element={<PageShell title="New Ticket"><TicketFormPage /></PageShell>} />

        {/* Integrations */}
        <Route path="/integrations" element={<PageShell title="Integrations"><IntegrationsPage /></PageShell>} />

        {/* Projects */}
        <Route path="/projects" element={<PageShell title="Projects"><ProjectsListPage /></PageShell>} />
        <Route path="/projects/new" element={<PageShell title="New Project"><ProjectFormPage /></PageShell>} />
        <Route path="/projects/:id" element={<PageShell title="Project Detail"><ProjectDetailPage /></PageShell>} />
        <Route path="/projects/:id/edit" element={<PageShell title="Edit Project"><ProjectFormPage /></PageShell>} />

        {/* Contracts */}
        <Route path="/contracts" element={<PageShell title="Contracts"><ContractsListPage /></PageShell>} />
        <Route path="/contracts/new" element={<PageShell title="New Contract"><ContractFormPage /></PageShell>} />
        <Route path="/contracts/:id/edit" element={<PageShell title="Edit Contract"><ContractFormPage /></PageShell>} />

        {/* Invoices */}
        <Route path="/invoices" element={<PageShell title="Invoices"><InvoicesListPage /></PageShell>} />
        <Route path="/invoices/new" element={<PageShell title="New Invoice"><InvoiceFormPage /></PageShell>} />

        {/* Placeholders for future epics */}
        <Route path="/campaigns" element={<PlaceholderPage title="Campaigns" />} />
        <Route path="/analytics" element={<PlaceholderPage title="Analytics" />} />
        <Route path="/profile" element={<PlaceholderPage title="Profile" />} />
        <Route path="/notifications" element={<PlaceholderPage title="Notifications" />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
