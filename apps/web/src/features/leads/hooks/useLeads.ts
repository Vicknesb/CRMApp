import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { leadsApi, type LeadCreate } from '../api/leadsApi'

export const LEADS_KEY = ['leads'] as const

export function useLeads(params?: Record<string, unknown>) {
  return useQuery({
    queryKey: [...LEADS_KEY, params],
    queryFn: () => leadsApi.list(params),
  })
}

export function useLead(id: string) {
  return useQuery({
    queryKey: [...LEADS_KEY, id],
    queryFn: () => leadsApi.get(id),
    enabled: !!id,
  })
}

export function useCreateLead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (data: LeadCreate) => leadsApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: LEADS_KEY }),
  })
}

export function useUpdateLead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<LeadCreate & { status: string }> }) =>
      leadsApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: LEADS_KEY }),
  })
}

export function useDeleteLead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => leadsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: LEADS_KEY }),
  })
}

export function useScoreLead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => leadsApi.score(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: LEADS_KEY }),
  })
}

export function useConvertLead() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: object }) => leadsApi.convert(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: LEADS_KEY }),
  })
}
