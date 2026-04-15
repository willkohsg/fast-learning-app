"use client";
import { use } from "react";
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { HeroVerdict } from "@/components/report/hero-verdict";
import { EvidenceBlock } from "@/components/report/evidence-block";
import { PatternCards } from "@/components/report/pattern-cards";
import { PillarsAccordion } from "@/components/report/pillars-accordion";
import { BridgeParagraph } from "@/components/report/bridge-paragraph";
import { DualCTA } from "@/components/report/dual-cta";
import type { Pillar } from "@/lib/pillars";

export default function ReportPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = use(params);
  const id = sessionId as Id<"sessions">;

  const session = useQuery(api.sessions.get, { id });
  const report = useQuery(api.reports.getBySession, { sessionId: id });
  const errors = useQuery(api.errors.listBySession, { sessionId: id });

  if (session === undefined || report === undefined || errors === undefined) {
    return (
      <main className="mx-auto max-w-2xl px-4 py-12">
        <p className="text-muted-foreground">Loading your report…</p>
      </main>
    );
  }

  if (!session) {
    return (
      <main className="mx-auto max-w-2xl px-4 py-12">
        <p>Session not found.</p>
      </main>
    );
  }

  if (!report) {
    return (
      <main className="mx-auto max-w-2xl px-4 py-12 space-y-3">
        <h1 className="text-xl font-semibold">Report not ready yet</h1>
        <p className="text-muted-foreground">
          We couldn't find a report for this session. Try returning to the
          diagnostic and submitting again.
        </p>
        <a
          href={`/diagnostic/${sessionId}/errors/0`}
          className="text-primary underline"
        >
          ← Back to diagnostic
        </a>
      </main>
    );
  }

  const verdictPillars = report.verdictPillars as Pillar[];
  const pillarScores = report.pillarScores as Record<Pillar, number>;
  const enrichedErrors = errors
    .filter((e) => e.primaryPillar)
    .map((e) => ({
      primaryPillar: e.primaryPillar as Pillar,
      topic: e.topic ?? "",
    }));

  const topPattern = report.topPatterns[0];
  const primaryPct = pillarScores[verdictPillars[0]];

  return (
    <main className="mx-auto max-w-2xl px-4 py-8 sm:py-12 space-y-8">
      <HeroVerdict
        verdictPillars={verdictPillars}
        pillarScores={pillarScores}
        studentName={session.studentName}
      />
      <EvidenceBlock
        verdictPillars={verdictPillars}
        pillarScores={pillarScores}
        totalErrors={errors.length}
        enrichedErrors={enrichedErrors}
      />
      <PatternCards patterns={report.topPatterns} />
      <PillarsAccordion
        pillarScores={pillarScores}
        verdictPillars={verdictPillars}
      />
      <BridgeParagraph verdictPillars={verdictPillars} />
      <DualCTA
        sessionId={id}
        studentName={session.studentName}
        level={session.level}
        verdictPillars={verdictPillars}
        pillarPercent={primaryPct}
        topPatternLabel={topPattern?.label}
      />
      <footer className="pt-6 border-t text-xs text-muted-foreground space-y-1">
        <p>
          This report is a starting point, not a diagnosis. Your data is held
          for 24 hours then purged.
        </p>
        <p>FAST Diagnostic Tool · Cambridge Learning Group</p>
      </footer>
    </main>
  );
}
