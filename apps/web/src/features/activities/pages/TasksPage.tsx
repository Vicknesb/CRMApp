import { useTasks, useDeleteTask, useUpdateTask } from "../hooks/useActivities";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

const STATUS_COLORS: Record<string, string> = {
  OPEN: "badge-info",
  IN_PROGRESS: "badge-warning",
  COMPLETED: "badge-success",
  CANCELLED: "badge-error",
};

const PRIORITY_COLORS: Record<string, string> = {
  LOW: "badge-ghost",
  MEDIUM: "badge-info",
  HIGH: "badge-warning",
  URGENT: "badge-error",
};

export function TasksPage() {
  const { data, isLoading } = useTasks();
  const deleteTask = useDeleteTask();
  const updateTask = useUpdateTask();

  const tasks = data?.data ?? [];
  const total = data?.meta?.total ?? 0;

  const complete = (id: string) =>
    updateTask.mutate({ id, body: { status: "COMPLETED" as const } });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tasks <Badge variant="neutral">{total}</Badge></h1>
      </div>
      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto rounded-box border border-base-300">
          <table className="table table-zebra">
            <thead>
              <tr><th>Title</th><th>Priority</th><th>Status</th><th>Due</th><th /></tr>
            </thead>
            <tbody>
              {tasks.length === 0 ? (
                <tr><td colSpan={5} className="text-center text-base-content/50 py-8">No tasks.</td></tr>
              ) : tasks.map((t) => (
                <tr key={t.id}>
                  <td className="font-medium">{t.title}</td>
                  <td><span className={`badge ${PRIORITY_COLORS[t.priority] ?? ""}`}>{t.priority}</span></td>
                  <td><span className={`badge ${STATUS_COLORS[t.status] ?? ""}`}>{t.status}</span></td>
                  <td>{t.dueAt ? new Date(t.dueAt).toLocaleDateString("en-IN") : "—"}</td>
                  <td className="text-right space-x-2">
                    {t.status !== "COMPLETED" && (
                      <Button size="sm" variant="ghost" onClick={() => complete(t.id)}>Complete</Button>
                    )}
                    <Button size="sm" variant="ghost"
                      onClick={() => confirm("Delete this task?") && deleteTask.mutate(t.id)}>
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
