"use client";
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL;

// Guard against undefined during the brief window before `npx convex dev`
// has written NEXT_PUBLIC_CONVEX_URL into .env.local. In production the var
// is always set, so the fallback only kicks in for first-run local dev.
const convex = new ConvexReactClient(
  convexUrl ?? "https://placeholder.convex.cloud",
);

export function Providers({ children }: { children: React.ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
