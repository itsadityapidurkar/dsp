import { ReactNode } from "react";
import { Inter } from "next/font/google";

import { MobileNav } from "@/components/layout/mobile-nav";
import { Sidebar } from "@/components/layout/sidebar";
import { ThemeProvider } from "@/components/providers/theme-provider";
import "./globals.css";


const inter = Inter({ subsets: ["latin"], variable: "--font-geist-sans" });


export const metadata = {
  title: "Market Lens",
  description: "Job market intelligence platform for demand, hiring patterns, and resume alignment.",
};


export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.variable}>
        <ThemeProvider>
          <div className="min-h-screen lg:flex">
            <Sidebar />
            <main className="flex-1 px-4 pb-24 pt-6 lg:px-8 lg:pb-8">{children}</main>
            <MobileNav />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
