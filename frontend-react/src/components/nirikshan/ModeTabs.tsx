import { FileAudio, FileVideo, Type } from "lucide-react";
import type { Mode } from "@/lib/nirikshan";
import { cn } from "@/lib/utils";

const TABS: { id: Mode; label: { en: string; hi: string }; icon: typeof Type }[] = [
  { id: "text", label: { en: "Text", hi: "पाठ" }, icon: Type },
  { id: "audio", label: { en: "Audio", hi: "ऑडियो" }, icon: FileAudio },
  { id: "video", label: { en: "Video", hi: "वीडियो" }, icon: FileVideo },
];

export function ModeTabs({
  mode,
  onChange,
  lang,
  disabled,
}: {
  mode: Mode;
  onChange: (m: Mode) => void;
  lang: "en" | "hi";
  disabled?: boolean;
}) {
  return (
    <div role="tablist" aria-label="Input mode" className="flex border-b border-border">
      {TABS.map((t) => {
        const active = t.id === mode;
        const Icon = t.icon;
        return (
          <button
            key={t.id}
            role="tab"
            type="button"
            aria-selected={active}
            disabled={disabled}
            onClick={() => onChange(t.id)}
            className={cn(
              "-mb-px inline-flex items-center gap-2 border-b-2 px-4 py-2.5 text-xs font-semibold uppercase tracking-[0.12em] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50",
              active
                ? "border-accent text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground",
            )}
          >
            <Icon className="h-4 w-4" aria-hidden />
            {t.label[lang]}
          </button>
        );
      })}
    </div>
  );
}