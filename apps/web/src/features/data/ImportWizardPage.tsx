import { useState, useRef } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiClient } from "../../lib/apiClient";

const MODULES = ["leads", "contacts", "accounts"];
const FIELD_MAP: Record<string, string[]> = {
  leads: ["firstName", "lastName", "email", "phone", "company", "source"],
  contacts: ["firstName", "lastName", "email", "phone"],
  accounts: ["name", "industry", "website", "phone"],
};

interface Mapping { sourceColumn: string; targetField: string }

export function ImportWizardPage() {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [module, setModule] = useState("leads");
  const [file, setFile] = useState<File | null>(null);
  const [headers, setHeaders] = useState<string[]>([]);
  const [mappings, setMappings] = useState<Mapping[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  const importMut = useMutation({
    mutationFn: async () => {
      const fd = new FormData();
      fd.append("module", module);
      fd.append("mappings", JSON.stringify(mappings.filter(m => m.targetField)));
      fd.append("file", file!);
      return apiClient.post("/data/import", fd, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data);
    },
    onSuccess: () => setStep(3),
  });

  function handleFile(f: File) {
    setFile(f);
    const reader = new FileReader();
    reader.onload = e => {
      const firstLine = (e.target?.result as string).split("\n")[0];
      const cols = firstLine.split(",").map(s => s.replace(/"/g, "").trim());
      setHeaders(cols);
      setMappings(cols.map(c => ({ sourceColumn: c, targetField: "" })));
      setStep(2);
    };
    reader.readAsText(f);
  }

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Import Data</h1>

      <ul className="steps mb-8 w-full">
        <li className={`step ${step >= 1 ? "step-primary" : ""}`}>Upload File</li>
        <li className={`step ${step >= 2 ? "step-primary" : ""}`}>Map Fields</li>
        <li className={`step ${step >= 3 ? "step-primary" : ""}`}>Done</li>
      </ul>

      {step === 1 && (
        <div className="card bg-base-100 shadow">
          <div className="card-body space-y-4">
            <div className="form-control">
              <label className="label"><span className="label-text">Module</span></label>
              <select className="select select-bordered w-full" value={module} onChange={e => setModule(e.target.value)}>
                {MODULES.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            <div
              className="border-2 border-dashed border-base-300 rounded-lg p-10 text-center cursor-pointer hover:border-primary transition-colors"
              onClick={() => fileRef.current?.click()}
              onDragOver={e => e.preventDefault()}
              onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleFile(f); }}
            >
              <p className="text-base-content/60">Drop a CSV file here or click to browse</p>
              <input ref={fileRef} type="file" accept=".csv" className="hidden" onChange={e => { const f = e.target.files?.[0]; if (f) handleFile(f); }} />
            </div>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="card bg-base-100 shadow">
          <div className="card-body">
            <h2 className="card-title">Map columns from <span className="text-primary">{file?.name}</span></h2>
            <table className="table w-full">
              <thead><tr><th>CSV Column</th><th>CRM Field</th></tr></thead>
              <tbody>
                {mappings.map((m, i) => (
                  <tr key={m.sourceColumn}>
                    <td><code>{m.sourceColumn}</code></td>
                    <td>
                      <select
                        className="select select-bordered select-sm w-full"
                        value={m.targetField}
                        onChange={e => setMappings(prev => prev.map((p, j) => j === i ? { ...p, targetField: e.target.value } : p))}
                      >
                        <option value="">— skip —</option>
                        {(FIELD_MAP[module] ?? []).map(f => <option key={f} value={f}>{f}</option>)}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="flex gap-3 mt-4">
              <button className="btn btn-ghost" onClick={() => setStep(1)}>Back</button>
              <button className="btn btn-primary" onClick={() => importMut.mutate()} disabled={importMut.isPending}>
                {importMut.isPending ? <span className="loading loading-spinner loading-sm" /> : "Import"}
              </button>
            </div>
          </div>
        </div>
      )}

      {step === 3 && importMut.data && (
        <div className="card bg-base-100 shadow">
          <div className="card-body text-center space-y-3">
            <div className="text-5xl">✓</div>
            <h2 className="text-xl font-semibold">Import Complete</h2>
            <div className="stats stats-horizontal">
              <div className="stat"><div className="stat-title">Total</div><div className="stat-value">{importMut.data.total}</div></div>
              <div className="stat"><div className="stat-title">Imported</div><div className="stat-value text-success">{importMut.data.imported}</div></div>
              <div className="stat"><div className="stat-title">Errors</div><div className="stat-value text-error">{importMut.data.errors}</div></div>
            </div>
            {importMut.data.errorRows?.length > 0 && (
              <div className="overflow-x-auto text-left">
                <p className="text-sm font-semibold mb-1">Error details:</p>
                <table className="table table-xs">
                  <thead><tr><th>Row</th><th>Error</th></tr></thead>
                  <tbody>{importMut.data.errorRows.map((e: any) => <tr key={e.row}><td>{e.row}</td><td>{e.error}</td></tr>)}</tbody>
                </table>
              </div>
            )}
            <button className="btn btn-primary" onClick={() => { setStep(1); setFile(null); setHeaders([]); setMappings([]); }}>Import Another</button>
          </div>
        </div>
      )}
    </div>
  );
}
