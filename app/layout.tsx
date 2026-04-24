import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RealityCheck AI | AI Fact-Checker",
  description:
    "Multi-agent AI fact-checker powered by Groq (Llama 3.3 70B) and Tavily live web search. Verify any claim in seconds.",
  openGraph: {
    title: "RealityCheck AI",
    description: "Verify any claim with live AI fact-checking.",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
