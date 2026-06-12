import apiClient from "@/lib/apiClient";

export interface Activity {
  id: string;
  type: string;
  subject: string;
  description?: string;
  relatedType?: string;
  relatedId?: string;
  happenedAt: string;
  userId: string;
}

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: string;
  priority: string;
  dueAt?: string;
  assigneeId: string;
  relatedType?: string;
  relatedId?: string;
  createdAt: string;
}

export const activitiesApi = {
  listActivities: (params?: Record<string, unknown>): Promise<{ data: Activity[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/activities", { params }),
  logActivity: (body: Partial<Activity>): Promise<Activity> => apiClient.post("/api/v1/activities", body),
  listTasks: (params?: Record<string, unknown>): Promise<{ data: Task[]; meta: { total: number } }> =>
    apiClient.get("/api/v1/tasks", { params }),
  getTask: (id: string): Promise<Task> => apiClient.get(`/api/v1/tasks/${id}`),
  createTask: (body: Partial<Task>): Promise<Task> => apiClient.post("/api/v1/tasks", body),
  updateTask: (id: string, body: Partial<Task>): Promise<Task> => apiClient.patch(`/api/v1/tasks/${id}`, body),
  deleteTask: (id: string): Promise<void> => apiClient.delete(`/api/v1/tasks/${id}`),
  overdueTask: (params?: Record<string, unknown>): Promise<{ data: Task[] }> =>
    apiClient.get("/api/v1/tasks/overdue", { params }),
};
