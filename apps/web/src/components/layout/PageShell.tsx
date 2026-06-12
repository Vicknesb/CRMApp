import { Header } from './Header'
import { Sidebar } from './Sidebar'

interface PageShellProps {
  title?: string
  children: React.ReactNode
}

export function PageShell({ title, children }: PageShellProps): JSX.Element {
  return (
    <div className="min-h-screen bg-base-100">
      <Sidebar />
      <Header title={title} />
      <main className="ml-64 pt-16 p-6 min-h-screen overflow-x-hidden">
        {children}
      </main>
    </div>
  )
}
