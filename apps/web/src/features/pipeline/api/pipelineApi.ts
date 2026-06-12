import apiClient from "@/lib/apiClient";

export interface Opportunity {
  id: string;
  title: string;
  value: number;
  probability?: number;
  stageId: string;
  accountId?: string;
  contactId?: string;
  ownerId: string;
  expectedCloseDate?: string;
  createdAt: string;
}

export interface OpportunityCreate {
  title: string;
  value: number;
  stageId: string;
  accountId?: string;
  contactId?: string;
  expectedCloseDate?: string;
}

export interface OpportunityUpdate extends Partial<OpportunityCreate> {}

export const pipelineApi = {
  list: (params?: Record<string, unknown>): Promise<{ data: Opportunity[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/opportunities", { params }),
  get: (id: string): Promise<Opportunity> => apiClient.get(`/api/v1/opportunities/${id}`),
  forecast: (): Promise<unknown> => apiClient.get("/api/v1/opportunities/forecast"),
  create: (body: OpportunityCreate): Promise<Opportunity> => apiClient.post("/api/v1/opportunities", body),
  update: (id: string, body: OpportunityUpdate): Promise<Opportunity> =>
    apiClient.patch(`/api/v1/opportunities/${id}`, body),
  moveStage: (id: string, stageId: string): Promise<Opportunity> =>
    apiClient.post(`/api/v1/opportunities/${id}/stage`, { stageId }),
  delete: (id: string): Promise<void> => apiClient.delete(`/api/v1/opportunities/${id}`),
};
