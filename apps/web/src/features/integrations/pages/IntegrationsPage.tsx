import { useConnectors, useDisconnect, useSyncCalendar } from "../hooks/useIntegrations";
import { PROVIDERS } from "../api/integrationsApi";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export function IntegrationsPage() {
  const { data, isLoading } = useConnectors();
  const disconnect = useDisconnect();
  const syncCalendar = useSyncCalendar();

  const connectors = data?.data ?? [];
  const activeMap = Object.fromEntries(connectors.map((c) => [c.provider, c]));

  const categories = [...new Set(PROVIDERS.map((p) => p.category))];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Integrations</h1>
        <Button size="sm" variant="ghost" onClick={() => syncCalendar.mutate()}>
          Sync Calendar
        </Button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><span className="loading loading-spinner loading-lg" /></div>
      ) : categories.map((cat) => (
        <div key={cat}>
          <h2 className="text-sm font-semibold text-base-content/60 uppercase tracking-wider mb-3">{cat}</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {PROVIDERS.filter((p) => p.category === cat).map((provider) => {
              const conn = activeMap[provider.key];
              const isActive = conn?.isActive;
              return (
                <div key={provider.key} className="card bg-base-100 border border-base-300 shadow-sm">
                  <div className="card-body p-4 flex flex-row items-center gap-4">
                    <span className="text-3xl">{provider.icon}</span>
                    <div className="flex-1">
                      <div className="font-semibold">{provider.label}</div>
                      <div className="text-xs text-base-content/50">
                        {isActive
                          ? `Connected ${new Date(conn.connectedAt).toLocaleDateString("en-IN")}`
                          : "Not connected"}
                      </div>
                    </div>
                    {isActive ? (
                      <Button size="sm" variant="ghost"
                        onClick={() => confirm(`Disconnect ${provider.label}?`) &&
                          disconnect.mutate(provider.key)}>
                        Disconnect
                      </Button>
                    ) : (
                      <Badge variant="neutral">Connect</Badge>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
