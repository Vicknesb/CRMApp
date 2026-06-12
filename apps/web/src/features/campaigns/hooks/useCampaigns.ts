import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { campaignsApi } from '../api/campaignsApi'

export const useCampaigns = (params?: { status?: string; type?: string }) =>
  useQuery({ queryKey: ['campaigns', params], queryFn: () => campaignsApi.list(params) })

export const useCampaign = (id: string) =>
  useQuery({ queryKey: ['campaigns', id], queryFn: () => campaignsApi.get(id), enabled: !!id })

export const useCampaignMetrics = (id: string) =>
  useQuery({ queryKey: ['campaigns', id, 'metrics'], queryFn: () => campaignsApi.metricsSummary(id), enabled: !!id })

export const useCreateCampaign = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: campaignsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['campaigns'] }),
  })
}

export const useUpdateCampaign = (id: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof campaignsApi.update>[1]) => campaignsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['campaigns'] }),
  })
}
