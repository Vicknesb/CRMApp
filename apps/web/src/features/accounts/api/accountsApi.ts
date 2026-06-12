import apiClient from "@/lib/apiClient";

export interface Account {
  id: string;
  name: string;
  industry?: string;
  type?: string;
  website?: string;
  phone?: string;
  annualRevenue?: number;
  employees?: number;
  healthScore?: number;
  createdAt: string;
}

export interface AccountCreate {
  name: string;
  industry?: string;
  type?: string;
  website?: string;
  phone?: string;
  annualRevenue?: number;
  employees?: number;
}

export interface AccountUpdate extends Partial<AccountCreate> {}

export const accountsApi = {
  list: (params?: Record<string, unknown>): Promise<{ data: Account[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/accounts", { params }),
  get: (id: string): Promise<Account> => apiClient.get(`/api/v1/accounts/${id}`),
  get360: (id: string): Promise<unknown> => apiClient.get(`/api/v1/accounts/${id}/360`),
  create: (body: AccountCreate): Promise<Account> => apiClient.post("/api/v1/accounts", body),
  update: (id: string, body: AccountUpdate): Promise<Account> => apiClient.patch(`/api/v1/accounts/${id}`, body),
  delete: (id: string): Promise<void> => apiClient.delete(`/api/v1/accounts/${id}`),
};
