import { internalMutation } from "./_generated/server";

/**
 * Seeds the 3 pillar-mapping tables. Idempotent — safe to call repeatedly.
 *
 * Mappings (William's IP, editable in Convex dashboard without redeploy):
 *
 * Error Type → Pillar (primary):
 *   Careless                    → T (default; overridden by carelessRoot when set)
 *   Conceptual misunderstanding → F
 *   Misread the question        → A
 *   Applied wrong formula       → S
 *   Did not complete working    → S
 *   Time management issue       → T
 *
 * Error Category → Pillar (reinforcement signal; same pillar = "reinforced"):
 *   Knowledge gap              → F
 *   Misapplied rule            → A
 *   Confusion between concepts → S
 *   Poor exam strategy         → T
 *   Anxiety / panic            → T
 *   Lack of practice           → S
 *
 * Careless Root → Pillar (follow-up routing, William 2026-04-15):
 *   Misunderstood the question   → A
 *   Knew what to do, made a slip → S
 *   Rushed because of time       → T
 */
export const seedMappings = internalMutation({
  args: {},
  handler: async (ctx) => {
    const typeMapping = [
      { errorType: "careless" as const, pillar: "T" as const },
      { errorType: "conceptual_misunderstanding" as const, pillar: "F" as const },
      { errorType: "misread_question" as const, pillar: "A" as const },
      { errorType: "applied_wrong_formula" as const, pillar: "S" as const },
      { errorType: "did_not_complete_working" as const, pillar: "S" as const },
      { errorType: "time_management_issue" as const, pillar: "T" as const },
    ];
    const categoryMapping = [
      { errorCategory: "knowledge_gap" as const, pillar: "F" as const },
      { errorCategory: "misapplied_rule" as const, pillar: "A" as const },
      { errorCategory: "confusion_between_concepts" as const, pillar: "S" as const },
      { errorCategory: "poor_exam_strategy" as const, pillar: "T" as const },
      { errorCategory: "anxiety_panic" as const, pillar: "T" as const },
      { errorCategory: "lack_of_practice" as const, pillar: "S" as const },
    ];
    const carelessRootMapping = [
      { carelessRoot: "misunderstood" as const, pillar: "A" as const },
      { carelessRoot: "slip" as const, pillar: "S" as const },
      { carelessRoot: "rushed" as const, pillar: "T" as const },
    ];

    const existingTypes = await ctx.db.query("errorTypePillar").collect();
    if (existingTypes.length === 0) {
      for (const row of typeMapping) await ctx.db.insert("errorTypePillar", row);
    }
    const existingCats = await ctx.db.query("errorCategoryPillar").collect();
    if (existingCats.length === 0) {
      for (const row of categoryMapping) await ctx.db.insert("errorCategoryPillar", row);
    }
    const existingCarelessRoots = await ctx.db
      .query("carelessRootPillar")
      .collect();
    if (existingCarelessRoots.length === 0) {
      for (const row of carelessRootMapping)
        await ctx.db.insert("carelessRootPillar", row);
    }

    return {
      typeCount: existingTypes.length || typeMapping.length,
      categoryCount: existingCats.length || categoryMapping.length,
      carelessRootCount:
        existingCarelessRoots.length || carelessRootMapping.length,
    };
  },
});
