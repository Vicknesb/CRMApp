import { NavLink } from 'react-router-dom'
import { cn } from '../../lib/cn'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/leads', label: 'Leads', icon: '🎯' },
  { to: '/contacts', label: 'Contacts', icon: '👥' },
  { to: '/accounts', label: 'Accounts', icon: '🏢' },
  { to: '/pipeline', label: 'Pipeline', icon: '💰' },
  { to: '/activities', label: 'Activities', icon: '📅' },
  { to: '/tickets', label: 'Tickets', icon: '🎫' },
  { to: '/projects', label: 'Projects', icon: '📁' },
  { to: '/contracts', label: 'Contracts', icon: '📝' },
  { to: '/invoices', label: 'Invoices', icon: '🧾' },
  { to: '/campaigns', label: 'Campaigns', icon: '📣' },
  { to: '/analytics', label: 'Analytics', icon: '📈' },
]

export function Sidebar(): JSX.Element {
  return (
    <aside className="fixed inset-y-0 left-0 w-64 bg-base-200 border-r border-base-300 flex flex-col z-20">
      <div className="h-16 flex items-center px-6 border-b border-base-300">
        <span className="text-xl font-bold text-brand">CRM</span>
        <span className="ml-2 text-sm text-base-content/60">Ideas2IT</span>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="menu menu-sm gap-1 px-2">
          {NAV_ITEMS.map(({ to, label, icon }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  cn('flex items-center gap-3 rounded-lg', isActive && 'active')
                }
              >
                <span>{icon}</span>
                <span>{label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  )
}
