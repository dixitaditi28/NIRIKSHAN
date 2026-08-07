import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { RotateCcw } from "lucide-react";

import {
  ACCEPTED,
  EXAMPLES,
  LOADING_STEPS,
  MAX_FILE_MB,
  T,
  demoResultFor,
  type AnalysisResult,
  type Lang,
  type Mode,
} from "@/lib/nirikshan";
import { BAND_STYLES } from "@/components/nirikshan/band";
import type { Band } from "@/lib/nirikshan";
import { Header } from "@/components/nirikshan/Header";
import { Panel } from "@/components/nirikshan/Panel";
import { ModeTabs } from "@/components/nirikshan/ModeTabs";
import { InputPanel } from "@/components/nirikshan/InputPanel";
import { ExampleChip } from "@/components/nirikshan/ExampleChip";
import { AnalyzeButton } from "@/components/nirikshan/AnalyzeButton";
import { InlineError } from "@/components/nirikshan/InlineError";
import { LoadingStatus } from "@/components/nirikshan/LoadingStatus";
import { VerdictBanner } from "@/components/nirikshan/VerdictBanner";
import { ScoreGauge } from "@/components/nirikshan/ScoreGauge";
import { RiskBar } from "@/components/nirikshan/RiskBar";
import { MatchTable } from "@/components/nirikshan/MatchTable";
import { GuidanceBlock } from "@/components/nirikshan/GuidanceBlock";
import { HelplineNotice } from "@/components/nirikshan/HelplineNotice";
import { cn } from "@/lib/utils";


export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "NIRIKSHAN — Check SEBI Messages for Fraud" },
      {
        name: "description",
        content:
          "Paste a suspicious SMS, email or WhatsApp message and get a trust score, phishing risk and matching official SEBI circulars in seconds.",
      },
      { property: "og:title", content: "NIRIKSHAN — Check SEBI Messages for Fraud" },
      {
        property: "og:description",
        content:
          "Regulatory verification and threat scoring for suspicious investor communications, in English and Hindi.",
      },
    ],
  }),
  component: Index,
});

const BAND_TONE: Record<Band, "success" | "info" | "warning" | "danger"> = {
  "Safe": "success",
  "Low Risk": "info",
  "Medium Risk": "warning",
  "High Risk": "danger",
};
type View = "idle" | "loading" | "results";

function Index() {
  const [dark, setDark] = useState(false);
  const [lang, setLang] = useState<Lang>("en");
  const [mode, setMode] = useState<Mode>("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [view, setView] = useState<View>("idle");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [demo, setDemo] = useState(false);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);

  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  const hasInput = mode === "text" ? text.trim().length > 0 : file !== null;

  function validateFile(f: File): string | null {
    if (mode === "text") return null;
    const spec = ACCEPTED[mode];
    const ok = spec.exts.some((e) => f.name.toLowerCase().endsWith(e));
    if (!ok) {
      return lang === "en"
        ? `Unsupported format. Accepted ${mode} files: ${spec.label}.`
        : `असमर्थित प्रारूप। स्वीकृत फ़ाइलें: ${spec.label}.`;
    }
    if (f.size > MAX_FILE_MB * 1024 * 1024) {
      return lang === "en"
        ? `File is ${(f.size / 1024 / 1024).toFixed(1)} MB. The maximum size is ${MAX_FILE_MB} MB.`
        : `फ़ाइल ${(f.size / 1024 / 1024).toFixed(1)} MB की है। अधिकतम आकार ${MAX_FILE_MB} MB है।`;
    }
    return null;
  }

  async function analyze(payload?: string) {
    const body = payload ?? text;
    if (mode === "text" && body.trim().length === 0) {
      setError(T.emptyInput[lang]);
      return;
    }
    if (mode !== "text") {
      if (!file) {
        setError(T.emptyFile[lang]);
        return;
      }
      const fileError = validateFile(file);
      if (fileError) {
        setError(fileError);
        return;
      }
    }

    setError(null);
    setView("loading");
    const startedAt = Date.now();

    let live: AnalysisResult | null = null;
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/analyze?text=${encodeURIComponent(body)}`,
        {
          method: "GET",
          signal: AbortSignal.timeout(4000),
        }
      );
      if (res.ok) live = (await res.json()) as AnalysisResult;
    } catch {
      live = null;
    }

    const minimum = LOADING_STEPS[lang].length * 700;
    const wait = Math.max(0, minimum - (Date.now() - startedAt));
    timers.current.push(
      setTimeout(() => {
        setDemo(live === null);
        setResult(live ?? demoResultFor(body || (file?.name ?? "")));
        setView("results");
      }, wait),
    );
  }

  function useExample(id: string) {
    const ex = EXAMPLES.find((e) => e.id === id);
    if (!ex) return;
    setMode("text");
    setFile(null);
    setText(ex.text);
    setError(null);
    timers.current.push(setTimeout(() => void analyze(ex.text), 350));
  }

  function reset() {
    setView("idle");
    setResult(null);
    setText("");
    setFile(null);
    setError(null);
    setDemo(false);
  }

  const locked = view === "loading";

  return (
    <div className="min-h-screen bg-background">
      <Header
        dark={dark}
        onToggleDark={() => setDark((d) => !d)}
        lang={lang}
        onToggleLang={() => setLang((l) => (l === "en" ? "hi" : "en"))}
      />

      <main className="mx-auto max-w-[1600px] px-4 py-6 sm:px-6">
        {view !== "results" ? (
          <div className="grid gap-4 lg:grid-cols-[minmax(0,1.55fr)_minmax(0,1fr)] lg:items-start">
            <Panel
              title={T.engine[lang]}
              aside={<span className="hidden sm:inline">{T.tryExample[lang]}</span>}
              bodyClassName="p-0"
            >
              <ModeTabs mode={mode} onChange={setMode} lang={lang} disabled={locked} />
              <div className={cn("space-y-3 p-4", locked && "pointer-events-none opacity-60")}>
                <p className="text-sm text-muted-foreground">{T.tagline[lang]}</p>
                <div className="flex flex-wrap gap-2">
                  {EXAMPLES.map((e) => (
                    <ExampleChip
                      key={e.id}
                      label={e.label[lang]}
                      disabled={locked}
                      onClick={() => useExample(e.id)}
                    />
                  ))}
                </div>
                <InputPanel
                  mode={mode}
                  lang={lang}
                  text={text}
                  onTextChange={(v) => {
                    setText(v);
                    if (error) setError(null);
                  }}
                  file={file}
                  onFileChange={(f) => {
                    setFile(f);
                    setError(f ? validateFile(f) : null);
                  }}
                  onSubmit={() => void analyze()}
                  disabled={locked}
                />
                {error ? <InlineError message={error} /> : null}
                <div className="flex justify-end">
                  <AnalyzeButton
                    onClick={() => void analyze()}
                    disabled={locked || !hasInput}
                    loading={locked}
                    label={locked ? T.analyzing[lang] : T.analyze[lang]}
                  />
                </div>
              </div>
            </Panel>

            <Panel title={lang === "en" ? "Analysis protocol" : "विश्लेषण प्रक्रिया"}>
              {locked ? (
                <LoadingStatus lang={lang} />
              ) : (
                <ol className="space-y-2.5 text-sm text-muted-foreground">
                  {LOADING_STEPS[lang].map((s) => (
                    <li key={s} className="flex items-start gap-2.5">
                      <span className="mt-2 block h-2 w-2 shrink-0 rounded-full bg-border" />
                      <span>{s}</span>
                    </li>
                  ))}
                </ol>
              )}
              <div className="mt-4 border-t border-border pt-3 text-xs leading-relaxed text-muted-foreground">
                {lang === "en"
                  ? "Messages are scored against the SEBI circular reference database. No account, no sign-in, nothing stored."
                  : "संदेशों की तुलना सेबी परिपत्र डेटाबेस से की जाती है। कोई खाता नहीं, कोई साइन-इन नहीं, कुछ भी संग्रहित नहीं।"}
              </div>
            </Panel>
          </div>
        ) : null}

        {view === "results" && result ? (
          <div className="reveal-up space-y-4">
            <VerdictBanner
              result={result}
              lang={lang}
              demo={demo}
              action={
                <button
                  type="button"
                  onClick={reset}
                  className="inline-flex min-h-11 items-center gap-2 rounded-sm bg-accent px-4 text-sm font-semibold text-accent-foreground transition-all duration-150 hover:-translate-y-px hover:brightness-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                >
                  <RotateCcw className="h-4 w-4" aria-hidden />
                  {T.checkAnother[lang]}
                </button>
              }
            />

            <div className="grid gap-4 lg:grid-cols-[minmax(0,0.85fr)_minmax(0,2fr)] lg:items-start">
              <Panel title={T.trustScore[lang]} bodyClassName="p-5">
                <ScoreGauge score={result.trust_score} band={result.band} lang={lang} />
              </Panel>

              <Panel title={T.breakdown[lang]} tone="info">
                <div className="space-y-4">
                  <RiskBar label={T.phishing[lang]} value={result.text_risk} tone="danger" />
                  <RiskBar label={T.authenticity[lang]} value={result.auth_trust} tone="info" />
                  <div className="flex items-center justify-between gap-3 rounded-sm border border-border bg-surface-muted px-3 py-2.5">
                    <span className="text-[0.7rem] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
                      {T.claims[lang]}
                    </span>
                    <span
                      className={cn(
                        "rounded-sm border px-2 py-0.5 text-xs font-bold uppercase tracking-wide",
                        result.claims_sebi_origin
                          ? "border-warning/50 bg-warning/10 text-warning"
                          : "border-border bg-card text-muted-foreground",
                      )}
                    >
                      {result.claims_sebi_origin ? T.yes[lang] : T.no[lang]}
                    </span>
                  </div>
                </div>
              </Panel>
            </div>

            <Panel
              title={T.matched[lang]}
              aside={
                <span className="tabular-nums">
                  {result.matches.length} {lang === "en" ? "found" : "मिले"}
                </span>
              }
            >
              <MatchTable matches={result.matches} lang={lang} />
            </Panel>

            <Panel
  title={`${T.whatToDo[lang]} — ${BAND_STYLES[result.band].label[lang]}`}
  tone={BAND_TONE[result.band]}
>
              <GuidanceBlock band={result.band} lang={lang} />
            </Panel>

            {result.band === "High Risk" ? <HelplineNotice lang={lang} /> : null}
          </div>
        ) : null}

        <footer className="mt-6 border-t border-border pt-4 text-xs text-muted-foreground">
          {lang === "en"
            ? "Research prototype. Analysis is based on available SEBI circular data and is not regulatory advice."
            : "अनुसंधान प्रोटोटाइप। विश्लेषण उपलब्ध सेबी परिपत्र डेटा पर आधारित है और यह नियामक सलाह नहीं है।"}
        </footer>
      </main>
    </div>
  );
}
