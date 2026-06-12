import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { kbApi } from "../api/kbApi";

export const useArticles = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["kb", params], queryFn: () => kbApi.list(params) });

export const useArticle = (id: string) =>
  useQuery({ queryKey: ["kb", id], queryFn: () => kbApi.get(id), enabled: !!id });

export const useSuggestArticles = (subject: string) =>
  useQuery({ queryKey: ["kb", "suggest", subject], queryFn: () => kbApi.suggest(subject), enabled: !!subject });

export const useCreateArticle = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: kbApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["kb"] }),
  });
};

export const useUpdateArticle = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: Parameters<typeof kbApi.update>[1] }) =>
      kbApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["kb"] }),
  });
};

export const useRateArticle = () =>
  useMutation({ mutationFn: ({ id, helpful }: { id: string; helpful: boolean }) => kbApi.rate(id, helpful) });
