"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";

/**
 * Screen 5: Faux-analysis transition. Research documents +10-20% conversion
 * lift from a 2-second "Analyzing your answers…" screen before the report
 * renders (UX research §1.1 Noom, §2.1).
 *
 * We do actually call the compute mutation in parallel — so the 2s animation
 * is the floor, and most of the time the mutation completes inside it.
 */
const ANIMATION_MS = 2200;

const STEPS = [
  "Mapping errors to FAST pillars…",
  "Detecting recurring patterns…",
  "Computing your pillar scores…",
  "Writing your diagnosis…",
];

export default function SubmitPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const compute = useMutation(api.reports.computeAndPersist);
  const [stepIdx, setStepIdx] = useState(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const rotate = setInterval(() => {
      setStepIdx((i) => (i + 1) % STEPS.length);
    }, ANIMATION_MS / STEPS.length);

    const minDelay = new Promise((r) => setTimeout(r, ANIMATION_MS));
    const mutationPromise = compute({
      sessionId: sessionId as Id<"sessions">,
    });

    Promise.all([minDelay, mutationPromise])
      .then(() => {
        if (cancelled) return;
        router.replace(`/diagnostic/${sessionId}/report`);
      })
      .catch((err: Error) => {
        if (cancelled) return;
        setErrorMsg(err.message ?? "Something went wrong.");
      });

    return () => {
      cancelled = true;
      clearInterval(rotate);
    };
  }, [sessionId, compute, router]);

  if (errorMsg) {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <div className="max-w-md space-y-4 text-center">
          <h2 className="text-xl font-semibold">We hit a snag</h2>
          <p className="text-sm text-muted-foreground">{errorMsg}</p>
          <button
            onClick={() => router.back()}
            className="text-sm underline text-primary"
          >
            ← Go back
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-6">
      <div className="max-w-md space-y-6 text-center">
        <div className="inline-flex h-16 w-16 items-center justify-center rounded-full border-4 border-primary/20 border-t-primary animate-spin mx-auto" />
        <h2 className="text-2xl font-bold">Analysing your errors…</h2>
        <p className="text-sm text-muted-foreground min-h-[1.5rem] transition-opacity">
          {STEPS[stepIdx]}
        </p>
      </div>
    </main>
  );
}
