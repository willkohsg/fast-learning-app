import { MIN_ERRORS_FOR_REPORT, GENTLE_CAP } from "@/lib/constants";

/**
 * Segmented progress bar that "unlocks" the report at the minimum threshold
 * and encourages (but doesn't force) more entries up to the soft cap.
 * Research recommends this framing over a shrinking-% bar (UX research §2.2).
 */
export function SegmentedProgress({ count }: { count: number }) {
  const unlocked = count >= MIN_ERRORS_FOR_REPORT;
  const cap = GENTLE_CAP;
  const cells = Array.from({ length: cap });

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center text-sm">
        <span className={unlocked ? "text-emerald-700 font-semibold" : ""}>
          {unlocked
            ? `✓ Report unlocked — ${count} errors logged`
            : `${count} / ${MIN_ERRORS_FOR_REPORT} minimum`}
        </span>
        <span className="text-xs text-muted-foreground">
          {unlocked ? "More errors = sharper diagnosis" : "Keep going"}
        </span>
      </div>
      <div className="flex gap-1">
        {cells.map((_, i) => (
          <div
            key={i}
            className={`h-2 flex-1 rounded-sm transition ${
              i < count
                ? unlocked
                  ? "bg-emerald-500"
                  : "bg-primary"
                : i < MIN_ERRORS_FOR_REPORT
                  ? "bg-primary/20"
                  : "bg-muted"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
