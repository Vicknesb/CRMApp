import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { integrationsApi } from "../api/integrationsApi";

export const useConnectors = () =>
  useQuery({ queryKey: ["integrations"], queryFn: () => integrationsApi.list() });

export const useConnect = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: integrationsApi.connect,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["integrations"] }),
  });
};

export const useDisconnect = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (provider: string) => integrationsApi.disconnect(provider),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["integrations"] }),
  });
};

export const useSyncCalendar = () =>
  useMutation({ mutationFn: integrationsApi.syncCalendar });
