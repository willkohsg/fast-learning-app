import { internalMutation } from "./_generated/server";

const TWENTY_FOUR_HOURS_MS = 24 * 60 * 60 * 1000;

/**
 * 24-hour retention policy (William, 2026-04-15, Q7).
 * Purges sessions older than 24h plus their errors, reports, uploaded files.
 * Leads are kept indefinitely (booking pipeline).
 */
export const purgeStaleSessions = internalMutation({
  args: {},
  handler: async (ctx) => {
    const cutoff = Date.now() - TWENTY_FOUR_HOURS_MS;
    const stale = await ctx.db
      .query("sessions")
      .filter((q) => q.lt(q.field("createdAt"), cutoff))
      .collect();

    let purged = 0;
    for (const s of stale) {
      // Delete uploaded files from storage.
      if (s.uploadedPaperFileIds) {
        for (const fileId of s.uploadedPaperFileIds) {
          try {
            await ctx.storage.delete(fileId);
          } catch {
            // ignore — file may already be gone
          }
        }
      }
      // Delete report.
      const reports = await ctx.db
        .query("reports")
        .withIndex("by_session", (q) => q.eq("sessionId", s._id))
        .collect();
      for (const r of reports) await ctx.db.delete(r._id);
      // Delete errors.
      const errors = await ctx.db
        .query("errors")
        .withIndex("by_session", (q) => q.eq("sessionId", s._id))
        .collect();
      for (const e of errors) await ctx.db.delete(e._id);
      // Delete the session itself.
      await ctx.db.delete(s._id);
      purged++;
    }
    return { purged };
  },
});
