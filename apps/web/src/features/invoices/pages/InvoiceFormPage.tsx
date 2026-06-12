import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useCreateInvoice } from '../hooks/useInvoices'

const lineItemSchema = z.object({
  description: z.string().min(1, 'Required'),
  quantity: z.number().int().min(1),
  unitPrice: z.string().min(1, 'Required'),
  hsnCode: z.string().optional(),
})

const schema = z.object({
  issueDate: z.string().min(1, 'Required'),
  dueDate: z.string().min(1, 'Required'),
  currency: z.enum(['INR', 'USD']).default('INR'),
  taxRate: z.string().default('18'),
  notes: z.string().optional(),
  lineItems: z.array(lineItemSchema).min(1, 'At least one line item required'),
})

type FormValues = z.infer<typeof schema>

export function InvoiceFormPage(): JSX.Element {
  const navigate = useNavigate()
  const createInvoice = useCreateInvoice()

  const { register, control, handleSubmit, watch, formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { currency: 'INR', taxRate: '18', lineItems: [{ description: '', quantity: 1, unitPrice: '' }] },
  })

  const { fields, append, remove } = useFieldArray({ control, name: 'lineItems' })
  const watchedItems = watch('lineItems')
  const watchedTaxRate = watch('taxRate')

  const subTotal = watchedItems?.reduce((sum, item) => {
    const price = parseFloat(item.unitPrice || '0')
    const qty = item.quantity || 1
    return sum + price * qty
  }, 0) ?? 0
  const taxRate = parseFloat(watchedTaxRate || '18')
  const taxAmount = subTotal * taxRate / 100
  const totalAmount = subTotal + taxAmount

  const onSubmit = async (values: FormValues) => {
    await createInvoice.mutateAsync({
      ...values,
      issueDate: new Date(values.issueDate).toISOString(),
      dueDate: new Date(values.dueDate).toISOString(),
    })
    navigate('/invoices')
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="max-w-3xl mx-auto space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Issue Date *</span></label>
          <input type="date" {...register('issueDate')} className="input input-bordered" />
          {errors.issueDate && <span className="text-error text-sm">{errors.issueDate.message}</span>}
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">Due Date *</span></label>
          <input type="date" {...register('dueDate')} className="input input-bordered" />
          {errors.dueDate && <span className="text-error text-sm">{errors.dueDate.message}</span>}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label"><span className="label-text">Currency</span></label>
          <select {...register('currency')} className="select select-bordered">
            <option value="INR">INR (₹)</option>
            <option value="USD">USD ($)</option>
          </select>
        </div>
        <div className="form-control">
          <label className="label"><span className="label-text">GST / Tax Rate (%)</span></label>
          <input type="number" {...register('taxRate')} className="input input-bordered" />
        </div>
      </div>

      {/* Line items */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold">Line Items</h3>
          <button type="button" className="btn btn-sm btn-ghost"
            onClick={() => append({ description: '', quantity: 1, unitPrice: '' })}>
            + Add Item
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="table table-sm border border-base-300 rounded-lg">
            <thead><tr><th>Description</th><th>Qty</th><th>Unit Price (₹)</th><th>Total</th><th></th></tr></thead>
            <tbody>
              {fields.map((field, idx) => {
                const item = watchedItems?.[idx]
                const lineTotal = (parseFloat(item?.unitPrice || '0') * (item?.quantity || 1))
                return (
                  <tr key={field.id}>
                    <td>
                      <input {...register(`lineItems.${idx}.description`)} className="input input-sm input-bordered w-full" placeholder="Service description" />
                    </td>
                    <td>
                      <input type="number" {...register(`lineItems.${idx}.quantity`, { valueAsNumber: true })} className="input input-sm input-bordered w-16" min={1} />
                    </td>
                    <td>
                      <input type="number" {...register(`lineItems.${idx}.unitPrice`)} className="input input-sm input-bordered w-28" placeholder="0" />
                    </td>
                    <td className="font-medium">₹{lineTotal.toLocaleString('en-IN')}</td>
                    <td>
                      {fields.length > 1 && (
                        <button type="button" className="btn btn-ghost btn-xs text-error" onClick={() => remove(idx)}>✕</button>
                      )}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        {/* Totals */}
        <div className="flex justify-end mt-4">
          <div className="space-y-1 text-sm w-64">
            <div className="flex justify-between"><span>Sub Total</span><span>₹{subTotal.toLocaleString('en-IN')}</span></div>
            <div className="flex justify-between text-base-content/60"><span>GST ({taxRate}%)</span><span>₹{taxAmount.toLocaleString('en-IN')}</span></div>
            <div className="flex justify-between font-bold text-base border-t border-base-300 pt-1">
              <span>Total</span><span>₹{totalAmount.toLocaleString('en-IN')}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="form-control">
        <label className="label"><span className="label-text">Notes</span></label>
        <textarea {...register('notes')} className="textarea textarea-bordered" rows={2} />
      </div>

      <div className="flex gap-3 justify-end">
        <button type="button" className="btn btn-ghost" onClick={() => navigate('/invoices')}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? <span className="loading loading-spinner loading-sm" /> : 'Create Invoice'}
        </button>
      </div>
    </form>
  )
}
