import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { contactsApi, ContactCreate, ContactUpdate } from "../api/contactsApi";

export const useContacts = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["contacts", params], queryFn: () => contactsApi.list(params) });

export const useContact = (id: string) =>
  useQuery({ queryKey: ["contacts", id], queryFn: () => contactsApi.get(id), enabled: !!id });

export const useCreateContact = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ContactCreate) => contactsApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["contacts"] }),
  });
};

export const useUpdateContact = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: ContactUpdate }) => contactsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["contacts"] }),
  });
};

export const useDeleteContact = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => contactsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["contacts"] }),
  });
};
