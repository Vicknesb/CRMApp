import { cn } from '../../lib/cn'

interface CardProps {
  className?: string
  children: React.ReactNode
}

export function Card({ className, children }: CardProps): JSX.Element {
  return (
    <div className={cn('card bg-base-100 shadow-sm border border-base-300', className)}>
      <div className="card-body">{children}</div>
    </div>
  )
}

export function CardTitle({ children }: { children: React.ReactNode }): JSX.Element {
  return <h2 className="card-title text-base font-semibold">{children}</h2>
}
