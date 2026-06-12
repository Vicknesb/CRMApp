import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCampaigns } from '../hooks/useCampaigns'
import { cn } from '@/lib/cn'

const TYPE_ICONS: Record<string, string> = {
  EMAIL: '📧', LINKEDIN: '💼', WEBINAR: '🎥', EVENT: '🎪', CONTENT: '📝', SMS: '💬',
}
const STATUS_COLORS: Record<string, string> = {
  DRAFT: 'badge-ghost', ACTIVE: 'badge-success', PAUSED: 'badge-warning', COMPLETED: 'badge-neutral',
}

export function CampaignsListPage(): JSX.Element {
  const [status, setStatus] = useState<string | undefined>()
  const { data, isLoading } = useCampaigns(status ? { status } : undefined)
  const campaigns: any[] = data?.data ?? []

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex gap-2 flex-wrap">
          {['', 'ACTIVE', 'DRAFT', 'PAUSED', 'COMPLETED'].map((s) => (
            <button key={s}
              className={cn('btn btn-sm', status === (s || undefined) ? 'btn-primary' : 'btn-ghost')}
              onClick={() => setStatus(s || undefined)}>
              {s || 'All'}
            </button>
          ))}
        </div>
        <Link to="/campaigns/new" className="btn btn-primary btn-sm">+ New Campaign</Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : campaigns.length === 0 ? (
        <div className="flex flex-col items-center py-20 text-base-content/40">
          <span className="text-4xl mb-2">📣</span>
          <p>No campaigns yet</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {campaigns.map((c) => (
            <Link key={c.id} to={`/campaigns/${c.id}`}
              className="card bg-base-100 border border-base-300 shadow-sm hover:shadow-md transition-shadow">
              <div className="card-body p-4">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{TYPE_ICONS[c.type] ?? '📣'}</span>
                    <h3 className="font-semibold line-clamp-1">{c.name}</h3>
                  </div>
                  <span className={cn('badge badge-sm shrink-0', STATUS_COLORS[c.status] ?? 'badge-ghost')}>
                    {c.status}
                  </span>
                </div>
                <div className="flex items-center justify-between mt-3 text-xs text-base-content/50">
                  <span className="badge badge-outline badge-xs">{c.type}</span>
                  {c.budget && <span>₹{Number(c.budget).toLocaleString('en-IN')}</span>}
                </div>
                {c.startDate && (
                  <p className="text-xs text-base-content/40 mt-1">
                    {new Date(c.startDate).toLocaleDateString('en-IN')}
                    {c.endDate && ` – ${new Date(c.endDate).toLocaleDateString('en-IN')}`}
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
