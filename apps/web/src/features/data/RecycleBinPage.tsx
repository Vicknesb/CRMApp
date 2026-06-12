import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../../lib/apiClient";

export function RecycleBinPage() {
  const [module, setModule] = useState("");
  const qc = useQueryClient();

  const binQ = useQuery({
    queryKey: ["recycle-bin", module],
    queryFn: () => apiClient.get(`/data/recycle-bin${module ? `?module=${module}` : ""}`).then(r => r.data),
  });

  const restore = useMutation({
    mutationFn: (id: string) => apiClient.post(`/data/recycle-bin/${id}/restore`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["recycle-bin"] }),
  });

  const purge = useMutation({
    mutationFn: () => apiClient.post("/data/recycle-bin/purge"),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["recycle-bin"] }),
  });

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Recycle Bin</h1>
        <button
          className="btn btn-error btn-outline btn-sm"
          onClick={() => { if (confirm("Purge all expired entries?")) purge.mutate(); }}
          disabled={purge.isPending}
        >
          Purge Expired
        </button>
      </div>

      <div className="flex gap-3 mb-4">
        <select className="select select-bordered select-sm" value={module} onChange={e => setModule(e.target.value)}>
          <option value="">All modules</option>
          {["leads","contacts","accounts","tickets","projects","contracts","invoices"].map(m => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto">
        {binQ.isLoading && <span className="loading loading-spinner" />}
        <table className="table table-zebra w-full">
          <thead>
            <tr><th>Module</th><th>Record ID</th><th>Deleted At</th><th>Purge At</th><th></th></tr>
          </thead>
          <tbody>
            {(binQ.data ?? []).length === 0 && !binQ.isLoading && (
              <tr><td colSpan={5} className="text-center text-base-content/50">Recycle bin is empty</td></tr>
            )}
            {(binQ.data ?? []).map((e: any) => (
              <tr key={e.id}>
                <td><span className="badge badge-outline">{e.module}</span></td>
                <td className="font-mono text-xs">{e.recordId}</td>
                <td className="text-sm">{new Date(e.deletedAt).toLocaleDateString()}</td>
                <td className="text-sm text-warning">{new Date(e.purgeAt).toLocaleDateString()}</td>
                <td>
                  <button
                    className="btn btn-xs btn-primary"
                    onClick={() => restore.mutate(e.id)}
                    disabled={restore.isPending}
                  >
                    Restore
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
