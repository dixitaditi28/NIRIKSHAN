import { PhoneCall } from "lucide-react";
import type { Lang } from "@/lib/nirikshan";
import { T } from "@/lib/nirikshan";

export function HelplineNotice({ lang }: { lang: Lang }) {
  return (
    <div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3 rounded-md border border-danger/40 bg-danger/10 px-4 py-3 sm:flex sm:justify-between">
      <p className="flex min-w-0 items-start gap-2 text-sm text-foreground">
        <PhoneCall className="mt-0.5 h-4 w-4 shrink-0 text-danger" aria-hidden />
        <span>{T.helpline[lang]}</span>
      </p>
      <a
        href="https://scores.sebi.gov.in"
        target="_blank"
        rel="noreferrer noopener"
        className="shrink-0 text-xs font-semibold text-brand-soft underline-offset-2 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      >
        {T.helplineLink[lang]} →
      </a>
    </div>
  );
}