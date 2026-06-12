import apiClient from '@/lib/apiClient'

export interface Campaign {
  id: string
  name: string
  type: string
  status: string
  budget?: string
  currency: string
  startDate?: string
  endDate?: string
  createdAt: string
}

export interface CampaignMetricsSummary {
  sent: number
  opens: number
  clicks: number
  conversions: number
  openRate: number
  clickRate: number
  conversionRate: number
}

export const campaignsApi = {
  list: (params?: { status?: string; type?: string }) =>
    apiClient.get('/api/v1/campaigns', { params }),
  get: (id: string) => apiClient.get(`/api/v1/campaigns/${id}`),
  create: (body: Partial<Campaign>) => apiClient.post('/api/v1/campaigns', body),
  update: (id: string, body: Partial<Campaign>) => apiClient.patch(`/api/v1/campaigns/${id}`, body),
  delete: (id: string) => apiClient.delete(`/api/v1/campaigns/${id}`),
  addSegment: (id: string, body: { name: string; filters: Record<string, unknown> }) =>
    apiClient.post(`/api/v1/campaigns/${id}/segments`, body),
  ingestMetric: (id: string, body: { metricKey: string; value: string }) =>
    apiClient.post(`/api/v1/campaigns/${id}/metrics`, body),
  metricsSummary: (id: string): Promise<{ data: CampaignMetricsSummary }> =>
    apiClient.get(`/api/v1/campaigns/${id}/metrics/summary`),
  roi: (id: string) => apiClient.get(`/api/v1/campaigns/${id}/roi`),
}
