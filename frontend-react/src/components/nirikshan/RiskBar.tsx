import { cn } from "@/lib/utils";

export function RiskBar({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: "danger" | "info" | "success" | "warning";
}) {
  const pct = Math.round(Math.min(Math.max(value, 0), 1) * 100);
  const fill = {
    danger: "bg-danger",
    info: "bg-info",
    success: "bg-success",
    warning: "bg-warning",
  }[tone];
  const text = {
    danger: "text-danger",
    info: "text-info",
    success: "text-success",
    warning: "text-warning",
  }[tone];

  return (
    <div>
      <div className="flex items-baseline justify-between gap-3">
        <span className="text-sm font-medium text-foreground">{label}</span>
        <span className={cn("text-sm font-semibold tabular-nums", text)}>{pct}%</span>
      </div>
      <div
        role="progressbar"
        aria-label={label}
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        className="mt-1.5 h-2 w-full overflow-hidden rounded-full border border-border bg-surface-muted"
      >
        <div className={cn("h-full rounded-full", fill)} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}