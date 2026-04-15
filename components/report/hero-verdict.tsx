import { PILLAR_META, type Pillar } from "@/lib/pillars";

export function HeroVerdict({
  verdictPillars,
  pillarScores,
  studentName,
}: {
  verdictPillars: Pillar[];
  pillarScores: Record<Pillar, number>;
  studentName?: string;
}) {
  const tied = verdictPillars.length > 1;
  const primary = verdictPillars[0];
  const meta = PILLAR_META[primary];
  const pct = pillarScores[primary];

  const greeting = studentName ? `${studentName}, ` : "";

  return (
    <section
      className={`rounded-2xl border-2 ${meta.borderClass} ${meta.bgClass} p-6 sm:p-8 space-y-4`}
    >
      <div className="flex items-start gap-4">
        <div
          className={`flex h-16 w-16 items-center justify-center rounded-2xl ${meta.textClass} bg-white/80 shadow-sm font-black text-3xl flex-shrink-0`}
        >
          {tied ? verdictPillars.join("/") : primary}
        </div>
        <div className="flex-1 min-w-0">
          <p className={`text-xs font-semibold uppercase tracking-wider ${meta.textClass}`}>
            Your weakest FAST pillar
          </p>
          <h1 className="text-2xl sm:text-3xl font-bold mt-1 leading-tight">
            {tied ? (
              <>
                {greeting}your weakest pillars are{" "}
                <span className={meta.textClass}>
                  {verdictPillars.join(" & ")}
                </span>{" "}
                — tied at ~{pct}% each.
              </>
            ) : (
              <>
                {greeting}your weakest pillar is{" "}
                <span className={meta.textClass}>{meta.name}</span> — {pct}% of
                your errors.
              </>
            )}
          </h1>
        </div>
      </div>
      <p className="text-base text-foreground/80 pt-2 border-t border-white/50">
        {meta.subline}
      </p>
    </section>
  );
}
