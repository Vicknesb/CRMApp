import apiClient from "@/lib/apiClient";

export interface Ticket {
  id: string;
  ticketNumber: string;
  subject: string;
  description?: string;
  status: string;
  priority: string;
  channel: string;
  accountId?: string;
  contactId?: string;
  assigneeId?: string;
  reporterId: string;
  resolvedAt?: string;
  createdAt: string;
}

export interface TicketNote {
  id: string;
  ticketId: string;
  body: string;
  isInternal: boolean;
  authorId: string;
  createdAt: string;
}

export const ticketsApi = {
  list: (params?: Record<string, unknown>): Promise<{ data: Ticket[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/tickets", { params }),
  get: (id: string): Promise<Ticket> => apiClient.get(`/api/v1/tickets/${id}`),
  create: (body: Partial<Ticket>): Promise<Ticket> => apiClient.post("/api/v1/tickets", body),
  update: (id: string, body: Partial<Ticket>): Promise<Ticket> =>
    apiClient.patch(`/api/v1/tickets/${id}`, body),
  delete: (id: string): Promise<void> => apiClient.delete(`/api/v1/tickets/${id}`),
  listNotes: (id: string): Promise<{ data: TicketNote[] }> =>
    apiClient.get(`/api/v1/tickets/${id}/notes`),
  addNote: (id: string, body: { body: string; isInternal: boolean }): Promise<TicketNote> =>
    apiClient.post(`/api/v1/tickets/${id}/notes`, body),
};
