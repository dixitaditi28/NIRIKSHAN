import type { AnalysisResult, Lang } from "@/lib/nirikshan";
import { T } from "@/lib/nirikshan";
import { BAND_STYLES } from "./band";
import { cn } from "@/lib/utils";

export function VerdictBanner({
  result,
  lang,
  demo,
  action,
}: {
  result: AnalysisResult;
  lang: Lang;
  demo: boolean;
  action?: React.ReactNode;
}) {
  const style = BAND_STYLES[result.band];
  const Icon = style.icon;
  return (
    <div className={cn("rounded-md border-2 border-l-8 p-5", style.border, style.bg)}>
      <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-4 sm:flex sm:items-center sm:justify-between">
        <div className="flex min-w-0 items-start gap-3">
          <span className={cn("mt-0.5 shrink-0", style.text)}>
            <Icon className="h-8 w-8" aria-hidden />
          </span>
          <div className="min-w-0">
            <p className="text-[0.68rem] font-semibold uppercase tracking-[0.18em] text-muted-foreground">
              {T.verdict[lang]}
            </p>
            <p className={cn("text-xl font-bold sm:text-2xl", style.text)}>{style.label[lang]}</p>
            <p className="mt-1 text-sm text-foreground">{style.headline[lang]}</p>
          </div>
        </div>
        {action ? <div className="shrink-0">{action}</div> : null}
      </div>
      {demo ? (
        <p className="mt-3 rounded-sm border border-border bg-card px-3 py-2 text-xs text-muted-foreground">
          {T.demoNote[lang]}
        </p>
      ) : null}
    </div>
  );
}