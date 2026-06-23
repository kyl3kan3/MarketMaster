import { StatusBadge } from "@/components/status-badge";
import type { ValidationPhase } from "@/lib/validation/types";

const gateClass = {
  green: "border-accent/45 bg-accent/10 text-accent",
  ready: "border-accent-3/40 bg-accent-3/10 text-accent-3",
  blocked: "border-accent-2/40 bg-accent-2/10 text-accent-2",
};

export function PhaseBoard({ phases }: { phases: ValidationPhase[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
      {phases.map((phase) => (
        <section
          key={phase.id}
          className="rounded-lg border border-line bg-surface p-4"
        >
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-sm text-muted">Phase {phase.number}</p>
              <h2 className="mt-1 text-lg font-semibold">{phase.title}</h2>
            </div>
            <span
              className={`rounded-md border px-2.5 py-1 text-xs font-medium ${gateClass[phase.gateStatus]}`}
            >
              {phase.gateStatus}
            </span>
          </div>
          <p className="mt-3 text-sm leading-6 text-muted">{phase.gate}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {Array.from(new Set(phase.tasks.map((task) => task.status))).map(
              (status) => (
                <StatusBadge key={status} status={status} />
              ),
            )}
          </div>
        </section>
      ))}
    </div>
  );
}
