import { useState } from "react";
import { Link } from "react-router-dom";
import { useAccounts, useDeleteAccount } from "../hooks/useAccounts";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export function AccountsListPage() {
  const [search, setSearch] = useState("");
  const { data, isLoading } = useAccounts(search ? { search } : undefined);
  const deleteAccount = useDeleteAccount();

  const accounts = data?.data ?? [];
  const total = data?.meta?.total ?? 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Accounts <Badge variant="neutral">{total}</Badge></h1>
        <Link to="/accounts/new"><Button>+ Add Account</Button></Link>
      </div>
      <input
        className="input input-bordered w-full max-w-sm"
        placeholder="Search accounts…"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto rounded-box border border-base-300">
          <table className="table table-zebra">
            <thead>
              <tr><th>Name</th><th>Industry</th><th>Type</th><th>Health</th><th /></tr>
            </thead>
            <tbody>
              {accounts.length === 0 ? (
                <tr><td colSpan={5} className="text-center text-base-content/50 py-8">No accounts found.</td></tr>
              ) : accounts.map((a) => (
                <tr key={a.id}>
                  <td>
                    <Link to={`/accounts/${a.id}`} className="font-medium link link-hover">{a.name}</Link>
                  </td>
                  <td>{a.industry ?? "—"}</td>
                  <td>{a.type ?? "—"}</td>
                  <td>
                    {a.healthScore != null ? (
                      <span className={`font-semibold ${a.healthScore >= 70 ? "text-success" : a.healthScore >= 40 ? "text-warning" : "text-error"}`}>
                        {a.healthScore}
                      </span>
                    ) : "—"}
                  </td>
                  <td className="text-right space-x-2">
                    <Link to={`/accounts/${a.id}/edit`}><Button size="sm" variant="ghost">Edit</Button></Link>
                    <Button size="sm" variant="ghost"
                      onClick={() => confirm("Delete this account?") && deleteAccount.mutate(a.id)}>
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
