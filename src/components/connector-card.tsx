import { StatusBadge } from "@/components/status-badge";
import type { Connector } from "@/lib/validation/types";

export function ConnectorCard({ connector }: { connector: Connector }) {
  return (
    <section className="rounded-lg border border-line bg-surface p-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm capitalize text-muted">{connector.category}</p>
          <h2 className="mt-1 text-lg font-semibold">{connector.name}</h2>
        </div>
        <StatusBadge status={connector.status} type="connector" />
      </div>
      <p className="mt-4 text-sm leading-6 text-foreground">
        {connector.actionNeeded}
      </p>
      <dl className="mt-4 space-y-3 text-sm">
        <div>
          <dt className="font-medium text-muted">Live action</dt>
          <dd className="mt-1 leading-6">{connector.liveCapability}</dd>
        </div>
        <div>
          <dt className="font-medium text-muted">Fallback</dt>
          <dd className="mt-1 leading-6">{connector.fallbackBehavior}</dd>
        </div>
        <div>
          <dt className="font-medium text-muted">Access needed</dt>
          <dd className="mt-1 leading-6">{connector.credentialHint}</dd>
        </div>
      </dl>
    </section>
  );
}
