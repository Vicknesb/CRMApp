import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ticketsApi } from "../api/ticketsApi";

export const useTickets = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["tickets", params], queryFn: () => ticketsApi.list(params) });

export const useTicket = (id: string) =>
  useQuery({ queryKey: ["tickets", id], queryFn: () => ticketsApi.get(id), enabled: !!id });

export const useCreateTicket = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ticketsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tickets"] }),
  });
};

export const useUpdateTicket = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: Parameters<typeof ticketsApi.update>[1] }) =>
      ticketsApi.update(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tickets"] }),
  });
};

export const useTicketNotes = (id: string) =>
  useQuery({ queryKey: ["tickets", id, "notes"], queryFn: () => ticketsApi.listNotes(id), enabled: !!id });

export const useAddNote = (ticketId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: { body: string; isInternal: boolean }) => ticketsApi.addNote(ticketId, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tickets", ticketId, "notes"] }),
  });
};
