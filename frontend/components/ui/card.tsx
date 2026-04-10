import { ReactNode } from "react";

import { cn } from "@/lib/utils";


export function Card({ children, className }: { children: ReactNode; className?: string }) {
  return <section className={cn("rounded-3xl border border-border bg-card p-6 shadow-sm", className)}>{children}</section>;
}
