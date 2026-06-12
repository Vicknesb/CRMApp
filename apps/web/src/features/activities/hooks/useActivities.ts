import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { activitiesApi } from "../api/activitiesApi";

export const useActivities = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["activities", params], queryFn: () => activitiesApi.listActivities(params) });

export const useTasks = (params?: Record<string, unknown>) =>
  useQuery({ queryKey: ["tasks", params], queryFn: () => activitiesApi.listTasks(params) });

export const useOverdueTasks = (assigneeId?: string) =>
  useQuery({
    queryKey: ["tasks", "overdue", assigneeId],
    queryFn: () => activitiesApi.overdueTask(assigneeId ? { assignee_id: assigneeId } : undefined),
  });

export const useCreateTask = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: activitiesApi.createTask,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tasks"] }),
  });
};

export const useUpdateTask = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: Parameters<typeof activitiesApi.updateTask>[1] }) =>
      activitiesApi.updateTask(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tasks"] }),
  });
};

export const useDeleteTask = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => activitiesApi.deleteTask(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["tasks"] }),
  });
};

export const useLogActivity = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: activitiesApi.logActivity,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["activities"] }),
  });
};
