import { internalQuery } from "./_generated/server";
import { v } from "convex/values";

/**
 * Internal queries used by the email/PDF action. Pulled into one file so
 * the action only imports `internal.internal_queries.*`.
 */

export const getReportBundle = internalQuery({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const session = await ctx.db.get(sessionId);
    if (!session) return null;
    const report = await ctx.db
      .query("reports")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first();
    if (!report) return null;
    const errors = await ctx.db
      .query("errors")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .collect();
    return { session, report, errors };
  },
});
