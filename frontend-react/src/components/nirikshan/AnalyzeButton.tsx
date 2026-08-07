import { Loader2, ScanSearch } from "lucide-react";

export function AnalyzeButton({
  onClick,
  disabled,
  loading,
  label,
}: {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="inline-flex min-h-11 items-center justify-center gap-2 rounded-sm bg-accent px-5 text-sm font-semibold text-accent-foreground shadow-sm transition-all duration-150 hover:-translate-y-px hover:brightness-95 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50"
    >
      {loading ? (
        <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
      ) : (
        <ScanSearch className="h-4 w-4" aria-hidden />
      )}
      {label}
    </button>
  );
}