import { useNavigate, useParams } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { PageShell } from '../../../components/layout/PageShell'
import { Button } from '../../../components/ui/Button'
import { useCreateLead, useUpdateLead, useLead } from '../hooks/useLeads'

const LeadFormSchema = z.object({
  firstName: z.string().min(1, 'Required'),
  lastName: z.string().min(1, 'Required'),
  email: z.string().email('Invalid email'),
  phone: z.string().optional(),
  company: z.string().optional(),
  jobTitle: z.string().optional(),
  source: z.string().default('OTHER'),
  budget: z.coerce.number().optional(),
  notes: z.string().optional(),
})

type LeadFormData = z.infer<typeof LeadFormSchema>

export function LeadFormPage(): JSX.Element {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = !!id
  const { data: existing } = useLead(id ?? '')
  const createLead = useCreateLead()
  const updateLead = useUpdateLead()

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LeadFormData>({
    resolver: zodResolver(LeadFormSchema),
    defaultValues: existing ?? {},
  })

  const onSubmit = async (data: LeadFormData) => {
    if (isEdit) {
      await updateLead.mutateAsync({ id: id!, data })
    } else {
      await createLead.mutateAsync(data)
    }
    navigate('/leads')
  }

  return (
    <PageShell title={isEdit ? 'Edit Lead' : 'New Lead'}>
      <div className="max-w-2xl">
        <form onSubmit={handleSubmit(onSubmit)} className="card bg-base-100 shadow-sm border border-base-300">
          <div className="card-body space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="form-control">
                <label className="label"><span className="label-text">First Name *</span></label>
                <input {...register('firstName')} className="input input-bordered" />
                {errors.firstName && <p className="text-error text-sm">{errors.firstName.message}</p>}
              </div>
              <div className="form-control">
                <label className="label"><span className="label-text">Last Name *</span></label>
                <input {...register('lastName')} className="input input-bordered" />
                {errors.lastName && <p className="text-error text-sm">{errors.lastName.message}</p>}
              </div>
            </div>

            <div className="form-control">
              <label className="label"><span className="label-text">Email *</span></label>
              <input {...register('email')} type="email" className="input input-bordered" />
              {errors.email && <p className="text-error text-sm">{errors.email.message}</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="form-control">
                <label className="label"><span className="label-text">Company</span></label>
                <input {...register('company')} className="input input-bordered" />
              </div>
              <div className="form-control">
                <label className="label"><span className="label-text">Job Title</span></label>
                <input {...register('jobTitle')} className="input input-bordered" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="form-control">
                <label className="label"><span className="label-text">Phone</span></label>
                <input {...register('phone')} className="input input-bordered" />
              </div>
              <div className="form-control">
                <label className="label"><span className="label-text">Source</span></label>
                <select {...register('source')} className="select select-bordered">
                  {['WEBSITE','REFERRAL','LINKEDIN','EMAIL','EVENT','COLD','OTHER'].map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-control">
              <label className="label"><span className="label-text">Budget (₹)</span></label>
              <input {...register('budget')} type="number" className="input input-bordered" />
            </div>

            <div className="form-control">
              <label className="label"><span className="label-text">Notes</span></label>
              <textarea {...register('notes')} className="textarea textarea-bordered" rows={3} />
            </div>

            <div className="flex gap-3 justify-end">
              <Button type="button" variant="ghost" onClick={() => navigate('/leads')}>Cancel</Button>
              <Button type="submit" loading={isSubmitting}>
                {isEdit ? 'Update Lead' : 'Create Lead'}
              </Button>
            </div>
          </div>
        </form>
      </div>
    </PageShell>
  )
}
