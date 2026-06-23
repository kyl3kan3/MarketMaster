import type { LucideIcon } from "lucide-react";

type MetricCardProps = {
  label: string;
  value: string;
  detail: string;
  icon: LucideIcon;
  tone?: "green" | "amber" | "blue" | "neutral";
};

const toneClass = {
  green: "text-accent border-accent/35 bg-accent/10",
  amber: "text-accent-2 border-accent-2/35 bg-accent-2/10",
  blue: "text-accent-3 border-accent-3/35 bg-accent-3/10",
  neutral: "text-muted border-line bg-surface",
};

export function MetricCard({
  label,
  value,
  detail,
  icon: Icon,
  tone = "neutral",
}: MetricCardProps) {
  return (
    <section className="rounded-lg border border-line bg-surface p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-muted">{label}</p>
          <p className="mt-3 text-3xl font-semibold text-foreground">{value}</p>
        </div>
        <div className={`rounded-md border p-2 ${toneClass[tone]}`}>
          <Icon aria-hidden="true" size={18} />
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-muted">{detail}</p>
    </section>
  );
}
