import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Button } from '../../../components/ui/Button'

const LoginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password is required'),
  totpCode: z.string().optional(),
})

type LoginForm = z.infer<typeof LoginSchema>

export function LoginPage(): JSX.Element {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [requires2FA, setRequires2FA] = useState(false)
  const [serverError, setServerError] = useState('')

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginForm>({
    resolver: zodResolver(LoginSchema),
  })

  const onSubmit = async (data: LoginForm) => {
    setServerError('')
    try {
      const user = await login(data.email, data.password, data.totpCode)
      if (user.requires2FA) {
        setRequires2FA(true)
        return
      }
      navigate('/', { replace: true })
    } catch (e: any) {
      setServerError(e.message ?? 'Login failed')
    }
  }

  return (
    <div className="min-h-screen bg-base-200 flex items-center justify-center p-4">
      <div className="card w-full max-w-md bg-base-100 shadow-xl">
        <div className="card-body">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold text-brand">CRM</h1>
            <p className="text-base-content/60 mt-1">Ideas2IT Internal CRM</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {!requires2FA ? (
              <>
                <div className="form-control">
                  <label className="label"><span className="label-text">Email</span></label>
                  <input
                    {...register('email')}
                    type="email"
                    className="input input-bordered w-full"
                    placeholder="you@ideas2it.com"
                    autoComplete="email"
                  />
                  {errors.email && <p className="text-error text-sm mt-1">{errors.email.message}</p>}
                </div>

                <div className="form-control">
                  <label className="label"><span className="label-text">Password</span></label>
                  <input
                    {...register('password')}
                    type="password"
                    className="input input-bordered w-full"
                    placeholder="••••••••"
                    autoComplete="current-password"
                  />
                  {errors.password && <p className="text-error text-sm mt-1">{errors.password.message}</p>}
                </div>
              </>
            ) : (
              <div className="form-control">
                <label className="label">
                  <span className="label-text">2FA Code</span>
                  <span className="label-text-alt text-base-content/60">from your authenticator app</span>
                </label>
                <input
                  {...register('totpCode')}
                  type="text"
                  inputMode="numeric"
                  maxLength={6}
                  className="input input-bordered w-full tracking-widest text-center text-2xl"
                  placeholder="000000"
                  autoFocus
                />
                {errors.totpCode && <p className="text-error text-sm mt-1">{errors.totpCode.message}</p>}
              </div>
            )}

            {serverError && (
              <div className="alert alert-error text-sm py-2">{serverError}</div>
            )}

            <Button type="submit" loading={isSubmitting} className="w-full">
              {requires2FA ? 'Verify Code' : 'Sign In'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
