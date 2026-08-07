import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";
import type { Lang } from "@/lib/nirikshan";
import { LOADING_STEPS } from "@/lib/nirikshan";
import { cn } from "@/lib/utils";

export function LoadingStatus({ lang }: { lang: Lang }) {
  const steps = LOADING_STEPS[lang];
  const [active, setActive] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setActive((i) => (i + 1) % steps.length), 700);
    return () => clearInterval(id);
  }, [steps.length]);

  return (
    <ol aria-live="polite" className="space-y-2.5">
      {steps.map((s, i) => (
        <li key={s} className="flex items-start gap-2.5 text-sm">
          <span className="mt-0.5 shrink-0">
            {i === active ? (
              <Loader2 className="h-4 w-4 animate-spin text-accent" aria-hidden />
            ) : (
              <span
                className={cn(
                  "block h-2 w-2 translate-y-1 rounded-full",
                  i < active ? "bg-brand-soft" : "bg-border",
                )}
              />
            )}
          </span>
          <span className={i === active ? "font-semibold text-foreground" : "text-muted-foreground"}>
            {s}
          </span>
        </li>
      ))}
    </ol>
  );
}