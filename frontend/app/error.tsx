"use client";

export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div className="mx-auto max-w-xl rounded-3xl border border-border bg-card p-8 text-center">
      <h2 className="text-2xl font-semibold">Something went wrong</h2>
      <p className="mt-3 text-muted-foreground">The view could not load right now.</p>
      <button className="mt-6 rounded-2xl bg-primary px-5 py-3 text-primary-foreground" onClick={() => reset()}>
        Try again
      </button>
    </div>
  );
}
