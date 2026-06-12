import apiClient from "@/lib/apiClient";

export interface Article {
  id: string;
  title: string;
  body: string;
  isPublished: boolean;
  views: number;
  categoryId?: string;
  authorId: string;
  createdAt: string;
}

export const kbApi = {
  list: (params?: Record<string, unknown>): Promise<{ data: Article[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/kb/articles", { params }),
  get: (id: string): Promise<Article> => apiClient.get(`/api/v1/kb/articles/${id}`),
  suggest: (subject: string): Promise<{ data: Article[] }> =>
    apiClient.get("/api/v1/kb/articles/suggest", { params: { subject } }),
  create: (body: Partial<Article>): Promise<Article> => apiClient.post("/api/v1/kb/articles", body),
  update: (id: string, body: Partial<Article>): Promise<Article> =>
    apiClient.patch(`/api/v1/kb/articles/${id}`, body),
  delete: (id: string): Promise<void> => apiClient.delete(`/api/v1/kb/articles/${id}`),
  rate: (id: string, helpful: boolean): Promise<unknown> =>
    apiClient.post(`/api/v1/kb/articles/${id}/rate`, { helpful }),
};
