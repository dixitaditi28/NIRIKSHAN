import { useEffect, useRef } from "react";
import { FileUp, X } from "lucide-react";
import type { Lang, Mode } from "@/lib/nirikshan";
import { ACCEPTED, MAX_FILE_MB, T } from "@/lib/nirikshan";

export function InputPanel({
  mode,
  lang,
  text,
  onTextChange,
  file,
  onFileChange,
  onSubmit,
  disabled,
}: {
  mode: Mode;
  lang: Lang;
  text: string;
  onTextChange: (v: string) => void;
  file: File | null;
  onFileChange: (f: File | null) => void;
  onSubmit: () => void;
  disabled?: boolean;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(Math.max(el.scrollHeight, 132), 380)}px`;
  }, [text, mode]);

  if (mode === "text") {
    return (
      <div>
        <label htmlFor="nirikshan-text" className="sr-only">
          {T.engine[lang]}
        </label>
        <textarea
          id="nirikshan-text"
          ref={ref}
          value={text}
          disabled={disabled}
          onChange={(e) => onTextChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSubmit();
            }
          }}
          placeholder={
            lang === "en"
              ? "Paste the SMS, email or WhatsApp message you want checked…"
              : "जिस SMS, ईमेल या व्हाट्सएप संदेश की जाँच करनी है उसे यहाँ चिपकाएँ…"
          }
          className="w-full resize-none rounded-sm border border-border bg-surface-muted p-3 text-sm leading-relaxed text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-60"
        />
        <p className="mt-1.5 text-xs text-muted-foreground">{T.hintEnter[lang]}</p>
      </div>
    );
  }

  const spec = ACCEPTED[mode];

  return (
    <div>
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          if (disabled) return;
          const f = e.dataTransfer.files?.[0];
          if (f) onFileChange(f);
        }}
        className="rounded-sm border border-dashed border-border bg-surface-muted px-4 py-8 text-center"
      >
        <FileUp className="mx-auto h-6 w-6 text-muted-foreground" aria-hidden />
        <p className="mt-2 text-sm font-medium text-foreground">{T.dropzone[lang]}</p>
        <p className="mt-1 text-xs text-muted-foreground">
          {spec.label} · max {MAX_FILE_MB} MB
        </p>
        <input
          ref={inputRef}
          type="file"
          className="sr-only"
          accept={spec.exts.join(",")}
          disabled={disabled}
          onChange={(e) => onFileChange(e.target.files?.[0] ?? null)}
        />
        <button
          type="button"
          disabled={disabled}
          onClick={() => inputRef.current?.click()}
          className="mt-3 inline-flex min-h-11 items-center rounded-sm border border-border bg-card px-4 text-sm font-semibold text-foreground transition-all duration-150 hover:-translate-y-px hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
        >
          {lang === "en" ? "Browse files" : "फ़ाइल चुनें"}
        </button>
      </div>
      {file ? (
        <div className="mt-2 flex items-center justify-between gap-3 rounded-sm border border-border px-3 py-2 text-sm">
          <span className="min-w-0 truncate text-foreground">{file.name}</span>
          <button
            type="button"
            aria-label={lang === "en" ? "Remove file" : "फ़ाइल हटाएँ"}
            onClick={() => onFileChange(null)}
            className="shrink-0 rounded-sm p-1 text-muted-foreground hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <X className="h-4 w-4" aria-hidden />
          </button>
        </div>
      ) : null}
    </div>
  );
}