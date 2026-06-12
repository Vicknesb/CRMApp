import { cn } from '../../lib/cn'

type BadgeVariant = 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info'

interface BadgeProps {
  variant?: BadgeVariant
  className?: string
  children: React.ReactNode
}

const VARIANT_MAP: Record<BadgeVariant, string> = {
  default: 'badge',
  primary: 'badge badge-primary',
  secondary: 'badge badge-secondary',
  success: 'badge badge-success',
  warning: 'badge badge-warning',
  error: 'badge badge-error',
  info: 'badge badge-info',
}

export function Badge({ variant = 'default', className, children }: BadgeProps): JSX.Element {
  return <span className={cn(VARIANT_MAP[variant], className)}>{children}</span>
}
