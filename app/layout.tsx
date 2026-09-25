import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AwardTrace — Public procurement decision trace",
  description: "Criterion-level traces from prospectively anchored public procurement releases on GenLayer StudioNet.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
