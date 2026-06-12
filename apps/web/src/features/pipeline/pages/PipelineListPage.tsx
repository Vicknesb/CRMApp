import { useState } from "react";
import { Link } from "react-router-dom";
import { useOpportunities, useDeleteOpportunity } from "../hooks/usePipeline";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export function PipelineListPage() {
  const [stageId, setStageId] = useState("");
  const { data, isLoading } = useOpportunities(stageId ? { stage_id: stageId } : undefined);
  const deleteOpp = useDeleteOpportunity();

  const opportunities = data?.data ?? [];
  const total = data?.meta?.total ?? 0;

  const formatINR = (v: number) =>
    v >= 10000000 ? `₹${(v / 10000000).toFixed(2)}Cr` : v >= 100000 ? `₹${(v / 100000).toFixed(1)}L` : `₹${v.toLocaleString("en-IN")}`;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Pipeline <Badge variant="neutral">{total}</Badge></h1>
        <Link to="/pipeline/new"><Button>+ Add Opportunity</Button></Link>
      </div>
      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : (
        <div className="overflow-x-auto rounded-box border border-base-300">
          <table className="table table-zebra">
            <thead>
              <tr><th>Title</th><th>Value</th><th>Probability</th><th>Expected Close</th><th /></tr>
            </thead>
            <tbody>
              {opportunities.length === 0 ? (
                <tr><td colSpan={5} className="text-center text-base-content/50 py-8">No opportunities found.</td></tr>
              ) : opportunities.map((o) => (
                <tr key={o.id}>
                  <td>
                    <Link to={`/pipeline/${o.id}`} className="font-medium link link-hover">{o.title}</Link>
                  </td>
                  <td className="font-mono">{formatINR(o.value)}</td>
                  <td>{o.probability != null ? `${o.probability}%` : "—"}</td>
                  <td>{o.expectedCloseDate ? new Date(o.expectedCloseDate).toLocaleDateString("en-IN") : "—"}</td>
                  <td className="text-right space-x-2">
                    <Link to={`/pipeline/${o.id}/edit`}><Button size="sm" variant="ghost">Edit</Button></Link>
                    <Button size="sm" variant="ghost"
                      onClick={() => confirm("Delete this opportunity?") && deleteOpp.mutate(o.id)}>
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
