"use client";
import { useParams, useRouter } from "next/navigation";
import { useMutation, useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { useState } from "react";
import {
  ErrorEntryForm,
  type ErrorEntryData,
} from "@/components/error-entry-form";
import { SegmentedProgress } from "@/components/progress-bar";
import { ReassuranceScreen } from "@/components/reassurance-screen";
import { Button } from "@/components/ui/button";
import {
  MIN_ERRORS_FOR_REPORT,
  NUDGE_AT,
  GENTLE_CAP,
} from "@/lib/constants";

export default function ErrorPage() {
  const { sessionId, index } = useParams<{
    sessionId: string;
    index: string;
  }>();
  const router = useRouter();
  const idx = Math.max(1, Number(index) || 1);

  const errors = useQuery(api.errors.listBySession, {
    sessionId: sessionId as Id<"sessions">,
  });
  const upsert = useMutation(api.errors.upsert);
  const removeErr = useMutation(api.errors.remove);

  const [showReassurance, setShowReassurance] = useState(false);

  if (errors === undefined) {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <p className="text-muted-foreground">Loading…</p>
      </main>
    );
  }

  const existing = errors.find((e) => e.qnNumber === idx);
  const count = errors.length;

  if (showReassurance) {
    return (
      <ReassuranceScreen
        count={count}
        onContinue={() => {
          setShowReassurance(false);
          const nextIdx = getNextFreeIndex(errors ?? [], idx);
          router.push(`/diagnostic/${sessionId}/errors/${nextIdx}`);
        }}
      />
    );
  }

  async function handleSave(d: ErrorEntryData) {
    const currentErrors = errors ?? [];
    await upsert({
      sessionId: sessionId as Id<"sessions">,
      qnNumber: d.qnNumber,
      topic: d.topic,
      errorType: d.errorType,
      errorCategory: d.errorCategory,
      carelessRoot: d.errorType === "careless" ? d.carelessRoot : undefined,
      rootCause: d.rootCause || undefined,
      details: d.details || undefined,
    });
    const newCount = existing ? count : count + 1;
    if ((NUDGE_AT as readonly number[]).includes(newCount)) {
      setShowReassurance(true);
      return;
    }
    const nextIdx = getNextFreeIndex(currentErrors, d.qnNumber);
    router.push(`/diagnostic/${sessionId}/errors/${nextIdx}`);
  }

  async function handleDelete() {
    if (!existing) return;
    await removeErr({ id: existing._id });
    const prev = Math.max(1, idx - 1);
    router.push(`/diagnostic/${sessionId}/errors/${prev}`);
  }

  const canSubmit = count >= MIN_ERRORS_FOR_REPORT;
  const atCap = count >= GENTLE_CAP;

  return (
    <main className="min-h-screen px-6 py-8 max-w-2xl mx-auto space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Step 3 of 4 — Error log
        </p>
        <h2 className="text-2xl font-bold mt-1">
          {existing ? `Edit error #${idx}` : `Error #${idx}`}
        </h2>
      </div>

      <SegmentedProgress count={count} />

      {atCap && !existing && (
        <div className="p-3 rounded-md bg-muted text-sm">
          You've logged {count} errors — that's our gentle cap. You can
          continue, but the diagnostic is already plenty sharp. Consider
          wrapping up.
        </div>
      )}

      <ErrorEntryForm
        key={idx}
        initial={{ qnNumber: idx, ...(existing ?? {}) }}
        onSave={handleSave}
        submitLabel={existing ? "Update & next" : "Save & next"}
      />

      <div className="flex flex-col gap-2 pt-4 border-t">
        {canSubmit && (
          <Button
            onClick={() => router.push(`/diagnostic/${sessionId}/submit`)}
            size="lg"
            variant="secondary"
          >
            I'm done — see my diagnosis ({count} error{count !== 1 ? "s" : ""})
          </Button>
        )}
        {existing && (
          <Button variant="ghost" onClick={handleDelete} className="text-destructive">
            Delete this error
          </Button>
        )}
        <Button
          variant="ghost"
          onClick={() => router.push(`/diagnostic/${sessionId}/errors/${Math.max(1, idx - 1)}`)}
          disabled={idx <= 1}
        >
          ← Previous error
        </Button>
      </div>
    </main>
  );
}

function getNextFreeIndex(
  errors: readonly { qnNumber: number }[],
  current: number,
): number {
  // Find the smallest positive qnNumber not already used, starting after current.
  const taken = new Set(errors.map((e) => e.qnNumber));
  let n = current + 1;
  while (taken.has(n)) n++;
  return n;
}
