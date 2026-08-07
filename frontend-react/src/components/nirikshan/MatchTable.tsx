import { ExternalLink } from "lucide-react";
import type { Lang, Match } from "@/lib/nirikshan";
import { T } from "@/lib/nirikshan";
import { EmptyState } from "./EmptyState";

export function MatchTable({ matches, lang }: { matches: Match[]; lang: Lang }) {
  if (matches.length === 0) {
    return <EmptyState title={T.noMatch[lang]} body={T.noMatchBody[lang]} />;
  }

  return (
    <>
      {/* stacked cards below ~600px */}
      <ul className="space-y-2 min-[600px]:hidden">
        {matches.map((m) => (
          <li key={m.source_url + m.title} className="rounded-sm border border-border p-3">
            <a
              href={m.source_url}
              target="_blank"
              rel="noreferrer noopener"
              className="inline-flex items-start gap-1.5 text-sm font-medium text-brand-soft underline-offset-2 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {m.title}
              <ExternalLink className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
            </a>
            <div className="mt-2 flex justify-between text-xs text-muted-foreground">
              <span>{m.date}</span>
              <span className="font-semibold tabular-nums text-foreground">
                {Math.round(m.distance * 100)}%
              </span>
            </div>
          </li>
        ))}
      </ul>

      <div className="hidden overflow-x-auto min-[600px]:block">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b border-border text-left text-[0.68rem] uppercase tracking-[0.14em] text-muted-foreground">
              <th scope="col" className="py-2 pr-3 font-semibold">{T.document[lang]}</th>
              <th scope="col" className="px-3 py-2 font-semibold">{T.date[lang]}</th>
              <th scope="col" className="py-2 pl-3 text-right font-semibold">{T.relevance[lang]}</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((m) => (
              <tr key={m.source_url + m.title} className="border-b border-border last:border-0">
                <td className="py-2.5 pr-3">
                  <a
                    href={m.source_url}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="inline-flex items-start gap-1.5 font-medium text-brand-soft underline-offset-2 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  >
                    {m.title}
                    <ExternalLink className="mt-0.5 h-3.5 w-3.5 shrink-0" aria-hidden />
                  </a>
                </td>
                <td className="whitespace-nowrap px-3 py-2.5 text-muted-foreground">{m.date}</td>
                <td className="py-2.5 pl-3 text-right font-semibold tabular-nums text-foreground">
                  {Math.round(m.distance * 100)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}