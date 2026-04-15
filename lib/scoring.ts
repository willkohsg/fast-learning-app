import type { Pillar } from "./pillars";
import type { ERROR_TYPES, ERROR_CATEGORIES } from "./constants";

export type ErrorType = (typeof ERROR_TYPES)[number]["value"];
export type ErrorCategory = (typeof ERROR_CATEGORIES)[number]["value"];
export type CarelessRoot = "misunderstood" | "slip" | "rushed";

export type ErrorInput = {
  qnNumber: number;
  topic: string;
  errorType: ErrorType;
  errorCategory: ErrorCategory;
  carelessRoot?: CarelessRoot;
  rootCause?: string;
  details?: string;
};

export type EnrichedError = ErrorInput & {
  primaryPillar: Pillar;
  reinforced: boolean;
};

export type PatternCard = {
  label: string;
  count: number;
  qnNumbers: number[];
  interpretation: string;
};

export type Report = {
  pillarScores: Record<Pillar, number>;
  topPatterns: PatternCard[];
  verdictPillars: Pillar[];
  enrichedErrors: EnrichedError[];
  totalErrors: number;
};

/**
 * Pure, deterministic scoring function. Given raw errors and the 3 pillar
 * mapping tables, produces enriched errors + pillar scores + top patterns +
 * verdict pillars (with the within-5pp tie-break rule).
 */
export function computeReport(
  errors: ErrorInput[],
  typeToPillar: Record<ErrorType, Pillar>,
  categoryToPillar: Record<ErrorCategory, Pillar>,
  carelessRootToPillar: Record<CarelessRoot, Pillar>,
): Report {
  const enriched: EnrichedError[] = errors.map((e) => {
    // Careless follow-up override: if user answered the 3-way sub-question,
    // route to A/S/T via carelessRootToPillar instead of the default T.
    const primaryPillar =
      e.errorType === "careless" && e.carelessRoot
        ? carelessRootToPillar[e.carelessRoot]
        : typeToPillar[e.errorType];
    const reinforced = categoryToPillar[e.errorCategory] === primaryPillar;
    return { ...e, primaryPillar, reinforced };
  });

  const counts: Record<Pillar, number> = { F: 0, A: 0, S: 0, T: 0 };
  for (const e of enriched) counts[e.primaryPillar]++;
  const total = enriched.length || 1;
  const pillarScores: Record<Pillar, number> = {
    F: Math.round((counts.F / total) * 100),
    A: Math.round((counts.A / total) * 100),
    S: Math.round((counts.S / total) * 100),
    T: Math.round((counts.T / total) * 100),
  };

  // Tie-break: any pillar within 5pp of the max and >0 is tied in the verdict.
  const max = Math.max(...Object.values(pillarScores));
  const verdictPillars = (Object.keys(pillarScores) as Pillar[])
    .filter((p) => max - pillarScores[p] <= 5 && pillarScores[p] > 0)
    .sort((a, b) => pillarScores[b] - pillarScores[a]);

  // Top 3 recurring patterns, grouped by (errorType, errorCategory).
  const patternMap = new Map<
    string,
    {
      count: number;
      qnNumbers: number[];
      errorType: ErrorType;
      errorCategory: ErrorCategory;
    }
  >();
  for (const e of enriched) {
    const k = `${e.errorType}|${e.errorCategory}`;
    const entry = patternMap.get(k) ?? {
      count: 0,
      qnNumbers: [],
      errorType: e.errorType,
      errorCategory: e.errorCategory,
    };
    entry.count++;
    entry.qnNumbers.push(e.qnNumber);
    patternMap.set(k, entry);
  }
  const topPatterns: PatternCard[] = [...patternMap.values()]
    .sort((a, b) => b.count - a.count)
    .slice(0, 3)
    .map((v) => ({
      label: `${humanize(v.errorType)} — reinforced by ${humanize(v.errorCategory)}`,
      count: v.count,
      qnNumbers: v.qnNumbers,
      interpretation: interpretPattern(v.errorType, v.errorCategory),
    }));

  return {
    pillarScores,
    verdictPillars,
    topPatterns,
    enrichedErrors: enriched,
    totalErrors: enriched.length,
  };
}

function humanize(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function interpretPattern(t: ErrorType, _c: ErrorCategory): string {
  // Tone: diagnosis, not advice. Cite what this pattern indicates, not how to fix.
  if (t === "misread_question")
    return "Signals the question wasn't decoded before solving — a classic A-pillar pattern.";
  if (t === "applied_wrong_formula")
    return "Signals a missing pattern-library entry for this question type.";
  if (t === "time_management_issue")
    return "Signals the clock won, not the question. A T-pillar pattern.";
  if (t === "conceptual_misunderstanding")
    return "Signals a foundation gap — F pillar.";
  if (t === "did_not_complete_working")
    return "Signals rushed or unclear solving flow — S pillar.";
  if (t === "careless")
    return "Routed by the student's own root cause (misunderstood / slip / rushed).";
  return "";
}
