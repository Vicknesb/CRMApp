import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useProjects } from '../hooks/useProjects'
import { cn } from '@/lib/cn'

const STATUS_COLORS: Record<string, string> = {
  PLANNING: 'badge-info',
  ACTIVE: 'badge-success',
  ON_HOLD: 'badge-warning',
  COMPLETED: 'badge-neutral',
  CANCELLED: 'badge-error',
}

export function ProjectsListPage(): JSX.Element {
  const [status, setStatus] = useState<string | undefined>()
  const { data, isLoading } = useProjects(status ? { status } : undefined)
  const projects: any[] = data?.data ?? []

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          {['', 'PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED'].map((s) => (
            <button
              key={s}
              className={cn('btn btn-sm', status === (s || undefined) ? 'btn-primary' : 'btn-ghost')}
              onClick={() => setStatus(s || undefined)}
            >
              {s || 'All'}
            </button>
          ))}
        </div>
        <Link to="/projects/new" className="btn btn-primary btn-sm">+ New Project</Link>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : projects.length === 0 ? (
        <div className="flex flex-col items-center py-20 text-base-content/40">
          <span className="text-4xl mb-2">📋</span>
          <p>No projects yet</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((p) => (
            <Link key={p.id} to={`/projects/${p.id}`}
              className="card bg-base-100 border border-base-300 shadow-sm hover:shadow-md transition-shadow">
              <div className="card-body p-4">
                <div className="flex items-start justify-between gap-2">
                  <h3 className="font-semibold line-clamp-1">{p.name}</h3>
                  <span className={cn('badge badge-sm shrink-0', STATUS_COLORS[p.status] ?? 'badge-ghost')}>
                    {p.status.replace('_', ' ')}
                  </span>
                </div>
                {p.description && (
                  <p className="text-sm text-base-content/60 line-clamp-2">{p.description}</p>
                )}
                <div className="flex items-center justify-between mt-2 text-xs text-base-content/50">
                  {p.budget && (
                    <span>₹{Number(p.budget).toLocaleString('en-IN')}</span>
                  )}
                  {p.endDate && (
                    <span>Due {new Date(p.endDate).toLocaleDateString('en-IN')}</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
