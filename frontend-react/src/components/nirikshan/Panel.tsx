import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

type Tone = "neutral" | "info" | "danger" | "warning" | "success";

const TONE_STYLES: Record<Tone, { header: string; title: string; border: string }> = {
  neutral: {
    header: "bg-surface-muted",
    title: "text-muted-foreground",
    border: "border-border",
  },
  info: {
    header: "bg-blue-50 dark:bg-blue-950/30",
    title: "text-blue-700 dark:text-blue-300",
    border: "border-border",
  },
  danger: {
    header: "bg-red-50 dark:bg-red-950/30",
    title: "text-red-700 dark:text-red-300",
    border: "border-red-200 dark:border-red-900",
  },
  warning: {
    header: "bg-amber-50 dark:bg-amber-950/30",
    title: "text-amber-700 dark:text-amber-300",
    border: "border-amber-200 dark:border-amber-900",
  },
  success: {
    header: "bg-green-50 dark:bg-green-950/30",
    title: "text-green-700 dark:text-green-300",
    border: "border-green-200 dark:border-green-900",
  },
};

export function Panel({
  title,
  aside,
  children,
  className,
  bodyClassName,
  tone = "neutral",
}: {
  title?: ReactNode;
  aside?: ReactNode;
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
  tone?: Tone;
}) {
  const t = TONE_STYLES[tone];
  return (
    <section className={cn("border-2 bg-card rounded-md overflow-hidden shadow-sm", t.border, className)}>
      {title ? (
        <header
          className={cn(
            "grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3 border-b px-4 py-3",
            t.border,
            t.header
          )}
        >
          <h2 className={cn("truncate text-sm font-bold uppercase tracking-[0.1em]", t.title)}>
            {title}
          </h2>
          {aside ? <div className="shrink-0 text-xs text-muted-foreground">{aside}</div> : null}
        </header>
      ) : null}
      <div className={cn("p-4", bodyClassName)}>{children}</div>
    </section>
  );
}