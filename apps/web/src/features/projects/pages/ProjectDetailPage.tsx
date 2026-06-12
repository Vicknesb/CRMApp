import { useParams, Link } from 'react-router-dom'
import { useProject, useProjectMilestones, useProjectTasks } from '../hooks/useProjects'
import { cn } from '@/lib/cn'

const STATUS_COLORS: Record<string, string> = {
  PLANNING: 'badge-info', ACTIVE: 'badge-success',
  ON_HOLD: 'badge-warning', COMPLETED: 'badge-neutral', CANCELLED: 'badge-error',
}
const TASK_COLORS: Record<string, string> = {
  PENDING: 'badge-ghost', IN_PROGRESS: 'badge-info',
  COMPLETED: 'badge-success', CANCELLED: 'badge-error',
}

export function ProjectDetailPage(): JSX.Element {
  const { id } = useParams<{ id: string }>()
  const { data: projectData, isLoading } = useProject(id ?? '')
  const { data: milestonesData } = useProjectMilestones(id ?? '')
  const { data: tasksData } = useProjectTasks(id ?? '')

  const project = projectData?.data
  const milestones: any[] = milestonesData?.data ?? []
  const tasks: any[] = tasksData?.data ?? []

  if (isLoading) return <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
  if (!project) return <div className="text-center py-12 text-error">Project not found</div>

  const completedTasks = tasks.filter(t => t.status === 'COMPLETED').length
  const progressPct = tasks.length ? Math.round((completedTasks / tasks.length) * 100) : 0

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">{project.name}</h1>
          {project.description && <p className="text-base-content/60 mt-1">{project.description}</p>}
        </div>
        <div className="flex items-center gap-2">
          <span className={cn('badge', STATUS_COLORS[project.status] ?? 'badge-ghost')}>
            {project.status.replace('_', ' ')}
          </span>
          <Link to={`/projects/${id}/edit`} className="btn btn-sm btn-ghost">Edit</Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Budget', value: project.budget ? `₹${Number(project.budget).toLocaleString('en-IN')}` : '—' },
          { label: 'Start', value: project.startDate ? new Date(project.startDate).toLocaleDateString('en-IN') : '—' },
          { label: 'End', value: project.endDate ? new Date(project.endDate).toLocaleDateString('en-IN') : '—' },
          { label: 'Progress', value: `${progressPct}%` },
        ].map(({ label, value }) => (
          <div key={label} className="stat bg-base-100 border border-base-300 rounded-box p-3">
            <div className="stat-title text-xs">{label}</div>
            <div className="stat-value text-lg">{value}</div>
          </div>
        ))}
      </div>

      {/* Progress bar */}
      {tasks.length > 0 && (
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span>Task completion</span>
            <span>{completedTasks}/{tasks.length}</span>
          </div>
          <progress className="progress progress-primary w-full" value={progressPct} max={100} />
        </div>
      )}

      {/* Milestones */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Milestones</h2>
        {milestones.length === 0 ? (
          <p className="text-base-content/50 text-sm">No milestones yet</p>
        ) : (
          <div className="space-y-2">
            {milestones.map((m) => (
              <div key={m.id} className="flex items-center gap-3 p-3 bg-base-100 border border-base-300 rounded-lg">
                <span className={cn('w-3 h-3 rounded-full shrink-0', m.completedAt ? 'bg-success' : 'bg-base-300')} />
                <span className={cn('flex-1', m.completedAt && 'line-through text-base-content/40')}>{m.name}</span>
                {m.dueDate && <span className="text-xs text-base-content/50">{new Date(m.dueDate).toLocaleDateString('en-IN')}</span>}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Tasks */}
      <div>
        <h2 className="text-lg font-semibold mb-3">Tasks</h2>
        {tasks.length === 0 ? (
          <p className="text-base-content/50 text-sm">No tasks yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead><tr><th>Title</th><th>Status</th><th>Priority</th><th>Due</th></tr></thead>
              <tbody>
                {tasks.map((t) => (
                  <tr key={t.id}>
                    <td>{t.title}</td>
                    <td><span className={cn('badge badge-sm', TASK_COLORS[t.status] ?? 'badge-ghost')}>{t.status}</span></td>
                    <td>{t.priority}</td>
                    <td>{t.dueAt ? new Date(t.dueAt).toLocaleDateString('en-IN') : '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
