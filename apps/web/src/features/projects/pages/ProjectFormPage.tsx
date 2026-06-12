import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateProject, useProject, useUpdateProject } from '../hooks/useProjects'

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
  status: z.enum(['PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED']).default('PLANNING'),
  startDate: z.string().optional(),
  endDate: z.string().optional(),
  budget: z.string().optional(),
  currency: z.enum(['INR', 'USD']).default('INR'),
})

type FormValues = z.infer<typeof schema>

export function ProjectFormPage(): JSX.Element {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = !!id

  const { data: existing } = useProject(id ?? '')
  const createProject = useCreateProject()
  const updateProject = useUpdateProject(id ?? '')

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  })

  useEffect(() => {
    if (existing?.data) {
      const p = existing.data
      reset({
        name: p.name,
        description: p.description ?? '',
        status: p.status,
        startDate: p.startDate?.slice(0, 10),
        endDate: p.endDate?.slice(0, 10),
        budget: p.budget ?? '',
        currency: p.currency,
      })
    }
  }, [existing, reset])

  const onSubmit = async (values: FormValues) => {
    const payload = {
      ...values,
      startDate: values.startDate ? new Date(values.startDate).toISOString() : undefined,
      endDate: values.endDate ? new Date(values.endDate).toISOString() : undefined,
    }
    if (isEdit) {
      await updateProject.mutateAsync(payload)
    } else {
      await createProject.mutateAsync(payload)
    }
    navigate('/projects')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-2xl mx-auto space-y-4">
      <div className="form-control">
        <label className="label"><span className="label-text">Project Name *</span></label>
        <input {...register('name')} className="input input-bordered" placeholder="e.g. CRM Phase 2" />
        {errors.name && <span className="text-error text-sm">{errors.name.message}</span>}
      </div>

      <div className="form-control">
        <label className="label"><span className="label-text">Description</span></label>
        <textarea {...register('description')} className="textarea textarea-bordered" rows={3} />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Status</span></label>
          <select {...register('status')} className="select select-bordered">
            {['PLANNING', 'ACTIVE', 'ON_HOLD', 'COMPLETED', 'CANCELLED'].map((s) => (
              <option key={s} value={s}>{s.replace('_', ' ')}</option>
            ))}
          </select>
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Currency</span></label>
          <select {...register('currency')} className="select select-bordered">
            <option value="INR">INR (₹)</option>
            <option value="USD">USD ($)</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Start Date</span></label>
          <input type="date" {...register('startDate')} className="input input-bordered" />
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">End Date</span></label>
          <input type="date" {...register('endDate')} className="input input-bordered" />
        </div>
      </div>

      <div className="form-control">
        <label className="label"><span className="label-text">Budget (₹)</span></label>
        <input type="number" {...register('budget')} className="input input-bordered" placeholder="e.g. 2500000" />
      </div>

      <div className="flex gap-3 justify-end pt-2">
        <button type="button" className="btn btn-ghost" onClick={() => navigate('/projects')}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? <span className="loading loading-spinner loading-sm" /> : isEdit ? 'Save Changes' : 'Create Project'}
        </button>
      </div>
    </form>
  )
}
