import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "FAST Diagnostic Tool — Cambridge Learning Group",
  description:
    "A free 15-minute error-log diagnostic for Sec 1–4 maths students in Singapore. Discover your weakest FAST pillar and what to do about it.",
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
  ),
  openGraph: {
    title: "FAST Diagnostic Tool",
    description:
      "Find your weakest maths pillar in 15 minutes. Free diagnostic for Sec 1–4 students.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background text-foreground">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
