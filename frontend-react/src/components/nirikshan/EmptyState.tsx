import { SearchX } from "lucide-react";

export function EmptyState({ title, body }: { title: string; body: string }) {
  return (
    <div className="flex items-start gap-3 rounded-sm border border-dashed border-border bg-surface-muted px-4 py-5">
      <SearchX className="mt-0.5 h-5 w-5 shrink-0 text-muted-foreground" aria-hidden />
      <div>
        <p className="text-sm font-semibold text-foreground">{title}</p>
        <p className="mt-1 text-sm text-muted-foreground">{body}</p>
      </div>
    </div>
  );
}