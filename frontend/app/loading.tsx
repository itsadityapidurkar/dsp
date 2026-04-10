export default function Loading() {
  return (
    <div className="space-y-4">
      <div className="h-40 animate-pulse rounded-[2rem] bg-secondary" />
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="h-72 animate-pulse rounded-3xl bg-secondary" />
        <div className="h-72 animate-pulse rounded-3xl bg-secondary" />
      </div>
    </div>
  );
}
