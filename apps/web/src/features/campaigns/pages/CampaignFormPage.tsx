import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateCampaign, useCampaign, useUpdateCampaign } from '../hooks/useCampaigns'

const CAMPAIGN_TYPES = ['EMAIL', 'LINKEDIN', 'WEBINAR', 'EVENT', 'CONTENT', 'SMS']

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  type: z.enum(['EMAIL', 'LINKEDIN', 'WEBINAR', 'EVENT', 'CONTENT', 'SMS']),
  status: z.enum(['DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED']).default('DRAFT'),
  startDate: z.string().optional(),
  endDate: z.string().optional(),
  budget: z.string().optional(),
  currency: z.enum(['INR', 'USD']).default('INR'),
})

type FormValues = z.infer<typeof schema>

export function CampaignFormPage(): JSX.Element {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = !!id

  const { data: existing } = useCampaign(id ?? '')
  const createCampaign = useCreateCampaign()
  const updateCampaign = useUpdateCampaign(id ?? '')

  const { register, handleSubmit, reset, watch, setValue,
    formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { type: 'EMAIL', status: 'DRAFT', currency: 'INR' },
  })

  const selectedType = watch('type')

  useEffect(() => {
    if (existing?.data) {
      const c = existing.data
      reset({
        name: c.name, type: c.type as FormValues['type'],
        status: c.status as FormValues['status'],
        startDate: c.startDate?.slice(0, 10),
        endDate: c.endDate?.slice(0, 10),
        budget: c.budget ?? '', currency: c.currency as 'INR' | 'USD',
      })
    }
  }, [existing, reset])

  const onSubmit = async (values: FormValues) => {
    const payload = {
      ...values,
      startDate: values.startDate ? new Date(values.startDate).toISOString() : undefined,
      endDate: values.endDate ? new Date(values.endDate).toISOString() : undefined,
    }
    if (isEdit) await updateCampaign.mutateAsync(payload)
    else await createCampaign.mutateAsync(payload)
    navigate('/campaigns')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-2xl mx-auto space-y-5">
      <div className="form-control">
        <label className="label"><span className="label-text">Campaign Name *</span></label>
        <input {...register('name')} className="input input-bordered" placeholder="Q3 Email Outreach" />
        {errors.name && <span className="text-error text-sm">{errors.name.message}</span>}
      </div>

      <div>
        <label className="label"><span className="label-text">Campaign Type *</span></label>
        <div className="flex flex-wrap gap-2">
          {CAMPAIGN_TYPES.map((t) => (
            <button key={t} type="button"
              className={`btn btn-sm ${selectedType === t ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setValue('type', t as FormValues['type'])}>
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Status</span></label>
          <select {...register('status')} className="select select-bordered">
            {['DRAFT', 'ACTIVE', 'PAUSED', 'COMPLETED'].map((s) => (
              <option key={s} value={s}>{s}</option>
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
        <input type="number" {...register('budget')} className="input input-bordered" placeholder="e.g. 100000" />
      </div>

      <div className="flex gap-3 justify-end pt-2">
        <button type="button" className="btn btn-ghost" onClick={() => navigate('/campaigns')}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? <span className="loading loading-spinner loading-sm" /> : isEdit ? 'Save Changes' : 'Create Campaign'}
        </button>
      </div>
    </form>
  )
}
