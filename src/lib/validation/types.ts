export type TrackerStatus =
  | "not_started"
  | "ready_for_execution"
  | "docs_complete_pending_execution"
  | "blocked_external_account"
  | "awaiting_real_world_evidence"
  | "pass_verified"
  | "fallback_verified"
  | "failed_needs_fix"
  | "scoped_out";

export type TaskCategory = "repo" | "external" | "human";

export type ConnectorStatus =
  | "live"
  | "fallback_ready"
  | "needs_credentials"
  | "not_configured"
  | "held_action"
  | "plan_blocked"
  | "auth_blocked";

export type ConnectorCategory =
  | "email"
  | "social"
  | "seo"
  | "creative"
  | "analytics"
  | "outbound";

export type PhaseId =
  | "phase-0"
  | "phase-1"
  | "phase-2"
  | "phase-3"
  | "phase-4"
  | "phase-5";

export type ValidationTask = {
  id: string;
  phaseId: PhaseId;
  label: string;
  category: TaskCategory;
  status: TrackerStatus;
  owner: string;
  notes: string;
  evidence: string;
};

export type ValidationPhase = {
  id: PhaseId;
  number: string;
  title: string;
  timeframe: string;
  gate: string;
  gateStatus: "green" | "blocked" | "ready";
  tasks: ValidationTask[];
};

export type Connector = {
  id: string;
  name: string;
  category: ConnectorCategory;
  actionNeeded: string;
  status: ConnectorStatus;
  liveCapability: string;
  fallbackBehavior: string;
  credentialHint: string;
  notes: string;
};

export type ValidationRun = {
  id: string;
  name: string;
  status: "planned" | "running" | "complete";
  summary: string;
  evidence: string[];
  metrics: {
    impressions: number | null;
    clicks: number | null;
    replies: number | null;
    signups: number | null;
  };
};
