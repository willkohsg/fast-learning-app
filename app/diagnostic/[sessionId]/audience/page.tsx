"use client";
import { useParams, useRouter } from "next/navigation";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { AUDIENCES } from "@/lib/constants";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function AudiencePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const setAudience = useMutation(api.sessions.setAudience);
  const [picked, setPicked] = useState<
    (typeof AUDIENCES)[number]["value"] | null
  >(null);
  const [saving, setSaving] = useState(false);

  async function handleContinue() {
    if (!picked) return;
    setSaving(true);
    await setAudience({
      id: sessionId as Id<"sessions">,
      audience: picked,
    });
    router.push(`/diagnostic/${sessionId}/upload`);
  }

  return (
    <main className="min-h-screen px-6 py-10 max-w-2xl mx-auto space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Step 1 of 4
        </p>
        <h1 className="text-3xl font-bold mt-1">Who's taking this?</h1>
        <p className="text-muted-foreground mt-2">
          We'll adjust the language to match.
        </p>
      </div>

      <div className="space-y-3">
        {AUDIENCES.map((a) => (
          <button
            key={a.value}
            type="button"
            onClick={() => setPicked(a.value)}
            className={`w-full text-left p-4 rounded-lg border-2 transition ${
              picked === a.value
                ? "border-primary bg-primary/5"
                : "border-border hover:border-primary/40"
            }`}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">{a.emoji}</span>
              <div className="flex-1">
                <p className="font-semibold">{a.label}</p>
                {"recommended" in a && a.recommended && (
                  <p className="text-xs text-primary mt-0.5">
                    Most common — recommended
                  </p>
                )}
              </div>
              {picked === a.value && (
                <span className="text-primary text-xl">✓</span>
              )}
            </div>
          </button>
        ))}
      </div>

      <Button
        onClick={handleContinue}
        disabled={!picked || saving}
        size="lg"
        className="w-full"
      >
        {saving ? "Saving…" : "Continue →"}
      </Button>
    </main>
  );
}
