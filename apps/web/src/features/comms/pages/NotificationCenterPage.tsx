import { useState } from 'react'
import { useNotifications, useMarkRead, useMarkAllRead } from '../hooks/useComms'
import { cn } from '@/lib/cn'

const TYPE_ICONS: Record<string, string> = {
  LEAD_ASSIGNED: '🎯', DEAL_WON: '🏆', DEAL_LOST: '😞',
  TICKET_ASSIGNED: '🎫', SLA_BREACH: '🔴', TASK_DUE: '⏰',
  CONTRACT_EXPIRY: '📋', INVOICE_OVERDUE: '💰', MENTION: '💬', SYSTEM: 'ℹ️',
}

export function NotificationCenterPage(): JSX.Element {
  const [unreadOnly, setUnreadOnly] = useState(false)
  const { data, isLoading } = useNotifications(unreadOnly)
  const markRead = useMarkRead()
  const markAllRead = useMarkAllRead()

  const notifications: any[] = data?.data ?? []
  const unreadCount = notifications.filter((n) => !n.readAt).length

  return (
    <div className="max-w-2xl mx-auto space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold">Notifications</h2>
          {unreadCount > 0 && (
            <span className="badge badge-error badge-sm">{unreadCount} unread</span>
          )}
        </div>
        <div className="flex gap-2">
          <label className="label cursor-pointer gap-2">
            <input type="checkbox" className="checkbox checkbox-sm"
              checked={unreadOnly} onChange={(e) => setUnreadOnly(e.target.checked)} />
            <span className="label-text text-sm">Unread only</span>
          </label>
          {unreadCount > 0 && (
            <button className="btn btn-ghost btn-sm" onClick={() => markAllRead.mutate()}>
              Mark all read
            </button>
          )}
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : notifications.length === 0 ? (
        <div className="flex flex-col items-center py-20 text-base-content/40">
          <span className="text-4xl mb-2">🔔</span>
          <p>{unreadOnly ? 'No unread notifications' : 'All caught up!'}</p>
        </div>
      ) : (
        <div className="space-y-2">
          {notifications.map((n) => (
            <div key={n.id}
              className={cn('flex items-start gap-3 p-3 rounded-lg border transition-colors cursor-pointer hover:bg-base-200',
                n.readAt ? 'bg-base-100 border-base-300' : 'bg-primary/5 border-primary/20')}
              onClick={() => !n.readAt && markRead.mutate(n.id)}>
              <span className="text-xl shrink-0 mt-0.5">{TYPE_ICONS[n.type] ?? '🔔'}</span>
              <div className="flex-1 min-w-0">
                <p className={cn('text-sm', !n.readAt && 'font-semibold')}>{n.title}</p>
                {n.body && <p className="text-xs text-base-content/60 mt-0.5 line-clamp-2">{n.body}</p>}
                <p className="text-xs text-base-content/40 mt-1">
                  {new Date(n.createdAt).toLocaleString('en-IN')}
                </p>
              </div>
              {!n.readAt && <span className="w-2 h-2 rounded-full bg-primary shrink-0 mt-2" />}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
