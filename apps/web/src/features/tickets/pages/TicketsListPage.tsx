import { useState } from "react";
import { Link } from "react-router-dom";
import { useTickets, useUpdateTicket } from "../hooks/useTickets";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

const STATUS_CLASS: Record<string, string> = {
  OPEN: "badge-info",
  IN_PROGRESS: "badge-warning",
  WAITING: "badge-ghost",
  RESOLVED: "badge-success",
  CLOSED: "badge-neutral",
};

const PRIORITY_CLASS: Record<string, string> = {
  LOW: "badge-ghost",
  MEDIUM: "badge-info",
  HIGH: "badge-warning",
  CRITICAL: "badge-error",
};

export function TicketsListPage() {
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const { data, isLoading } = useTickets({
    ...(status ? { status } : {}),
    ...(search ? { search } : {}),
  });
  const updateTicket = useUpdateTicket();
  const tickets = data?.data ?? [];
  const total = data?.meta?.total ?? 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Support Tickets <Badge variant="neutral">{total}</Badge></h1>
        <Link to="/tickets/new"><Button>+ New Ticket</Button></Link>
      </div>
      <div className="flex gap-3 flex-wrap">
        <input className="input input-bordered flex-1 min-w-48" placeholder="Search…" value={search}
          onChange={(e) => setSearch(e.target.value)} />
        <select className="select select-bordered" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Statuses</option>
          {["OPEN","IN_PROGRESS","WAITING","RESOLVED","CLOSED"].map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>
      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto rounded-box border border-base-300">
          <table className="table table-zebra">
            <thead><tr><th>#</th><th>Subject</th><th>Priority</th><th>Status</th><th>Channel</th><th /></tr></thead>
            <tbody>
              {tickets.length === 0 ? (
                <tr><td colSpan={6} className="text-center text-base-content/50 py-8">No tickets found.</td></tr>
              ) : tickets.map((t) => (
                <tr key={t.id}>
                  <td className="font-mono text-sm">{t.ticketNumber}</td>
                  <td><Link to={`/tickets/${t.id}`} className="link link-hover font-medium">{t.subject}</Link></td>
                  <td><span className={`badge ${PRIORITY_CLASS[t.priority] ?? ""}`}>{t.priority}</span></td>
                  <td><span className={`badge ${STATUS_CLASS[t.status] ?? ""}`}>{t.status}</span></td>
                  <td>{t.channel}</td>
                  <td className="text-right">
                    {t.status !== "RESOLVED" && (
                      <Button size="sm" variant="ghost"
                        onClick={() => updateTicket.mutate({ id: t.id, body: { status: "RESOLVED" } })}>
                        Resolve
                      </Button>
                    )}
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
