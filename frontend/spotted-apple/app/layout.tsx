import '@/app/lib/styles/globals.css';
import { inter } from "@/app/lib/fonts";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Spotted Apple",
  description: "Share playlist with everybody",
};

export default function RootLayout({ children, }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}