import type {
  ConnectorStatus,
  TrackerStatus,
  ValidationPhase,
  ValidationTask,
} from "./types";
import { validationPhases } from "./tracker";

export const statusMeta: Record<
  TrackerStatus,
  { label: string; className: string; description: string }
> = {
  not_started: {
    label: "Not started",
    className: "border-line bg-surface text-muted",
    description: "No implementation or execution work has been recorded.",
  },
  ready_for_execution: {
    label: "Ready",
    className: "border-accent-3/35 bg-accent-3/10 text-accent-3",
    description: "The task is prepared and waiting for the real execution step.",
  },
  docs_complete_pending_execution: {
    label: "Docs complete",
    className: "border-accent/35 bg-accent/10 text-accent",
    description: "The repo contains the structure or runbook; live evidence is still pending.",
  },
  blocked_external_account: {
    label: "Account blocked",
    className: "border-accent-2/40 bg-accent-2/10 text-accent-2",
    description: "Requires external credentials, accounts, DNS, or elapsed warmup time.",
  },
  awaiting_real_world_evidence: {
    label: "Needs evidence",
    className: "border-white/20 bg-white/10 text-foreground",
    description: "Requires a real run, metric, URL, screenshot, or human QA note.",
  },
  pass_verified: {
    label: "Pass",
    className: "border-accent/50 bg-accent/15 text-accent",
    description: "Live execution was verified.",
  },
  fallback_verified: {
    label: "Fallback",
    className: "border-accent-3/45 bg-accent-3/10 text-accent-3",
    description: "Manual fallback was tested and accepted.",
  },
  failed_needs_fix: {
    label: "Failed",
    className: "border-danger/45 bg-danger/10 text-danger",
    description: "The task failed and needs remediation.",
  },
  scoped_out: {
    label: "Scoped out",
    className: "border-line bg-surface-strong text-muted",
    description: "The task is intentionally out of scope.",
  },
};

export const connectorStatusMeta: Record<
  ConnectorStatus,
  { label: string; className: string }
> = {
  live: {
    label: "Live",
    className: "border-accent/50 bg-accent/15 text-accent",
  },
  fallback_ready: {
    label: "Fallback ready",
    className: "border-accent-3/45 bg-accent-3/10 text-accent-3",
  },
  needs_credentials: {
    label: "Needs credentials",
    className: "border-accent-2/40 bg-accent-2/10 text-accent-2",
  },
  not_configured: {
    label: "Not configured",
    className: "border-line bg-surface-strong text-muted",
  },
  held_action: {
    label: "Held action",
    className: "border-accent-2/40 bg-accent-2/10 text-accent-2",
  },
  plan_blocked: {
    label: "Plan blocked",
    className: "border-danger/45 bg-danger/10 text-danger",
  },
  auth_blocked: {
    label: "Auth blocked",
    className: "border-danger/45 bg-danger/10 text-danger",
  },
};

export function getAllTasks(phases: ValidationPhase[] = validationPhases) {
  return phases.flatMap((phase) => phase.tasks);
}

export function countTasksByStatus(tasks: ValidationTask[]) {
  return tasks.reduce<Record<TrackerStatus, number>>(
    (counts, task) => {
      counts[task.status] += 1;
      return counts;
    },
    {
      not_started: 0,
      ready_for_execution: 0,
      docs_complete_pending_execution: 0,
      blocked_external_account: 0,
      awaiting_real_world_evidence: 0,
      pass_verified: 0,
      fallback_verified: 0,
      failed_needs_fix: 0,
      scoped_out: 0,
    },
  );
}

export function getSystemCoverage(tasks: ValidationTask[]) {
  const represented = tasks.filter((task) => task.status !== "not_started").length;
  return Math.round((represented / tasks.length) * 100);
}

export function getVerifiedCommercialCount(tasks: ValidationTask[]) {
  return tasks.filter(
    (task) =>
      task.status === "pass_verified" || task.status === "fallback_verified",
  ).length;
}

export function getBlockedCount(tasks: ValidationTask[]) {
  return tasks.filter(
    (task) =>
      task.status === "blocked_external_account" ||
      task.status === "awaiting_real_world_evidence",
  ).length;
}
