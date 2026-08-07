import { Languages, Moon, Sun } from "lucide-react";
import type { Lang } from "@/lib/nirikshan";

export function Header({
  dark,
  onToggleDark,
  lang,
  onToggleLang,
}: {
  dark: boolean;
  onToggleDark: () => void;
  lang: Lang;
  onToggleLang: () => void;
}) {
  return (
    <header className="sticky top-0 z-20 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/80">
      <div className="mx-auto grid max-w-[1600px] grid-cols-[minmax(0,1fr)_auto] items-center gap-4 px-4 py-3 sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <span
            aria-hidden
            className="grid h-9 w-9 shrink-0 place-items-center rounded-sm bg-primary font-semibold text-primary-foreground"
          >
            नि
          </span>
          <div className="min-w-0">
            <p className="truncate text-lg font-bold tracking-[0.16em] text-foreground">NIRIKSHAN</p>
            <p className="truncate text-[0.68rem] uppercase tracking-[0.18em] text-muted-foreground">
              Regulatory communication verification
            </p>
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={onToggleLang}
            aria-label={lang === "en" ? "Switch to Hindi" : "अंग्रेज़ी में बदलें"}
            className="inline-flex min-h-11 items-center gap-2 rounded-sm border border-border px-3 text-xs font-semibold uppercase tracking-[0.12em] text-foreground transition-colors duration-150 hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <Languages className="h-4 w-4" aria-hidden />
            {lang === "en" ? "EN" : "हिं"}
          </button>
          <button
            type="button"
            onClick={onToggleDark}
            aria-label={dark ? "Switch to light theme" : "Switch to dark theme"}
            className="inline-flex min-h-11 min-w-11 items-center justify-center rounded-sm border border-border text-foreground transition-colors duration-150 hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            {dark ? <Sun className="h-4 w-4" aria-hidden /> : <Moon className="h-4 w-4" aria-hidden />}
          </button>
        </div>
      </div>
      <div className="h-0.5 w-full bg-accent" />
    </header>
  );
}