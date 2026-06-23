import { AlertTriangle, ClipboardCheck, RadioTower, ShieldCheck } from "lucide-react";
import { MetricCard } from "@/components/metric-card";
import { PhaseBoard } from "@/components/phase-board";
import { StatusBadge } from "@/components/status-badge";
import {
  connectors,
  constraints,
  validationPhases,
  validationRuns,
} from "@/lib/validation/tracker";
import {
  countTasksByStatus,
  getAllTasks,
  getBlockedCount,
  getSystemCoverage,
  getVerifiedCommercialCount,
} from "@/lib/validation/status";

export default function Home() {
  const tasks = getAllTasks(validationPhases);
  const counts = countTasksByStatus(tasks);
  const coverage = getSystemCoverage(tasks);
  const verifiedCommercial = getVerifiedCommercialCount(tasks);
  const blocked = getBlockedCount(tasks);
  const fallbackReady = connectors.filter(
    (connector) => connector.status === "fallback_ready",
  ).length;
  const liveOrHeld = connectors.filter(
    (connector) =>
      connector.status === "live" || connector.status === "held_action",
  ).length;

  return (
    <div className="space-y-8">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Tracker coverage"
          value={`${coverage}%`}
          detail={`${tasks.length} checklist items have an owner, status, and evidence requirement.`}
          icon={ClipboardCheck}
          tone="green"
        />
        <MetricCard
          label="Can-sell evidence"
          value={`${verifiedCommercial}/${tasks.length}`}
          detail="Read-only connector probes exist; outward publishing and buyer evidence are still pending."
          icon={ShieldCheck}
          tone="amber"
        />
        <MetricCard
          label="Live or held paths"
          value={`${liveOrHeld}/${connectors.length}`}
          detail={`${fallbackReady} social paths are fallback-ready; SEO and GA4 remain blocked.`}
          icon={RadioTower}
          tone="blue"
        />
        <MetricCard
          label="Blocked or pending"
          value={`${blocked}`}
          detail="External accounts, warmup time, live publishing, or human QA are required."
          icon={AlertTriangle}
          tone="amber"
        />
      </section>

      <section className="border-b border-line pb-8">
        <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-medium text-accent">System status</p>
            <h2 className="mt-2 text-3xl font-semibold">
              Validation system complete, sell gate not green.
            </h2>
          </div>
          <StatusBadge status="blocked_external_account" />
        </div>
        <p className="mt-4 max-w-4xl text-base leading-7 text-muted">
          The repo now contains a Vercel-ready validation command center, connector
          status model, fallback runbook, and execution log. The business tracker
          remains blocked until live accounts, real content, publishing proof,
          analytics, and warmup evidence are attached.
        </p>
      </section>

      <section className="space-y-4">
        <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm text-muted">Phase gates</p>
            <h2 className="text-2xl font-semibold">Current readiness map</h2>
          </div>
          <p className="text-sm text-muted">
            {counts.docs_complete_pending_execution} docs-ready /{" "}
            {counts.blocked_external_account} account-blocked /{" "}
            {counts.awaiting_real_world_evidence} evidence-pending
          </p>
        </div>
        <PhaseBoard phases={validationPhases} />
      </section>

      <section className="grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-lg border border-line bg-surface p-5">
          <p className="text-sm text-muted">Next run</p>
          <h2 className="mt-2 text-xl font-semibold">
            {validationRuns[0].name}
          </h2>
          <p className="mt-3 text-sm leading-6 text-muted">
            {validationRuns[0].summary}
          </p>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {validationRuns[0].evidence.map((item) => (
              <div
                key={item}
                className="rounded-md border border-line bg-background px-3 py-3 text-sm text-muted"
              >
                {item}
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-lg border border-line bg-surface p-5">
          <p className="text-sm text-muted">Constraints</p>
          <h2 className="mt-2 text-xl font-semibold">Hard limits</h2>
          <ul className="mt-4 space-y-3">
            {constraints.map((constraint) => (
              <li key={constraint} className="text-sm leading-6 text-muted">
                {constraint}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
