import { StatusBadge } from "@/components/status-badge";
import type { ValidationPhase } from "@/lib/validation/types";

export function ValidationTable({ phase }: { phase: ValidationPhase }) {
  return (
    <section className="border-b border-line py-6 last:border-b-0">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm text-muted">
            Phase {phase.number} / {phase.timeframe}
          </p>
          <h2 className="mt-1 text-xl font-semibold">{phase.title}</h2>
        </div>
        <p className="max-w-2xl text-sm leading-6 text-muted">{phase.gate}</p>
      </div>
      <div className="mt-5 overflow-x-auto rounded-lg border border-line">
        <table className="min-w-[860px] w-full border-collapse text-left text-sm">
          <thead className="bg-surface-strong text-muted">
            <tr>
              <th className="px-4 py-3 font-medium">Task</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Owner</th>
              <th className="px-4 py-3 font-medium">Evidence required</th>
            </tr>
          </thead>
          <tbody>
            {phase.tasks.map((task) => (
              <tr key={task.id} className="border-t border-line">
                <td className="px-4 py-4 align-top">
                  <p className="font-medium text-foreground">{task.label}</p>
                  <p className="mt-1 leading-6 text-muted">{task.notes}</p>
                </td>
                <td className="px-4 py-4 align-top">
                  <StatusBadge status={task.status} />
                </td>
                <td className="px-4 py-4 align-top text-muted">{task.owner}</td>
                <td className="px-4 py-4 align-top leading-6 text-muted">
                  {task.evidence}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
