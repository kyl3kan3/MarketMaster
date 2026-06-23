import { FileCheck2 } from "lucide-react";
import { StatusBadge } from "@/components/status-badge";
import {
  connectors,
  validationPhases,
  validationRuns,
} from "@/lib/validation/tracker";
import { getAllTasks, getBlockedCount } from "@/lib/validation/status";

export default function ReportsPage() {
  const tasks = getAllTasks(validationPhases);
  const blocked = getBlockedCount(tasks);
  const blockedConnectors = connectors.filter(
    (connector) =>
      connector.status === "needs_credentials" ||
      connector.status === "not_configured" ||
      connector.status === "plan_blocked" ||
      connector.status === "auth_blocked",
  );

  return (
    <div className="space-y-7">
      <section className="border-b border-line pb-6">
        <p className="text-sm font-medium text-accent-2">Readout</p>
        <h1 className="mt-2 text-3xl font-semibold">
          Validation completion report
        </h1>
        <p className="mt-4 max-w-4xl text-base leading-7 text-muted">
          This report is ready to export or paste into an operating note after
          live execution evidence is collected.
        </p>
      </section>

      <section className="rounded-lg border border-line bg-surface p-5">
        <div className="flex items-start gap-3">
          <div className="rounded-md border border-accent/35 bg-accent/10 p-2 text-accent">
            <FileCheck2 aria-hidden="true" size={20} />
          </div>
          <div>
            <h2 className="text-xl font-semibold">
              Repo implementation complete
            </h2>
            <p className="mt-2 text-sm leading-6 text-muted">
              Next.js dashboard, connector matrix, fallback documentation,
              execution log, and tracker status model are implemented.
            </p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-line bg-surface p-4">
          <p className="text-sm text-muted">Blocked tasks</p>
          <p className="mt-3 text-3xl font-semibold">{blocked}</p>
        </div>
        <div className="rounded-lg border border-line bg-surface p-4">
          <p className="text-sm text-muted">Blocked connectors</p>
          <p className="mt-3 text-3xl font-semibold">
            {blockedConnectors.length}
          </p>
        </div>
        <div className="rounded-lg border border-line bg-surface p-4">
          <p className="text-sm text-muted">Live dogfood runs</p>
          <p className="mt-3 text-3xl font-semibold">0</p>
        </div>
      </section>

      <section className="grid gap-5 lg:grid-cols-2">
        <div className="rounded-lg border border-line bg-surface p-5">
          <h2 className="text-xl font-semibold">Can-sell gate</h2>
          <div className="mt-4">
            <StatusBadge status="blocked_external_account" />
          </div>
          <p className="mt-4 text-sm leading-6 text-muted">
            The readiness checklist is intentionally blocked until live email,
            social publishing, subscriber capture, measurement, copy QA, and
            outbound warmup evidence are recorded.
          </p>
        </div>
        <div className="rounded-lg border border-line bg-surface p-5">
          <h2 className="text-xl font-semibold">Next evidence packet</h2>
          <ul className="mt-4 space-y-3">
            {validationRuns[0].evidence.map((item) => (
              <li key={item} className="text-sm leading-6 text-muted">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
