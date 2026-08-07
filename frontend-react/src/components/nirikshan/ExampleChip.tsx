export function ExampleChip({
  label,
  onClick,
  disabled,
}: {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="rounded-full border border-border bg-surface-muted px-3 py-1.5 text-xs font-medium text-foreground transition-all duration-150 hover:-translate-y-px hover:border-brand-soft hover:bg-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"
    >
      {label}
    </button>
  );
}