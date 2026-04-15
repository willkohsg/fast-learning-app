"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { recallSession, forgetSession } from "@/lib/session-storage";

export default function LandingPage() {
  const [resumeId, setResumeId] = useState<string | null>(null);

  useEffect(() => {
    setResumeId(recallSession());
  }, []);

  return (
    <main className="min-h-screen px-6 py-12 max-w-2xl mx-auto">
      <div className="space-y-8">
        <div className="space-y-2">
          <p className="text-sm font-semibold uppercase tracking-wider text-primary">
            FAST DIAGNOSTIC TOOL
          </p>
          <h1 className="text-4xl font-bold leading-tight sm:text-5xl">
            Find the <span className="text-primary">ONE THING</span> costing
            your child the most marks in exams.
          </h1>
          <p className="text-lg text-muted-foreground pt-2">
            A free, 15-minute error-log diagnostic for Sec 1–4 maths students in
            Singapore. Upload a recent paper, log the mistakes, and get a
            personalised report pinpointing the area your child need to
            strengthen.
          </p>
        </div>

        {resumeId && (
          <div className="p-4 rounded-lg border-2 border-amber-300 bg-amber-50">
            <p className="text-sm font-semibold text-amber-900">
              Welcome back — you have a diagnostic in progress.
            </p>
            <div className="flex gap-3 mt-3">
              <Link
                href={`/diagnostic/${resumeId}/audience`}
                className="inline-flex items-center justify-center rounded-md bg-amber-600 text-white px-4 py-2 text-sm font-medium hover:bg-amber-700 transition"
              >
                Resume where I left off
              </Link>
              <button
                type="button"
                onClick={() => {
                  forgetSession();
                  setResumeId(null);
                }}
                className="text-sm text-amber-900 underline"
              >
                Start over
              </button>
            </div>
          </div>
        )}

        <Link
          href="/diagnostic/new"
          className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-4 text-lg font-semibold text-primary-foreground shadow-sm hover:opacity-90 transition"
        >
          {resumeId ? "Start a fresh diagnostic →" : "Start the diagnostic →"}
        </Link>

        <div className="pt-8 border-t space-y-4 text-sm text-muted-foreground">
          <div className="grid sm:grid-cols-3 gap-4">
            <div>
              <p className="font-semibold text-foreground">⏱ 15 minutes</p>
              <p>One error per screen. No fluff.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">🔒 Private</p>
              <p>No login. Auto-deleted in 24 hours.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">📊 Specific</p>
              <p>Every insight cites your own errors.</p>
            </div>
          </div>
          <p className="pt-4">
            By Cambridge Learning Group — The FAST Learning System: Going From Knowing To Scoring
          </p>
        </div>
      </div>
    </main>
  );
}
