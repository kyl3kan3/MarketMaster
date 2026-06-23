import { connectorStatusMeta, statusMeta } from "@/lib/validation/status";
import type { ConnectorStatus, TrackerStatus } from "@/lib/validation/types";

type StatusBadgeProps =
  | {
      status: TrackerStatus;
      type?: "task";
    }
  | {
      status: ConnectorStatus;
      type: "connector";
    };

export function StatusBadge(props: StatusBadgeProps) {
  const meta =
    props.type === "connector"
      ? connectorStatusMeta[props.status]
      : statusMeta[props.status];

  return (
    <span
      className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-medium ${meta.className}`}
    >
      {meta.label}
    </span>
  );
}
