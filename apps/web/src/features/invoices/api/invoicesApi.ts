import apiClient from '@/lib/apiClient'

export interface LineItem {
  description: string
  quantity: number
  unitPrice: string
  hsnCode?: string
}

export interface Invoice {
  id: string
  number: string
  status: string
  accountId?: string
  contractId?: string
  totalAmount: string
  subTotal: string
  taxRate: string
  taxAmount: string
  currency: string
  issueDate: string
  dueDate: string
  createdAt: string
}

export const invoicesApi = {
  list: (params?: { status?: string; accountId?: string }) =>
    apiClient.get('/api/v1/invoices', { params }),
  get: (id: string) => apiClient.get(`/api/v1/invoices/${id}`),
  create: (body: { lineItems: LineItem[]; issueDate: string; dueDate: string; taxRate?: string; currency?: string; accountId?: string; contractId?: string; notes?: string }) =>
    apiClient.post('/api/v1/invoices', body),
  update: (id: string, body: Partial<Pick<Invoice, 'status' | 'dueDate'>>) =>
    apiClient.patch(`/api/v1/invoices/${id}`, body),
  delete: (id: string) => apiClient.delete(`/api/v1/invoices/${id}`),
  recordPayment: (id: string, body: { amount: string; method: string; paidAt: string; reference?: string }) =>
    apiClient.post(`/api/v1/invoices/${id}/payments`, body),
  revenue: (period?: string) => apiClient.get('/api/v1/invoices/revenue', { params: { period: period ?? 'monthly' } }),
  aging: () => apiClient.get('/api/v1/invoices/aging'),
}
