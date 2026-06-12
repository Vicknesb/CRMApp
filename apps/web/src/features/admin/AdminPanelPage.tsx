import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { apiClient } from "../../lib/apiClient";
import { cn } from "../../lib/cn";

type Tab = "users" | "permissions" | "custom-fields" | "workflows" | "audit-log";

const CustomFieldSchema = z.object({
  module: z.string().min(1),
  fieldName: z.string().min(1),
  fieldType: z.enum(["text", "number", "date", "select", "boolean"]),
  label: z.string().min(1),
  options: z.string().optional(),
});

type CustomFieldForm = z.infer<typeof CustomFieldSchema>;

export function AdminPanelPage() {
  const [tab, setTab] = useState<Tab>("users");
  const qc = useQueryClient();

  const usersQ = useQuery({
    queryKey: ["admin-users"],
    queryFn: () => apiClient.get("/admin/users").then(r => r.data),
    enabled: tab === "users",
  });

  const permsQ = useQuery({
    queryKey: ["admin-permissions"],
    queryFn: () => apiClient.get("/admin/permissions").then(r => r.data),
    enabled: tab === "permissions",
  });

  const fieldsQ = useQuery({
    queryKey: ["admin-custom-fields"],
    queryFn: () => apiClient.get("/admin/custom-fields").then(r => r.data),
    enabled: tab === "custom-fields",
  });

  const workflowsQ = useQuery({
    queryKey: ["admin-workflows"],
    queryFn: () => apiClient.get("/admin/workflows").then(r => r.data),
    enabled: tab === "workflows",
  });

  const auditQ = useQuery({
    queryKey: ["admin-audit"],
    queryFn: () => apiClient.get("/admin/audit-logs?limit=50").then(r => r.data),
    enabled: tab === "audit-log",
  });

  const { register, handleSubmit, reset, formState: { errors } } = useForm<CustomFieldForm>({
    resolver: zodResolver(CustomFieldSchema),
  });

  const createField = useMutation({
    mutationFn: (data: CustomFieldForm) =>
      apiClient.post("/admin/custom-fields", {
        ...data,
        options: data.options ? data.options.split(",").map(s => s.trim()) : [],
      }),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ["admin-custom-fields"] }); reset(); },
  });

  const tabs: { id: Tab; label: string }[] = [
    { id: "users", label: "Users" },
    { id: "permissions", label: "Permissions" },
    { id: "custom-fields", label: "Custom Fields" },
    { id: "workflows", label: "Workflows" },
    { id: "audit-log", label: "Audit Log" },
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Admin Panel</h1>

      <div className="tabs tabs-boxed mb-6">
        {tabs.map(t => (
          <button
            key={t.id}
            className={cn("tab", tab === t.id && "tab-active")}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "users" && (
        <div className="overflow-x-auto">
          {usersQ.isLoading && <span className="loading loading-spinner" />}
          <table className="table table-zebra w-full">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Role</th><th>2FA</th><th>Active</th></tr>
            </thead>
            <tbody>
              {(usersQ.data ?? []).map((u: any) => (
                <tr key={u.id}>
                  <td>{u.firstName} {u.lastName}</td>
                  <td>{u.email}</td>
                  <td><span className="badge badge-outline">{u.role}</span></td>
                  <td>{u.isTwoFactorEnabled ? "✓" : "—"}</td>
                  <td>{u.isActive ? <span className="badge badge-success">Active</span> : <span className="badge badge-error">Inactive</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "permissions" && (
        <div className="overflow-x-auto">
          {permsQ.isLoading && <span className="loading loading-spinner" />}
          <table className="table table-zebra w-full">
            <thead><tr><th>Role</th><th>Module</th><th>Actions</th></tr></thead>
            <tbody>
              {(permsQ.data ?? []).map((p: any) => (
                <tr key={p.id}>
                  <td><span className="badge badge-outline">{p.role}</span></td>
                  <td>{p.module}</td>
                  <td>{(p.actions ?? []).join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "custom-fields" && (
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card bg-base-100 shadow">
            <div className="card-body">
              <h2 className="card-title">Add Custom Field</h2>
              <form onSubmit={handleSubmit(d => createField.mutate(d))} className="space-y-3">
                <select className="select select-bordered w-full" {...register("module")}>
                  <option value="">Module</option>
                  {["leads","contacts","accounts","tickets","projects"].map(m => <option key={m} value={m}>{m}</option>)}
                </select>
                <input className="input input-bordered w-full" placeholder="Field name" {...register("fieldName")} />
                <select className="select select-bordered w-full" {...register("fieldType")}>
                  {["text","number","date","select","boolean"].map(t => <option key={t} value={t}>{t}</option>)}
                </select>
                <input className="input input-bordered w-full" placeholder="Label" {...register("label")} />
                <input className="input input-bordered w-full" placeholder="Options (comma-sep, for select)" {...register("options")} />
                <button className="btn btn-primary w-full" type="submit" disabled={createField.isPending}>
                  {createField.isPending ? <span className="loading loading-spinner loading-sm" /> : "Add Field"}
                </button>
              </form>
            </div>
          </div>

          <div className="overflow-x-auto">
            {fieldsQ.isLoading && <span className="loading loading-spinner" />}
            <table className="table table-zebra w-full">
              <thead><tr><th>Module</th><th>Field</th><th>Type</th><th>Label</th></tr></thead>
              <tbody>
                {(fieldsQ.data ?? []).map((f: any) => (
                  <tr key={f.id}>
                    <td>{f.module}</td>
                    <td><code>{f.fieldName}</code></td>
                    <td>{f.fieldType}</td>
                    <td>{f.label}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === "workflows" && (
        <div className="overflow-x-auto">
          {workflowsQ.isLoading && <span className="loading loading-spinner" />}
          <table className="table table-zebra w-full">
            <thead><tr><th>Name</th><th>Module</th><th>Trigger</th><th>Actions</th><th>Active</th></tr></thead>
            <tbody>
              {(workflowsQ.data ?? []).map((w: any) => (
                <tr key={w.id}>
                  <td>{w.name}</td>
                  <td>{w.module}</td>
                  <td>{w.triggerType}</td>
                  <td>{(w.actions ?? []).map((a: any) => a.type).join(", ")}</td>
                  <td>{w.isActive ? <span className="badge badge-success">On</span> : <span className="badge">Off</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {tab === "audit-log" && (
        <div className="overflow-x-auto">
          {auditQ.isLoading && <span className="loading loading-spinner" />}
          <table className="table table-zebra w-full text-sm">
            <thead><tr><th>Time</th><th>User</th><th>Action</th><th>Module</th><th>Record</th></tr></thead>
            <tbody>
              {(auditQ.data ?? []).map((a: any) => (
                <tr key={a.id}>
                  <td className="text-xs text-base-content/60">{new Date(a.createdAt).toLocaleString()}</td>
                  <td>{a.userId}</td>
                  <td><span className="badge badge-outline badge-sm">{a.action}</span></td>
                  <td>{a.module}</td>
                  <td className="font-mono text-xs">{a.recordId ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
