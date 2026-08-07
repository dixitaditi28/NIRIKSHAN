import { Check } from "lucide-react";
import type { Band, Lang } from "@/lib/nirikshan";
import { GUIDANCE } from "@/lib/nirikshan";

export function GuidanceBlock({ band, lang }: { band: Band; lang: Lang }) {
  return (
    <ul className="grid gap-2 sm:grid-cols-2">
      {GUIDANCE[band][lang].map((step) => (
        <li
          key={step}
          className="flex items-start gap-2 rounded-sm border border-border bg-surface-muted px-3 py-2 text-sm text-foreground"
        >
          <Check className="mt-0.5 h-4 w-4 shrink-0 text-brand-soft" aria-hidden />
          <span>{step}</span>
        </li>
      ))}
    </ul>
  );
}