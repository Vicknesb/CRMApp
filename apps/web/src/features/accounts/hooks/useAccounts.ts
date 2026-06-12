import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { accountsApi, AccountCreate, AccountUpdate } from "../api/accountsApi";

export const useAccounts = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["accounts", params], queryFn: () => accountsApi.list(params) });

export const useAccount = (id: string) =>
  useQuery({ queryKey: ["accounts", id], queryFn: () => accountsApi.get(id), enabled: !!id });

export const useAccount360 = (id: string) =>
  useQuery({ queryKey: ["accounts", id, "360"], queryFn: () => accountsApi.get360(id), enabled: !!id });

export const useCreateAccount = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: AccountCreate) => accountsApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["accounts"] }),
  });
};

export const useUpdateAccount = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: AccountUpdate }) => accountsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["accounts"] }),
  });
};

export const useDeleteAccount = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => accountsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["accounts"] }),
  });
};
