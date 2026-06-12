import { apiClient } from '../../../lib/apiClient'

export interface Lead {
  id: string
  firstName: string
  lastName: string
  email: string
  phone?: string
  company?: string
  jobTitle?: string
  status: string
  source: string
  score: number
  qualStage?: string
  budget?: number
  currency: string
  notes?: string
  ownerId?: string
  assigneeId?: string
  createdAt: string
  updatedAt: string
}

export interface LeadCreate {
  firstName: string
  lastName: string
  email: string
  phone?: string
  company?: string
  jobTitle?: string
  source?: string
  budget?: number
  notes?: string
}

export interface LeadsListResponse {
  items: Lead[]
  total: number
  page: number
  page_size: number
}

export const leadsApi = {
  list: (params?: Record<string, unknown>) =>
    apiClient.get<Lead[]>('/leads', { params }),
  get: (id: string) => apiClient.get<Lead>(`/leads/${id}`),
  create: (data: LeadCreate) => apiClient.post<Lead>('/leads', data),
  update: (id: string, data: Partial<LeadCreate & { status: string }>) =>
    apiClient.patch<Lead>(`/leads/${id}`, data),
  delete: (id: string) => apiClient.delete(`/leads/${id}`),
  score: (id: string) => apiClient.post<{ score: number; delta: number }>(`/leads/${id}/score`),
  assign: (id: string, assigneeId: string) =>
    apiClient.post<Lead>(`/leads/${id}/assign?assignee_id=${assigneeId}`),
  convert: (id: string, data: object) => apiClient.post(`/leads/${id}/convert`, data),
}
