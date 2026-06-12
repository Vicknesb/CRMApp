import apiClient from "@/lib/apiClient";

export interface Contact {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  title?: string;
  department?: string;
  isPrimary: boolean;
  createdAt: string;
}

export interface ContactCreate {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  title?: string;
  department?: string;
  accountId?: string;
}

export interface ContactUpdate extends Partial<ContactCreate> {}

export const contactsApi = {
  list: (params?: Record<string, unknown>): Promise<{ data: Contact[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/contacts", { params }),
  get: (id: string): Promise<Contact> => apiClient.get(`/api/v1/contacts/${id}`),
  create: (body: ContactCreate): Promise<Contact> => apiClient.post("/api/v1/contacts", body),
  update: (id: string, body: ContactUpdate): Promise<Contact> => apiClient.patch(`/api/v1/contacts/${id}`, body),
  delete: (id: string): Promise<void> => apiClient.delete(`/api/v1/contacts/${id}`),
};
