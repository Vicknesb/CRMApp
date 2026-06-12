import apiClient from '@/lib/apiClient'

export const analyticsApi = {
  dashboard: (role?: string) => apiClient.get('/api/v1/analytics/dashboard', { params: { role } }),
  listReports: () => apiClient.get('/api/v1/analytics/reports'),
  runReport: (key: string) => apiClient.get(`/api/v1/analytics/reports/${key}`),
  runCustom: (definition: {
    module: string
    fields: string[]
    filters?: Array<{ field: string; operator: string; value: unknown }>
    groupBy?: string
    aggregate?: string
    aggregateField?: string
  }) => apiClient.post('/api/v1/analytics/reports/run', definition),
}
