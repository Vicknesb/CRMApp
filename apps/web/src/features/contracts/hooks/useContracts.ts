import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { contractsApi } from '../api/contractsApi'

export const useContracts = (params?: { status?: string }) =>
  useQuery({ queryKey: ['contracts', params], queryFn: () => contractsApi.list(params) })

export const useContract = (id: string) =>
  useQuery({ queryKey: ['contracts', id], queryFn: () => contractsApi.get(id), enabled: !!id })

export const useRenewals = (days?: number) =>
  useQuery({ queryKey: ['contracts', 'renewals', days], queryFn: () => contractsApi.renewals(days) })

export const useCreateContract = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: contractsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['contracts'] }),
  })
}

export const useUpdateContract = (id: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof contractsApi.update>[1]) => contractsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['contracts'] }),
  })
}

export const useSignContract = (contractId: string) => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: Parameters<typeof contractsApi.requestSignature>[1]) =>
      contractsApi.requestSignature(contractId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['contracts', contractId] }),
  })
}
