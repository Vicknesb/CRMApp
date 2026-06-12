import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useContracts, useRenewals } from '../hooks/useContracts'
import { cn } from '@/lib/cn'

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'badge-ghost', ACTIVE: 'badge-success',
  EXPIRED: 'badge-error', TERMINATED: 'badge-error', RENEWED: 'badge-info',
}

export function ContractsListPage(): JSX.Element {
  const [tab, setTab] = useState<'all' | 'renewals'>('all')
  const { data, isLoading } = useContracts()
  const { data: renewalData } = useRenewals(90)

  const contracts: any[] = data?.data ?? []
  const renewals: any[] = renewalData?.data ?? []

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="tabs tabs-boxed">
          <button className={cn('tab', tab === 'all' && 'tab-active')} onClick={() => setTab('all')}>All Contracts</button>
          <button className={cn('tab', tab === 'renewals' && 'tab-active')} onClick={() => setTab('renewals')}>
            Renewals {renewals.length > 0 && <span className="badge badge-error badge-sm ml-1">{renewals.length}</span>}
          </button>
        </div>
        <Link to="/contracts/new" className="btn btn-primary btn-sm">+ New Contract</Link>
      </div>

      {tab === 'renewals' ? (
        <div className="space-y-2">
          {renewals.length === 0 ? (
            <p className="text-center py-12 text-base-content/40">No contracts expiring within 90 days</p>
          ) : renewals.map((r: any) => (
            <div key={r.contractId} className="flex items-center justify-between p-4 bg-base-100 border border-warning/40 rounded-lg">
              <div>
                <p className="font-medium">{r.title}</p>
                <p className="text-sm text-base-content/60">{r.number}</p>
              </div>
              <div className="text-right">
                <p className={cn('font-bold', r.daysUntilExpiry <= 30 ? 'text-error' : 'text-warning')}>
                  {r.daysUntilExpiry}d left
                </p>
                {r.autoRenew && <span className="badge badge-success badge-sm">Auto-renew</span>}
              </div>
            </div>
          ))}
        </div>
      ) : isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr><th>Number</th><th>Title</th><th>Status</th><th>Value</th><th>End Date</th><th>Auto-renew</th></tr>
            </thead>
            <tbody>
              {contracts.length === 0 ? (
                <tr><td colSpan={6} className="text-center py-8 text-base-content/40">No contracts</td></tr>
              ) : contracts.map((c) => (
                <tr key={c.id} className="hover">
                  <td><Link to={`/contracts/${c.id}`} className="link link-hover font-mono text-sm">{c.number}</Link></td>
                  <td>{c.title}</td>
                  <td><span className={cn('badge badge-sm', STATUS_COLORS[c.status] ?? 'badge-ghost')}>{c.status}</span></td>
                  <td>₹{Number(c.value).toLocaleString('en-IN')}</td>
                  <td>{new Date(c.endDate).toLocaleDateString('en-IN')}</td>
                  <td>{c.autoRenew ? '✓' : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
