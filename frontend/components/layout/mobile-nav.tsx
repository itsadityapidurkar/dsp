"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
  { href: "/", label: "Dashboard" },
  { href: "/trends", label: "Trends" },
  { href: "/roles", label: "Roles" },
  { href: "/compare", label: "Compare" },
  { href: "/resume", label: "Resume" },
] as const;


export function MobileNav() {
  const pathname = usePathname();
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 grid grid-cols-5 border-t border-border bg-card/95 p-2 backdrop-blur lg:hidden">
      {items.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={`rounded-xl px-2 py-3 text-center text-xs ${pathname === item.href ? "bg-primary text-primary-foreground" : "text-muted-foreground"}`}
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
