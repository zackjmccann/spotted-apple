import '@/app/ui/global.css';
import { inter } from "@/app/ui/fonts";
import type { Metadata } from "next";
import { UserProvider } from '@auth0/nextjs-auth0/client';

export const metadata: Metadata = {
  title: "Spotted Apple",
  description: "Share playlist with everybody",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
    <UserProvider>
      <body className={inter.className}>{children}</body>
    </UserProvider>
    </html>
  );
}