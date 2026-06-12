import { useState } from 'react'
import { Link } from 'react-router-dom'
import { PageShell } from '../../../components/layout/PageShell'
import { Badge } from '../../../components/ui/Badge'
import { Button } from '../../../components/ui/Button'
import { useLeads, useDeleteLead } from '../hooks/useLeads'

const STATUS_VARIANT: Record<string, 'success' | 'warning' | 'info' | 'error' | 'default'> = {
  NEW: 'info',
  CONTACTED: 'warning',
  QUALIFIED: 'success',
  UNQUALIFIED: 'error',
  CONVERTED: 'default',
}

export function LeadsListPage(): JSX.Element {
  const [search, setSearch] = useState('')
  const { data: leads, isLoading } = useLeads(search ? { search } : undefined)
  const deleteLead = useDeleteLead()

  return (
    <PageShell title="Leads">
      <div className="flex items-center justify-between mb-6">
        <input
          className="input input-bordered w-64"
          placeholder="Search leads..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Link to="/leads/new">
          <Button size="sm">+ New Lead</Button>
        </Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20">
          <span className="loading loading-spinner loading-lg text-primary" />
        </div>
      ) : (
        <div className="card bg-base-100 shadow-sm border border-base-300">
          <div className="overflow-x-auto">
            <table className="table table-zebra">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Company</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Source</th>
                  <th>Score</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {(leads ?? []).map((lead) => (
                  <tr key={lead.id}>
                    <td>
                      <Link to={`/leads/${lead.id}`} className="link link-hover font-medium">
                        {lead.firstName} {lead.lastName}
                      </Link>
                    </td>
                    <td>{lead.company ?? '—'}</td>
                    <td className="text-sm">{lead.email}</td>
                    <td>
                      <Badge variant={STATUS_VARIANT[lead.status] ?? 'default'}>
                        {lead.status}
                      </Badge>
                    </td>
                    <td className="text-sm">{lead.source}</td>
                    <td>
                      <span className="font-semibold text-primary">{lead.score}</span>
                    </td>
                    <td>
                      <div className="flex gap-1">
                        <Link to={`/leads/${lead.id}/edit`}>
                          <Button size="xs" variant="ghost">Edit</Button>
                        </Link>
                        <Button
                          size="xs"
                          variant="error"
                          onClick={() => deleteLead.mutate(lead.id)}
                        >
                          Del
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
                {(leads ?? []).length === 0 && (
                  <tr>
                    <td colSpan={7} className="text-center text-base-content/50 py-8">
                      No leads found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </PageShell>
  )
}
