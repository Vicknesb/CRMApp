import apiClient from '@/lib/apiClient'

export interface Contract {
  id: string
  number: string
  title: string
  status: string
  accountId?: string
  value: string
  currency: string
  startDate: string
  endDate: string
  autoRenew: boolean
  createdAt: string
}

export const contractsApi = {
  list: (params?: { status?: string; accountId?: string }) =>
    apiClient.get('/api/v1/contracts', { params }),
  get: (id: string) => apiClient.get(`/api/v1/contracts/${id}`),
  create: (body: Partial<Contract>) => apiClient.post('/api/v1/contracts', body),
  update: (id: string, body: Partial<Contract>) => apiClient.patch(`/api/v1/contracts/${id}`, body),
  delete: (id: string) => apiClient.delete(`/api/v1/contracts/${id}`),
  renewals: (days?: number) => apiClient.get('/api/v1/contracts/renewals', { params: { days: days ?? 90 } }),
  addAmendment: (id: string, body: { description: string; effectiveAt: string }) =>
    apiClient.post(`/api/v1/contracts/${id}/amendments`, body),
  requestSignature: (id: string, body: { signerName: string; signerEmail: string; provider?: string }) =>
    apiClient.post(`/api/v1/contracts/${id}/signatures`, body),
}
