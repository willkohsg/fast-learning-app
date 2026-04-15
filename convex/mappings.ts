import { query } from "./_generated/server";

/**
 * Returns all three pillar-mapping tables as plain objects, keyed by
 * their enum value. Used by the scoring function to enrich errors.
 */
export const getAll = query({
  args: {},
  handler: async (ctx) => {
    const typeRows = await ctx.db.query("errorTypePillar").collect();
    const catRows = await ctx.db.query("errorCategoryPillar").collect();
    const crRows = await ctx.db.query("carelessRootPillar").collect();
    return {
      typeToPillar: Object.fromEntries(
        typeRows.map((r) => [r.errorType, r.pillar]),
      ),
      categoryToPillar: Object.fromEntries(
        catRows.map((r) => [r.errorCategory, r.pillar]),
      ),
      carelessRootToPillar: Object.fromEntries(
        crRows.map((r) => [r.carelessRoot, r.pillar]),
      ),
    };
  },
});
