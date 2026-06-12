import { Link } from 'react-router-dom'

interface HeaderProps {
  title?: string
}

export function Header({ title }: HeaderProps): JSX.Element {
  return (
    <header className="fixed top-0 left-64 right-0 h-16 bg-base-100 border-b border-base-300 flex items-center justify-between px-6 z-10">
      {title && <h1 className="text-lg font-semibold">{title}</h1>}
      <div className="ml-auto flex items-center gap-3">
        <Link
          to="/notifications"
          className="btn btn-ghost btn-circle"
          aria-label="Notifications"
        >
          <span className="text-xl">🔔</span>
        </Link>
        <Link
          to="/profile"
          className="btn btn-ghost btn-circle avatar"
          aria-label="Profile"
        >
          <div className="w-8 rounded-full bg-brand text-white flex items-center justify-center text-sm font-bold">
            U
          </div>
        </Link>
      </div>
    </header>
  )
}
