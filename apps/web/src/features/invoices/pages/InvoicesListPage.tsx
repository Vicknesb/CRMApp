import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useInvoices, useAgingReport } from '../hooks/useInvoices'
import { cn } from '@/lib/cn'

const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'badge-ghost', SENT: 'badge-info',
  PAID: 'badge-success', OVERDUE: 'badge-error', CANCELLED: 'badge-neutral',
}

export function InvoicesListPage(): JSX.Element {
  const [tab, setTab] = useState<'all' | 'aging'>('all')
  const [status, setStatus] = useState<string | undefined>()
  const { data, isLoading } = useInvoices(status ? { status } : undefined)
  const { data: agingData } = useAgingReport()

  const invoices: any[] = data?.data ?? []
  const aging: any[] = agingData?.data ?? []

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="tabs tabs-boxed">
          <button className={cn('tab', tab === 'all' && 'tab-active')} onClick={() => setTab('all')}>All Invoices</button>
          <button className={cn('tab', tab === 'aging' && 'tab-active')} onClick={() => setTab('aging')}>Aging Report</button>
        </div>
        <Link to="/invoices/new" className="btn btn-primary btn-sm">+ New Invoice</Link>
      </div>

      {tab === 'aging' ? (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {aging.map((b: any) => (
            <div key={b.bucket} className="stat bg-base-100 border border-base-300 rounded-box">
              <div className="stat-title">{b.bucket} days</div>
              <div className={cn('stat-value text-xl', b.bucket === '90+' ? 'text-error' : 'text-warning')}>
                ₹{Number(b.totalAmount).toLocaleString('en-IN')}
              </div>
              <div className="stat-desc">{b.invoiceCount} invoice{b.invoiceCount !== 1 ? 's' : ''}</div>
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="flex gap-2 flex-wrap">
            {['', 'DRAFT', 'SENT', 'PAID', 'OVERDUE'].map((s) => (
              <button key={s} className={cn('btn btn-sm', status === (s || undefined) ? 'btn-primary' : 'btn-ghost')}
                onClick={() => setStatus(s || undefined)}>
                {s || 'All'}
              </button>
            ))}
          </div>
          {isLoading ? (
            <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
          ) : (
            <div className="overflow-x-auto">
              <table className="table">
                <thead><tr><th>Number</th><th>Status</th><th>Amount</th><th>Due Date</th><th></th></tr></thead>
                <tbody>
                  {invoices.length === 0 ? (
                    <tr><td colSpan={5} className="text-center py-8 text-base-content/40">No invoices</td></tr>
                  ) : invoices.map((inv) => (
                    <tr key={inv.id} className="hover">
                      <td><Link to={`/invoices/${inv.id}`} className="link link-hover font-mono text-sm">{inv.number}</Link></td>
                      <td><span className={cn('badge badge-sm', STATUS_COLORS[inv.status] ?? 'badge-ghost')}>{inv.status}</span></td>
                      <td className="font-medium">₹{Number(inv.totalAmount).toLocaleString('en-IN')}</td>
                      <td>{new Date(inv.dueDate).toLocaleDateString('en-IN')}</td>
                      <td><Link to={`/invoices/${inv.id}`} className="btn btn-xs btn-ghost">View</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}
