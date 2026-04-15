"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { rememberSession } from "@/lib/session-storage";

/**
 * Entrypoint that creates a fresh session and redirects to the
 * audience-selection screen. This is the target of the landing-page CTA.
 */
export default function NewDiagnosticPage() {
  const router = useRouter();
  const createSession = useMutation(api.sessions.create);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const id = await createSession();
      if (cancelled) return;
      rememberSession(id);
      router.replace(`/diagnostic/${id}/audience`);
    })();
    return () => {
      cancelled = true;
    };
  }, [createSession, router]);

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <p className="text-muted-foreground">Starting your diagnostic…</p>
    </main>
  );
}
