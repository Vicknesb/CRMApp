import { Routes, Route, Navigate } from 'react-router-dom'
import { PageShell } from './components/layout/PageShell'

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
      <Route path="/" element={<PlaceholderPage title="Dashboard" />} />
      <Route path="/leads" element={<PlaceholderPage title="Leads" />} />
      <Route path="/contacts" element={<PlaceholderPage title="Contacts" />} />
      <Route path="/accounts" element={<PlaceholderPage title="Accounts" />} />
      <Route path="/pipeline" element={<PlaceholderPage title="Pipeline" />} />
      <Route path="/activities" element={<PlaceholderPage title="Activities" />} />
      <Route path="/tickets" element={<PlaceholderPage title="Tickets" />} />
      <Route path="/projects" element={<PlaceholderPage title="Projects" />} />
      <Route path="/contracts" element={<PlaceholderPage title="Contracts" />} />
      <Route path="/invoices" element={<PlaceholderPage title="Invoices" />} />
      <Route path="/campaigns" element={<PlaceholderPage title="Campaigns" />} />
      <Route path="/analytics" element={<PlaceholderPage title="Analytics" />} />
      <Route path="/profile" element={<PlaceholderPage title="Profile" />} />
      <Route path="/notifications" element={<PlaceholderPage title="Notifications" />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
