import apiClient from '@/lib/apiClient'

export interface Project {
  id: string
  name: string
  description?: string
  status: string
  startDate?: string
  endDate?: string
  budget?: string
  currency: string
  accountId?: string
  createdAt: string
}

export interface ProjectTask {
  id: string
  projectId: string
  title: string
  status: string
  priority: string
  assigneeId?: string
  effortHours?: string
  dueAt?: string
}

export interface Milestone {
  id: string
  projectId: string
  name: string
  dueDate?: string
  completedAt?: string
  order: number
}

export const projectsApi = {
  list: (params?: { status?: string; accountId?: string }) =>
    apiClient.get('/api/v1/projects', { params }),
  get: (id: string) => apiClient.get(`/api/v1/projects/${id}`),
  create: (body: Partial<Project>) => apiClient.post('/api/v1/projects', body),
  update: (id: string, body: Partial<Project>) => apiClient.patch(`/api/v1/projects/${id}`, body),
  delete: (id: string) => apiClient.delete(`/api/v1/projects/${id}`),

  listMilestones: (id: string) => apiClient.get(`/api/v1/projects/${id}/milestones`),
  createMilestone: (id: string, body: Partial<Milestone>) =>
    apiClient.post(`/api/v1/projects/${id}/milestones`, body),

  listTasks: (id: string) => apiClient.get(`/api/v1/projects/${id}/tasks`),
  createTask: (id: string, body: Partial<ProjectTask>) =>
    apiClient.post(`/api/v1/projects/${id}/tasks`, body),
  updateTask: (id: string, taskId: string, body: Partial<ProjectTask>) =>
    apiClient.patch(`/api/v1/projects/${id}/tasks/${taskId}`, body),

  listDocuments: (id: string) => apiClient.get(`/api/v1/projects/${id}/documents`),
  addDocument: (id: string, body: { name: string; url: string; mimeType?: string }) =>
    apiClient.post(`/api/v1/projects/${id}/documents`, body),
}
