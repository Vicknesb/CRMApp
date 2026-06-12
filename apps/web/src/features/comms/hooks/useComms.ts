import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { commsApi } from '../api/commsApi'

export const useNotifications = (unread?: boolean) =>
  useQuery({ queryKey: ['notifications', unread], queryFn: () => commsApi.listNotifications(unread) })

export const useMarkRead = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: commsApi.markRead,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notifications'] }),
  })
}

export const useMarkAllRead = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: commsApi.markAllRead,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notifications'] }),
  })
}

export const useComments = (relatedType: string, relatedId: string) =>
  useQuery({
    queryKey: ['comments', relatedType, relatedId],
    queryFn: () => commsApi.listComments(relatedType, relatedId),
    enabled: !!relatedType && !!relatedId,
  })

export const useAddComment = (relatedType: string, relatedId: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: commsApi.addComment,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['comments', relatedType, relatedId] }),
  })
}

export const useEmailTemplates = () =>
  useQuery({ queryKey: ['email-templates'], queryFn: commsApi.listTemplates })
