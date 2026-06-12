import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { invoicesApi } from '../api/invoicesApi'

export const useInvoices = (params?: { status?: string }) =>
  useQuery({ queryKey: ['invoices', params], queryFn: () => invoicesApi.list(params) })

export const useInvoice = (id: string) =>
  useQuery({ queryKey: ['invoices', id], queryFn: () => invoicesApi.get(id), enabled: !!id })

export const useCreateInvoice = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: invoicesApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['invoices'] }),
  })
}

export const useRecordPayment = (invoiceId: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof invoicesApi.recordPayment>[1]) =>
      invoicesApi.recordPayment(invoiceId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['invoices', invoiceId] }),
  })
}

export const useRevenueReport = (period?: string) =>
  useQuery({ queryKey: ['invoices', 'revenue', period], queryFn: () => invoicesApi.revenue(period) })

export const useAgingReport = () =>
  useQuery({ queryKey: ['invoices', 'aging'], queryFn: invoicesApi.aging })
