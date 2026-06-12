import apiClient from '@/lib/apiClient'

export const commsApi = {
  listNotifications: (unread?: boolean) =>
    apiClient.get('/api/v1/notifications', { params: { unread: unread ? 'true' : undefined } }),
  markRead: (id: string) => apiClient.patch(`/api/v1/notifications/${id}/read`, {}),
  markAllRead: () => apiClient.post('/api/v1/notifications/read-all', {}),

  listComments: (relatedType: string, relatedId: string) =>
    apiClient.get('/api/v1/comments', { params: { relatedType, relatedId } }),
  addComment: (body: { content: string; relatedType: string; relatedId: string; parentId?: string }) =>
    apiClient.post('/api/v1/comments', body),
  deleteComment: (id: string) => apiClient.delete(`/api/v1/comments/${id}`),

  listTemplates: () => apiClient.get('/api/v1/email-templates'),
  createTemplate: (body: { name: string; subject: string; body: string; variables?: string[] }) =>
    apiClient.post('/api/v1/email-templates', body),
  previewTemplate: (id: string, variables: Record<string, string>) =>
    apiClient.post(`/api/v1/email-templates/${id}/preview`, variables),
}
