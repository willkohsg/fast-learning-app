export function PatternCards({
  patterns,
}: {
  patterns: {
    label: string;
    count: number;
    qnNumbers: number[];
    interpretation: string;
  }[];
}) {
  if (patterns.length === 0) return null;

  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">Top recurring patterns</h2>
      <div className="space-y-3">
        {patterns.map((p, i) => (
          <div
            key={i}
            className="rounded-lg border p-4 bg-card hover:shadow-sm transition"
          >
            <div className="flex items-start justify-between gap-3">
              <p className="font-semibold flex-1">{p.label}</p>
              <span className="shrink-0 text-xs font-semibold bg-primary/10 text-primary px-2 py-1 rounded">
                {p.count}×
              </span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Q{p.qnNumbers.join(", Q")}
            </p>
            <p className="text-sm mt-2 text-foreground/80">
              {p.interpretation}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
