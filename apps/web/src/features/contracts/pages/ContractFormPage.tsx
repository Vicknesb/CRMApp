import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useContract, useCreateContract, useUpdateContract } from '../hooks/useContracts'

const schema = z.object({
  title: z.string().min(1, 'Title is required'),
  startDate: z.string().min(1, 'Start date required'),
  endDate: z.string().min(1, 'End date required'),
  value: z.string().min(1, 'Value required'),
  currency: z.enum(['INR', 'USD']).default('INR'),
  terms: z.string().optional(),
  autoRenew: z.boolean().default(false),
  renewalNoticeDays: z.number().int().min(1).max(365).default(30),
})

type FormValues = z.infer<typeof schema>

export function ContractFormPage(): JSX.Element {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const isEdit = !!id

  const { data: existing } = useContract(id ?? '')
  const createContract = useCreateContract()
  const updateContract = useUpdateContract(id ?? '')

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  })

  useEffect(() => {
    if (existing?.data) {
      const c = existing.data
      reset({
        title: c.title,
        startDate: c.startDate?.slice(0, 10),
        endDate: c.endDate?.slice(0, 10),
        value: c.value,
        currency: c.currency as 'INR' | 'USD',
        terms: c.terms ?? '',
        autoRenew: c.autoRenew,
        renewalNoticeDays: c.renewalNoticeDays ?? 30,
      })
    }
  }, [existing, reset])

  const onSubmit = async (values: FormValues) => {
    const payload = {
      ...values,
      startDate: new Date(values.startDate).toISOString(),
      endDate: new Date(values.endDate).toISOString(),
    }
    if (isEdit) {
      await updateContract.mutateAsync(payload)
    } else {
      await createContract.mutateAsync(payload)
    }
    navigate('/contracts')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-2xl mx-auto space-y-4">
      <div className="form-control">
        <label className="label"><span className="label-text">Contract Title *</span></label>
        <input {...register('title')} className="input input-bordered" placeholder="e.g. Annual Support Agreement" />
        {errors.title && <span className="text-error text-sm">{errors.title.message}</span>}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Start Date *</span></label>
          <input type="date" {...register('startDate')} className="input input-bordered" />
          {errors.startDate && <span className="text-error text-sm">{errors.startDate.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">End Date *</span></label>
          <input type="date" {...register('endDate')} className="input input-bordered" />
          {errors.endDate && <span className="text-error text-sm">{errors.endDate.message}</span>}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Value (₹) *</span></label>
          <input type="number" {...register('value')} className="input input-bordered" placeholder="500000" />
          {errors.value && <span className="text-error text-sm">{errors.value.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Currency</span></label>
          <select {...register('currency')} className="select select-bordered">
            <option value="INR">INR (₹)</option>
            <option value="USD">USD ($)</option>
          </select>
        </div>
      </div>

      <div className="form-control">
        <label className="label"><span className="label-text">Terms & Conditions</span></label>
        <textarea {...register('terms')} className="textarea textarea-bordered" rows={4} />
      </div>

      <div className="flex items-center gap-6">
        <label className="label cursor-pointer gap-2">
          <input type="checkbox" {...register('autoRenew')} className="checkbox checkbox-primary" />
          <span className="label-text">Auto-renew</span>
        </label>
        <div className="form-control flex-row items-center gap-2">
          <label className="label"><span className="label-text">Renewal notice (days)</span></label>
          <input type="number" {...register('renewalNoticeDays', { valueAsNumber: true })}
            className="input input-bordered w-24" />
        </div>
      </div>

      <div className="flex gap-3 justify-end pt-2">
        <button type="button" className="btn btn-ghost" onClick={() => navigate('/contracts')}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? <span className="loading loading-spinner loading-sm" /> : isEdit ? 'Save Changes' : 'Create Contract'}
        </button>
      </div>
    </form>
  )
}
