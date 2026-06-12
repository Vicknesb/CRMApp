import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { pipelineApi, OpportunityCreate, OpportunityUpdate } from "../api/pipelineApi";

export const useOpportunities = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["opportunities", params], queryFn: () => pipelineApi.list(params) });

export const useOpportunity = (id: string) =>
  useQuery({ queryKey: ["opportunities", id], queryFn: () => pipelineApi.get(id), enabled: !!id });

export const useForecast = () =>
  useQuery({ queryKey: ["opportunities", "forecast"], queryFn: () => pipelineApi.forecast() });

export const useCreateOpportunity = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: OpportunityCreate) => pipelineApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["opportunities"] }),
  });
};

export const useUpdateOpportunity = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: OpportunityUpdate }) => pipelineApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["opportunities"] }),
  });
};

export const useMoveStage = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, stageId }: { id: string; stageId: string }) => pipelineApi.moveStage(id, stageId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["opportunities"] }),
  });
};

export const useDeleteOpportunity = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => pipelineApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["opportunities"] }),
  });
};
