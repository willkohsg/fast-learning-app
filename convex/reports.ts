import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { pillarValidator } from "./schema";

type Pillar = "F" | "A" | "S" | "T";

export const getBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) =>
    await ctx.db
      .query("reports")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first(),
});

/**
 * Computes pillar scores + top patterns + verdict for the session's errors
 * and persists them. Applies the Careless follow-up override when present.
 * Requires >= 5 errors.
 */
export const computeAndPersist = mutation({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const errors = await ctx.db
      .query("errors")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .collect();
    if (errors.length < 5) {
      throw new Error("Need at least 5 errors to generate a report.");
    }

    const typeRows = await ctx.db.query("errorTypePillar").collect();
    const catRows = await ctx.db.query("errorCategoryPillar").collect();
    const crRows = await ctx.db.query("carelessRootPillar").collect();
    const typeToPillar = Object.fromEntries(
      typeRows.map((r) => [r.errorType, r.pillar]),
    ) as Record<string, Pillar>;
    const catToPillar = Object.fromEntries(
      catRows.map((r) => [r.errorCategory, r.pillar]),
    ) as Record<string, Pillar>;
    const carelessRootToPillar = Object.fromEntries(
      crRows.map((r) => [r.carelessRoot, r.pillar]),
    ) as Record<string, Pillar>;

    const counts: Record<Pillar, number> = { F: 0, A: 0, S: 0, T: 0 };
    for (const e of errors) {
      const p =
        e.errorType === "careless" && e.carelessRoot
          ? carelessRootToPillar[e.carelessRoot]!
          : typeToPillar[e.errorType]!;
      counts[p]++;
      await ctx.db.patch(e._id, {
        primaryPillar: p,
        reinforced: catToPillar[e.errorCategory] === p,
      });
    }

    const total = errors.length;
    const scores = {
      F: Math.round((counts.F / total) * 100),
      A: Math.round((counts.A / total) * 100),
      S: Math.round((counts.S / total) * 100),
      T: Math.round((counts.T / total) * 100),
    };
    const max = Math.max(...Object.values(scores));
    const verdictPillars = (Object.keys(scores) as Pillar[])
      .filter((p) => max - scores[p] <= 5 && scores[p] > 0)
      .sort((a, b) => scores[b] - scores[a]);

    // Group patterns by (errorType, errorCategory).
    const patternMap = new Map<
      string,
      {
        count: number;
        qnNumbers: number[];
        errorType: string;
        errorCategory: string;
      }
    >();
    for (const e of errors) {
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
    const topPatterns = [...patternMap.values()]
      .sort((a, b) => b.count - a.count)
      .slice(0, 3)
      .map((v) => ({
        label: `${humanize(v.errorType)} — reinforced by ${humanize(v.errorCategory)}`,
        count: v.count,
        qnNumbers: v.qnNumbers,
        interpretation: interpretPattern(v.errorType),
      }));

    const existing = await ctx.db
      .query("reports")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first();
    const reportDoc = {
      sessionId,
      pillarScores: scores,
      topPatterns,
      verdictPillars,
      generatedAt: Date.now(),
    };
    if (existing) {
      await ctx.db.replace(existing._id, reportDoc);
    } else {
      await ctx.db.insert("reports", reportDoc);
    }
    await ctx.db.patch(sessionId, {
      status: "submitted",
      submittedAt: Date.now(),
    });
    return { ok: true, verdictPillars };
  },
});

function humanize(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

function interpretPattern(t: string): string {
  switch (t) {
    case "misread_question":
      return "Signals the question wasn't decoded before solving — a classic A-pillar pattern.";
    case "applied_wrong_formula":
      return "Signals a missing pattern-library entry for this question type.";
    case "time_management_issue":
      return "Signals the clock won, not the question. A T-pillar pattern.";
    case "conceptual_misunderstanding":
      return "Signals a foundation gap — F pillar.";
    case "did_not_complete_working":
      return "Signals rushed or unclear solving flow — S pillar.";
    case "careless":
      return "Routed by the student's own root cause (misunderstood / slip / rushed).";
    default:
      return "";
  }
}

// Re-export for client-type imports if needed
export const _pillarValidator = pillarValidator;
