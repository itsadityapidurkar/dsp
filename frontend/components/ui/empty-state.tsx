export function EmptyState({ message }: { message: string }) {
  return <div className="rounded-2xl border border-dashed border-border px-4 py-10 text-center text-sm text-muted-foreground">{message}</div>;
}
