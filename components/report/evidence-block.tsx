import { PILLAR_META, type Pillar } from "@/lib/pillars";

/**
 * Block 2 of the report: cites actual error counts and categories,
 * using the user's own data. "Specific over general" (voice rule §4.3).
 */
export function EvidenceBlock({
  verdictPillars,
  pillarScores,
  totalErrors,
  enrichedErrors,
}: {
  verdictPillars: Pillar[];
  pillarScores: Record<Pillar, number>;
  totalErrors: number;
  enrichedErrors: { primaryPillar: Pillar; topic: string }[];
}) {
  const primary = verdictPillars[0];
  const verdictCount = enrichedErrors.filter(
    (e) => e.primaryPillar === primary,
  ).length;

  // Collect topics contributing to the weakest pillar (unique, first 3).
  const topicsRaw = enrichedErrors
    .filter((e) => e.primaryPillar === primary && e.topic.trim().length > 0)
    .map((e) => e.topic.trim());
  const topics = Array.from(new Set(topicsRaw)).slice(0, 3);

  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">Here's what we saw</h2>
      <p className="text-base text-foreground/80 leading-relaxed">
        Of your <strong>{totalErrors}</strong> logged errors,{" "}
        <strong>{verdictCount}</strong> traced back to the{" "}
        <strong>{PILLAR_META[primary].letter} pillar</strong> (
        {PILLAR_META[primary].name}).{" "}
        {topics.length > 0 && (
          <>
            The clustering was strongest in{" "}
            <strong>{topics.join(", ")}</strong>.{" "}
          </>
        )}
        That's {pillarScores[primary]}% of your mistakes driven by one pattern —
        which means it's also one of the fastest things to fix.
      </p>
    </section>
  );
}
