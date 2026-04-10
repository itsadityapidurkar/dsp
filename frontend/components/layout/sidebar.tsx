"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Columns2, Compass, MoonStar, Search, SunMedium, Upload } from "lucide-react";
import { useTheme } from "next-themes";

import { cn } from "@/lib/utils";


const sections = [
  {
    title: "Analytics",
    items: [
      { href: "/", label: "Dashboard", icon: BarChart3 },
      { href: "/trends", label: "Explore Trends", icon: Compass },
      { href: "/roles", label: "Role Explorer", icon: Search },
    ],
  },
  {
    title: "Tools",
    items: [
      { href: "/compare", label: "Compare Roles", icon: Columns2 },
      { href: "/resume", label: "Resume Analyzer", icon: Upload },
    ],
  },
] as const;


export function Sidebar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();

  return (
    <aside className="sticky top-0 hidden h-screen w-72 shrink-0 border-r border-border bg-card/85 p-6 backdrop-blur lg:block">
      <div className="mb-8">
        <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Career Intelligence</p>
        <h1 className="mt-3 text-2xl font-semibold">Market Lens</h1>
        <p className="mt-2 text-sm text-muted-foreground">Understand demand, compare roles, and close skill gaps with market-facing insight.</p>
      </div>
      <div className="space-y-6">
        {sections.map((section) => (
          <div key={section.title}>
            <p className="mb-3 text-xs font-medium uppercase tracking-[0.24em] text-muted-foreground">{section.title}</p>
            <nav className="space-y-2">
              {section.items.map((item) => {
                const Icon = item.icon;
                const active = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm transition hover:bg-secondary",
                      active && "bg-primary text-primary-foreground shadow-sm",
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        ))}
      </div>
      <button
        className="mt-8 flex w-full items-center justify-between rounded-2xl border border-border px-4 py-3 text-sm"
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      >
        <span>Theme</span>
        {theme === "dark" ? <SunMedium className="h-4 w-4" /> : <MoonStar className="h-4 w-4" />}
      </button>
    </aside>
  );
}
