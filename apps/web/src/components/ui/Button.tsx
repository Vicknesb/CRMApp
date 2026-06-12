import { cn } from '../../lib/cn'

type Variant = 'primary' | 'secondary' | 'ghost' | 'error' | 'warning'
type Size = 'xs' | 'sm' | 'md' | 'lg'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  loading?: boolean
}

const VARIANT_MAP: Record<Variant, string> = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  ghost: 'btn-ghost',
  error: 'btn-error',
  warning: 'btn-warning',
}

const SIZE_MAP: Record<Size, string> = {
  xs: 'btn-xs',
  sm: 'btn-sm',
  md: '',
  lg: 'btn-lg',
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading,
  className,
  children,
  disabled,
  ...props
}: ButtonProps): JSX.Element {
  return (
    <button
      className={cn('btn', VARIANT_MAP[variant], SIZE_MAP[size], loading && 'loading', className)}
      disabled={disabled || loading}
      {...props}
    >
      {children}
    </button>
  )
}
