import type { Band, Lang } from "@/lib/nirikshan";
import { BAND_STYLES } from "./band";
import { cn } from "@/lib/utils";

export function ScoreGauge({ score, band, lang }: { score: number; band: Band; lang: Lang }) {
  const style = BAND_STYLES[band];
  const Icon = style.icon;
  const r = 62;
  const c = 2 * Math.PI * r;
  const dash = (Math.min(Math.max(score, 0), 100) / 100) * c;
  return (
    <div className="flex flex-col items-center">
      <div className="relative h-[160px] w-[160px]">
        <svg viewBox="0 0 160 160" className="h-full w-full -rotate-90" aria-hidden>
          <circle cx="80" cy="80" r={r} fill="none" strokeWidth="12" className="stroke-border" />
          <circle
            cx="80"
            cy="80"
            r={r}
            fill="none"
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${c}`}
            className={cn("transition-[stroke-dasharray] duration-500", style.text)}
            stroke="currentColor"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn("text-4xl font-bold tabular-nums leading-none", style.text)}>{score}</span>
          <span className="mt-1 text-xs text-muted-foreground">/100</span>
        </div>
      </div>
      <p className={cn("mt-2 inline-flex items-center gap-1.5 text-sm font-semibold", style.text)}>
        <Icon className="h-4 w-4" aria-hidden />
        {style.label[lang]}
      </p>
    </div>
  );
}